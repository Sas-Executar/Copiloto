---
name: "incident-notice-email"
title: "Incident Notice Email"
category: "emails"
purpose: "Comunicar incidente de forma factual e responsável."
visual_profile: "email"
outputs: ["email"]
required_inputs: ["contexto"]
---

# Incident Notice Email

Comunicar incidente de forma factual e responsável.

## Output structure

1. Assunto
2. Incidente
3. Impacto
4. Estado atual
5. Mitigação
6. Próxima atualização

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
