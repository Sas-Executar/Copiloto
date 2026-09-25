# Visual System

Use an editorial report language rather than a conventional card-heavy dashboard.

## Priorities
- typographic hierarchy;
- whitespace;
- thin rules;
- stable alignment;
- restrained accent;
- deterministic geometry.

## Typography
Use system sans for content and monospace for kicker, section labels, property keys, technical metadata, and footer labels.

Recommended sizes:
- hero KPI: 44px desktop / 38px compact;
- title: 22px;
- now title: 18px;
- property body: 15px;
- labels/meta: 10–12px.

## Color

Source: `EXECUTAR-REPORT-PRINT-DS-001` v1.0 (`references/200-executive-report-print-contract.md`), resolved in `assets/tokens/tokens.json` and published as `assets/tokens/tokens.css`. Consumed via `var(--exec-color-*)` in `assets/report.css` — do not hardcode hex here or in the CSS.

- page background: `var(--exec-color-surface-shell)` → `#FFFFFF`
- sheet: `var(--exec-color-surface-page)` → `#FFFFFF`
- primary ink: `var(--exec-color-ink-title)` → `#4B4A4A`
- secondary ink: `var(--exec-color-ink-secondary)` → `#7C7B7B`
- separators: `var(--exec-color-rule-subtle)` → `#EAEAEA`
- accent: `var(--exec-color-brand)` → `#00BF63`
- accent surface: `var(--exec-color-accent-soft)` → `#F3F6FA`
- chip surface: `var(--exec-color-accent-soft-strong)` → `#CFE2F4`
- chip ink: `var(--exec-color-brand-strong)` → `#007A45`

The report must remain intelligible without color — grayscale/photocopy
usability is a hard requirement, independent of which theme eventually fills
these tokens.

## Avoid
Drop shadows, strong radii, gradients, decorative charts, dense iconography, and unnecessary status colors.

## Reading order
1. identity/header;
2. project progress;
3. execution depth;
4. temporal triptych;
5. immediate action;
6. operational properties;
7. tags;
8. footer.
