---
name: "executive-memo"
title: "Executive Memo"
category: "writing"
purpose: "Gerar memo corporativo estruturado para decisão."
visual_profile: "memo"
outputs: ["markdown", "docx-ready"]
required_inputs: ["contexto"]
---

# Executive Memo

Gerar memo corporativo estruturado para decisão.

## Output structure

1. To/From/Date
2. Assunto
3. Contexto
4. Análise
5. Opções
6. Recomendação
7. Riscos
8. Decisão requerida

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
