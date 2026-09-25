#!/usr/bin/env python3
"""Resolvedor da família de tokens Executar Playbook (raw -> alias -> componente).

Existe para que gerador e validador leiam exatamente os mesmos valores. Se cada
script relesse o JSON do seu jeito, o validador acabaria aprovando artefato que
o gerador produziu errado — os dois divergiriam em silêncio.

Uso como biblioteca:
    from tokens import Tokens
    t = Tokens.load()
    t.mm("exec-page-margin")        # 10.0
    t.color("exec-color-brand")     # "#RRGGBB" (exemplo ilustrativo — valor real vem do contrato de tokens)
    t.css_block()                   # ":root{--exec-...:...}"

Uso como CLI:
    python3 tokens.py --css              # imprime o bloco CSS
    python3 tokens.py --lacunas          # lista o que continua indefinido
    python3 tokens.py --contraste        # tabela de contraste dos pares que importam
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REF = re.compile(r"^\{([a-z0-9-]+)\}$")
ASSETS = Path(__file__).resolve().parent.parent / "assets" / "tokens"
# AGUARDANDO CONTRATO DE TOKENS: este repositório não traz mais um
# executar-playbook.tokens.json com valores concretos. `tokens.json` é o
# arquivo que o novo contrato de tokens do usuário deve preencher, seguindo
# a forma documentada em assets/tokens/tokens.schema.json (ver também
# assets/tokens/README.md e references/design-tokens.md).
DEFAULT_PATH = ASSETS / "tokens.json"
TEMAS_PATH = ASSETS / "temas.json"

# Pares que precisam de verificação de contraste toda vez que a paleta mudar.
# (frente, fundo, uso, minimo)
PARES_CONTRASTE = [
    ("ink-body", "surface-page", "corpo de texto", 4.5),
    ("ink-title", "surface-page", "titulo", 4.5),
    ("ink-placeholder", "surface-page", "placeholder", 4.5),
    ("ink-muted", "surface-page", "rotulo decorativo", 3.0),
    # brand (#00BF63) é só preenchimento (barra, régua, ponto); texto de marca usa brand-strong.
    ("brand-strong", "surface-page", "texto de marca", 4.5),
    ("brand-strong", "brand-soft", "texto de marca sobre chip", 4.5),
    ("brand-strong", "accent-soft-alt", "texto de marca sobre destaque", 4.5),
    ("ink-secondary-strong", "surface-page", "rotulo de dado", 4.5),
    ("ink-secondary-strong", "surface-sunken", "rotulo sobre cabecalho", 4.5),
    ("ink-inverse", "surface-inverse", "texto sobre capa escura", 4.5),
    ("ink-inverse", "brand-strong", "texto sobre marca", 4.5),
    ("rule-strong", "surface-page", "contorno de checkbox/campo", 3.0),
]
# Nomes de token, sem o prefixo `exec-color-` (esse prefixo só existe quando o
# alias vira custom property CSS, não na camada alias do JSON). O par
# ink-inverse/surface-inverse é pulado até surface-inverse deixar de ser
# LACUNA — ver references/design-tokens.md.


def _luminancia(hexcolor: str) -> float:
    h = hexcolor.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    canais = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        canais.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = canais
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(frente: str, fundo: str) -> float:
    """Razão de contraste WCAG 2.x entre duas cores hex."""
    a, b = _luminancia(frente), _luminancia(fundo)
    claro, escuro = max(a, b), min(a, b)
    return round((claro + 0.05) / (escuro + 0.05), 2)


class Tokens:
    def __init__(self, data: dict):
        self.meta = data["meta"]
        self.raw = data["raw"]
        self.alias = data["alias"]
        self.componente = data["componente"]
        self.tema = "executar"
        self.tema_rotulo = "EXECUTAR"
        self._cache: dict[str, object] = {}

    @classmethod
    def load(cls, path: Path | None = None, tema: str | None = None) -> "Tokens":
        alvo = path or DEFAULT_PATH
        if not alvo.exists():
            raise FileNotFoundError(
                f"{alvo} não existe. Este stack aguarda o novo contrato de tokens do "
                "usuário: crie assets/tokens/tokens.json seguindo a forma documentada "
                "em assets/tokens/tokens.schema.json antes de gerar ou validar artefatos "
                "visuais. Ver também assets/tokens/README.md."
            )
        t = cls(json.loads(alvo.read_text(encoding="utf-8")))
        if tema:
            t.aplicar_tema(tema)
        return t

    @staticmethod
    def temas(path: Path | None = None) -> dict:
        alvo = path or TEMAS_PATH
        if not alvo.exists():
            raise FileNotFoundError(
                f"{alvo} não existe. Crie assets/tokens/temas.json seguindo a forma "
                "documentada em assets/tokens/temas.schema.json quando o novo contrato "
                "de tokens chegar."
            )
        return json.loads(alvo.read_text(encoding="utf-8"))

    def aplicar_tema(self, nome: str, path: Path | None = None) -> None:
        """Sobrepõe valores na camada alias. Um tema só troca leitura visual —
        se precisar criar token novo, é sinal de que virou outro contrato."""
        temas = self.temas(path)
        if nome not in temas or nome.startswith("_"):
            raise KeyError(f"tema desconhecido: {nome}. Disponíveis: {sorted(k for k in temas if not k.startswith('_'))}")
        self.tema = nome
        self.tema_rotulo = temas[nome].get("rotulo", nome)
        for chave, valor in temas[nome].get("overrides", {}).items():
            if chave not in self.alias:
                raise KeyError(f"tema {nome!r} tenta criar o token {chave!r}, que não existe na camada alias")
            self.alias[chave] = dict(self.alias[chave], valor=valor, origem="DECISAO",
                                     base=f"sobreposição do tema {nome}")
        self._cache.clear()

    # -- resolução ---------------------------------------------------------
    def _bruto(self, nome: str):
        for camada in (self.alias, self.raw):
            if nome in camada and not nome.startswith("_"):
                return camada[nome]
        raise KeyError(f"token desconhecido: {nome}")

    def resolve(self, nome: str):
        """Valor final de um token, seguindo referências {outro-token}."""
        if nome in self._cache:
            return self._cache[nome]
        entrada = self._bruto(nome)
        valor = entrada["valor"]
        visto = {nome}
        while isinstance(valor, str) and (m := REF.match(valor)):
            alvo = m.group(1)
            if alvo in visto:
                raise ValueError(f"referência circular em {nome}")
            visto.add(alvo)
            valor = self._bruto(alvo)["valor"]
        self._cache[nome] = valor
        return valor

    def origem(self, nome: str) -> str:
        return self._bruto(nome)["origem"]

    def base(self, nome: str) -> str:
        return self._bruto(nome).get("base", "")

    def color(self, nome: str) -> str:
        v = self.resolve(nome)
        if not isinstance(v, str) or not v.startswith("#"):
            raise ValueError(f"{nome} não é cor: {v!r}")
        return v

    def mm(self, nome: str) -> float:
        """Valor em milímetros, como float. Recusa converter px-image."""
        v = self.resolve(nome)
        if isinstance(v, (int, float)):
            return float(v)
        if not isinstance(v, str):
            raise ValueError(f"{nome} indefinido (LACUNA) — decida antes de usar")
        if v.endswith("mm"):
            return float(v[:-2])
        if "px-image" in v:
            raise ValueError(f"{nome} está em px-image; converter exige decisão explícita, não acontece aqui")
        raise ValueError(f"{nome} não está em mm: {v!r}")

    def lacunas(self) -> list[str]:
        out = []
        for camada in (self.raw, self.alias):
            for nome, e in camada.items():
                if nome.startswith("_"):
                    continue
                if e.get("origem") == "LACUNA" or e.get("valor") is None:
                    out.append(nome)
        return sorted(out)

    def nomes_alias(self) -> list[str]:
        return [n for n in self.alias if not n.startswith("_")]

    # -- saídas ------------------------------------------------------------
    @staticmethod
    def _nome_css(nome: str) -> str:
        """Nome final da custom property CSS para um alias.

        A camada alias em tokens.json guarda nomes "nus" (ex.: "brand",
        "ink-title") mas cada consumidor espera um prefixo diferente
        conforme sua vocabulary: `--exec-color-*` para a maioria dos
        artefatos (report.css, peca-a4.svg, relatorio-exemplo.html...),
        sem prefixo para o namespace PRISM (armazenado como "prism-*" só
        dentro do JSON, para não colidir de nome), e sem prefixo também
        para geometria/tipografia (`exec-page-width`, `exec-space-4`...),
        que já carregam seu nome final de CSS na própria chave.
        """
        if nome.startswith("prism-"):
            return nome[len("prism-"):]
        if nome.startswith("exec-"):
            return nome
        return f"exec-color-{nome}"

    def css_block(self, indent: str = "  ") -> str:
        """Bloco :root com a camada alias resolvida. Componentes consomem só isto."""
        linhas = [":root{"]
        for nome in self.nomes_alias():
            valor = self.resolve(nome)
            if valor is None:
                continue
            linhas.append(f"{indent}--{self._nome_css(nome)}:{valor};")
        linhas.append("}")
        return "\n".join(linhas)

    def relatorio_contraste(self) -> list[dict]:
        out = []
        for frente, fundo, uso, minimo in PARES_CONTRASTE:
            try:
                r = contraste(self.color(frente), self.color(fundo))
            except (KeyError, ValueError):
                continue
            out.append({
                "frente": frente, "fundo": fundo, "uso": uso,
                "razao": r, "minimo": minimo, "passa": r >= minimo,
            })
        return out


CABECALHO_CSS = """/*
  Gerado a partir de assets/tokens/tokens.json via `python3 scripts/tokens.py --escrever-css`.
  Nao editar a mao.
  Fonte: EXECUTAR-REPORT-PRINT-DS-001 v1.0 (references/200-executive-report-print-contract.md).
*/
"""


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tokens", type=Path, default=DEFAULT_PATH)
    p.add_argument("--tema", default=None, help="playbook | swiss | editorial")
    p.add_argument("--listar-temas", action="store_true")
    p.add_argument("--css", action="store_true")
    p.add_argument("--escrever-css", action="store_true",
                   help="regrava assets/tokens/tokens.css a partir do tokens.json (único jeito de mudar o .css)")
    p.add_argument("--lacunas", action="store_true")
    p.add_argument("--contraste", action="store_true")
    p.add_argument("--sincronizar", nargs="+", type=Path, default=None,
                   help="reescreve o bloco entre /* TOKENS:INICIO */ e /* TOKENS:FIM */ nos arquivos dados")
    args = p.parse_args()

    try:
        if args.listar_temas:
            for nome, spec in Tokens.temas().items():
                if nome.startswith("_"):
                    continue
                print(f"{nome:10} {spec['rotulo']}\n           {spec['descricao']}")
            return 0

        t = Tokens.load(args.tokens, args.tema)
    except FileNotFoundError as e:
        print(f"AGUARDANDO CONTRATO DE TOKENS: {e}", file=sys.stderr)
        return 1

    if args.sincronizar:
        marca = re.compile(r"(/\* TOKENS:INICIO \*/).*?(/\* TOKENS:FIM \*/)", re.S)
        for caminho in args.sincronizar:
            texto = caminho.read_text(encoding="utf-8")
            novo, n = marca.subn(lambda m: f"{m.group(1)}\n{t.css_block()}\n    {m.group(2)}", texto)
            if n:
                caminho.write_text(novo, encoding="utf-8")
            print(f"{'sincronizado' if n else 'sem marcadores'}: {caminho}")

    if args.css:
        print(t.css_block())
    if args.escrever_css:
        destino = ASSETS / "tokens.css"
        destino.write_text(CABECALHO_CSS + t.css_block() + "\n", encoding="utf-8")
        print(f"escrito: {destino}")
    if args.lacunas:
        for n in t.lacunas():
            print(f"LACUNA  {n}  — {t.base(n)}")
    if args.contraste:
        falhas = 0
        for r in t.relatorio_contraste():
            marca = "ok  " if r["passa"] else "FALHA"
            falhas += 0 if r["passa"] else 1
            print(f"{marca} {r['razao']:>6}:1 (min {r['minimo']}) {r['uso']}: {r['frente']} sobre {r['fundo']}")
        if falhas:
            return 1
    if not (args.css or args.escrever_css or args.lacunas or args.contraste or args.sincronizar):
        p.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
