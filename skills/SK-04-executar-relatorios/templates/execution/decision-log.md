---
name: "decision-log"
title: "Decision Log"
category: "execution"
purpose: "Registrar decisões, contexto, alternativas e consequências."
visual_profile: "register"
outputs: ["markdown", "html"]
required_inputs: ["decisões"]
---

# Decision Log

Registrar decisões, contexto, alternativas e consequências.

## Output structure

1. Decisão
2. Data
3. Contexto
4. Alternativas
5. Racional
6. Consequências
7. Revisão

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
