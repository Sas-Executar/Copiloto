# Input Normalization

## Supported textual inputs
Directly process `.txt`, `.md`, pasted text, and simple HTML after visible-text extraction.

For PDF, DOCX, spreadsheet, slide, image, scan, or other binary/visual formats, use an appropriate extraction tool first.

## Preserve
Never remove numbers, units, dates, percentages, task states, checkboxes, headings, list ordering, explicit negations, source identifiers, dependencies, or quoted decisions.

## Normalize
Normalize repeated blank lines, duplicated whitespace, HTML entities, obvious repeated page headers, bullet markers, and broken line wraps only when meaning is unambiguous.

## Section detection
Use explicit headings first.

When headings are absent, infer groups conservatively from blank-line boundaries, bullet clusters, repeated labels, temporal markers, and status keywords.

Record uncertain boundaries as uncertainty rather than fact.
