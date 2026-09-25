---
name: "okr"
title: "OKR"
category: "strategy"
purpose: "Converter estratégia em objetivos e resultados-chave mensuráveis."
visual_profile: "scorecard"
outputs: ["markdown", "html"]
required_inputs: ["objetivo"]
---

# OKR

Converter estratégia em objetivos e resultados-chave mensuráveis.

## Output structure

1. Objetivo
2. KR1
3. KR2
4. KR3
5. Baseline
6. Owner
7. Cadência
8. Riscos

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
