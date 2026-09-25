---
name: "decision-request-email"
title: "Decision Request Email"
category: "emails"
purpose: "Solicitar decisão entre alternativas explícitas."
visual_profile: "email"
outputs: ["email"]
required_inputs: ["contexto"]
---

# Decision Request Email

Solicitar decisão entre alternativas explícitas.

## Output structure

1. Assunto
2. Decisão
3. Opções
4. Trade-offs
5. Recomendação
6. Data limite

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
