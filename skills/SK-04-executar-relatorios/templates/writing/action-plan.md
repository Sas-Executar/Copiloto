---
name: "action-plan"
title: "Action Plan"
category: "writing"
purpose: "Converter diagnóstico em plano sequencial e verificável."
visual_profile: "plan"
outputs: ["markdown", "json"]
required_inputs: ["diagnóstico"]
---

# Action Plan

Converter diagnóstico em plano sequencial e verificável.

## Output structure

1. Objetivo
2. Ações
3. Sequência
4. Owners
5. Dependências
6. Prazos
7. Riscos
8. Critérios de conclusão

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
