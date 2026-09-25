---
name: "handoff-email"
title: "Handoff Email"
category: "emails"
purpose: "Transferir responsabilidade sem perda de contexto."
visual_profile: "email"
outputs: ["email"]
required_inputs: ["contexto"]
---

# Handoff Email

Transferir responsabilidade sem perda de contexto.

## Output structure

1. Assunto
2. Objetivo
3. Estado atual
4. Entregáveis
5. Pendências
6. Riscos
7. Próximo owner

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
