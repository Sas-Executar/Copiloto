---
name: "mirror-map"
title: "Mirror Map"
category: "customer"
purpose: "Comparar a experiência externa do cliente com a realidade interna da operação."
visual_profile: "mirror"
outputs: ["markdown", "html"]
required_inputs: ["jornada", "processo interno"]
---

# Mirror Map

Comparar a experiência externa do cliente com a realidade interna da operação.

## Output structure

1. Etapa
2. O cliente vê
3. A operação faz
4. Sistemas
5. Gap
6. Risco
7. Melhoria

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
