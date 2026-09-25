---
name: "meeting-workbook"
title: "Meeting Workbook"
category: "workbooks"
purpose: "Preparar, executar e fechar reunião com decisões e ações."
visual_profile: "workbook"
outputs: ["markdown", "html"]
required_inputs: ["reunião"]
---

# Meeting Workbook

Preparar, executar e fechar reunião com decisões e ações.

## Output structure

1. Objetivo
2. Contexto
3. Agenda
4. Decisões
5. Ações
6. Owners
7. Prazos
8. Open loops

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
