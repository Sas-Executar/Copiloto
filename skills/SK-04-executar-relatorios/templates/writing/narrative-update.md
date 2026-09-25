---
name: "narrative-update"
title: "Narrative Update"
category: "writing"
purpose: "Gerar atualização narrativa para liderança sem formato de dashboard."
visual_profile: "narrative"
outputs: ["markdown", "docx-ready"]
required_inputs: ["status"]
---

# Narrative Update

Gerar atualização narrativa para liderança sem formato de dashboard.

## Output structure

1. O que mudou
2. Por que importa
3. O que aprendemos
4. Risco
5. Decisão
6. Próximo passo

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
