---
name: "customer-journey"
title: "Customer Journey Map"
category: "customer"
purpose: "Mapear etapas, objetivos, ações, emoções e fricções do cliente."
visual_profile: "journey"
outputs: ["markdown", "html"]
required_inputs: ["cliente", "jornada"]
---

# Customer Journey Map

Mapear etapas, objetivos, ações, emoções e fricções do cliente.

## Output structure

1. Etapas
2. Objetivo do cliente
3. Ações
4. Touchpoints
5. Emoções
6. Fricções
7. Oportunidades

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
