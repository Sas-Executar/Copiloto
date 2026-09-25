#!/usr/bin/env python3
"""Valida artefatos Desk&Go (SVG/HTML) contra o contrato de marcação Executar Playbook.

O foco são as duas coisas que mais quebram em produção e que ninguém pega
olhando na tela: campo vazio que parece dado real, e caixa de marcar que não dá
para marcar (pequena demais, traço fino demais, ou já vem marcada num caderno
que deveria sair em branco).

Modos:
  --modo branco      caderno para imprimir e preencher à mão. Campo vazio é o
                     estado esperado; nenhuma caixa pode vir marcada.
  --modo preenchido  artefato final com dados reais. Campo vazio vira aviso e
                     sentinela de placeholder dentro de campo preenchido é erro.

Uso:
  python3 validar_artefato.py peca.svg
  python3 validar_artefato.py out/*.svg --modo branco --format json
  python3 validar_artefato.py relatorio.html --modo preenchido
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tokens import Tokens, contraste  # noqa: E402

SVG_NS = "http://www.w3.org/2000/svg"

SENTINELA_PADRAO = "— pendente"

# Marcadores de rascunho. Os curtos são case-sensitive de propósito: "todo" é
# palavra corrente em português e pegá-la como sentinela geraria falso positivo
# em praticamente todo artefato.
SENTINELAS_RASCUNHO = [
    (re.compile(r"\blorem ipsum\b", re.I), "lorem ipsum"),
    (re.compile(r"\bTODO\b"), "TODO"),
    (re.compile(r"\bTBD\b"), "TBD"),
    (re.compile(r"\bFIXME\b"), "FIXME"),
    (re.compile(r"\bXXX+\b"), "XXX"),
    (re.compile(r"\bA\s+DEFINIR\b", re.I), "A DEFINIR"),
    (re.compile(r"A_DEFINIR"), "A_DEFINIR"),
    (re.compile(r"preencher aqui", re.I), "preencher aqui"),
    (re.compile(r"\{\{|\}\}|\[\[|\]\]"), "delimitador de template não substituído"),
]
# Três estados, não dois. "blank" é um campo desenhado para alguém escrever
# depois — a pauta já diz isso e carimbar "— pendente" em quarenta campos de um
# caderno vira ruído. "empty" é dado que deveria existir e não existe: aí a
# ausência precisa estar escrita, senão some no meio do texto preenchido.
ESTADOS_CAMPO = {"blank", "empty", "filled"}
ESTADOS_CHECK = {"off", "on", "na"}

HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
VAR_USO = re.compile(r"var\(\s*(--[a-z0-9-]+)")
VAR_DECL = re.compile(r"(--[a-z0-9-]+)\s*:")
TAG_STYLE = re.compile(r"<style\b[^>]*>.*?</style>", re.S | re.I)
TAG_COMENT = re.compile(r"<!--.*?-->", re.S)

# Limites físicos. Não são gosto: abaixo disso a peça falha no papel.
MIN_LADO_CHECK_MM = 3.5      # menor caixa que ainda aceita um traço de caneta
MIN_TRACO_MM = 0.25          # abaixo disso o traço some na impressão
TOLERANCIA_QUADRADO = 0.15   # 15% de diferença entre lados ainda lê como quadrado
MIN_CONTRASTE_PLACEHOLDER = 4.5


@dataclass
class Achado:
    codigo: str
    severidade: str  # ERRO | AVISO | INFO
    onde: str
    mensagem: str


@dataclass
class Relatorio:
    arquivo: str
    modo: str
    achados: list[Achado] = field(default_factory=list)
    contagem: dict = field(default_factory=dict)

    def add(self, codigo, severidade, onde, mensagem):
        self.achados.append(Achado(codigo, severidade, onde, mensagem))

    @property
    def erros(self) -> int:
        return sum(1 for a in self.achados if a.severidade == "ERRO")

    @property
    def status(self) -> str:
        return "FAIL" if self.erros else "PASS"

    def to_dict(self) -> dict:
        return {
            "arquivo": self.arquivo,
            "modo": self.modo,
            "status": self.status,
            "contagem": self.contagem,
            "achados": [a.__dict__ for a in self.achados],
        }


# --------------------------------------------------------------------------
# leitura
# --------------------------------------------------------------------------

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}


class ArvoreHTML(HTMLParser):
    """Monta uma árvore de elementos. Uma versão anterior lia uma janela fixa de
    caracteres em volta do marcador, e a janela invadia o elemento seguinte: um
    campo preenchido herdava o placeholder do vizinho e uma caixa desmarcada
    herdava a marca da de baixo. Escopo tem que ser estrutural, não por distância."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.raiz = {"tag": "#raiz", "attrs": {}, "filhos": [], "texto": ""}
        self.pilha = [self.raiz]

    def handle_starttag(self, tag, attrs):
        no = {"tag": tag, "attrs": dict(attrs), "filhos": [], "texto": ""}
        self.pilha[-1]["filhos"].append(no)
        if tag not in VOID:
            self.pilha.append(no)

    def handle_startendtag(self, tag, attrs):
        self.pilha[-1]["filhos"].append({"tag": tag, "attrs": dict(attrs), "filhos": [], "texto": ""})

    def handle_endtag(self, tag):
        for i in range(len(self.pilha) - 1, 0, -1):
            if self.pilha[i]["tag"] == tag:
                del self.pilha[i:]
                return

    def handle_data(self, data):
        self.pilha[-1]["texto"] += data


def _descendentes(no: dict):
    yield no
    for filho in no["filhos"]:
        yield from _descendentes(filho)


def _texto_de(no: dict) -> str:
    return " ".join(n["texto"] for n in _descendentes(no) if n["texto"].strip())


def _classes_de(no: dict) -> set[str]:
    out: set[str] = set()
    for n in _descendentes(no):
        out |= _classes(n["attrs"])
    return out


def _classes(attrs: dict) -> set[str]:
    return set((attrs.get("class") or "").split())


def _texto_svg(el: ET.Element) -> str:
    return "".join(el.itertext())


def _sem_ns(tag: str) -> str:
    return tag.split("}", 1)[-1]


# --------------------------------------------------------------------------
# checagens compartilhadas
# --------------------------------------------------------------------------

def checar_tokens(rel: Relatorio, bruto: str, tk: Tokens, permitir_flat: bool):
    """Regra raw->alias: cor só aparece dentro do bloco de estilo, nunca solta
    num atributo de apresentação. Quem hardcoda cor no componente perde a
    capacidade de trocar o acento sem reescrever o arquivo."""
    sem_coment = TAG_COMENT.sub("", bruto)
    estilos = "\n".join(TAG_STYLE.findall(sem_coment))
    fora = TAG_STYLE.sub("", sem_coment)

    if not permitir_flat:
        for m in HEX.finditer(fora):
            trecho = fora[max(0, m.start() - 60):m.start()].splitlines()[-1:] or [""]
            rel.add("TK001", "ERRO", trecho[0].strip()[-50:] or "?",
                    f"cor {m.group(0)} literal fora do bloco de tokens; consuma var(--exec-*)")

    declarados = set(VAR_DECL.findall(estilos)) | {f"--{n}" for n in tk.nomes_alias()}
    for m in VAR_USO.finditer(sem_coment):
        if m.group(1) not in declarados:
            rel.add("TK002", "ERRO", m.group(1), "variável usada mas não declarada nem presente na camada alias")

    if "px-image" in sem_coment:
        rel.add("TK003", "ERRO", "documento",
                "unidade px-image vazou para o artefato; ela é pixel do JPG de referência, "
                "não medida física — converter exige decisão registrada na camada de tokens")

    for padrao, rotulo in SENTINELAS_RASCUNHO:
        if padrao.search(fora):
            rel.add("TXT001", "ERRO", rotulo, f"sentinela de rascunho {rotulo!r} presente no conteúdo do artefato")


def checar_contraste_placeholder(rel: Relatorio, tk: Tokens):
    try:
        r = contraste(tk.color("ink-placeholder"), tk.color("surface-page"))
    except (KeyError, ValueError):
        return
    if r < MIN_CONTRASTE_PLACEHOLDER:
        rel.add("PH007", "ERRO", "exec-color-ink-placeholder",
                f"contraste {r}:1 contra a superfície da página; mínimo {MIN_CONTRASTE_PLACEHOLDER}:1. "
                "Placeholder é mais leve que dado real, não ilegível.")


def checar_campo(rel: Relatorio, onde: str, estado: str | None, classes: set[str],
                 texto: str, sentinela: str, modo: str, vistos: set[str], campo: str):
    if campo in vistos:
        rel.add("PH008", "ERRO", onde, f"data-field {campo!r} duplicado no mesmo artefato")
    vistos.add(campo)

    if estado is None:
        rel.add("PH001", "ERRO", onde, "campo sem data-state; o validador não consegue saber se está vazio ou preenchido")
        return
    if estado not in ESTADOS_CAMPO:
        rel.add("PH002", "ERRO", onde, f"data-state={estado!r} inválido; use {sorted(ESTADOS_CAMPO)}")
        return

    tem_sentinela = sentinela.lower() in texto.lower()

    if estado == "blank":
        if not ({"exec-field__box", "linha-escrita"} & classes):
            rel.add("PH011", "ERRO", onde,
                    "campo para preencher sem área de escrita (exec-field__box ou linha-escrita); "
                    "sobra um rótulo solto e ninguém sabe onde escrever")
        if tem_sentinela:
            rel.add("PH013", "AVISO", onde,
                    f"campo de preenchimento carimbado com {sentinela!r}; ele não está pendente, "
                    "está esperando a caneta — a pauta já comunica isso")
        if modo == "preenchido":
            rel.add("PH009", "AVISO", onde, "campo em branco num artefato declarado como preenchido")
    elif estado == "empty":
        if "exec-is-placeholder" not in classes:
            rel.add("PH003", "ERRO", onde,
                    "campo vazio sem a classe exec-is-placeholder; sem ela o campo sai com o mesmo peso de um dado real")
        if not tem_sentinela:
            rel.add("PH004", "ERRO", onde, f"campo vazio sem o texto sentinela {sentinela!r}")
        if modo == "preenchido":
            rel.add("PH009", "AVISO", onde, "campo continua vazio num artefato declarado como preenchido")
    else:
        if tem_sentinela:
            rel.add("PH005", "ERRO", onde,
                    f"campo marcado como preenchido ainda contém {sentinela!r}; placeholder vazou para o dado")
        if "exec-is-placeholder" in classes:
            rel.add("PH006", "ERRO", onde,
                    "campo preenchido com classe de placeholder; o leitor vai ler dado real como pendência")
        if not texto.strip():
            rel.add("PH010", "ERRO", onde, "campo marcado como preenchido mas sem conteúdo")
        if modo == "branco":
            rel.add("PH014", "AVISO", onde,
                    "campo preenchido num caderno declarado em branco; confirme se o dado deveria estar impresso")


def checar_check(rel: Relatorio, onde: str, estado: str | None, rotulo: str,
                 modo: str, vistos: set[str], ident: str, tem_marca: bool):
    if ident in vistos:
        rel.add("CB007", "ERRO", onde, f"data-check {ident!r} duplicado no mesmo artefato")
    vistos.add(ident)

    if estado is None:
        rel.add("CB001", "ERRO", onde, "caixa de marcar sem data-state")
        return
    if estado not in ESTADOS_CHECK:
        rel.add("CB002", "ERRO", onde, f"data-state={estado!r} inválido; use {sorted(ESTADOS_CHECK)}")
        return
    if not rotulo.strip():
        rel.add("CB006", "ERRO", onde, "caixa de marcar sem rótulo; uma caixa sozinha não diz o que está sendo marcado")
    if modo == "branco" and estado == "on":
        rel.add("CB008", "ERRO", onde,
                "caixa já marcada num caderno em branco; quem imprime recebe uma decisão que não tomou")
    if estado == "on" and not tem_marca:
        rel.add("CB009", "ERRO", onde, "estado on sem a marca desenhada (exec-check__mark)")
    if estado != "on" and tem_marca:
        rel.add("CB009", "ERRO", onde, f"marca desenhada com data-state={estado!r}")


# --------------------------------------------------------------------------
# SVG
# --------------------------------------------------------------------------

def _num(valor: str | None) -> float | None:
    if valor is None:
        return None
    m = re.match(r"^\s*(-?\d*\.?\d+)", valor)
    return float(m.group(1)) if m else None


def validar_svg(caminho: Path, tk: Tokens, modo: str, sentinela: str, permitir_flat: bool) -> Relatorio:
    rel = Relatorio(str(caminho), modo)
    bruto = caminho.read_text(encoding="utf-8", errors="replace")

    try:
        raiz = ET.fromstring(bruto)
    except ET.ParseError as e:
        rel.add("XML001", "ERRO", "documento", f"SVG malformado: {e}")
        rel.contagem = {"campos": 0, "checkboxes": 0}
        return rel

    checar_tokens(rel, bruto, tk, permitir_flat)
    checar_contraste_placeholder(rel, tk)

    # Escala: quantos mm vale uma unidade do viewBox. Sem isso, medir a caixa
    # de marcar em unidades de usuário não diz nada sobre o papel.
    escala = 1.0
    largura_mm = _num(raiz.get("width"))
    vb = (raiz.get("viewBox") or "").split()
    if largura_mm and len(vb) == 4 and (raiz.get("width") or "").endswith("mm"):
        try:
            escala = largura_mm / float(vb[2])
        except (ValueError, ZeroDivisionError):
            escala = 1.0
    else:
        rel.add("GEO003", "AVISO", "svg",
                "largura não declarada em mm com viewBox correspondente; medidas físicas não puderam ser conferidas")

    alvo_w, alvo_h = tk.mm("exec-page-width"), tk.mm("exec-page-height")
    altura_mm = _num(raiz.get("height"))
    if largura_mm and altura_mm:
        if abs(largura_mm - alvo_w) > 0.5 or abs(altura_mm - alvo_h) > 0.5:
            rel.add("GEO001", "ERRO", "svg",
                    f"geometria {largura_mm}×{altura_mm}mm diverge do contrato {alvo_w}×{alvo_h}mm")

    campos = checks = 0
    vistos_campo: set[str] = set()
    vistos_check: set[str] = set()

    for el in raiz.iter():
        attrs = el.attrib
        campo = attrs.get("data-field")
        ident = attrs.get("data-check")

        if campo:
            campos += 1
            classes = set()
            for filho in el.iter():
                classes |= _classes(filho.attrib)
            checar_campo(rel, f"data-field={campo}", attrs.get("data-state"), classes,
                         _texto_svg(el), sentinela, modo, vistos_campo, campo)

        if ident:
            checks += 1
            tem_marca = any("exec-check__mark" in _classes(f.attrib) for f in el.iter())
            rotulo = attrs.get("data-label") or _texto_svg(el)
            checar_check(rel, f"data-check={ident}", attrs.get("data-state"), rotulo,
                         modo, vistos_check, ident, tem_marca)

            caixa = next((f for f in el.iter() if "exec-check__box" in _classes(f.attrib)), None)
            if caixa is None:
                rel.add("CB010", "ERRO", f"data-check={ident}", "sem elemento com classe exec-check__box")
            else:
                w = (_num(caixa.get("width")) or 0) * escala
                h = (_num(caixa.get("height")) or 0) * escala
                if w and h:
                    if min(w, h) < MIN_LADO_CHECK_MM:
                        rel.add("CB003", "ERRO", f"data-check={ident}",
                                f"caixa de {w:.2f}×{h:.2f}mm; mínimo {MIN_LADO_CHECK_MM}mm de lado para caber um traço de caneta")
                    if max(w, h) and abs(w - h) / max(w, h) > TOLERANCIA_QUADRADO:
                        rel.add("CB004", "AVISO", f"data-check={ident}",
                                f"caixa {w:.2f}×{h:.2f}mm fora do quadrado; caixa retangular lê como campo de texto")
                traco = _num(caixa.get("stroke-width"))
                if traco is not None and traco * escala < MIN_TRACO_MM:
                    rel.add("CB005", "ERRO", f"data-check={ident}",
                            f"traço de {traco * escala:.2f}mm; abaixo de {MIN_TRACO_MM}mm some na impressão")

    rel.contagem = {"campos": campos, "checkboxes": checks}
    if campos == 0 and checks == 0:
        rel.add("MK001", "AVISO", "documento",
                "nenhum data-field nem data-check encontrado; ou o artefato não tem campos, ou não segue o contrato de marcação")
    return rel


# --------------------------------------------------------------------------
# HTML
# --------------------------------------------------------------------------

def validar_html(caminho: Path, tk: Tokens, modo: str, sentinela: str, permitir_flat: bool) -> Relatorio:
    rel = Relatorio(str(caminho), modo)
    bruto = caminho.read_text(encoding="utf-8", errors="replace")

    arvore = ArvoreHTML()
    arvore.feed(bruto)

    checar_tokens(rel, bruto, tk, permitir_flat)
    checar_contraste_placeholder(rel, tk)

    estilos = "\n".join(TAG_STYLE.findall(bruto))
    if "print-color-adjust" not in estilos:
        rel.add("PR001", "ERRO", "<style>",
                "sem print-color-adjust: exact; o navegador clareia cor e fundo no PDF e derruba o contraste")
    if "@page" not in estilos:
        rel.add("PR002", "ERRO", "<style>", "sem regra @page; o motor de impressão aplica margem e escala próprias")
    if "page-break-inside" not in estilos and "break-inside" not in estilos:
        rel.add("PR003", "AVISO", "<style>",
                "sem controle de quebra; blocos vão ser cortados ao meio entre páginas num relatório longo")

    campos = checks = 0
    vistos_campo: set[str] = set()
    vistos_check: set[str] = set()

    for no in _descendentes(arvore.raiz):
        attrs = no["attrs"]
        campo = attrs.get("data-field")
        ident = attrs.get("data-check")

        if campo:
            campos += 1
            checar_campo(rel, f"data-field={campo}", attrs.get("data-state"), _classes_de(no),
                         _texto_de(no), sentinela, modo, vistos_campo, campo)

        if ident:
            checks += 1
            classes = _classes_de(no)
            rotulo = attrs.get("data-label") or _texto_de(no)
            checar_check(rel, f"data-check={ident}", attrs.get("data-state"), rotulo,
                         modo, vistos_check, ident, "exec-check__mark" in classes)
            if "exec-check__box" not in classes:
                rel.add("CB010", "ERRO", f"data-check={ident}", "sem elemento com classe exec-check__box")

    if checks and "--exec-check-size" not in estilos:
        rel.add("CB011", "AVISO", "<style>",
                "caixas de marcar presentes mas o lado não vem de var(--exec-check-size); "
                "a geometria física não pode ser conferida")

    rel.contagem = {"campos": campos, "checkboxes": checks}
    return rel




# --------------------------------------------------------------------------

def imprimir_texto(rels: list[Relatorio]) -> None:
    for rel in rels:
        print(f"\n{rel.status}  {rel.arquivo}  (modo {rel.modo})")
        print(f"      campos: {rel.contagem.get('campos', 0)}  caixas: {rel.contagem.get('checkboxes', 0)}")
        if not rel.achados:
            print("      nenhum achado")
        for a in rel.achados:
            print(f"      [{a.severidade:5}] {a.codigo}  {a.onde}")
            print(f"              {a.mensagem}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("arquivos", nargs="+", type=Path)
    p.add_argument("--modo", choices=["branco", "preenchido"], default="branco")
    p.add_argument("--format", choices=["texto", "json"], default="texto")
    p.add_argument("--sentinela", default=SENTINELA_PADRAO)
    p.add_argument("--tokens", type=Path, default=None)
    p.add_argument("--permitir-flat", action="store_true",
                   help="aceita cor literal fora do bloco de tokens; use só na variante achatada para "
                        "renderizador que não resolve var() em SVG")
    args = p.parse_args()

    try:
        tk = Tokens.load(args.tokens)
    except FileNotFoundError as e:
        print(f"AGUARDANDO CONTRATO DE TOKENS: {e}", file=sys.stderr)
        return 1
    rels: list[Relatorio] = []
    for caminho in args.arquivos:
        if not caminho.exists():
            rel = Relatorio(str(caminho), args.modo)
            rel.add("IO001", "ERRO", "arquivo", "não encontrado")
            rels.append(rel)
            continue
        fn = validar_html if caminho.suffix.lower() in {".html", ".htm"} else validar_svg
        rels.append(fn(caminho, tk, args.modo, args.sentinela, args.permitir_flat))

    if args.format == "json":
        print(json.dumps({
            "status": "FAIL" if any(r.erros for r in rels) else "PASS",
            "arquivos": [r.to_dict() for r in rels],
        }, ensure_ascii=False, indent=2))
    else:
        imprimir_texto(rels)

    return 1 if any(r.erros for r in rels) else 0


if __name__ == "__main__":
    raise SystemExit(main())
