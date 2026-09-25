# Placeholder e caixa de marcar — o contrato de marcação

Esta é a parte da skill que mais evita retrabalho caro. Os dois defeitos que ela
persegue não aparecem na tela: campo vazio que parece dado real, e caixa que não
dá para marcar. Os dois só aparecem depois de impresso, quando já custou papel,
tempo e uma reunião constrangida.

## Por que um contrato de marcação, e não só "capricho visual"

O validador precisa saber, sem renderizar nada, qual elemento é campo, qual é
caixa, e em que estado cada um está. Por isso os artefatos carregam atributos
`data-*` e classes previsíveis. É o que permite rodar a conferência em cinco
peças e quarenta páginas de relatório em menos de um segundo.

Funciona igual em SVG e em HTML.

## Campos: três estados, não dois

```xml
<g class="exec-field" data-field="proposito" data-state="filled">
  <text class="rotulo">PROPÓSITO</text>
  <text class="valor">Tirar o operador solo do improviso.</text>
</g>
```

| estado | quando usar | o que o artefato precisa ter |
|---|---|---|
| `blank` | campo desenhado para alguém escrever depois | uma área de escrita: `exec-field__box` ou `linha-escrita` |
| `empty` | dado que deveria existir e não existe | classe `exec-is-placeholder` **e** o texto sentinela `— pendente` |
| `filled` | tem dado real | conteúdo não vazio, sem a sentinela, sem a classe de placeholder |

A distinção entre `blank` e `empty` não é preciosismo. Num caderno para imprimir
e preencher à mão, carimbar "— pendente" em quarenta campos vira ruído: a pauta
já comunica "escreva aqui". Num relatório de quarenta páginas, ao contrário, um
campo vazio sem marcação nenhuma desaparece no meio do texto preenchido e o
leitor conclui que o dado é zero. Cada situação tem um tratamento.

**Por que três sinais juntos no `empty`** — itálico, cor mais leve e texto
sentinela. Cor sozinha não sobrevive a fotocópia em preto e branco, e o
relatório impresso circula fotocopiado mais vezes do que se imagina.

## Caixas de marcar

```xml
<g class="exec-check" data-check="ac-01" data-state="off" data-label="Evidência anexada">
  <rect class="exec-check__box" width="4" height="4" stroke-width="0.35"/>
  <text class="exec-check__label">Evidência anexada</text>
</g>
```

| estado | desenho | significado |
|---|---|---|
| `off` | só a caixa | não feito |
| `on` | caixa + `exec-check__mark` | feito |
| `na` | caixa + `exec-check__na` | não se aplica — **registrado, não apagado** |

`na` existe porque apagar um critério que não se aplica esconde a informação de
que ele foi considerado. Quem lê depois não distingue "não se aplica" de
"esqueceram".

**A caixa declara `width`, `height` e `stroke-width` como atributos**, não só em
CSS. É o que permite conferir a geometria física sem renderizar. Os mínimos:

- lado ≥ **3,5mm** — menos que isso não cabe um traço de caneta
- traço ≥ **0,25mm** — menos que isso some na impressão
- diferença entre os lados ≤ 15% — caixa retangular lê como campo de texto

## Rodando o validador

```bash
python3 scripts/validar_artefato.py peca.svg --modo branco
python3 scripts/validar_artefato.py out/*.svg relatorio.html --modo preenchido --format json
```

`--modo branco` é o caderno para imprimir: campo vazio é o esperado e **nenhuma
caixa pode vir marcada** (quem imprime receberia uma decisão que não tomou).
`--modo preenchido` é o artefato final com dados: campo ainda vazio vira aviso e
sentinela dentro de campo preenchido vira erro.

Sai `0` quando não há erro, `1` quando há. Avisos não derrubam a saída.

## Códigos

**Campos**

| código | grau | o quê |
|---|---|---|
| `PH001` | erro | campo sem `data-state` |
| `PH002` | erro | `data-state` fora de blank/empty/filled |
| `PH003` | erro | `empty` sem a classe `exec-is-placeholder` |
| `PH004` | erro | `empty` sem o texto sentinela |
| `PH005` | erro | `filled` contendo a sentinela — placeholder vazou para o dado |
| `PH006` | erro | `filled` com classe de placeholder |
| `PH008` | erro | `data-field` duplicado |
| `PH009` | aviso | campo vazio ou em branco num artefato declarado preenchido |
| `PH010` | erro | `filled` sem conteúdo |
| `PH011` | erro | `blank` sem área de escrita |
| `PH013` | aviso | `blank` carimbado com a sentinela |
| `PH014` | aviso | `filled` num caderno declarado em branco |
| `PH007` | erro | cor de placeholder abaixo de 4,5:1 contra a superfície |

**Caixas**

| código | grau | o quê |
|---|---|---|
| `CB001` | erro | sem `data-state` |
| `CB002` | erro | estado fora de off/on/na |
| `CB003` | erro | lado abaixo de 3,5mm |
| `CB004` | aviso | fora do quadrado |
| `CB005` | erro | traço abaixo de 0,25mm |
| `CB006` | erro | sem rótulo |
| `CB007` | erro | `data-check` duplicado |
| `CB008` | erro | marcada num caderno em branco |
| `CB009` | erro | marca e estado discordam |
| `CB010` | erro | sem `exec-check__box` |
| `CB011` | aviso | HTML sem `--exec-check-size`; a geometria não pôde ser conferida |

**Tokens, geometria, impressão e texto**

| código | grau | o quê |
|---|---|---|
| `TK001` | erro | cor literal fora do bloco de estilo |
| `TK002` | erro | `var(--…)` usada sem declaração |
| `TK003` | erro | `px-image` vazou para o artefato |
| `GEO001` | erro | geometria fora do A4 do contrato |
| `GEO003` | aviso | sem largura em mm com viewBox; medidas físicas não conferidas |
| `PR001` | erro | HTML impresso sem `print-color-adjust: exact` |
| `PR002` | erro | HTML sem `@page` |
| `PR003` | aviso | HTML sem controle de quebra |
| `TXT001` | erro | sentinela de rascunho no conteúdo |
| `MK001` | aviso | nenhum marcador encontrado |
| `XML001` | erro | SVG malformado |

## A fixture de regressão

`assets/data/fixture-quebrada.svg` planta dezesseis defeitos, um por checagem. Se ela
passar, o validador quebrou:

```bash
python3 scripts/validar_artefato.py assets/data/fixture-quebrada.svg --modo branco
```

## Duas armadilhas já resolvidas — não reintroduza

1. **"todo" é palavra corrente em português.** As sentinelas curtas (`TODO`,
   `TBD`, `XXX`, `FIXME`) são casadas em caixa alta com limite de palavra. Baixar
   para minúsculas faz o validador reprovar praticamente todo artefato real.
2. **Escopo de elemento é estrutural, não por distância.** Uma versão anterior do
   ramo HTML lia uma janela de caracteres em volta do marcador; a janela invadia
   o elemento seguinte e um campo preenchido herdava o placeholder do vizinho. O
   validador monta uma árvore e pergunta pelo subconjunto certo.
