---
name: "daily-plan"
title: "Daily Execution Plan"
category: "execution"
purpose: "Definir foco operacional do dia com mínima carga cognitiva."
visual_profile: "execution"
outputs: ["markdown", "html"]
required_inputs: ["tarefas"]
---

# Daily Execution Plan

Definir foco operacional do dia com mínima carga cognitiva.

## Output structure

1. Outcome do dia
2. Agora
3. Depois
4. Bloqueios
5. Tempo previsto
6. Done criteria

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
