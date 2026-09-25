#!/usr/bin/env python3
"""Status report (EXECUTAR_STATUS_REPORT_V1): JSON canônico -> HTML de impressão e/ou e-mail HTML.

Os dois saem de templates imutáveis com placeholders em chaves duplas:
  assets/templates/status-report-v1.html        impressão A4 / navegador (tokens.css + report.css)
  assets/templates/status-report-v1.email.html  e-mail (gerado por build_email.py, CSS inline)
Placeholder comum recebe texto escapado; STYLE e os terminados em _HTML recebem fragmentos montados aqui a partir
de texto escapado. O Copiloto Operacional (executar-Blog/apps/copiloto) aplica a mesma regra em
TypeScript — o teste de paridade de lá compara a saída com este script.

Uso: render_report.py report.json saida.html [--email saida.email.html]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "templates" / "status-report-v1.html"
TEMPLATE_EMAIL = ROOT / "assets" / "templates" / "status-report-v1.email.html"
PLACEHOLDER = re.compile(r"{{([A-Z0-9_]+)}}")
PROPS = ["context", "problem", "process", "progress", "step_1", "step_2", "step_3", "risk", "prevention", "delivery"]


def pct(v) -> str:
    if v is None:
        return "—"
    return f"{int(v)}%" if float(v).is_integer() else f"{v:g}%"


def cycle(cur, total) -> str:
    return "—" if cur is None or total is None else f"{cur:02d} / {total:02d}"


def estilo() -> str:
    return (ROOT / "assets" / "tokens" / "tokens.css").read_text(encoding="utf-8") + "\n" + (ROOT / "assets" / "report.css").read_text(encoding="utf-8")


def tags_html(itens, cls: str) -> str:
    return "".join(f'<span class="{cls}">{escape(str(x))}</span>' for x in itens) or f'<span class="{cls}">—</span>'


def placeholders(data: dict) -> dict[str, str]:
    """Texto dos placeholders (sem escape). Chaves *_HTML e STYLE já vêm como HTML seguro."""
    m, p, d, t, n, props, tags = data["meta"], data["progress"], data["depth"], data["triptych"], data["now"], data["properties"], data["tags"]
    out = {
        "TITLE": m["title"], "KICKER": m["kicker"], "SCHEMA": m["schema"], "STATUS": m["status"],
        "DATE": m["date"] or "não identificada",
        "PCT_OVERALL": pct(p["overall_percent"]), "CYCLE": cycle(p["cycle_current"], p["cycle_total"]),
        "PCT_TODAY": pct(p["today_percent"]),
        "PROGRESS_WIDTH": str(round(max(0, min(100, p["overall_percent"] or 0)))),
        "DEPTH_PROJECT": d["project"], "DEPTH_CYCLE": d["cycle"], "DEPTH_TODAY": d["today"],
        "DEPTH_TASK": d["task"], "DEPTH_ACTION": d["action"],
        "NOW_TITLE": n["title"], "NOW_META": n["meta"], "NOW_CHIP": n["chip"],
        "TRACE": data.get("trace") or f"fontes: {m['source_count']}",
        "PREHEADER": f"{pct(p['overall_percent'])} concluído · agora: {n['title']}",
    }
    for chave, rotulo in (("yesterday", "YESTERDAY"), ("today", "TODAY"), ("tomorrow", "TOMORROW")):
        out[f"TRI_{rotulo}_PCT"] = pct(t[chave]["percent"])
        out[f"TRI_{rotulo}_TITLE"] = t[chave]["title"]
        out[f"TRI_{rotulo}_STATE"] = t[chave]["state"]
    for k in PROPS:
        out[f"PROP_{k.upper()}"] = props[k]
    out["TAGS_FOCUS_HTML"] = tags_html(tags["focus"], "tag-brand")
    out["TAGS_STATE_HTML"] = tags_html(tags["state"], "tag-brand")
    out["TAGS_ORIGIN_HTML"] = tags_html(tags["origin"], "tag-neutral")
    return out


def preencher(template: str, valores: dict[str, str]) -> str:
    faltando = sorted(set(PLACEHOLDER.findall(template)) - set(valores))
    if faltando:
        raise ValueError(f"placeholders sem valor: {faltando}")

    def troca(mt):
        k = mt.group(1)
        v = str(valores[k])
        return v if k == "STYLE" or k.endswith("_HTML") else escape(v, quote=True)

    return PLACEHOLDER.sub(troca, template)


def render(data: dict) -> str:
    valores = placeholders(data) | {"STYLE": estilo()}
    return preencher(TEMPLATE.read_text(encoding="utf-8"), valores)


def render_email(data: dict) -> str:
    return preencher(TEMPLATE_EMAIL.read_text(encoding="utf-8"), placeholders(data))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada", type=Path)
    ap.add_argument("saida", type=Path)
    ap.add_argument("--email", type=Path, help="também grava a versão e-mail HTML")
    a = ap.parse_args()
    data = json.loads(a.entrada.read_text(encoding="utf-8"))
    try:
        a.saida.write_text(render(data), encoding="utf-8")
        print(f"WROTE: {a.saida}")
        if a.email:
            a.email.write_text(render_email(data), encoding="utf-8")
            print(f"WROTE: {a.email}")
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
