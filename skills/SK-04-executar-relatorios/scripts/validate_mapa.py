#!/usr/bin/env python3
"""Validate a canonical EXECUTAR Mapa-OS JSON document."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from simple_schema import validate_instance

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "output.schema.json"
EVIDENCE_STATES = {"complete", "approved", "implemented", "tested", "verified", "published"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    schema = load(SCHEMA)
    errors.extend(f"schema:{error}" for error in validate_instance(data, schema))

    items = data.get("items", [])
    ids = [item.get("id") for item in items]
    if len(ids) != len(set(ids)):
        errors.append("invariant: item IDs must be unique")
    by_id = {item.get("id"): item for item in items}

    for level in ("delivery", "workflow", "action"):
        active = [i.get("id") for i in items if i.get("level") == level and i.get("state") == "active"]
        if len(active) > 1:
            errors.append(f"wip:{level}: expected at most one active item; found {active}")

    for item in items:
        for dep in item.get("dependencies", []):
            if dep not in by_id:
                errors.append(f"dependency:{item.get('id')}: unknown dependency {dep}")
        if item.get("state") in EVIDENCE_STATES and not item.get("evidence_refs"):
            errors.append(f"evidence:{item.get('id')}: state {item.get('state')} requires evidence")

    evidence_ids = {e.get("evidence_id") for e in data.get("evidence", [])}
    for item in items:
        for evidence_ref in item.get("evidence_refs", []):
            if evidence_ref not in evidence_ids:
                errors.append(f"evidence:{item.get('id')}: unknown evidence {evidence_ref}")

    horizons = data.get("horizons", {})
    if len(horizons.get("now", [])) > 1:
        errors.append("wip:horizons.now must contain at most one action")
    next_action = data.get("next_action")
    if next_action:
        action_id = next_action.get("action_id")
        item = by_id.get(action_id)
        if not item or item.get("level") != "action":
            errors.append(f"next_action:{action_id}: must reference an action item")
        elif item.get("blocked") or item.get("state") == "blocked":
            errors.append(f"next_action:{action_id}: blocked action cannot be selected")
        if horizons.get("now") != [action_id]:
            errors.append("next_action must be the sole horizons.now item")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_mapa.py <mapa-os.json>", file=sys.stderr)
        return 2
    errors = validate(load(Path(sys.argv[1])))
    if errors:
        print("BLOCKED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
