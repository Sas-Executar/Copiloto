---
name: "portfolio-map"
title: "Portfolio Map"
category: "strategy"
purpose: "Posicionar iniciativas por valor, esforço, risco e horizonte."
visual_profile: "matrix"
outputs: ["markdown", "html"]
required_inputs: ["iniciativas"]
---

# Portfolio Map

Posicionar iniciativas por valor, esforço, risco e horizonte.

## Output structure

1. Iniciativas
2. Valor
3. Esforço
4. Risco
5. Horizonte
6. Dependências
7. Priorização

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
