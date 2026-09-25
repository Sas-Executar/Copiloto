#!/usr/bin/env python3
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
catalog_path = ROOT/"templates"/"catalog.json"
data = json.loads(catalog_path.read_text(encoding="utf-8"))
errors = []

if data["template_count"] != len(data["templates"]):
    errors.append("template_count does not match catalog length")

seen = set()
for item in data["templates"]:
    slug = item["slug"]
    if slug in seen:
        errors.append(f"duplicate slug: {slug}")
    seen.add(slug)
    p = ROOT / item["path"]
    if not p.exists():
        errors.append(f"missing template file: {item['path']}")
        continue
    txt = p.read_text(encoding="utf-8")
    if not txt.startswith("---\n"):
        errors.append(f"missing frontmatter: {item['path']}")
    if "## Output structure" not in txt:
        errors.append(f"missing output structure: {item['path']}")
    if "Preserve source-grounded facts" not in txt:
        errors.append(f"missing grounding rule: {item['path']}")

if errors:
    raise SystemExit("\n".join("ERROR: "+e for e in errors))
print(f"VALID: {len(data['templates'])} business templates passed.")
