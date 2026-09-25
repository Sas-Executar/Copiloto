---
name: "decision-matrix"
title: "Decision Matrix"
category: "strategy"
purpose: "Comparar alternativas por critérios explícitos."
visual_profile: "matrix"
outputs: ["markdown", "html"]
required_inputs: ["decisão", "alternativas"]
---

# Decision Matrix

Comparar alternativas por critérios explícitos.

## Output structure

1. Decisão
2. Alternativas
3. Critérios
4. Pesos
5. Pontuação
6. Trade-offs
7. Recomendação

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
