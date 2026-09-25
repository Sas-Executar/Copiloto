#!/usr/bin/env python3
from pathlib import Path
from html import escape
import json, sys

ROOT = Path(__file__).resolve().parents[1]
TOKENS_CSS = (ROOT / "assets" / "tokens" / "tokens.css").read_text(encoding="utf-8")
CSS = TOKENS_CSS + "\n" + (ROOT / "assets" / "report.css").read_text(encoding="utf-8")

def pct(v):
    if v is None:
        return "—"
    if float(v).is_integer():
        return f"{int(v)}%"
    return f"{v:g}%"

def cycle(cur, total):
    return "—" if cur is None or total is None else f"{cur:02d} / {total:02d}"

def tag_html(items, cls):
    return "".join(f'<span class="{cls}">{escape(str(x))}</span>' for x in items)

def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: render_report.py report.json output.html")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    m, p, d, t, n, props = data["meta"], data["progress"], data["depth"], data["triptych"], data["now"], data["properties"]

    prop_labels = [
        ("context","contexto",False),("problem","problema",True),("process","processo",False),
        ("progress","progresso",True),("step_1","passo_1",False),("step_2","passo_2",False),
        ("step_3","passo_3",False),("risk","risco",True),("prevention","prevencao",False),("delivery","entrega",False)
    ]
    prop_rows = "\n".join(
        f'<tr><td class="key mono{" accent" if accent else ""}">{label}</td><td>{escape(props[key])}</td></tr>'
        for key,label,accent in prop_labels
    )

    tri = []
    for key,label in [("yesterday","ONTEM"),("today","HOJE"),("tomorrow","AMANHÃ")]:
        b=t[key]
        current = ' class="current"' if key=="today" else ""
        tri.append(
            f'<td{current}><div class="tri-top"><span>{label}</span><b>{pct(b["percent"])}</b></div>'
            f'<div class="tri-title">{escape(b["title"])}</div><div class="tri-state">{escape(b["state"])}</div></td>'
        )

    width = max(0, min(100, p["overall_percent"] or 0))
    page = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(m["title"])}</title>
<style>{CSS}</style>
</head>
<body>
<main class="sheet">
<header class="header mono">
<div class="kicker">{escape(m["kicker"])}</div>
<div class="title">{escape(m["title"])}</div>
<div class="meta">schema: {escape(m["schema"])} &nbsp;&nbsp; status: {escape(m["status"])} &nbsp;&nbsp; data: {escape(str(m["date"] or "não identificada"))}</div>
</header>
<section class="section">
<div class="section-label mono">PROGRESSO / PROJETO</div>
<table class="dashboard-table" role="presentation"><tr>
<td style="width:50%"><div class="hero">{pct(p["overall_percent"])}</div><div class="hero-label">concluído</div></td>
<td class="stat" style="width:25%"><strong>{cycle(p["cycle_current"],p["cycle_total"])}</strong><span>ciclo atual</span></td>
<td class="stat" style="width:25%"><strong>{pct(p["today_percent"])}</strong><span>hoje</span></td>
</tr></table>
<div class="progress-track"><div class="progress-fill" style="width:{width}%"></div></div>
<div class="depth-wrap"><table class="depth-table" role="presentation"><tr>
<td><div class="depth-name mono">Projeto</div><div class="depth-val">{escape(d["project"])}</div></td>
<td><div class="depth-name mono">Ciclo</div><div class="depth-val">{escape(d["cycle"])}</div></td>
<td class="depth-current"><div class="depth-name mono">Hoje</div><div class="depth-val">{escape(d["today"])}</div></td>
<td><div class="depth-name mono">Tarefa</div><div class="depth-val">{escape(d["task"])}</div></td>
<td><div class="depth-name mono">Ação</div><div class="depth-val">{escape(d["action"])}</div></td>
</tr></table></div>
<div class="triptych-wrap"><table class="triptych-table" role="presentation"><tr>{''.join(tri)}</tr></table></div>
<div class="now"><div class="now-row"><div>
<div class="section-label mono now-label">AGORA</div>
<div class="now-title">{escape(n["title"])}</div>
<div class="now-meta">{escape(n["meta"])}</div>
</div><span class="chip">{escape(n["chip"])}</span></div></div>
</section>
<section class="section">
<div class="section-label mono">STATUS / PROPERTIES</div>
<table class="properties" role="presentation">{prop_rows}</table>
<div class="tags">
<div class="tag-label mono">FOCO</div>{tag_html(data["tags"]["focus"],"tag-purple")}
<div class="tag-label mono">ESTADO</div>{tag_html(data["tags"]["state"],"tag-purple")}
<div class="tag-label mono">ORIGEM</div>{tag_html(data["tags"]["origin"],"tag-grey")}
</div>
</section>
<footer class="footer mono">{escape(m["schema"])} · leitura: header → progresso → agora → properties → tags</footer>
</main>
</body>
</html>'''
    Path(sys.argv[2]).write_text(page, encoding="utf-8")
    print(f"WROTE: {sys.argv[2]}")

if __name__ == "__main__":
    main()
