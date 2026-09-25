# Quality Gates

A report is deliverable only when applicable gates pass.

## Q1 Source fidelity
No unsupported facts, metrics, owners, deadlines, or completion states.

## Q2 Structural completeness
Required sections: meta, progress, depth, triptych, now, properties, tags, provenance, quality.

## Q3 Missing-data behavior
Unknown metrics use `null`; required human semantic fields use `Não identificado no documento`.

## Q4 Provenance
Every populated material semantic field has provenance; derived metrics are marked as derived.

## Q5 Conflict handling
Contradictions are listed in `quality.conflicts` and never silently collapsed.

## Q6 Operational clarity
The report exposes context, problem, process, next actions, risk, and delivery.

## Q7 Visual hierarchy
Labels remain subordinate to content; decorative noise is avoided.

## Q8 Print
No clipped text, horizontal overflow, unreadable type, or browser-only artifacts.

## Q9 Deterministic validation
Run:
```bash
python scripts/validate_report.py report.json
python scripts/render_report.py report.json output.html
python scripts/validate_skill.py
```
