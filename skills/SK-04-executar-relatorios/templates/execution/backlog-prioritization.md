---
name: "backlog-prioritization"
title: "Backlog Prioritization"
category: "execution"
purpose: "Ordenar backlog por valor, urgência, risco e esforço."
visual_profile: "table"
outputs: ["markdown", "html"]
required_inputs: ["backlog"]
---

# Backlog Prioritization

Ordenar backlog por valor, urgência, risco e esforço.

## Output structure

1. Item
2. Valor
3. Urgência
4. Risco
5. Esforço
6. Dependências
7. Prioridade

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
