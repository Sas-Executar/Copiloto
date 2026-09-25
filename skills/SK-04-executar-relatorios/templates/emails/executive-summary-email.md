---
name: "executive-summary-email"
title: "Executive Summary Email"
category: "emails"
purpose: "Enviar síntese curta para liderança."
visual_profile: "email"
outputs: ["email"]
required_inputs: ["contexto"]
---

# Executive Summary Email

Enviar síntese curta para liderança.

## Output structure

1. Assunto
2. Contexto
3. 3 pontos-chave
4. Implicação
5. Decisão requerida

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
