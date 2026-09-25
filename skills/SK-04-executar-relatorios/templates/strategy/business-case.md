---
name: "business-case"
title: "Business Case"
category: "strategy"
purpose: "Formalizar justificativa, opções, valor, custo e riscos de uma decisão."
visual_profile: "executive"
outputs: ["markdown", "html"]
required_inputs: ["problema", "opções"]
---

# Business Case

Formalizar justificativa, opções, valor, custo e riscos de uma decisão.

## Output structure

1. Contexto
2. Problema
3. Opções
4. Benefícios
5. Custos
6. Riscos
7. Recomendação
8. Critérios de sucesso

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
