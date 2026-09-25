# Mapeamento do formulário inicial (V2.3)

A entrada de um ciclo (`schemas/editorial-form.schema.json`) só exige `pack_id`.
`problem_id`, tese, evidências, artigo e assets **não** fazem parte do formulário
inicial — eles nascem dentro da trilha, na etapa certa (`problem_id` em S02, tese
em S05, evidências em S12, artigo master em S17...). Ver `references/sop-kp-001.md`.

Campos aceitos no formulário inicial: `pack_id` (obrigatório), `cycle_id`,
`cycle_title`, `produto_esperado` (deixe `null` — a decisão é tomada em S17),
`asset_plan` (overrides opcionais de quantidade por tipo de asset do Bloco F),
`extensions` (qualquer outro campo já conhecido, preservado sem uso pelo motor).

O normalizador (`scripts/normalize_form.py`) aceita JSON/YAML, CSV e XLSX quando
`openpyxl` estiver disponível. Campos desconhecidos são preservados em `extensions`.
