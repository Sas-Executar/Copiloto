#!/usr/bin/env python3
"""Gera relatórios extensos da família Executar Playbook a partir de um spec JSON.

O relatório longo é o lugar onde placeholder vira problema de verdade: numa peça
A4 você enxerga os campos vazios de relance; em quarenta páginas, um "—" solto no
meio de uma tabela passa direto e vira número inventado na leitura de outra
pessoa. Por isso o mesmo contrato de marcação das peças vale aqui, e o validador
roda antes de o arquivo sair do diretório temporário.

O template é dirigido por dados: nenhum conteúdo de cliente mora dentro deste
arquivo. Trocar de cliente é trocar de spec.

Uso:
  python3 gerar_relatorio.py --spec ../assets/data/exemplo-relatorio.json --saida rel.html
  python3 gerar_relatorio.py --spec spec.json --saida rel.html --modo preenchido
  python3 gerar_relatorio.py --lote specs/ --saida-dir out/
"""

from __future__ import annotations

import argparse
import html
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tokens import Tokens  # noqa: E402
from validar_artefato import validar_html  # noqa: E402

SENTINELA = "— pendente"


def e(t) -> str:
    return html.escape(str(t), quote=True)


# ---------------------------------------------------------------------------
# campos e caixas: uma única porta de entrada, para que nenhum bloco invente
# o seu próprio jeito de representar ausência
# ---------------------------------------------------------------------------

def campo(ident: str, rotulo: str, valor, *, para_preencher: bool = False) -> str:
    """Três estados. `para_preencher` marca o campo desenhado para receber caneta;
    valor ausente num relatório que deveria ter o dado vira "empty" com sentinela."""
    if para_preencher:
        return (f'<div class="campo" data-field="{e(ident)}" data-state="blank">'
                f'<span class="rotulo">{e(rotulo)}</span>'
                f'<span class="exec-field__box linha-escrita"></span></div>')
    if valor in (None, ""):
        return (f'<div class="campo" data-field="{e(ident)}" data-state="empty">'
                f'<span class="rotulo">{e(rotulo)}</span>'
                f'<span class="valor exec-is-placeholder">{SENTINELA}</span></div>')
    return (f'<div class="campo" data-field="{e(ident)}" data-state="filled">'
            f'<span class="rotulo">{e(rotulo)}</span>'
            f'<span class="valor">{e(valor)}</span></div>')


def caixa(ident: str, texto: str, estado: str = "off", nota: str | None = None) -> str:
    marca = '<span class="exec-check__mark"></span>' if estado == "on" else ""
    na = '<span class="exec-check__na"></span>' if estado == "na" else ""
    extra = f'<span class="nota">{e(nota)}</span>' if nota else ""
    return (f'<li class="exec-check" data-check="{e(ident)}" data-state="{e(estado)}" data-label="{e(texto)}">'
            f'<span class="exec-check__box">{marca}{na}</span>'
            f'<span class="exec-check__label">{e(texto)}</span>{extra}</li>')


def celula(valor) -> str:
    if valor in (None, ""):
        return f'<td class="exec-is-placeholder">{SENTINELA}</td>'
    if isinstance(valor, (int, float)):
        return f'<td class="num">{e(valor)}</td>'
    return f"<td>{e(valor)}</td>"


# ---------------------------------------------------------------------------
# blocos
# ---------------------------------------------------------------------------

def bloco(b: dict, prefixo: str, n: int) -> str:
    t = b.get("tipo")

    if t == "paragrafo":
        return f'<p>{e(b["texto"])}</p>'

    if t == "lista":
        itens = "".join(f"<li>{e(i)}</li>" for i in b["itens"])
        return f"<ul class=\"lista\">{itens}</ul>"

    if t == "destaque":
        return (f'<aside class="destaque"><span class="rotulo">{e(b.get("rotulo", "Destaque"))}</span>'
                f'<p>{e(b["texto"])}</p></aside>')

    if t == "campo":
        return campo(b.get("id", f"{prefixo}-c{n}"), b["rotulo"], b.get("valor"),
                     para_preencher=bool(b.get("para_preencher")))

    if t == "kpi":
        # O número grande nunca carrega a metodologia junto: linha separada.
        metodo = f'<span class="kpi-metodo">{e(b["metodo"])}</span>' if b.get("metodo") else ""
        ident = b.get("id", f"{prefixo}-kpi{n}")
        if b.get("valor") in (None, ""):
            corpo = f'<span class="kpi-valor exec-is-placeholder">{SENTINELA}</span>'
            estado = "empty"
        else:
            corpo = f'<span class="kpi-valor">{e(b["valor"])}</span>'
            estado = "filled"
        return (f'<div class="kpi campo" data-field="{e(ident)}" data-state="{estado}">'
                f'<span class="rotulo">{e(b["rotulo"])}</span>{corpo}{metodo}</div>')

    if t == "barra":
        pct = max(0, min(100, float(b.get("percentual", 0))))
        nota = f'<span class="nota">{e(b["nota"])}</span>' if b.get("nota") else ""
        return (f'<div class="barra"><span class="rotulo">{e(b["rotulo"])}</span>'
                f'<span class="trilha"><span class="preenchimento" style="width:{pct:g}%"></span></span>'
                f'<span class="valor-barra">{pct:g}%</span>{nota}</div>')

    if t == "medidor":
        linhas = []
        for s in b["series"]:
            pct = max(0, min(100, float(s.get("percentual", 0))))
            classe = "preenchimento" if s.get("destaque", True) else "preenchimento alt"
            linhas.append(f'<div class="medidor-linha"><span class="medidor-nome">{e(s["nome"])}</span>'
                          f'<span class="trilha"><span class="{classe}" style="width:{pct:g}%"></span></span>'
                          f'<span class="valor-barra">{e(s.get("valor", f"{pct:g}%"))}</span></div>')
        return f'<div class="medidor"><span class="rotulo">{e(b["rotulo"])}</span>{"".join(linhas)}</div>'

    if t == "tabela":
        cab = "".join(f"<th>{e(c)}</th>" for c in b["colunas"])
        corpo = "".join("<tr>" + "".join(celula(v) for v in linha) + "</tr>" for linha in b["linhas"])
        legenda = f'<caption>{e(b["legenda"])}</caption>' if b.get("legenda") else ""
        return f'<table class="tabela">{legenda}<thead><tr>{cab}</tr></thead><tbody>{corpo}</tbody></table>'

    if t == "checklist":
        itens = "".join(
            caixa(i.get("id", f"{prefixo}-ck{n}-{j}"), i["texto"], i.get("estado", "off"), i.get("nota"))
            for j, i in enumerate(b["itens"], 1)
        )
        titulo = f'<span class="rotulo">{e(b["rotulo"])}</span>' if b.get("rotulo") else ""
        return f'<div class="checklist">{titulo}<ul>{itens}</ul></div>'

    if t == "cronograma":
        raias = []
        for r in b["raias"]:
            ini = max(0, min(100, float(r.get("inicio", 0))))
            lar = max(1, min(100 - ini, float(r.get("duracao", 10))))
            raias.append(f'<div class="raia"><span class="raia-nome">{e(r["nome"])}</span>'
                         f'<span class="raia-pista"><span class="raia-barra" '
                         f'style="margin-left:{ini:g}%;width:{lar:g}%"></span></span></div>')
        return f'<div class="cronograma"><span class="rotulo">{e(b["rotulo"])}</span>{"".join(raias)}</div>'

    raise ValueError(f"bloco de tipo desconhecido: {t!r}")


# ---------------------------------------------------------------------------
# folha de estilo
# ---------------------------------------------------------------------------

def folha(tk: Tokens) -> str:
    return f"""
/* TOKENS:INICIO */
{tk.css_block()}
/* TOKENS:FIM */

/* A margem física real vive numa área interna, nunca no @page: se ela for
   declarada no @page o motor de impressão aplica escala por conta própria. */
@page {{ size: {tk.mm('exec-page-width'):g}mm {tk.mm('exec-page-height'):g}mm; margin: 0; }}

*, *::before, *::after {{
  box-sizing: border-box;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}}

html, body {{ margin: 0; padding: 0; background: var(--exec-color-surface-page); }}
body {{ font-family: var(--exec-font-stack); color: var(--exec-color-ink-body);
        font-size: 10pt; line-height: 1.5; }}

.folha {{ width: {tk.mm('exec-page-width'):g}mm; min-height: {tk.mm('exec-page-height'):g}mm;
          padding: {tk.mm('exec-page-margin'):g}mm; margin: 0 auto;
          page-break-after: always; break-after: page; position: relative; }}
.folha:last-child {{ page-break-after: auto; break-after: auto; }}

h1 {{ font-size: 24pt; line-height: 1.2; color: var(--exec-color-ink-title); margin: 0 0 4mm; }}
h2 {{ font-size: 15pt; line-height: 1.25; color: var(--exec-color-ink-title); margin: 0 0 3mm;
      page-break-after: avoid; break-after: avoid; }}
h3 {{ font-size: 11pt; color: var(--exec-color-ink-title); margin: 6mm 0 2mm;
      page-break-after: avoid; break-after: avoid; }}
p  {{ margin: 0 0 3mm; max-width: 150mm; }}

/* Nenhum bloco de dado é cortado ao meio entre páginas. */
.kpi, .barra, .medidor, .checklist, .destaque, .cronograma, .campo,
table, tr, figure {{ page-break-inside: avoid; break-inside: avoid; }}

.eyebrow {{ display:inline-block; background: var(--exec-color-brand);
            color: var(--exec-color-ink-inverse); border-radius: var(--exec-radius-control);
            padding: 1.2mm 4mm; font-size: 7.5pt; font-weight: 600; letter-spacing: .06em; }}
.rotulo  {{ display:block; font-size: 7.5pt; font-weight: 600; letter-spacing: .04em;
            color: var(--exec-color-ink-body); margin-bottom: 1mm; }}
.nota, .legenda {{ display:block; font-size: 7pt; color: var(--exec-color-ink-muted); }}

/* Campo vazio: itálico + cinza legível + sentinela. As três coisas juntas,
   porque só a cor não sobrevive a fotocópia em preto e branco. */
.exec-is-placeholder {{ font-style: italic; color: var(--exec-color-ink-placeholder); }}
.campo {{ margin: 0 0 3mm; }}
.valor {{ display:block; }}
.exec-field__box {{ display:block; height: 6mm; border: var(--exec-stroke-subtle) solid var(--exec-color-rule-strong);
                    border-radius: var(--exec-radius-check); }}
.linha-escrita   {{ border-top: none; border-left: none; border-right: none; }}

.kpi-valor  {{ display:block; font-size: 34pt; line-height: 1.05; color: var(--exec-color-ink-data); }}
.kpi-metodo {{ display:block; font-size: 7pt; color: var(--exec-color-ink-muted); margin-top: 1mm; }}

.trilha        {{ display:block; height: 5mm; background: var(--exec-color-data-track);
                  border-radius: var(--exec-radius-control); overflow: hidden; }}
.preenchimento {{ display:block; height: 100%; background: var(--exec-color-data-fill); }}
.preenchimento.alt {{ background: var(--exec-color-data-fill-alt); }}
.valor-barra   {{ display:block; font-size: 8pt; margin-top: 1mm; }}
.barra, .medidor, .cronograma {{ margin: 0 0 5mm; }}
.medidor-linha {{ display:grid; grid-template-columns: 38mm 1fr 18mm; gap: 3mm;
                  align-items:center; margin-bottom: 2mm; }}
.medidor-nome  {{ font-size: 8pt; }}
.medidor-linha .valor-barra {{ margin:0; text-align:right; }}

.raia      {{ display:grid; grid-template-columns: 34mm 1fr; gap: 3mm; align-items:center; margin-bottom: 2mm; }}
.raia-nome {{ font-size: 8pt; }}
.raia-pista{{ display:block; height: 4.5mm; background: var(--exec-color-data-track);
              border-radius: var(--exec-radius-control); }}
.raia-barra{{ display:block; height: 100%; background: var(--exec-color-brand);
              border-radius: var(--exec-radius-control); }}

.tabela {{ width:100%; border-collapse: collapse; margin: 0 0 5mm; font-size: 8.5pt; }}
.tabela caption {{ caption-side: bottom; text-align:left; font-size: 7pt;
                   color: var(--exec-color-ink-muted); padding-top: 1.5mm; }}
.tabela th {{ text-align:left; font-size: 7.5pt; letter-spacing:.04em;
              background: var(--exec-color-surface-sunken); padding: 2mm; }}
.tabela td {{ padding: 2mm; border-bottom: var(--exec-stroke-hairline) solid var(--exec-color-rule-subtle); }}
.tabela td.num {{ text-align:right; font-variant-numeric: tabular-nums; }}
.tabela tbody tr:nth-child(even) td {{ background: var(--exec-color-surface-raised); }}

.checklist ul {{ list-style:none; margin:0; padding:0; }}
.exec-check {{ display:grid; grid-template-columns: var(--exec-check-size) 1fr;
               gap: 2.5mm; align-items:start; margin-bottom: 2.5mm; }}
.exec-check__box {{ width: var(--exec-check-size); height: var(--exec-check-size);
                    border: var(--exec-check-stroke) solid var(--exec-color-rule-strong);
                    border-radius: var(--exec-radius-check); position:relative; display:block; }}
.exec-check__mark {{ position:absolute; left: 22%; top: 8%; width: 34%; height: 62%;
                     border-right: var(--exec-stroke-strong) solid var(--exec-color-brand);
                     border-bottom: var(--exec-stroke-strong) solid var(--exec-color-brand);
                     transform: rotate(42deg); display:block; }}
.exec-check__na  {{ position:absolute; left: 10%; top: 48%; width: 80%; height: 0;
                    border-top: var(--exec-stroke-subtle) solid var(--exec-color-ink-muted);
                    transform: rotate(-38deg); display:block; }}
.exec-check__label {{ font-size: 8.5pt; }}
.exec-check .nota {{ grid-column: 2; }}

.destaque {{ background: var(--exec-color-accent-blue); border-left: var(--exec-stroke-selected) solid var(--exec-color-brand);
             border-radius: var(--exec-radius-artifact); padding: 4mm; margin: 0 0 5mm; }}
.destaque p {{ margin:0; }}

.capa {{ background: var(--exec-color-surface-inverse); color: var(--exec-color-ink-inverse);
         display:flex; flex-direction:column; justify-content:space-between; }}
.capa h1, .capa .rotulo, .capa .valor {{ color: var(--exec-color-ink-inverse); }}
.capa .exec-is-placeholder {{ color: var(--exec-color-ink-inverse); opacity: .78; }}
.capa-meta {{ display:grid; grid-template-columns: repeat(2, 1fr); gap: 4mm; font-size: 8.5pt; }}

.indice li {{ display:grid; grid-template-columns: 8mm 1fr; gap: 2mm; padding: 1.8mm 0;
              border-bottom: var(--exec-stroke-hairline) solid var(--exec-color-rule-subtle); }}
.indice ul {{ list-style:none; margin:0; padding:0; }}
.indice .num-secao {{ color: var(--exec-color-ink-muted); font-variant-numeric: tabular-nums; }}

.rodape {{ position:absolute; left: {tk.mm('exec-page-margin'):g}mm; right: {tk.mm('exec-page-margin'):g}mm;
           bottom: 6mm; display:flex; justify-content:space-between;
           font-size: 7pt; color: var(--exec-color-ink-muted);
           border-top: var(--exec-stroke-hairline) solid var(--exec-color-rule-subtle); padding-top: 2mm; }}

@media screen {{
  body {{ background: var(--exec-color-surface-sunken); padding: 8mm 0; }}
  .folha {{ background: var(--exec-color-surface-page); margin-bottom: 6mm; }}
}}
"""


# ---------------------------------------------------------------------------
# montagem
# ---------------------------------------------------------------------------

def render(spec: dict, tk: Tokens) -> str:
    meta = spec.get("meta", {})
    titulo = meta.get("titulo", "Relatório")
    secoes = spec.get("secoes", [])
    total = len(secoes) + 3  # capa, índice, resumo

    def rodape(n: int) -> str:
        return (f'<div class="rodape"><span>{e(titulo)} · v{e(meta.get("versao", "1.0"))}</span>'
                f'<span>{n:02d} / {total:02d}</span></div>')

    paginas: list[str] = []

    # capa
    capa_campos = "".join(
        campo(f"meta-{k}", r, meta.get(k))
        for k, r in (("cliente", "CLIENTE"), ("periodo", "PERÍODO"),
                     ("responsavel", "RESPONSÁVEL"), ("confidencialidade", "CLASSIFICAÇÃO"))
    )
    paginas.append(
        f'<section class="folha capa"><div><span class="eyebrow">{e(meta.get("serie", "EXECUTAR PLAYBOOK"))}</span>'
        f'<h1>{e(titulo)}</h1><p>{e(meta.get("subtitulo", ""))}</p></div>'
        f'<div class="capa-meta">{capa_campos}</div></section>'
    )

    # índice
    linhas = "".join(
        f'<li><span class="num-secao">{i:02d}</span><span>{e(s.get("titulo", ""))}</span></li>'
        for i, s in enumerate(secoes, 1)
    )
    paginas.append(f'<section class="folha indice"><h2>Índice</h2><ul>{linhas}</ul>{rodape(2)}</section>')

    # resumo executivo
    resumo = "".join(f"<p>{e(p)}</p>" for p in spec.get("resumo_executivo", []))
    if not resumo:
        resumo = f'<p class="exec-is-placeholder">{SENTINELA}</p>'
    pendencias = spec.get("pendencias", [])
    bloco_pend = ""
    if pendencias:
        itens = "".join(caixa(p.get("id", f"pend-{i}"), p["texto"], p.get("estado", "off"), p.get("nota"))
                        for i, p in enumerate(pendencias, 1))
        bloco_pend = f'<div class="checklist"><span class="rotulo">PENDÊNCIAS ABERTAS</span><ul>{itens}</ul></div>'
    paginas.append(f'<section class="folha"><h2>Resumo executivo</h2>{resumo}{bloco_pend}{rodape(3)}</section>')

    # seções
    for i, s in enumerate(secoes, 1):
        prefixo = f"s{i:02d}"
        corpo = "".join(bloco(b, prefixo, j) for j, b in enumerate(s.get("blocos", []), 1))
        paginas.append(
            f'<section class="folha"><h2>{i:02d} · {e(s.get("titulo", ""))}</h2>{corpo}{rodape(i + 3)}</section>'
        )

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<style>{folha(tk)}</style>
</head>
<body>
{"".join(paginas)}
</body>
</html>
"""


def gerar_um(spec_path: Path, saida: Path, tema: str, modo: str) -> Path:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    tk = Tokens.load(tema=spec.get("tema", tema))
    saida.parent.mkdir(parents=True, exist_ok=True)

    stage = Path(tempfile.mkdtemp(prefix="deskgo-rel-", dir=saida.parent))
    try:
        provisorio = stage / saida.name
        provisorio.write_text(render(spec, tk), encoding="utf-8", newline="\n")
        rel = validar_html(provisorio, tk, modo, SENTINELA, permitir_flat=False)
        if rel.erros:
            detalhe = "; ".join(f"{a.codigo} {a.onde}: {a.mensagem}" for a in rel.achados if a.severidade == "ERRO")
            raise ValueError(f"{spec_path.name} reprovou no validador — {detalhe}")
        provisorio.replace(saida)
        return saida
    finally:
        shutil.rmtree(stage, ignore_errors=True)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--spec", type=Path)
    p.add_argument("--saida", type=Path)
    p.add_argument("--lote", type=Path, help="diretório com um .json por relatório")
    p.add_argument("--saida-dir", type=Path)
    p.add_argument("--tema", default="executar", help="identidade única do contrato de tokens (ver assets/tokens/temas.json)")
    p.add_argument("--modo", choices=["branco", "preenchido"], default="preenchido")
    args = p.parse_args()

    try:
        if args.lote:
            if not args.saida_dir:
                print("ERRO: --lote exige --saida-dir", file=sys.stderr)
                return 2
            especs = sorted(args.lote.glob("*.json"))
            if not especs:
                print(f"ERRO: nenhum .json em {args.lote}", file=sys.stderr)
                return 2
            # Nome previsível: {id}-{versao}.html. Sem isso ninguém reencontra o
            # arquivo três meses depois.
            feitos = []
            for spec_path in especs:
                spec = json.loads(spec_path.read_text(encoding="utf-8"))
                meta = spec.get("meta", {})
                nome = f"{meta.get('id', spec_path.stem)}-v{meta.get('versao', '1.0')}.html"
                feitos.append(gerar_um(spec_path, args.saida_dir / nome, args.tema, args.modo))
            print(json.dumps({"status": "PASS", "arquivos": [str(f) for f in feitos]}, ensure_ascii=False))
            return 0

        if not (args.spec and args.saida):
            p.print_help()
            return 0
        saida = gerar_um(args.spec, args.saida, args.tema, args.modo)
        print(json.dumps({"status": "PASS", "arquivo": str(saida)}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as erro:
        print(f"ERRO: {erro}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
