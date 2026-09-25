#!/usr/bin/env python3
"""Render the immutable Prism Status Report V4 template."""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

from simple_schema import validate_instance

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "assets" / "templates" / "status-report-prisma-a4-v4.html"
DEFAULT_SCHEMA = ROOT / "schemas" / "prism-report.schema.json"
TOKEN_RE = re.compile(r"{{[A-Z0-9_]+}}")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_payload(data: dict, schema_path: Path = DEFAULT_SCHEMA) -> None:
    errors = validate_instance(data, load_json(schema_path))
    if errors:
        lines = ["Payload inválido:"]
        lines.extend(f"- {error}" for error in errors)
        raise ValueError("\n".join(lines))


def to_placeholders(data: dict) -> dict[str, str]:
    m, e, c, d = data["meta"], data["epic"], data["calendar"], data["deliverables"]
    i, h = e["intent"], d["hero"]
    out = {
        "EPIC_NUMBER": m["epic_number"], "EPIC_STATE": m["epic_state"],
        "DOC_TOP_EYEBROW": m["eyebrow_top"], "DOC_PERIOD_SHORT": m["period_short"],
        "EPIC_PROGRESS_PCT": str(e["progress_pct"]), "EPIC_EYEBROW": e["eyebrow"],
        "EPIC_TITLE": e["title"], "EPIC_DESCRIPTION": e["description"],
        "EPIC_INTENT_LABEL": i["label"], "EPIC_INTENT_TITLE": i["title"],
        "EPIC_INTENT_TEXT": i["text"], "CALENDAR_EYEBROW": c["eyebrow"],
        "CALENDAR_TITLE": c["title"], "CALENDAR_WEEK_ID": c["week_id"],
        "CALENDAR_PERIOD": c["period"], "RESULT_EYEBROW": d["eyebrow"],
        "RESULT_TITLE": d["title"], "RESULT_META": d["meta"],
        "RESULT_HERO_TAG": h["tag"], "RESULT_HERO_TITLE": h["title"],
        "RESULT_HERO_DESCRIPTION": h["description"],
        "RESULT_HERO_STATE_LABEL": h["result_label"],
        "RESULT_HERO_STATE_VALUE": h["result_value"],
        "RESULT_NEXT_LABEL": d["next"]["label"], "RESULT_NEXT_VALUE": d["next"]["value"],
        "DOC_TRACE": d["trace"],
    }
    for idx, kpi in enumerate(data["kpis"], 1):
        for key in ("label", "value", "caption"):
            out[f"EPIC_KPI_{idx:02d}_{key.upper()}"] = kpi[key]
    for idx, day in enumerate(c["days"], 1):
        for key in ("number", "weekday", "date", "title", "focus"):
            out[f"CALENDAR_DAY_{idx:02d}_{key.upper()}"] = day[key]
        tracks = list(day["tracks"]) + [""] * 3
        out[f"CALENDAR_DAY_{idx:02d}_TRACK_01"] = tracks[0]
        out[f"CALENDAR_DAY_{idx:02d}_TRACK_02"] = tracks[1]
        if idx == 7:
            out[f"CALENDAR_DAY_{idx:02d}_TRACK_03"] = tracks[2]
    for idx, item in enumerate(d["items"], 1):
        for key in ("title", "description", "status"):
            out[f"RESULT_ITEM_{idx:02d}_{key.upper()}"] = item[key]
    return out


def render(data: dict, template_text: str) -> tuple[str, dict[str, str]]:
    validate_payload(data)
    values = to_placeholders(data)
    expected = {token[2:-2] for token in TOKEN_RE.findall(template_text)}
    if expected != set(values):
        missing = sorted(expected - set(values))
        extra = sorted(set(values) - expected)
        raise ValueError(f"placeholder mismatch; missing={missing}; extra={extra}")
    rendered = template_text
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", html.escape(str(value), quote=True))
    if TOKEN_RE.search(rendered):
        raise ValueError("unresolved placeholders remain")
    return rendered, values


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--tokens", type=Path)
    args = parser.parse_args()
    try:
        rendered, values = render(load_json(args.input), DEFAULT_TEMPLATE.read_text(encoding="utf-8"))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    if args.tokens:
        args.tokens.parent.mkdir(parents=True, exist_ok=True)
        args.tokens.write_text(json.dumps(values, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {args.output}; placeholders={len(values)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
