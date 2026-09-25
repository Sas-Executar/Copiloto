---
name: "meeting-followup-email"
title: "Meeting Follow-up Email"
category: "emails"
purpose: "Fechar reunião com decisões, ações e responsabilidades."
visual_profile: "email"
outputs: ["email"]
required_inputs: ["contexto"]
---

# Meeting Follow-up Email

Fechar reunião com decisões, ações e responsabilidades.

## Output structure

1. Assunto
2. Agradecimento contextual
3. Decisões
4. Ações/owners
5. Prazos
6. Próximo checkpoint

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
