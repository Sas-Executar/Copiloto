---
name: "raci"
title: "RACI"
category: "execution"
purpose: "Definir responsabilidade e autoridade por atividade."
visual_profile: "matrix"
outputs: ["markdown", "html"]
required_inputs: ["atividades", "pessoas"]
---

# RACI

Definir responsabilidade e autoridade por atividade.

## Output structure

1. Atividade
2. Responsible
3. Accountable
4. Consulted
5. Informed
6. Lacunas

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
