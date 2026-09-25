---
name: "risk-report"
title: "Risk Report"
category: "reports"
purpose: "Consolidar exposição, controles, tendências e decisões de risco."
visual_profile: "risk"
outputs: ["markdown", "html"]
required_inputs: ["riscos"]
---

# Risk Report

Consolidar exposição, controles, tendências e decisões de risco.

## Output structure

1. Top risks
2. Mudanças
3. Exposição
4. Controles
5. Triggers
6. Mitigações
7. Owners
8. Decisões

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
