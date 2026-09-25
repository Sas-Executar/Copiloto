---
name: "deadline-reminder-email"
title: "Deadline Reminder Email"
category: "emails"
purpose: "Reforçar prazo e dependências sem ambiguidade."
visual_profile: "email"
outputs: ["email"]
required_inputs: ["contexto"]
---

# Deadline Reminder Email

Reforçar prazo e dependências sem ambiguidade.

## Output structure

1. Assunto
2. Entrega
3. Data
4. Dependências
5. Risco de atraso
6. Ação requerida

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
