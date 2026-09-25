---
name: "empathy-map"
title: "Empathy Map"
category: "customer"
purpose: "Organizar sinais sobre o que o cliente pensa, sente, vê, diz e faz."
visual_profile: "canvas"
outputs: ["markdown", "html"]
required_inputs: ["cliente"]
---

# Empathy Map

Organizar sinais sobre o que o cliente pensa, sente, vê, diz e faz.

## Output structure

1. Pensa e sente
2. Vê
3. Ouve
4. Diz e faz
5. Dores
6. Ganhos
7. Hipóteses

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
