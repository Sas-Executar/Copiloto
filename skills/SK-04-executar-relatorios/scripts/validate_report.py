#!/usr/bin/env python3
from pathlib import Path
import json, sys

MISSING = "Não identificado no documento"
REQ_TOP = ["meta","progress","depth","triptych","now","properties","tags","provenance","quality"]
REQ_PROPS = ["context","problem","process","progress","step_1","step_2","step_3","risk","prevention","delivery"]

def percent(v, path, errors):
    if v is not None and (not isinstance(v, (int,float)) or isinstance(v,bool) or not 0 <= v <= 100):
        errors.append(f"{path} must be null or 0..100")

def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_report.py report.json")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = [f"missing top-level key: {k}" for k in REQ_TOP if k not in data]
    if errors:
        raise SystemExit("\n".join("ERROR: "+e for e in errors))

    if data["meta"].get("schema") != "EXECUTAR_STATUS_REPORT_V1":
        errors.append("meta.schema must equal EXECUTAR_STATUS_REPORT_V1")
    if not isinstance(data["meta"].get("source_count"), int) or data["meta"]["source_count"] < 1:
        errors.append("meta.source_count must be integer >= 1")

    for k in ["overall_percent","today_percent"]:
        percent(data["progress"].get(k), f"progress.{k}", errors)

    cc, ct = data["progress"].get("cycle_current"), data["progress"].get("cycle_total")
    if cc is not None and (not isinstance(cc, int) or cc < 0):
        errors.append("progress.cycle_current must be null or integer >= 0")
    if ct is not None and (not isinstance(ct, int) or ct < 1):
        errors.append("progress.cycle_total must be null or integer >= 1")
    if cc is not None and ct is not None and cc > ct:
        errors.append("progress.cycle_current cannot exceed cycle_total")

    for k in ["project","cycle","today","task","action"]:
        if not isinstance(data["depth"].get(k), str) or not data["depth"][k].strip():
            errors.append(f"depth.{k} must be non-empty string")

    for k in ["yesterday","today","tomorrow"]:
        b = data["triptych"].get(k, {})
        for f in ["title","state"]:
            if not isinstance(b.get(f), str) or not b[f].strip():
                errors.append(f"triptych.{k}.{f} must be non-empty string")
        percent(b.get("percent"), f"triptych.{k}.percent", errors)

    for k in ["title","meta","chip"]:
        if not isinstance(data["now"].get(k), str) or not data["now"][k].strip():
            errors.append(f"now.{k} must be non-empty string")

    for k in REQ_PROPS:
        if not isinstance(data["properties"].get(k), str) or not data["properties"][k].strip():
            errors.append(f"properties.{k} must be non-empty string")

    for k in ["focus","state","origin"]:
        if not isinstance(data["tags"].get(k), list):
            errors.append(f"tags.{k} must be array")

    if not isinstance(data["provenance"].get("sources"), list) or not data["provenance"]["sources"]:
        errors.append("provenance.sources must contain at least one source")

    field_map = data["provenance"].get("field_map")
    if not isinstance(field_map, dict):
        errors.append("provenance.field_map must be object")
        field_map = {}

    required_prov = [
        "properties.context","properties.problem","properties.process","properties.progress",
        "properties.step_1","properties.step_2","properties.step_3",
        "properties.risk","properties.prevention","properties.delivery","now.title"
    ]
    for path in required_prov:
        value = data["now"]["title"] if path == "now.title" else data["properties"][path.split(".")[-1]]
        if value != MISSING and path not in field_map:
            errors.append(f"missing provenance for populated field: {path}")

    for k in ["conflicts","warnings","missing_fields"]:
        if not isinstance(data["quality"].get(k), list):
            errors.append(f"quality.{k} must be array")

    if errors:
        raise SystemExit("\n".join("ERROR: "+e for e in errors))
    print("VALID: report structure, ranges, required fields, and provenance gates passed.")

if __name__ == "__main__":
    main()
