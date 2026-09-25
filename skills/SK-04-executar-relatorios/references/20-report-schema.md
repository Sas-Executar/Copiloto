# Canonical Report Schema

The canonical machine schema is `references/report.schema.json`.

## Header
- `meta.title`
- `meta.kicker` default `EXECUTAR / STATUS REPORT`
- `meta.schema` default `EXECUTAR_STATUS_REPORT_V1`
- `meta.status`
- `meta.date`
- `meta.source_count`

## Progress
Use only supported or directly derivable values:
- `progress.overall_percent`
- `progress.cycle_current`
- `progress.cycle_total`
- `progress.today_percent`

## Depth
Represent execution depth:
- `project`
- `cycle`
- `today`
- `task`
- `action`

## Triptych
Represent `yesterday`, `today`, and `tomorrow`, each with `title`, `state`, and `percent`.

Do not invent temporal states.

## Now
Represent the single highest-priority executable action:
- `title`
- `meta`
- `chip`

## Properties
Canonical order:
1. `context`
2. `problem`
3. `process`
4. `progress`
5. `step_1`
6. `step_2`
7. `step_3`
8. `risk`
9. `prevention`
10. `delivery`

Each field contains one concise operational statement.

## Tags
Use `focus`, `state`, and `origin`.

## Provenance
`provenance.sources` inventories documents.

`provenance.field_map` maps canonical fields to source evidence.

## Quality
Preserve:
- `quality.conflicts`
- `quality.warnings`
- `quality.missing_fields`
