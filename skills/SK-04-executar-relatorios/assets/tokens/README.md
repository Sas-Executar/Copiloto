# assets/tokens/ — identidade EXECUTAR resolvida

Uma identidade canônica, não uma família de temas trocáveis.

- `tokens.json` — valores reais (raw → alias → componente, proveniência
  `FONTE`/`DECISAO`/`LACUNA` por item), fonte: `EXECUTAR-REPORT-PRINT-DS-001`
  v1.0 (ver `references/200-executive-report-print-contract.md`).
- `tokens.css` — gerado a partir de `tokens.json`; **não edite à mão**, edite
  o JSON e regenere.
- `temas.json` — um único tema (`executar`) com `overrides: {}`: é a base,
  não uma variação dela.
- `tokens.schema.json` / `temas.schema.json` — forma esperada dos dois
  arquivos acima.

Rode `python3 scripts/tokens.py --contraste --lacunas` antes de gerar
qualquer artefato visual — confirme que a lista de lacunas bate com a seção
"Lacunas em aberto" de `references/design-tokens.md`, nem mais nem menos.

Ver `references/design-tokens.md` para o contrato completo.
