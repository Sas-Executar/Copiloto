#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
skill = ROOT / "SKILL.md"
errors = []

# Resources that are legitimately referenced from SKILL.md/prose but do not
# exist on disk yet by design: the design-token contract is a placeholder
# awaiting the user's new token values (see references/design-tokens.md and
# assets/tokens/README.md). Do not flag these as broken links.
EXPECTED_PENDING = {
    "assets/tokens/tokens.json",
    "assets/tokens/temas.json",
}

if not skill.exists():
    errors.append("SKILL.md missing")
else:
    text = skill.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append("SKILL.md YAML frontmatter missing")
    else:
        fm = m.group(1)
        if not re.search(r"^name:\s*executar-relatorios\s*$", fm, re.M):
            errors.append("frontmatter name must be executar-relatorios")
        # description may be a single line ("description: ...") or a YAML
        # block scalar ("description: >" / "description: |" followed by
        # indented lines) — collect either form before judging length.
        desc_line = re.search(r"^description:[ \t]*(.*)$", fm, re.M)
        if not desc_line:
            errors.append("description is missing or too vague")
        else:
            first = desc_line.group(1).strip()
            if first in (">", "|", ">-", "|-", ""):
                start = desc_line.end()
                rest = fm[start:]
                block_lines = []
                for line in rest.splitlines():
                    if line.strip() == "" or line.startswith((" ", "\t")):
                        block_lines.append(line.strip())
                        continue
                    break
                desc_text = " ".join(block_lines).strip()
            else:
                desc_text = first
            if len(desc_text) < 80:
                errors.append("description is missing or too vague")
    if len(text.splitlines()) > 500:
        errors.append("SKILL.md exceeds 500-line progressive-disclosure target")
    refs = set(re.findall(r"`((?:references|scripts|assets|examples|evals|schemas|templates)/[^`]+)`", text))
    for rel in sorted(refs):
        if rel in EXPECTED_PENDING:
            continue
        if not (ROOT / rel).exists():
            errors.append(f"referenced resource missing: {rel}")

for rel in [
    "references/00-operating-contract.md",
    "references/20-report-schema.md",
    "references/30-information-mapping.md",
    "references/design-tokens.md",
    "schemas/report.schema.json",
    "schemas/activation.schema.json",
    "schemas/output.schema.json",
    "schemas/prism-report.schema.json",
    "assets/tokens/tokens.schema.json",
    "assets/tokens/temas.schema.json",
    "scripts/validate_report.py",
    "scripts/render_report.py",
    "scripts/validate_mapa.py",
    "scripts/tokens.py",
    "assets/report.css",
    "assets/templates/status-report-v1.html",
    "assets/templates/status-report-v1.email.src.html",
    "assets/templates/status-report-v1.email.html",
    "scripts/build_email.py",
    "references/120-email-html.md",
    "manifest.json",
    "VERSION",
]:
    if not (ROOT / rel).exists():
        errors.append(f"required resource missing: {rel}")

# Relatórios impressos e e-mail bebem só dos tokens (EXECUTAR-REPORT-PRINT-DS-001):
# nenhum hex fora do bloco TOKENS gerado, nenhuma LACUNA consumida, e-mail gerado em dia.
import re as _re
import subprocess as _sp
import sys as _sys
sys_path = str(ROOT / "scripts")
_sys.path.insert(0, sys_path)
from tokens import Tokens as _Tokens  # noqa: E402

_t = _Tokens.load()
_lacunas = {_t._nome_css(n) for n in _t.lacunas() if n in _t.alias}
_bloco = _re.compile(r"/\* TOKENS:INICIO \*/.*?/\* TOKENS:FIM \*/", _re.S)
for rel in [
    "assets/report.css",
    "assets/templates/status-report-v1.html",
    "assets/templates/status-report-v1.email.src.html",
    "assets/templates/status-report-prisma-a4-v4.html",
]:
    fonte = (ROOT / rel).read_text(encoding="utf-8")
    fora = _bloco.sub("", fonte)
    hexes = sorted(set(_re.findall(r"#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b(?![0-9A-Fa-f-])", fora)))
    if hexes:
        errors.append(f"{rel}: hex fora do bloco de tokens: {hexes}")
    for nome in sorted(set(_re.findall(r"var\(--([a-z0-9-]+)\)", fora)) & _lacunas):
        errors.append(f"{rel}: consome token LACUNA --{nome}")
if _sp.run([_sys.executable, str(ROOT / "scripts" / "build_email.py"), "--checar"], capture_output=True).returncode:
    errors.append("assets/templates/*.email.html desatualizado: rode scripts/build_email.py")

if errors:
    raise SystemExit("\n".join("ERROR: "+e for e in errors))
print("VALID: skill package structure and progressive-disclosure references passed.")
