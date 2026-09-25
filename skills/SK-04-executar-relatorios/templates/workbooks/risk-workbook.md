---
name: "risk-workbook"
title: "Risk Workbook"
category: "workbooks"
purpose: "Identificar, avaliar e tratar riscos com evidência."
visual_profile: "workbook"
outputs: ["markdown", "html"]
required_inputs: ["riscos"]
---

# Risk Workbook

Identificar, avaliar e tratar riscos com evidência.

## Output structure

1. Risco
2. Causa
3. Probabilidade
4. Impacto
5. Controle atual
6. Tratamento
7. Owner
8. Trigger

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
