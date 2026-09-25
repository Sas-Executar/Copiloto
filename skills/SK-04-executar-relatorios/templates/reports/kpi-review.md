---
name: "kpi-review"
title: "KPI Review"
category: "reports"
purpose: "Revisar métricas, tendências, causas e ações."
visual_profile: "scorecard"
outputs: ["markdown", "html"]
required_inputs: ["métricas"]
---

# KPI Review

Revisar métricas, tendências, causas e ações.

## Output structure

1. KPI
2. Atual
3. Baseline
4. Meta
5. Tendência
6. Driver
7. Risco
8. Ação

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
