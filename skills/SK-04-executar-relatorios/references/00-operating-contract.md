# Operating Contract

## Authority order
1. Source document content.
2. Explicit user instructions for the current task.
3. Canonical report schema.
4. Mapping heuristics.
5. Visual rules.

Never let presentation override source truth.

## Grounding
Every material report statement must be traceable to at least one source fact.

Record traceability in `provenance.field_map`.

A field may contain a direct source fact, directly derivable calculation, or explicit synthesis of multiple supported facts.

A field must not contain invented metrics, owners, dates, completion states, or causal relationships.

## Missing data
Use `null` for machine fields such as percentages and counts.

Use `Não identificado no documento` for required human-facing semantic fields.

Do not replace missing data with generic advice unless recommendations are explicitly requested.

## Conflicts
When sources disagree:
- preserve both facts in provenance;
- choose neither silently;
- add a concise entry to `quality.conflicts`;
- render the least misleading human-facing wording.

## Semantic compression
Compress wording, not meaning.

Prefer concrete noun + operative verb + object, explicit dependency, explicit next action, and verifiable output.

## Provenance minimum
Track provenance for overall progress, current cycle, today state, now action, context, problem, process, progress statement, each step, risk, prevention, and delivery.
