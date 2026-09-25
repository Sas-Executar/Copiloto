---
name: "vendor-request-email"
title: "Vendor Request Email"
category: "emails"
purpose: "Solicitar informação, proposta ou ação a fornecedor."
visual_profile: "email"
outputs: ["email"]
required_inputs: ["contexto"]
---

# Vendor Request Email

Solicitar informação, proposta ou ação a fornecedor.

## Output structure

1. Assunto
2. Pedido
3. Especificação
4. Critério
5. Prazo
6. Contato

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
