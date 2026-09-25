---
name: "launch-announcement-email"
title: "Launch Announcement Email"
category: "emails"
purpose: "Comunicar lançamento com valor, disponibilidade e ação esperada."
visual_profile: "email"
outputs: ["email"]
required_inputs: ["contexto"]
---

# Launch Announcement Email

Comunicar lançamento com valor, disponibilidade e ação esperada.

## Output structure

1. Assunto
2. O que lançou
3. Para quem
4. Valor
5. Disponibilidade
6. CTA
7. Suporte

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
