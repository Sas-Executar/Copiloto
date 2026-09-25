# Visuais sob demanda — wireframe primeiro

Quando alguém pede um visual que não é uma das cinco peças nem um relatório —
"faz um painel de indicadores", "preciso de um comparativo", "queria um
cronograma numa folha" — o caminho é wireframe antes de peça final.

## Por que wireframe antes

Um wireframe colorido e bonito faz a conversa virar sobre cor. O arranjo passa
sem ninguém olhar, e o problema de estrutura só aparece depois de a peça estar
pronta, quando mudar custa caro. Por isso os wireframes desta biblioteca são
deliberadamente feios: cinza, tracejado, com o nome do slot escrito dentro. A
única pergunta que sobra é a certa — "os blocos estão na ordem que faz sentido?"

Pule o wireframe só quando o pedido for uma variação pequena de algo já
aprovado nesta conversa.

## O fluxo

1. **Traduza o pedido em blocos.** Veja o catálogo abaixo e escolha os que
   cobrem o que a pessoa descreveu. Se nada encaixar, diga qual bloco falta em
   vez de forçar um parecido.
2. **Emita o wireframe.**
   ```bash
   python3 scripts/gerar_wireframe.py --composicao capa,kpi,cronograma,checklist --saida wf.svg
   python3 scripts/gerar_wireframe.py --bloco medidor --largura 120 --altura 30 --saida wf-medidor.svg
   python3 scripts/gerar_wireframe.py --catalogo --saida catalogo.svg
   ```
3. **Entregue e pergunte** o que muda de posição, o que sobra, o que falta.
4. **Só então construa a peça final** com os tokens, seguindo
   `references/token-stack.md` e o contrato de marcação de
   `references/placeholder-checkbox.md`.
5. **Valide** com `scripts/validar_artefato.py` antes de entregar.

## O catálogo

```bash
python3 scripts/gerar_wireframe.py --listar
```

| bloco | padrão | serve para |
|---|---|---|
| `campo` | 90×22 | rótulo + caixa de preenchimento |
| `campo-linhas` | 90×30 | campo com pauta para escrita à mão |
| `checklist` | 90×30 | caixas de marcar com critério de aceite |
| `kpi` | 90×38 | indicador dominante com a metodologia em linha separada |
| `barra` | 90×16 | trilha + preenchimento + valor |
| `medidor` | 90×26 | duas ou mais séries comparadas |
| `cartao` | 90×40 | card com ícone, título, corpo e rodapé |
| `grade-cartoes` | 190×60 | grade 3×2 de cards de mesma largura |
| `cronograma` | 190×40 | quatro raias com barras e grade temporal |
| `matriz` | 60×60 | matriz 2×2 de posicionamento |
| `mosaico` | 190×60 | mosaico assimétrico de quatro blocos |
| `indice` | 90×40 | linhas de índice com divisória e paginação |
| `capa` | 190×70 | capa escura com cápsulas e faixa de imagem |
| `tabela` | 190×36 | cabeçalho, linhas zebradas, numérico à direita |
| `pilula` | 90×10 | tags e chips |

Os padrões vêm do que a extração observou nas nove referências — grades de 2, 3
e 4 colunas, mosaico assimétrico, cronograma de quatro raias, medidor de duas
séries. Não são tamanhos arbitrários.

## Acrescentando um bloco novo

Cada bloco é uma função com assinatura `(x, y, w, h) -> fragmento SVG` em
`scripts/gerar_wireframe.py`, registrada no dicionário `BLOCOS` com largura e
altura padrão e uma linha de descrição. Acrescente e ele aparece no catálogo, no
`--listar` e no `--composicao` sozinho.

Mantenha a paleta do wireframe em cinza. A tentação de "só dar uma cor para
ficar mais claro" é exatamente o que destrói a utilidade da etapa.

## Duas regras que valem para a peça final, não para o wireframe

- **Papel nunca sugere ação de tela impossível no papel.** Um botão "+ Novo
  projeto" impresso é uma promessa que o papel não cumpre. Troque por uma nota
  ou por um QR que leve à ação real.
- **Valor-destaque nunca carrega a metodologia junto.** O número grande numa
  linha, a regra de cálculo em outra, menor. O bloco `kpi` já é desenhado assim.
