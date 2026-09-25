---
name: "kanban"
title: "Kanban"
category: "execution"
purpose: "Visualizar fluxo de trabalho e WIP por estado."
visual_profile: "kanban"
outputs: ["markdown", "html"]
required_inputs: ["tarefas"]
---

# Kanban

Visualizar fluxo de trabalho e WIP por estado.

## Output structure

1. Backlog
2. Ready
3. Doing
4. Blocked
5. Review
6. Done
7. WIP limits

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
