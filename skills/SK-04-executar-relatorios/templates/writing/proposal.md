---
name: "proposal"
title: "Business Proposal"
category: "writing"
purpose: "Gerar proposta executiva com problema, abordagem, valor e próximos passos."
visual_profile: "proposal"
outputs: ["markdown", "docx-ready"]
required_inputs: ["problema"]
---

# Business Proposal

Gerar proposta executiva com problema, abordagem, valor e próximos passos.

## Output structure

1. Problema
2. Objetivo
3. Escopo
4. Abordagem
5. Entregáveis
6. Prazo
7. Investimento
8. Próximos passos

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
