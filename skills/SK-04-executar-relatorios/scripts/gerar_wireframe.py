#!/usr/bin/env python3
"""Biblioteca de wireframes da família Executar Playbook.

Um wireframe aqui é deliberadamente feio: cinza, tracejado, com o nome do slot
escrito dentro. Serve para combinar a ESTRUTURA antes de gastar tempo com a
peça final. Quando o wireframe já sai colorido e bonito, a conversa vira sobre
cor e o arranjo passa sem ninguém olhar — que é justamente o erro caro.

Uso:
  python3 gerar_wireframe.py --catalogo --saida wf-catalogo.svg
  python3 gerar_wireframe.py --bloco kpi --largura 90 --altura 40 --saida wf-kpi.svg
  python3 gerar_wireframe.py --listar
  python3 gerar_wireframe.py --composicao capa,kpi,cronograma,checklist --saida wf-pagina.svg
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# AGUARDANDO CONTRATO DE TOKENS: as declarações var(--exec-color-*) abaixo não
# têm valor definido em lugar nenhum deste pacote. O wireframe gerado só
# renderiza com cor depois que assets/tokens/tokens.json existir (ver
# references/design-tokens.md); até lá, ele imprime a geometria correta em
# preto/transparente por herança de :root ausente.
ESTILO = """
    text { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; fill: var(--exec-color-ink-placeholder); }
    .wf-caixa   { fill: var(--exec-color-surface-page); stroke: var(--exec-color-ink-placeholder); stroke-width: .4; stroke-dasharray: 1.6 1.2; }
    .wf-solido  { fill: var(--exec-color-rule-subtle); stroke: var(--exec-color-rule-default); stroke-width: .3; }
    .wf-escuro  { fill: var(--exec-color-rule-default); stroke: none; }
    .wf-linha   { stroke: var(--exec-color-rule-default); stroke-width: .3; }
    .wf-slot    { font-size: 2.6px; letter-spacing: .3px; }
    .wf-nome    { font-size: 3.2px; font-weight: 600; fill: var(--exec-color-ink-title); }
    .wf-nota    { font-size: 2.2px; fill: var(--exec-color-ink-muted); }
    .wf-cota    { stroke: var(--exec-color-ink-muted); stroke-width: .25; }
"""


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _caixa(x, y, w, h, rotulo="", classe="wf-caixa", r=1.5):
    s = f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{r:g}" class="{classe}"/>'
    if rotulo:
        s += f'<text x="{x + 2:g}" y="{y + 4:g}" class="wf-slot">{esc(rotulo)}</text>'
    return s


def _linhas(x, y, w, n, passo=4):
    return "".join(
        f'<line x1="{x:g}" y1="{y + i * passo:g}" x2="{x + w:g}" y2="{y + i * passo:g}" class="wf-linha"/>'
        for i in range(n)
    )


# --------------------------------------------------------------------------
# blocos. assinatura: (x, y, w, h) -> fragmento svg
# --------------------------------------------------------------------------

def bl_campo(x, y, w, h):
    return (f'<text x="{x:g}" y="{y + 2.5:g}" class="wf-slot">RÓTULO DO CAMPO</text>'
            + _caixa(x, y + 4, w, h - 4, "valor ou — pendente"))


def bl_campo_linhas(x, y, w, h):
    n = max(1, int((h - 8) // 4))
    return (f'<text x="{x:g}" y="{y + 2.5:g}" class="wf-slot">RÓTULO DO CAMPO</text>'
            + _caixa(x, y + 4, w, h - 4)
            + _linhas(x + 2.5, y + 10, w - 5, n))


def bl_checklist(x, y, w, h):
    n = max(1, int(h // 7))
    out = []
    for i in range(n):
        yy = y + i * 7
        out.append(_caixa(x, yy, 4, 4, "", "wf-caixa", 0.4))
        out.append(f'<text x="{x + 6:g}" y="{yy + 3.1:g}" class="wf-slot">critério de aceite {i + 1}</text>')
    out.append(f'<text x="{x:g}" y="{y + n * 7 + 2:g}" class="wf-nota">caixa 4 mm · traço 0,35 mm</text>')
    return "".join(out)


def bl_kpi(x, y, w, h):
    return (_caixa(x, y, w, h)
            + f'<text x="{x + 3:g}" y="{y + 6:g}" class="wf-slot">RÓTULO DO INDICADOR</text>'
            + f'<rect x="{x + 3:g}" y="{y + 9:g}" width="{min(34, w - 6):g}" height="{max(8, h * .4):g}" class="wf-escuro"/>'
            + f'<text x="{x + 3:g}" y="{y + h - 3:g}" class="wf-nota">linha separada: regra de cálculo</text>')


def bl_barra(x, y, w, h):
    return (f'<text x="{x:g}" y="{y + 2.5:g}" class="wf-slot">PROGRESSO</text>'
            + f'<rect x="{x:g}" y="{y + 4:g}" width="{w:g}" height="5" rx="2.5" class="wf-solido"/>'
            + f'<rect x="{x:g}" y="{y + 4:g}" width="{w * .6:g}" height="5" rx="2.5" class="wf-escuro"/>'
            + f'<text x="{x:g}" y="{y + 13:g}" class="wf-nota">valor + unidade</text>')


def bl_medidor(x, y, w, h):
    out = [f'<text x="{x:g}" y="{y + 2.5:g}" class="wf-slot">MEDIDOR COMPARADO</text>']
    for i, frac in enumerate((.72, .41)):
        yy = y + 5 + i * 9
        out.append(f'<text x="{x:g}" y="{yy + 4:g}" class="wf-nota">série {i + 1}</text>')
        out.append(f'<rect x="{x + 18:g}" y="{yy:g}" width="{w - 30:g}" height="6" rx="3" class="wf-solido"/>')
        out.append(f'<rect x="{x + 18:g}" y="{yy:g}" width="{(w - 30) * frac:g}" height="6" rx="3" class="wf-escuro"/>')
        out.append(f'<text x="{x + w:g}" y="{yy + 4.4:g}" text-anchor="end" class="wf-nota">00%</text>')
    return "".join(out)


def bl_cartao(x, y, w, h):
    return (_caixa(x, y, w, h)
            + f'<rect x="{x + 3:g}" y="{y + 3:g}" width="8" height="8" rx="4" class="wf-solido"/>'
            + f'<text x="{x + 14:g}" y="{y + 8.5:g}" class="wf-slot">título do card</text>'
            + _linhas(x + 3, y + 16, w - 6, max(1, int((h - 24) // 4)))
            + f'<text x="{x + 3:g}" y="{y + h - 3:g}" class="wf-nota">rodapé do card</text>')


def bl_grade_cartoes(x, y, w, h):
    cols, rows, gap = 3, 2, 3
    cw = (w - gap * (cols - 1)) / cols
    ch = (h - gap * (rows - 1)) / rows
    return "".join(
        _caixa(x + c * (cw + gap), y + r * (ch + gap), cw, ch, f"card {r * cols + c + 1}")
        for r in range(rows) for c in range(cols)
    )


def bl_cronograma(x, y, w, h):
    out = [f'<text x="{x:g}" y="{y + 2.5:g}" class="wf-slot">CRONOGRAMA</text>']
    for i in range(4):
        yy = y + 5 + i * ((h - 10) / 4)
        out.append(f'<rect x="{x:g}" y="{yy:g}" width="16" height="5" rx="2.5" class="wf-solido"/>')
        out.append(f'<rect x="{x + 18 + i * 6:g}" y="{yy:g}" width="{(w - 24) * (.5 - i * .08):g}" height="5" rx="2.5" class="wf-escuro"/>')
    for g in range(5):
        gx = x + 18 + g * ((w - 18) / 5)
        out.append(f'<line x1="{gx:g}" y1="{y + 4:g}" x2="{gx:g}" y2="{y + h - 4:g}" class="wf-linha"/>')
    out.append(f'<text x="{x + 18:g}" y="{y + h:g}" class="wf-nota">eixo temporal</text>')
    return "".join(out)


def bl_matriz(x, y, w, h):
    lado = min(w, h)
    return (_caixa(x, y, lado, lado)
            + f'<line x1="{x + lado / 2:g}" y1="{y:g}" x2="{x + lado / 2:g}" y2="{y + lado:g}" class="wf-linha"/>'
            + f'<line x1="{x:g}" y1="{y + lado / 2:g}" x2="{x + lado:g}" y2="{y + lado / 2:g}" class="wf-linha"/>'
            + "".join(f'<text x="{x + 2 + (i % 2) * lado / 2:g}" y="{y + 4 + (i // 2) * lado / 2:g}" class="wf-slot">Q{i + 1}</text>'
                      for i in range(4)))


def bl_mosaico(x, y, w, h):
    g = 3
    return (_caixa(x, y, w * .58 - g / 2, h * .62 - g / 2, "bloco maior")
            + _caixa(x + w * .58 + g / 2, y, w * .42 - g / 2, h * .62 - g / 2, "bloco alto")
            + _caixa(x, y + h * .62 + g / 2, w * .35 - g / 2, h * .38 - g / 2, "apoio")
            + _caixa(x + w * .35 + g / 2, y + h * .62 + g / 2, w * .65 - g / 2, h * .38 - g / 2, "faixa de imagem"))


def bl_indice(x, y, w, h):
    n = max(1, int(h // 8))
    out = []
    for i in range(n):
        yy = y + i * 8
        out.append(f'<text x="{x:g}" y="{yy + 4:g}" class="wf-nota">{i + 1:02d}</text>')
        out.append(f'<text x="{x + 8:g}" y="{yy + 4:g}" class="wf-slot">título da seção</text>')
        out.append(f'<text x="{x + w:g}" y="{yy + 4:g}" text-anchor="end" class="wf-nota">p. 00</text>')
        out.append(f'<line x1="{x:g}" y1="{yy + 6:g}" x2="{x + w:g}" y2="{yy + 6:g}" class="wf-linha"/>')
    return "".join(out)


def bl_capa(x, y, w, h):
    return (f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="3" class="wf-solido"/>'
            + f'<rect x="{x + 4:g}" y="{y + 5:g}" width="{w * .5:g}" height="{h * .22:g}" class="wf-escuro"/>'
            + f'<text x="{x + 4:g}" y="{y + h * .38:g}" class="wf-slot">título da capa</text>'
            + "".join(f'<rect x="{x + w - 4 - (i + 1) * 16:g}" y="{y + 5:g}" width="14" height="6" rx="3" class="wf-caixa"/>'
                      for i in range(2))
            + _caixa(x + 4, y + h * .5, w - 8, h * .42, "faixa de imagem"))


def bl_tabela(x, y, w, h):
    cols = 4
    cw = w / cols
    out = [f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="6" class="wf-solido"/>']
    out += [f'<text x="{x + c * cw + 2:g}" y="{y + 4:g}" class="wf-nota">col {c + 1}</text>' for c in range(cols)]
    n = max(1, int((h - 6) // 5))
    for i in range(n):
        yy = y + 6 + i * 5
        if i % 2 == 1:
            out.append(f'<rect x="{x:g}" y="{yy:g}" width="{w:g}" height="5" class="wf-solido" opacity=".5"/>')
        out.append(f'<line x1="{x:g}" y1="{yy + 5:g}" x2="{x + w:g}" y2="{yy + 5:g}" class="wf-linha"/>')
    out.append(f'<text x="{x + w:g}" y="{y + h + 3:g}" text-anchor="end" class="wf-nota">numérico alinhado à direita</text>')
    return "".join(out)


def bl_pilula(x, y, w, h):
    return "".join(
        f'<rect x="{x + i * 22:g}" y="{y:g}" width="20" height="7" rx="3.5" class="wf-caixa"/>'
        f'<text x="{x + i * 22 + 4:g}" y="{y + 4.6:g}" class="wf-nota">tag {i + 1}</text>'
        for i in range(min(3, max(1, int(w // 22))))
    )


BLOCOS = {
    "campo": (bl_campo, 90, 22, "Rótulo + caixa de preenchimento"),
    "campo-linhas": (bl_campo_linhas, 90, 30, "Campo com pauta para escrita à mão"),
    "checklist": (bl_checklist, 90, 30, "Caixas de marcar com critério de aceite"),
    "kpi": (bl_kpi, 90, 38, "Indicador dominante com metodologia em linha separada"),
    "barra": (bl_barra, 90, 16, "Trilha + preenchimento + valor"),
    "medidor": (bl_medidor, 90, 26, "Duas séries comparadas lado a lado"),
    "cartao": (bl_cartao, 90, 40, "Card com ícone, título, corpo e rodapé"),
    "grade-cartoes": (bl_grade_cartoes, 190, 60, "Grade 3×2 de cards de mesma largura"),
    "cronograma": (bl_cronograma, 190, 40, "Quatro raias com barras e grade temporal"),
    "matriz": (bl_matriz, 60, 60, "Matriz 2×2 de posicionamento"),
    "mosaico": (bl_mosaico, 190, 60, "Mosaico assimétrico de quatro blocos"),
    "indice": (bl_indice, 90, 40, "Linhas de índice com divisória e paginação"),
    "capa": (bl_capa, 190, 70, "Capa escura com cápsulas e faixa de imagem"),
    "tabela": (bl_tabela, 190, 36, "Cabeçalho, linhas zebradas e alinhamento numérico"),
    "pilula": (bl_pilula, 90, 10, "Tags e chips"),
}


def _svg(corpo: str, w: float, h: float, titulo: str) -> str:
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:g}mm" height="{h:g}mm" '
            f'viewBox="0 0 {w:g} {h:g}" role="img" aria-labelledby="t">\n'
            f'  <title id="t">{esc(titulo)}</title>\n'
            f'  <style>{ESTILO}</style>\n'
            f'  <rect width="{w:g}" height="{h:g}" fill="var(--exec-color-surface-page)"/>\n'
            f'{corpo}\n</svg>\n')


def render_bloco(nome: str, largura: float | None, altura: float | None) -> str:
    fn, dw, dh, desc = BLOCOS[nome]
    w = largura or dw
    h = altura or dh
    corpo = (f'  <text x="6" y="8" class="wf-nome">{esc(nome)}</text>'
             f'<text x="6" y="12" class="wf-nota">{esc(desc)} · {w:g} × {h:g} mm</text>'
             + fn(6, 18, w - 12, h - 24))
    return _svg(corpo, w, h + 0, f"wireframe {nome}")


def render_catalogo() -> str:
    """Folha única com todos os blocos, para escolher apontando.

    Blocos largos ocupam a linha inteira; os estreitos entram aos pares. A folha
    cresce até caber tudo — catálogo truncado esconde justamente o bloco que
    ninguém lembrou de pedir.
    """
    W, margem, calha = 297.0, 12.0, 12.0
    util = W - 2 * margem
    col = (util - calha) / 2

    filas: list[list[tuple[str, tuple]]] = []
    pendente: list[tuple[str, tuple]] = []
    for nome, spec in BLOCOS.items():
        if spec[1] > col:
            if pendente:
                filas.append(pendente)
                pendente = []
            filas.append([(nome, spec)])
        else:
            pendente.append((nome, spec))
            if len(pendente) == 2:
                filas.append(pendente)
                pendente = []
    if pendente:
        filas.append(pendente)

    topo = 32.0
    y = topo
    partes = []
    for fila in filas:
        altura = max(spec[2] for _, spec in fila)
        for i, (nome, (fn, dw, dh, desc)) in enumerate(fila):
            x = margem + i * (col + calha)
            largura = util if len(fila) == 1 else col
            partes.append(f'<text x="{x:g}" y="{y:g}" class="wf-nome">{esc(nome)}</text>'
                          f'<text x="{x:g}" y="{y + 3.6:g}" class="wf-nota">{esc(desc)}</text>')
            partes.append(fn(x, y + 6, largura, dh))
        y += altura + 18

    H = y + 8
    cabecalho = ('  <text x="12" y="18" class="wf-nome">Catálogo de wireframes · Executar Playbook</text>'
                 '<text x="12" y="23" class="wf-nota">Baixa fidelidade de propósito: aprove o arranjo aqui, '
                 'depois peça a peça final com os tokens.</text>')
    return _svg(cabecalho + "".join(partes), W, H, "catálogo de wireframes")


def render_composicao(nomes: list[str]) -> str:
    """Empilha blocos numa página A4 para simular uma peça inteira."""
    W, H, margem = 210.0, 297.0, 10.0
    partes = ['  <text x="10" y="16" class="wf-nome">Composição · rascunho de página</text>']
    y = 22.0
    for nome in nomes:
        fn, dw, dh, desc = BLOCOS[nome]
        if y + dh + 10 > H - margem:
            break
        partes.append(f'<text x="{margem:g}" y="{y:g}" class="wf-nota">{esc(nome)}</text>')
        partes.append(fn(margem, y + 3, W - 2 * margem, dh))
        y += dh + 10
    return _svg("".join(partes), W, H, "composição de wireframe")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--bloco", choices=sorted(BLOCOS))
    p.add_argument("--catalogo", action="store_true")
    p.add_argument("--composicao", help="nomes de blocos separados por vírgula")
    p.add_argument("--listar", action="store_true")
    p.add_argument("--largura", type=float)
    p.add_argument("--altura", type=float)
    p.add_argument("--saida", type=Path)
    args = p.parse_args()

    if args.listar:
        for nome, (_, w, h, desc) in BLOCOS.items():
            print(f"{nome:16} {w:>4.0f}×{h:<4.0f}mm  {desc}")
        return 0

    if args.catalogo:
        svg = render_catalogo()
    elif args.composicao:
        nomes = [n.strip() for n in args.composicao.split(",") if n.strip()]
        desconhecidos = [n for n in nomes if n not in BLOCOS]
        if desconhecidos:
            print(f"ERRO: bloco desconhecido: {', '.join(desconhecidos)}", file=sys.stderr)
            return 2
        svg = render_composicao(nomes)
    elif args.bloco:
        svg = render_bloco(args.bloco, args.largura, args.altura)
    else:
        p.print_help()
        return 0

    ET.fromstring(svg)  # falha alto se o fragmento saiu malformado
    if args.saida:
        args.saida.parent.mkdir(parents=True, exist_ok=True)
        args.saida.write_text(svg, encoding="utf-8", newline="\n")
        print(f'{{"status":"PASS","arquivo":"{args.saida}"}}')
    else:
        sys.stdout.write(svg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
