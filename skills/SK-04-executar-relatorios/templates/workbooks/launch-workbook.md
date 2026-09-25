---
name: "launch-workbook"
title: "Launch Workbook"
category: "workbooks"
purpose: "Controlar readiness, entregáveis, gates, canais e pós-lançamento."
visual_profile: "workbook"
outputs: ["markdown", "html"]
required_inputs: ["lançamento"]
---

# Launch Workbook

Controlar readiness, entregáveis, gates, canais e pós-lançamento.

## Output structure

1. Objetivo
2. Entregáveis
3. Readiness
4. Gates
5. Dependências
6. Comunicação
7. Riscos
8. Pós-lançamento

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
