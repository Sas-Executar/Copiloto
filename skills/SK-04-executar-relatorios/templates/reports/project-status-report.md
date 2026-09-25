---
name: "project-status-report"
title: "Project Status Report"
category: "reports"
purpose: "Detalhar progresso por escopo, prazo, risco e dependências."
visual_profile: "dashboard"
outputs: ["markdown", "html"]
required_inputs: ["projeto"]
---

# Project Status Report

Detalhar progresso por escopo, prazo, risco e dependências.

## Output structure

1. Resumo
2. Escopo
3. Prazo
4. Entregáveis
5. Riscos
6. Issues
7. Dependências
8. Ações

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
