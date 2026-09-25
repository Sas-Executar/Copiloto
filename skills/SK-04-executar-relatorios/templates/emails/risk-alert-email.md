---
name: "risk-alert-email"
title: "Risk Alert Email"
category: "emails"
purpose: "Alertar sobre risco material e mitigação proposta."
visual_profile: "email"
outputs: ["email"]
required_inputs: ["contexto"]
---

# Risk Alert Email

Alertar sobre risco material e mitigação proposta.

## Output structure

1. Assunto
2. Risco
3. Trigger
4. Impacto
5. Mitigação
6. Owner
7. Próxima revisão

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
