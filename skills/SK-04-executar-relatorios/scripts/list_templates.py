#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT/"templates"/"catalog.json").read_text(encoding="utf-8"))
category = sys.argv[1] if len(sys.argv) > 1 else None

rows = data["templates"]
if category:
    rows = [r for r in rows if r["category"] == category]

for r in rows:
    print(f'{r["category"]:10}  {r["slug"]:28}  {r["title"]}')
