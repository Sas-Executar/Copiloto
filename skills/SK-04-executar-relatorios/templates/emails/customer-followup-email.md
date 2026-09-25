---
name: "customer-followup-email"
title: "Customer Follow-up Email"
category: "emails"
purpose: "Retomar conversa com cliente e registrar próximo passo."
visual_profile: "email"
outputs: ["email"]
required_inputs: ["contexto"]
---

# Customer Follow-up Email

Retomar conversa com cliente e registrar próximo passo.

## Output structure

1. Assunto
2. Contexto
3. Necessidade
4. Resposta
5. Próxima ação
6. Prazo

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
