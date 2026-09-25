---
name: "persona"
title: "Persona"
category: "customer"
purpose: "Consolidar perfil operacional baseado em evidências, não ficção."
visual_profile: "profile"
outputs: ["markdown", "html"]
required_inputs: ["pesquisa"]
---

# Persona

Consolidar perfil operacional baseado em evidências, não ficção.

## Output structure

1. Contexto
2. Objetivos
3. Comportamentos
4. Necessidades
5. Fricções
6. Critérios de decisão
7. Evidências

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
