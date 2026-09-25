---
name: "approval-request-email"
title: "Approval Request Email"
category: "emails"
purpose: "Solicitar aprovação com contexto suficiente para decisão."
visual_profile: "email"
outputs: ["email"]
required_inputs: ["contexto"]
---

# Approval Request Email

Solicitar aprovação com contexto suficiente para decisão.

## Output structure

1. Assunto
2. O que precisa aprovar
3. Contexto
4. Opções
5. Recomendação
6. Prazo

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
