---
name: "raid-log"
title: "RAID Log"
category: "execution"
purpose: "Registrar risks, assumptions, issues e dependencies."
visual_profile: "register"
outputs: ["markdown", "html"]
required_inputs: ["projeto"]
---

# RAID Log

Registrar risks, assumptions, issues e dependencies.

## Output structure

1. Risks
2. Assumptions
3. Issues
4. Dependencies
5. Owner
6. Next action
7. Due date

## Rules

- Preserve source-grounded facts and provenance.
- Do not invent absent metrics, owners, deadlines, decisions, or outcomes.
- Use `Não identificado no documento` or `null` when required information is absent.
- Keep semantic content independent from the selected renderer.
- Prefer concise operational language and verifiable outputs.
