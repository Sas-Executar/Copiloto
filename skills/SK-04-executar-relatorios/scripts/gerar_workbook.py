#!/usr/bin/env python3
"""Gera o Desk&Go Business Workbook: cinco peças A4 na família Executar Playbook.

Duas garantias que valem mais que a aparência:

1. Determinismo — mesma versão + mesmo tema produzem bytes idênticos. Sem data,
   sem contador, sem ordem de dicionário dependente de execução.
2. Nada parcial — as peças são escritas num diretório temporário, validadas
   uma a uma, e só então movidas. Pacote pela metade é pior que pacote nenhum:
   alguém imprime as três que saíram e descobre o buraco na reunião.

Uso:
  python3 gerar_workbook.py --output-dir out/
  python3 gerar_workbook.py --output-dir out/ --force
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tokens import Tokens  # noqa: E402
from validar_artefato import validar_svg  # noqa: E402

VERSAO = "1.0.0"

# ---------------------------------------------------------------------------
# Geometria da página. Deriva dos tokens, não de números soltos.
# ---------------------------------------------------------------------------
GRADE_COLUNAS = 12
Y_CORPO = 42.0
Y_LIMITE = 252.0          # abaixo disso começa o bloco de aceite
GAP_LINHA = 3.0

# ---------------------------------------------------------------------------
# As cinco peças. Ordem e escopo fixos — nunca pergunte quais incluir.
#   ("secao", titulo)
#   ("campo", id, rótulo, colunas, altura_mm)
# ---------------------------------------------------------------------------
PECAS: tuple = (
    ("01", "Fundação do Negócio", (
        ("secao", "Identidade"),
        ("campo", "proposito", "PROPÓSITO", 6, 22),
        ("campo", "problema", "PROBLEMA QUE RESOLVE", 6, 22),
        ("campo", "publico", "PÚBLICO", 6, 22),
        ("campo", "proposta-valor", "PROPOSTA DE VALOR", 6, 22),
        ("secao", "Portfólio híbrido — três ofertas"),
        ("campo", "oferta-digital", "OFERTA DIGITAL", 4, 24),
        ("campo", "oferta-servico", "OFERTA DE SERVIÇO", 4, 24),
        ("campo", "oferta-fisica", "OFERTA FÍSICA", 4, 24),
        ("secao", "Matriz de hipóteses — cinco linhas"),
        ("campo", "hipotese-1", "HIPÓTESE 1 · COMO TESTAR · SINAL DE FALSA", 12, 11),
        ("campo", "hipotese-2", "HIPÓTESE 2 · COMO TESTAR · SINAL DE FALSA", 12, 11),
        ("campo", "hipotese-3", "HIPÓTESE 3 · COMO TESTAR · SINAL DE FALSA", 12, 11),
        ("campo", "hipotese-4", "HIPÓTESE 4 · COMO TESTAR · SINAL DE FALSA", 12, 11),
        ("campo", "hipotese-5", "HIPÓTESE 5 · COMO TESTAR · SINAL DE FALSA", 12, 11),
        ("secao", "Posição competitiva"),
        ("campo", "concorrentes", "TRÊS CONCORRENTES E O QUE CADA UM FAZ MELHOR", 7, 26),
        ("matriz", "matriz-posicao", "MATRIZ 2×2", 5, 26),
    ), (
        "Três ofertas descritas, uma em cada natureza",
        "Cinco hipóteses com sinal de falsificação escrito",
        "Três concorrentes nomeados, não categorias genéricas",
        "Proposta de valor cabe numa frase falada em voz alta",
    )),

    ("02", "GTM / Lançamento", (
        ("secao", "Direção"),
        ("campo", "objetivo-lancamento", "OBJETIVO DO LANÇAMENTO", 6, 22),
        ("campo", "mensagem-chave", "MENSAGEM-CHAVE", 6, 22),
        ("secao", "Matriz de canais — três canais"),
        ("campo", "canal-1", "CANAL 1 · PAPEL · ESFORÇO SEMANAL", 4, 26),
        ("campo", "canal-2", "CANAL 2 · PAPEL · ESFORÇO SEMANAL", 4, 26),
        ("campo", "canal-3", "CANAL 3 · PAPEL · ESFORÇO SEMANAL", 4, 26),
        ("secao", "Cronograma de oito semanas"),
        ("campo", "semanas-1-4", "SEMANAS 1 A 4", 6, 30),
        ("campo", "semanas-5-8", "SEMANAS 5 A 8", 6, 30),
        ("secao", "Métricas e síntese"),
        ("campo", "metrica-1", "MÉTRICA 1 · META", 4, 18),
        ("campo", "metrica-2", "MÉTRICA 2 · META", 4, 18),
        ("campo", "metrica-3", "MÉTRICA 3 · META", 4, 18),
        ("campo", "sintese-executiva", "SÍNTESE EXECUTIVA", 12, 20),
    ), (
        "Cada métrica tem meta numérica, não adjetivo",
        "As oito semanas têm dono e entrega, não só tema",
        "Mensagem-chave testada com alguém de fora",
        "Nenhum canal depende de orçamento ainda não aprovado",
    )),

    ("03", "Roadmap", (
        ("secao", "Visão de doze meses"),
        ("campo", "visao-12-meses", "ONDE O NEGÓCIO PRECISA ESTAR EM DOZE MESES", 12, 22),
        ("secao", "Quatro fases trimestrais"),
        ("campo", "q1", "Q1 · TEMA E ENTREGA", 3, 30),
        ("campo", "q2", "Q2 · TEMA E ENTREGA", 3, 30),
        ("campo", "q3", "Q3 · TEMA E ENTREGA", 3, 30),
        ("campo", "q4", "Q4 · TEMA E ENTREGA", 3, 30),
        ("secao", "Agora, próximo, depois"),
        ("campo", "agora", "AGORA", 4, 28),
        ("campo", "proximo", "PRÓXIMO", 4, 28),
        ("campo", "depois", "DEPOIS", 4, 28),
        ("secao", "Marcos, governança e risco"),
        ("campo", "marcos-do-ano", "TRÊS MARCOS DO ANO", 6, 24),
        ("campo", "governanca-risco", "GOVERNANÇA E RISCOS ABERTOS", 6, 24),
    ), (
        "Cada trimestre tem uma entrega verificável, não um tema",
        "Agora contém no máximo o que uma pessoa executa",
        "Os três marcos têm data e critério de conclusão",
        "Todo risco aberto tem dono e próximo passo",
    )),

    ("04", "Kanban de Sprints", (
        ("secao", "Dados do ciclo"),
        ("campo", "ciclo-numero", "CICLO Nº", 3, 16),
        ("campo", "ciclo-periodo", "PERÍODO", 3, 16),
        ("campo", "ciclo-objetivo", "OBJETIVO DO CICLO", 6, 16),
        ("secao", "Board — limite de trabalho em andamento na coluna do meio"),
        ("campo", "a-fazer", "A FAZER", 4, 62),
        ("campo", "fazendo", "FAZENDO · LIMITE 2", 4, 62),
        ("campo", "feito", "FEITO", 4, 62),
        ("secao", "Síntese e cartões destacáveis"),
        ("campo", "sintese-ciclo", "O QUE O CICLO ENSINOU", 12, 20),
        ("cartoes", "cartoes-destacaveis", "CARTÕES PARA RECORTAR", 12, 30),
    ), (
        "A coluna do meio respeitou o limite o ciclo inteiro",
        "Todo item em Feito tem evidência anexada",
        "O que não coube foi devolvido ao backlog, não esquecido",
        "A síntese aponta uma mudança concreta para o próximo ciclo",
    )),

    ("05", "Business Model Canvas", (
        ("secao", "Metade esquerda — como o negócio entrega"),
        ("campo", "bmc-parcerias", "PARCERIAS-CHAVE", 4, 52),
        ("campo", "bmc-atividades", "ATIVIDADES-CHAVE", 4, 52),
        ("campo", "bmc-recursos", "RECURSOS-CHAVE", 4, 52),
        ("secao", "Centro e metade direita — como o negócio se relaciona"),
        ("campo", "bmc-proposta", "PROPOSTA DE VALOR", 4, 52),
        ("campo", "bmc-relacionamento", "RELACIONAMENTO", 4, 52),
        ("campo", "bmc-canais", "CANAIS", 4, 52),
        ("secao", "Base — quem paga e quanto custa"),
        ("campo", "bmc-segmentos", "SEGMENTOS DE CLIENTE", 4, 40),
        ("campo", "bmc-custos", "ESTRUTURA DE CUSTOS", 4, 40),
        ("campo", "bmc-receita", "FONTES DE RECEITA", 4, 40),
    ), (
        "Os nove blocos preenchidos, nenhum em branco por esquecimento",
        "Cada fonte de receita liga a um segmento nomeado",
        "Custos incluem o tempo do fundador, não só o desembolso",
        "As duas metades leem juntas sem se contradizer",
    )),
)


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------------------
# blocos
# ---------------------------------------------------------------------------

def _pauta(x: float, y: float, w: float, h: float, inicio: float = 8.0, passo: float = 6.0) -> str:
    linhas = []
    cursor = inicio
    while cursor <= h - 3:
        linhas.append(f'<line x1="{x + 3:g}" y1="{y + cursor:g}" x2="{x + w - 3:g}" '
                      f'y2="{y + cursor:g}" class="linha-escrita" stroke-width="0.25"/>')
        cursor += passo
    return "".join(linhas)


def bloco_campo(x, y, w, h, ident, rotulo) -> str:
    return (f'<g class="exec-field" data-field="{ident}" data-state="blank">'
            f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="1" '
            f'class="exec-field__box" stroke-width="0.35"/>'
            f'<text x="{x + 3:g}" y="{y + 5:g}" class="rotulo">{esc(rotulo)}</text>'
            f'{_pauta(x, y, w, h)}'
            '</g>')


def bloco_matriz(x, y, w, h, ident, rotulo) -> str:
    cx, cy = x + w / 2, y + 8 + (h - 10) / 2
    return (f'<g class="exec-field" data-field="{ident}" data-state="blank">'
            f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="1" '
            f'class="exec-field__box" stroke-width="0.35"/>'
            f'<text x="{x + 3:g}" y="{y + 5:g}" class="rotulo">{esc(rotulo)}</text>'
            f'<line x1="{cx:g}" y1="{y + 8:g}" x2="{cx:g}" y2="{y + h - 2:g}" class="linha-escrita" stroke-width="0.25"/>'
            f'<line x1="{x + 3:g}" y1="{cy:g}" x2="{x + w - 3:g}" y2="{cy:g}" class="linha-escrita" stroke-width="0.25"/>'
            '</g>')


def bloco_cartoes(x, y, w, h, ident, rotulo) -> str:
    """Cartões destacáveis: tracejado só entre unidades macro, como manda o
    vocabulário único de separador por nível."""
    n = 4
    cw = (w - 3 * (n - 1)) / n
    cartoes = "".join(
        f'<rect x="{x + i * (cw + 3):g}" y="{y + 7:g}" width="{cw:g}" height="{h - 9:g}" rx="1" '
        f'class="recorte" stroke-width="0.35"/>'
        for i in range(n)
    )
    return (f'<g class="exec-field" data-field="{ident}" data-state="blank">'
            f'<text x="{x:g}" y="{y + 4:g}" class="rotulo">{esc(rotulo)}</text>'
            f'{cartoes}'
            f'<rect x="{x:g}" y="{y + 7:g}" width="{w:g}" height="{h - 9:g}" rx="1" '
            f'class="exec-field__box" fill="none" stroke-width="0" opacity="0"/>'
            '</g>')


def bloco_check(x, y, ident, rotulo, lado: float, traco: float) -> str:
    return (f'<g class="exec-check" data-check="{ident}" data-state="off" data-label="{esc(rotulo)}">'
            f'<rect x="{x:g}" y="{y:g}" width="{lado:g}" height="{lado:g}" rx="0.4" '
            f'class="exec-check__box" stroke-width="{traco:g}"/>'
            f'<text x="{x + lado + 2:g}" y="{y + lado * 0.78:g}" class="exec-check__label">{esc(rotulo)}</text>'
            '</g>')


# ---------------------------------------------------------------------------
# montagem da página
# ---------------------------------------------------------------------------

def render_peca(numero: str, titulo: str, spec: tuple, aceites: tuple, tk: Tokens) -> str:
    margem = tk.mm("exec-page-margin")
    largura = tk.mm("exec-page-width")
    altura = tk.mm("exec-page-height")
    conteudo = tk.mm("exec-content-width")
    calha = tk.mm("exec-grid-gutter")
    lado_check = tk.mm("exec-check-size")
    traco_check = tk.mm("exec-check-stroke")
    col = (conteudo - calha * (GRADE_COLUNAS - 1)) / GRADE_COLUNAS

    def span(n: int) -> float:
        return n * col + calha * (n - 1)

    partes: list[str] = []
    y = Y_CORPO
    cursor_col = 0
    altura_linha = 0.0

    def quebrar():
        nonlocal y, cursor_col, altura_linha
        if cursor_col:
            y += altura_linha + GAP_LINHA
        cursor_col = 0
        altura_linha = 0.0

    for item in spec:
        if item[0] == "secao":
            quebrar()
            partes.append(f'<text x="{margem:g}" y="{y + 3:g}" class="titulo-secao">{esc(item[1])}</text>')
            y += 6.0
            continue

        tipo, ident, rotulo, colunas, h = item
        if cursor_col + colunas > GRADE_COLUNAS:
            quebrar()
        x = margem + cursor_col * (col + calha)
        w = span(colunas)
        construtor = {"campo": bloco_campo, "matriz": bloco_matriz, "cartoes": bloco_cartoes}[tipo]
        partes.append(construtor(x, y, w, h, ident, rotulo))
        cursor_col += colunas
        altura_linha = max(altura_linha, h)
    quebrar()

    if y > Y_LIMITE:
        raise ValueError(
            f"peça {numero} estourou a mancha: conteúdo termina em {y:.1f}mm, limite {Y_LIMITE}mm. "
            "Reduza a altura de um bloco ou mova para uma segunda folha — não encolha a margem."
        )

    # bloco de aceite, ancorado no rodapé para que todas as peças tenham o
    # mesmo lugar de conferência
    y_aceite = Y_LIMITE + 2
    aceite = [f'<line x1="{margem:g}" y1="{y_aceite:g}" x2="{largura - margem:g}" y2="{y_aceite:g}" '
              f'class="regua-unidade" stroke-width="0.35"/>',
              f'<text x="{margem:g}" y="{y_aceite + 6:g}" class="titulo-secao">Critérios de aceite da peça</text>']
    for i, texto in enumerate(aceites):
        cx = margem + (i % 2) * (conteudo / 2)
        cy = y_aceite + 10 + (i // 2) * 7
        aceite.append(bloco_check(cx, cy, f"p{numero}-ac-{i + 1:02d}", texto, lado_check, traco_check))

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{largura:g}mm" height="{altura:g}mm" viewBox="0 0 {largura:g} {altura:g}" role="img" aria-labelledby="titulo descricao">
  <title id="titulo">{esc(numero)} — {esc(titulo)}</title>
  <desc id="descricao">Peça {esc(numero)} de 05 do Desk&amp;Go Business Workbook, tema {esc(tk.tema_rotulo)}. Campos em branco, para imprimir e preencher.</desc>
  <style>
    /* TOKENS:INICIO */
{tk.css_block()}
    /* TOKENS:FIM */
    .pagina        {{ fill: var(--exec-color-surface-page); }}
    .faixa-marca   {{ fill: var(--exec-color-brand); }}
    text           {{ font-family: var(--exec-font-stack); }}
    .eyebrow       {{ font-size: 2.8px; font-weight: 600; letter-spacing: .6px; fill: var(--exec-color-ink-inverse); }}
    .numero        {{ font-size: 9px; font-weight: 600; fill: var(--exec-color-brand); }}
    .titulo-pagina {{ font-size: 9px; font-weight: 600; fill: var(--exec-color-ink-title); }}
    .titulo-secao  {{ font-size: 4.2px; font-weight: 600; fill: var(--exec-color-ink-title); }}
    .rotulo        {{ font-size: 2.8px; font-weight: 600; letter-spacing: .3px; fill: var(--exec-color-ink-body); }}
    .meta          {{ font-size: 2.4px; fill: var(--exec-color-ink-muted); }}
    .exec-field__box   {{ fill: none; stroke: var(--exec-color-rule-strong); }}
    .linha-escrita     {{ stroke: var(--exec-color-rule-subtle); }}
    .regua             {{ stroke: var(--exec-color-rule-default); }}
    .regua-unidade     {{ stroke: var(--exec-color-rule-default); stroke-dasharray: 1.4 1.4; }}
    .recorte           {{ fill: none; stroke: var(--exec-color-rule-default); stroke-dasharray: 1.2 1.2; }}
    .exec-check__box   {{ fill: none; stroke: var(--exec-color-rule-strong); }}
    .exec-check__label {{ font-size: 2.8px; fill: var(--exec-color-ink-body); }}
    .corte             {{ stroke: var(--exec-color-ink-data); stroke-width: .3; }}
  </style>
  <rect width="{largura:g}" height="{altura:g}" class="pagina"/>
  <path class="corte" d="M0 {margem:g}h6M{margem:g} 0v6M{largura - 6:g} {margem:g}h6M{largura - margem:g} 0v6M0 {altura - margem:g}h6M{margem:g} {altura - 6:g}v6M{largura - 6:g} {altura - margem:g}h6M{largura - margem:g} {altura - 6:g}v6"/>
  <rect x="{margem:g}" y="{margem:g}" width="72" height="6" rx="3" class="faixa-marca"/>
  <text x="{margem + 4:g}" y="{margem + 4:g}" class="eyebrow">DESK&amp;GO BUSINESS WORKBOOK · {esc(tk.tema_rotulo.upper())}</text>
  <text x="{margem:g}" y="{margem + 19:g}" class="numero">{esc(numero)}</text>
  <text x="{margem + 16:g}" y="{margem + 19:g}" class="titulo-pagina">{esc(titulo)}</text>
  <line x1="{margem:g}" y1="{margem + 24:g}" x2="{largura - margem:g}" y2="{margem + 24:g}" class="regua" stroke-width="0.5"/>
  {"".join(partes)}
  {"".join(aceite)}
  <text x="{margem:g}" y="{altura - 8:g}" class="meta">A4 {largura:g} × {altura:g} mm · margem segura {margem:g} mm · campos em branco por decisão · v{VERSAO}</text>
  <text x="{largura - margem:g}" y="{altura - 8:g}" class="meta" text-anchor="end">{esc(numero)}/05</text>
</svg>
'''


def nome_arquivo(numero: str, titulo: str, tema: str) -> str:
    slug = (titulo.lower()
            .replace(" / ", "-").replace(" ", "-")
            .replace("ç", "c").replace("ã", "a").replace("ó", "o").replace("í", "i").replace("é", "e"))
    return f"{numero}-{slug}-{tema}.svg"


def gerar(output_dir: Path, tema: str, force: bool) -> list[Path]:
    tk = Tokens.load(tema=tema)
    output_dir = output_dir.resolve()
    destinos = [output_dir / nome_arquivo(n, t, tema) for n, t, _, _ in PECAS]

    if output_dir.exists() and any(output_dir.iterdir()) and not force:
        raise FileExistsError(f"diretório não vazio; use --force somente com autorização: {output_dir}")

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="deskgo-wb-", dir=output_dir.parent))
    try:
        provisorios = []
        for numero, titulo, spec, aceites in PECAS:
            caminho = stage / nome_arquivo(numero, titulo, tema)
            caminho.write_text(render_peca(numero, titulo, spec, aceites, tk), encoding="utf-8", newline="\n")
            ET.parse(caminho)
            rel = validar_svg(caminho, tk, "branco", "— pendente", permitir_flat=False)
            if rel.erros:
                detalhe = "; ".join(f"{a.codigo} {a.onde}: {a.mensagem}" for a in rel.achados if a.severidade == "ERRO")
                raise ValueError(f"peça {numero} reprovou no validador — {detalhe}")
            provisorios.append(caminho)

        output_dir.mkdir(parents=True, exist_ok=True)
        for origem, destino in zip(provisorios, destinos):
            origem.replace(destino)
        return destinos
    finally:
        shutil.rmtree(stage, ignore_errors=True)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument("--tema", default="executar", help="identidade única do contrato de tokens (ver assets/tokens/temas.json)")
    p.add_argument("--force", action="store_true", help="sobrescreve diretório não vazio; só com autorização explícita")
    args = p.parse_args()
    try:
        arquivos = gerar(args.output_dir, args.tema, args.force)
    except (OSError, ValueError, KeyError) as erro:
        print(f"ERRO: {erro}", file=sys.stderr)
        return 2
    print(json.dumps({"status": "PASS", "tema": args.tema,
                      "arquivos": [str(a) for a in arquivos]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
