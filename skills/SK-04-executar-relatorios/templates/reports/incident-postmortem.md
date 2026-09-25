---
name: "incident-postmortem"
title: "Incident Postmortem"
category: "reports"
purpose: "Documentar incidente, impacto, causa e prevenção."
visual_profile: "postmortem"
outputs: ["markdown", "html"]
required_inputs: ["incidente"]
---

# Incident Postmortem

Documentar incidente, impacto, causa e prevenção.

## Output structure

1. Resumo
2. Timeline
3. Impacto
4. Causa raiz
5. Fatores contribuintes
6. Resposta
7. Ações corretivas
8. Lições

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
