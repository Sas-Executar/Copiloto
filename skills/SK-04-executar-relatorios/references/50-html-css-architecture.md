# HTML/CSS Architecture

## Structural layers
Use `body` as neutral canvas, `.sheet` as report surface, `.header` as identity block, `.section` as vertical rhythm, and semantic component classes.

Use fixed-layout tables only for compact presentation grids:
- KPI row;
- execution depth;
- yesterday/today/tomorrow;
- key/value properties.

`table-layout: fixed` is intentional here because reports benefit from stable alignment and predictable print geometry.

## Canonical classes
`.sheet`, `.header`, `.kicker`, `.title`, `.meta`, `.section`, `.section-label`, `.dashboard-table`, `.hero`, `.progress-track`, `.progress-fill`, `.depth-table`, `.depth-current`, `.triptych-table`, `.current`, `.now`, `.chip`, `.properties`, `.tags`, `.footer`.

## Responsive rule
At compact widths reduce outer padding and typography while preserving semantic order and content.

## Portability
Generate self-contained HTML with inline CSS and no external fonts, CDN dependencies, JavaScript, or remote assets by default.
