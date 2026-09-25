---
name: "weekly-digest-email"
title: "Weekly Digest Email"
category: "emails"
purpose: "Resumir a semana para stakeholders."
visual_profile: "email"
outputs: ["email"]
required_inputs: ["contexto"]
---

# Weekly Digest Email

Resumir a semana para stakeholders.

## Output structure

1. Assunto
2. Principais avanços
3. Métricas
4. Riscos
5. Decisões
6. Próxima semana

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
