---
name: "dependency-map"
title: "Dependency Map"
category: "execution"
purpose: "Mapear dependências entre entregáveis e gargalos."
visual_profile: "map"
outputs: ["markdown", "html"]
required_inputs: ["entregáveis"]
---

# Dependency Map

Mapear dependências entre entregáveis e gargalos.

## Output structure

1. Nós
2. Dependências
3. Bloqueadores
4. Caminho crítico
5. Sequência
6. Mitigações

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
