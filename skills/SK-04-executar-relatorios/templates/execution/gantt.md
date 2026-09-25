---
name: "gantt"
title: "Gantt"
category: "execution"
purpose: "Representar entregáveis, fases, dependências e marcos em tempo."
visual_profile: "gantt"
outputs: ["markdown", "html"]
required_inputs: ["tarefas", "datas"]
---

# Gantt

Representar entregáveis, fases, dependências e marcos em tempo.

## Output structure

1. Fases
2. Entregáveis
3. Início
4. Fim
5. Dependências
6. Marcos
7. Estado

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
