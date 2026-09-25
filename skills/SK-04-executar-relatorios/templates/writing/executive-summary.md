---
name: "executive-summary"
title: "Executive Summary Generator"
category: "writing"
purpose: "Gerar síntese executiva curta, factual e orientada à decisão."
visual_profile: "text"
outputs: ["markdown", "docx-ready"]
required_inputs: ["fonte"]
---

# Executive Summary Generator

Gerar síntese executiva curta, factual e orientada à decisão.

## Output structure

1. Contexto
2. Situação
3. Implicação
4. Decisão necessária
5. Próxima ação

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
