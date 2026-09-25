# Print Rules

Use CSS Paged Media.

```css
@page {
  size: A4;
  margin: 12mm;
}
```

For print:
- force white page background;
- remove browser padding and outer sheet border;
- keep critical semantic blocks together where practical;
- preserve text contrast;
- do not shrink long reports below readable size.

Recommended:
```css
@media print {
  body { padding: 0; background: var(--exec-color-surface-page); }
  .sheet { max-width: none; width: 100%; border: 0; }
  .section, .now, .triptych-wrap, .depth-wrap { break-inside: avoid; }
}
```

Zero and unknown are different: render unknown metrics as `—`, not `0%`.
