#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "templates" / "status-report-prisma-a4-v4.html"
tokens = sorted(set(re.findall(r"{{([A-Z0-9_]+)}}", TEMPLATE.read_text(encoding="utf-8"))))
print(f"unique_placeholders={len(tokens)}")
if len(tokens) != 100:
    raise SystemExit(f"BLOCKED: expected 100 placeholders; found {len(tokens)}")
if any(not token.startswith(("DOC_", "EPIC_", "CALENDAR_", "RESULT_")) for token in tokens):
    raise SystemExit("BLOCKED: non-canonical namespace")
print("PASS")
