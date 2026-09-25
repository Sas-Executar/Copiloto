---
name: "voice-of-customer"
title: "Voice of Customer"
category: "customer"
purpose: "Sintetizar evidências, temas, tensões e linguagem do cliente."
visual_profile: "report"
outputs: ["markdown", "html"]
required_inputs: ["feedback"]
---

# Voice of Customer

Sintetizar evidências, temas, tensões e linguagem do cliente.

## Output structure

1. Fontes
2. Citações-chave
3. Temas
4. Necessidades
5. Objeções
6. Riscos
7. Oportunidades

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
