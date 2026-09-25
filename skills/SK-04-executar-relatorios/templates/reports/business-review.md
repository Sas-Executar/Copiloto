---
name: "business-review"
title: "Business Review"
category: "reports"
purpose: "Revisar desempenho, KPIs, causas e prioridades."
visual_profile: "review"
outputs: ["markdown", "html"]
required_inputs: ["métricas"]
---

# Business Review

Revisar desempenho, KPIs, causas e prioridades.

## Output structure

1. Resumo executivo
2. KPIs
3. Variações
4. Causas
5. Segmentos
6. Riscos
7. Prioridades
8. Decisões

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
