# Progressive Disclosure and Skill Maintenance

## Layer 1 — Metadata
The YAML `name` and `description` determine triggering; keep the description specific and phrase-rich.

## Layer 2 — SKILL.md
Keep purpose, workflow, invariants, and pointers to resources.

Do not duplicate large schemas or edge-case catalogs.

## Layer 3 — Bundled resources
Load references only when relevant, execute scripts for deterministic operations, use assets for output generation, and inspect examples when implementation guidance is needed.

## Canonical-home rule
One concept should have one canonical home.

Avoid duplicating detailed rules across SKILL.md and references.

## Trigger tests
Positive:
- "gere um status report deste texto"
- "transforme estes documentos em relatório EXECUTAR"
- "renderize este status como HTML para impressão"

Negative:
- "resuma este texto em três bullets"
- "crie um dashboard React"
- "corrija apenas a gramática deste documento"
