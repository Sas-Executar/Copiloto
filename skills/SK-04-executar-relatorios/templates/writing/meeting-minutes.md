---
name: "meeting-minutes"
title: "Meeting Minutes"
category: "writing"
purpose: "Gerar ata executiva focada em decisões e ações."
visual_profile: "minutes"
outputs: ["markdown", "docx-ready"]
required_inputs: ["notas"]
---

# Meeting Minutes

Gerar ata executiva focada em decisões e ações.

## Output structure

1. Objetivo
2. Participantes
3. Decisões
4. Ações
5. Owners
6. Prazos
7. Pendências

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
