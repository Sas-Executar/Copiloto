# Desk&Go Business Workbook — contrato das cinco peças

Escopo fixo: sempre as cinco, sempre nesta ordem. Nunca pergunte quais incluir.
Se o pedido parecer sugerir um subconjunto, confirme antes de se desviar — pode
ser que a pessoa queira uma peça avulsa, que é outro fluxo.

| # | Peça | Blocos |
|---:|---|---|
| 01 | **Fundação do Negócio** | propósito · problema · público · proposta de valor · portfólio híbrido (digital/serviço/físico) · matriz de hipóteses (5 linhas) · posição competitiva (3 concorrentes + matriz 2×2) |
| 02 | **GTM / Lançamento** | objetivo · mensagem-chave · matriz de 3 canais · cronograma de 8 semanas · 3 métricas com meta · síntese executiva |
| 03 | **Roadmap** | visão de 12 meses · 4 fases trimestrais · agora/próximo/depois · 3 marcos do ano · governança e riscos |
| 04 | **Kanban de Sprints** | dados do ciclo · board A Fazer/Fazendo/Feito com limite na coluna do meio · síntese do ciclo · cartões destacáveis |
| 05 | **Business Model Canvas** | os nove blocos clássicos, em três faixas que leem juntas |

## Contexto que molda os campos

O workbook é para um fundador solo com portfólio híbrido — uma oferta digital,
uma de serviço, uma física — operando sozinho por 12+ meses antes de trazer time
ou sócios. Os rótulos refletem isso ("3 ofertas", "1 fundador", horizonte solo).
Não generalize para "equipe" ou "sócios" a menos que peçam explicitamente para
adaptar o kit.

## Geometria

A4 retrato, 210×297mm, margem segura 10mm, grade de 12 colunas com calha de 3mm
(coluna útil ≈ 13,08mm). Tudo derivado dos tokens — o gerador lê
`exec-page-margin`, `exec-grid-gutter` e companhia, não constantes soltas.

A mancha de conteúdo termina em 252mm; abaixo disso fica o bloco de critérios de
aceite, ancorado no rodapé para que todas as peças tenham o mesmo lugar de
conferência. **Se um bloco estourar esse limite, o gerador falha** em vez de
encolher a margem — margem comida é o começo de toda peça que sai errada da
gráfica.

## Gerando

```bash
python3 scripts/gerar_workbook.py --output-dir out/
```

`--force` só com autorização explícita para sobrescrever diretório não vazio.

Duas garantias embutidas:

- **Determinismo** — mesma versão e mesmo tema produzem bytes idênticos. Sem
  data, sem contador, sem ordem dependente de execução. Dá para versionar os SVG
  e enxergar o diff real quando algo muda.
- **Nada parcial** — as peças são escritas num diretório temporário, validadas
  uma a uma em `--modo branco`, e só então movidas. Pacote pela metade é pior
  que pacote nenhum: alguém imprime as três que saíram e descobre o buraco na
  reunião.

O gerador roda o validador internamente. Uma peça que reprove derruba a geração
inteira com o código do defeito na mensagem.

## Empacotando

```bash
mkdir -p /mnt/user-data/outputs
cd out/ && zip -j /mnt/user-data/outputs/deskgo-workbook-<tema>.zip *.svg
```

Nomeie com o tema para distinguir execuções. Entregue só o zip via
`present_files`, nunca os cinco SVG soltos.

## Tema

O contrato atual (`EXECUTAR-REPORT-PRINT-DS-001`) define uma identidade única,
`executar` — não há mais família de temas trocáveis (`playbook`/`swiss`/
`editorial` foram descontinuados junto com o stack de tokens anterior; ver
`references/design-tokens.md`). Não pergunte tema ao usuário: `--tema` do
gerador já usa `executar` como padrão e não precisa ser informado.

## Estendendo uma peça

As peças são declarativas, no topo de `scripts/gerar_workbook.py`:

```python
("campo", "proposito", "PROPÓSITO", 6, 22)   # tipo, id, rótulo, colunas, altura mm
("secao", "Portfólio híbrido")
("matriz", "matriz-posicao", "MATRIZ 2×2", 5, 26)
("cartoes", "cartoes-destacaveis", "CARTÕES PARA RECORTAR", 12, 30)
```

O motor de layout empacota da esquerda para a direita até fechar 12 colunas e
quebra sozinho. Para acrescentar um bloco, some as alturas e confira que a peça
ainda termina antes de 252mm — ou o gerador vai avisar por você.

Conteúdo real do usuário **não** entra editando o SVG por cima. Se ele forneceu
dados, isso é uma extensão do gerador (peça confirmação antes) ou vira um
relatório, que é o fluxo de `references/playbook-relatorios.md`.
