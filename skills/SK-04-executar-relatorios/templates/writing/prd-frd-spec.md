---
name: "prd-frd-spec"
title: "PRD / FRD / Specs"
category: "writing"
purpose: "Converter decisões em requisitos de produto, funcionais e técnicos."
visual_profile: "spec"
outputs: ["markdown", "json"]
required_inputs: ["produto"]
---

# PRD / FRD / Specs

Converter decisões em requisitos de produto, funcionais e técnicos.

## Output structure

1. Problema
2. Usuários
3. Objetivos
4. Requisitos
5. Fluxos
6. Estados
7. Critérios de aceitação
8. Não-escopo

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
