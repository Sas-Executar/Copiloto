# Business Template Routing

The Business Pack contains 75 templates across strategy, execution, customer, workbooks, reports, writing, and email.

## Routing principle

1. Extract and validate source facts first.
2. Select a semantic template.
3. Populate only source-supported fields.
4. Record missing fields explicitly.
5. Select a visual renderer independently.
6. Validate the output before rendering.

## Categories

### Strategy
Use for models, choices, prioritization, positioning, economics, and portfolio decisions.

### Execution
Use for work sequencing, WIP, dependencies, time, ownership, and delivery control.

### Customer
Use for journeys, service operations, customer evidence, jobs, personas, and funnels.

### Workbooks
Use when the user needs a guided working document rather than a static report.

### Reports
Use for recurring or point-in-time business reporting and analysis.

### Writing
Use when the primary output is corporate prose, specification, procedure, memo, or plan.

### Emails
Use when the primary output is a sendable corporate email.

## Renderer independence

A template does not own its visual form.

Examples:
- `now-next-later` can render as roadmap, table, wall, or executive one-pager.
- `customer-journey` can render as journey grid, swimlane, or workshop board.
- `project-status-report` can render as editorial report, dashboard, or print brief.
- `executive-memo` can render as plain text, email-like memo, or PDF-ready document.

## Template selection heuristic

Prefer the narrowest template that matches the user's real intent.

Do not use a business-model template merely because the source contains business language.

Do not use a Gantt when reliable timing is absent.

Do not use a Kanban when item states are absent.

Do not use RACI when roles are absent.

## Missing-data policy

Visual completeness must never override evidentiary completeness.

Unknown data remains unknown.
