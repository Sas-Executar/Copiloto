---
name: "escalation-email"
title: "Escalation Email"
category: "emails"
purpose: "Escalar bloqueio com fatos, impacto e decisão requerida."
visual_profile: "email"
outputs: ["email"]
required_inputs: ["contexto"]
---

# Escalation Email

Escalar bloqueio com fatos, impacto e decisão requerida.

## Output structure

1. Assunto
2. Situação
3. Impacto
4. O que já foi tentado
5. Decisão requerida
6. Prazo

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
