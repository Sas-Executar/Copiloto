# Package playbook — relatórios extensos

Um relatório longo não é uma peça grande. A diferença prática: numa folha A4 você
enxerga os campos vazios de relance; em quarenta páginas, um traço solto no meio
de uma tabela passa direto e vira número inventado na leitura de outra pessoa.
Por isso o pacote inteiro é dirigido por dados e conferido por máquina.

## O que "package" significa aqui

Não é um arquivo, são cinco coisas que viajam juntas — sem alguma delas, quem
recebe tem que adivinhar:

1. **Template dirigido por dados** — `scripts/gerar_relatorio.py`. Nenhum
   conteúdo de cliente mora dentro dele. Trocar de cliente é trocar de spec.
2. **Spec de exemplo com casos de borda** — `assets/data/exemplo-relatorio.json`.
   Valor ausente, zero (que é dado, não ausência), texto longo, célula sem valor,
   campo para preencher à mão, e as três situações de caixa. Exemplo só com o
   caminho feliz não prova nada.
3. **Export em lote com nome previsível** — `--lote` produz
   `{id}-v{versao}.html`. Sem isso ninguém reencontra o arquivo em três meses.
4. **Validação antes da entrega** — o gerador roda o validador no arquivo em
   staging e só move se passar.
5. **Handoff escrito** — este arquivo. Tokens, blocos, casos de borda, checklist
   de pré-impressão.

## Gerando

```bash
python3 scripts/gerar_relatorio.py --spec spec.json --saida rel.html
python3 scripts/gerar_relatorio.py --lote specs/ --saida-dir out/
```

O contrato atual define uma identidade única, `executar` (ver
`references/design-tokens.md`) — `--tema` não precisa ser informado. `--modo
branco` gera um relatório para preencher à mão; o padrão é `preenchido`.

## Estrutura do spec

```json
{
  "tema": "executar",
  "meta": { "id", "serie", "titulo", "subtitulo", "cliente",
            "periodo", "responsavel", "confidencialidade", "versao" },
  "resumo_executivo": ["parágrafo", "parágrafo"],
  "pendencias": [{ "id", "texto", "estado", "nota" }],
  "secoes": [{ "titulo": "...", "blocos": [ … ] }]
}
```

Qualquer campo de `meta` pode ser `null` — vira placeholder marcado, não some.

O relatório monta sozinho capa, índice numerado, resumo executivo com as
pendências abertas, as seções e o rodapé paginado.

## Blocos disponíveis

| tipo | campos | nota |
|---|---|---|
| `paragrafo` | `texto` | |
| `lista` | `itens[]` | |
| `destaque` | `rotulo`, `texto` | callout com barra de acento |
| `campo` | `id`, `rotulo`, `valor`, `para_preencher` | `valor: null` → placeholder; `para_preencher: true` → pauta |
| `kpi` | `id`, `rotulo`, `valor`, `metodo` | o `metodo` sai em linha separada, sempre |
| `barra` | `rotulo`, `percentual`, `nota` | |
| `medidor` | `rotulo`, `series[]` com `nome`, `percentual`, `valor`, `destaque` | |
| `tabela` | `colunas[]`, `linhas[][]`, `legenda` | célula `null` → placeholder; número → alinhado à direita com dígitos tabulares |
| `checklist` | `rotulo`, `itens[]` com `id`, `texto`, `estado`, `nota` | |
| `cronograma` | `rotulo`, `raias[]` com `nome`, `inicio`, `duracao` (em %) | |

**Célula `null` não é zero.** A tabela do exemplo carrega essa legenda escrita,
porque a distinção é a origem mais comum de erro de leitura em relatório longo.

## Regras de impressão embutidas

- `@page` com o tamanho, `margin: 0`. A margem física de verdade vive no
  `padding` da folha — declarada no `@page`, o motor aplica escala própria.
- `print-color-adjust: exact` no seletor global. Sem isso o navegador clareia cor
  e fundo no PDF e derruba o contraste.
- `page-break-inside: avoid` em todo bloco de dado: KPI, barra, medidor,
  checklist, destaque, cronograma, campo, tabela e linha de tabela. Nenhum é
  cortado ao meio entre páginas.
- `page-break-after: avoid` nos títulos, para não deixar título órfão no pé.

O validador acusa `PR001`, `PR002` e `PR003` se alguma dessas sumir.

## Exportando para PDF

A exportação headless sai em **RGB**. Conversão para CMYK é etapa externa de
pré-impressão e precisa constar do handoff — nunca trate como resolvida pelo
template.

## Checklist antes de entregar

- [ ] `validar_artefato.py` sem erro no modo certo
- [ ] Todo KPI com a regra de cálculo em linha separada
- [ ] Toda célula sem valor marcada como ausência, não como zero
- [ ] Nenhuma caixa pré-marcada se o relatório for para preencher
- [ ] `tokens.py --contraste` sem reprovação no tema usado
- [ ] Nomes de arquivo previsíveis se for lote
- [ ] Entregue via `present_files`, nunca só descrito em texto
