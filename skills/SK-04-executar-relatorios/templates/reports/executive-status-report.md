---
name: "executive-status-report"
title: "Executive Status Report"
category: "reports"
purpose: "Comunicar estado executivo, progresso, riscos e próximas ações."
visual_profile: "editorial"
outputs: ["markdown", "html"]
required_inputs: ["projeto"]
---

# Executive Status Report

Comunicar estado executivo, progresso, riscos e próximas ações.

## Output structure

1. Contexto
2. Progresso
3. Agora
4. Próximos passos
5. Risco
6. Mitigação
7. Decisões
8. Entrega

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
