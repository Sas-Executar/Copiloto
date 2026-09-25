---
name: "change-report"
title: "Change Report"
category: "reports"
purpose: "Registrar mudança de plano, motivo, impacto e novo baseline."
visual_profile: "change"
outputs: ["markdown", "html"]
required_inputs: ["mudança"]
---

# Change Report

Registrar mudança de plano, motivo, impacto e novo baseline.

## Output structure

1. Mudança
2. Motivo
3. Impacto
4. O que sai
5. O que entra
6. Dependências
7. Novo plano
8. Aprovação

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
