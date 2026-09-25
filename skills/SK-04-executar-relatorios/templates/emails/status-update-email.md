---
name: "status-update-email"
title: "Status Update Email"
category: "emails"
purpose: "Atualizar stakeholders sobre estado, progresso, risco e próximos passos."
visual_profile: "email"
outputs: ["email"]
required_inputs: ["contexto"]
---

# Status Update Email

Atualizar stakeholders sobre estado, progresso, risco e próximos passos.

## Output structure

1. Assunto
2. Resumo
3. Progresso
4. Bloqueios
5. Próximos passos
6. Pedido/CTA

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
