# Contrato de tokens de design

**Os valores concretos existem.** Fonte: `EXECUTAR-REPORT-PRINT-DS-001` v1.0,
trazido verbatim em `references/200-executive-report-print-contract.md` e
implementado em `assets/templates/executive-report-a4.html`. Os valores
resolvidos vivem em `assets/tokens/tokens.json` (camadas raw/alias/componente)
e são publicados como custom properties CSS em `assets/tokens/tokens.css`,
gerado a partir do JSON — não edite o `.css` à mão.

Não hardcode hex, nem em CSS, nem em SVG, nem em prosa de referência — use o
alias correspondente (`var(--exec-color-*)` ou, no template PRISM, o nome sem
prefixo). Um punhado de aliases herdados da vocabulary anterior continua sem
valor porque o contrato novo genuinamente não os cobre — ver "Lacunas em
aberto" abaixo. Onde um desses aparece num `:root`, o marcador permanece
`/* A DEFINIR — LACUNA */`: isso é honesto, não um resíduo de merge.

## De onde vem esse contrato

O stack anterior (família "Executar Playbook", extração `REFERENCE_ONLY` de
JPGs de referência) foi descartado por inteiro nesta integração — não é mais
a fonte de nenhum valor. O contrato atual vem de uma hierarquia de autoridade
própria (ver `references/200-executive-report-print-contract.md` §2):
Desyng-System-ecossistema → `01-Executar-Echo/packages/design-tokens` →
`01-Executar-Echo/packages/design-system` → Showroom EXECUTAR. É a paleta
Green/Azure/Neutral + IBM Plex, com valor hex medido diretamente — não mais
`px-image` de uma extração.

## As três camadas

```
raw        valor primitivo (cor medida, número bruto). Nenhum componente
           consome esta camada diretamente.
  ↓
alias      o que o componente consome: --exec-color-brand, --exec-space-4…
  ↓
componente o que cada peça usa: field.placeholder, check.box, kpi.value…
```

A camada alias existe para que trocar o acento visual seja uma linha, e não
uma caçada por valor espalhado pelo arquivo. Regra que sustenta isso:
**acento é sempre presentacional, nunca estrutural.** Trocar cor não pode
mexer em hierarquia, grade ou dado.

## Proveniência: todo item declara de onde veio

Cada entrada em um futuro `assets/tokens/tokens.json` deve carregar `origem`
e `base`, seguindo `assets/tokens/tokens.schema.json`:

| origem | significa | o que se pode fazer |
|---|---|---|
| `FONTE` | medido ou observado na fonte de design atual | usar como está |
| `DECISAO` | a fonte deixou indefinido e esta camada fixou um valor | usar, mas ler a `base` antes de mudar |
| `LACUNA` | continua indefinido | **decidir e registrar antes de usar** — o validador deve acusar se vazar para um artefato |

Todo `DECISAO` carrega, em `base`, o cálculo ou critério que justificou o
valor — nunca um número solto sem explicação.

## Validação de contraste

Qualquer par texto/fundo precisa atender:
- **≥ 4,5:1** para texto normal (corpo, placeholder, título);
- **≥ 3:1** para objeto gráfico (contorno de checkbox, borda de campo,
  rótulo puramente decorativo).

`scripts/tokens.py --contraste` recalcula essa tabela assim que
`assets/tokens/tokens.json` existir. Nenhum tema deve ser considerado pronto
sem essa checagem passando.

## Temas: sobreposição, não reescrita

Um tema é uma sobreposição de valores na camada alias — nunca cria token
novo, nunca mexe em grade, geometria ou hierarquia. Se um tema precisar
mudar layout, ele não é tema: é outro contrato de peça, e o lugar dele é em
`references/workbook/contrato-workbook.md`.

O contrato atual define UMA identidade canônica, não uma família de temas
trocáveis (a família anterior tinha `playbook`/`swiss`/`editorial`; esses
nomes não existem mais). `assets/tokens/temas.json` registra essa identidade
única (`executar`) com `overrides: {}` — é a base, não uma variação dela. Um
tema novo só se justifica se e quando o usuário pedir explicitamente uma
segunda leitura visual da mesma estrutura.

## Falha de contraste conhecida (bloqueia o workbook, não é LACUNA)

`ink-placeholder` (`neutral-9`, `#959494`, herdado de `--text-muted` do
contrato) TEM valor — mas esse valor dá 3,03:1 de contraste contra
`surface-page`, abaixo do mínimo de 4,5:1 que `scripts/validar_artefato.py`
exige para texto de placeholder (regra específica do workbook, ver
`references/workbook/placeholder-checkbox.md`). `scripts/gerar_workbook.py`
recusa corretamente gerar qualquer peça enquanto isso não for resolvido —
não é um bug, é o validador funcionando. Três opções pendentes de decisão
do usuário estão detalhadas em `MERGE_NOTES.md` (seção "2026-09-23 —
Bugs reais..."). Não escolha uma sozinho.

## Lacunas em aberto

Estes aliases não têm valor porque o contrato genuinamente não os cobre —
decidir antes de usar, não inferir:

- `surface-inverse`, `ink-muted-alt`, `ink-inverse-muted`, `data-neutral` —
  ver `base` de cada um em `assets/tokens/tokens.json` para o raciocínio.
- `accent-blue`, `accent-green`, `accent-lavender`, `accent-peach`,
  `accent-violet` — paleta categórica de 5 cores do gerador de wireframe
  (`scripts/gerar_wireframe.py`). O contrato novo define só verde/azure
  funcionais e proíbe paleta paralela (§1 do contrato). Na prática, nenhum
  desses aliases é hoje consumido pelo wireframe (ele usa `ink-placeholder`,
  `surface-page`, `rule-subtle`/`rule-default`, `ink-title`, `ink-muted` —
  todos já resolvidos); a lacuna só importa se alguém reintroduzir uma
  paleta categórica de rascunho no futuro. Decidir então se ela deve vir de
  tons de verde/azure/neutro ou permanecer fora do contrato por ser artefato
  de rascunho não-final.

## Unidades

- Em SVG A4, o `viewBox` é `0 0 210 297`: 1 unidade de usuário = 1mm. Isso é
  geometria de página, não decisão de marca — permanece fixo.
- Nenhuma medida em `px-image` (ou equivalente de uma extração visual) vira
  mm, pt ou px de CSS por conversão silenciosa. Toda medida física é uma
  `DECISAO` registrada com a base do cálculo.
- Escala de espaço fechada (herdada da família anterior, reaproveitável):
  1 · 2 · 3 · 4 · 6 · 8 · 12 · 16 · 24 · 32 mm. Um valor fora da escala é
  sinal de que alguém mediu na tela em vez de decidir.

## Dois vocabulários de raio

Sempre que existe objeto de identidade e chrome de interação na mesma peça,
eles não compartilham raio — mesmo que o valor numérico ainda não esteja
definido:

- raio de artefato (cards, pranchas — o que é do produto);
- raio de controle (botão, pílula, trilha de barra — sempre cápsula/circular);
- raio de checkbox (quase reto de propósito: arredondado demais lê como
  botão, e ninguém escreve dentro de um botão).

## Como mexer sem quebrar

1. Edite `assets/tokens/tokens.json` (nunca `tokens.css` diretamente — ele é
   gerado).
2. Rode `python3 scripts/tokens.py --contraste --lacunas` — nenhuma
   reprovação nova, e confirme que a lista de lacunas ainda bate com a seção
   acima (nem mais, nem menos).
3. Regenere `assets/tokens/tokens.css` e ressincronize os blocos
   `/* TOKENS:INICIO */ … /* TOKENS:FIM */` em `assets/templates/peca-a4.svg`,
   `assets/templates/relatorio-exemplo.html` e
   `assets/templates/status-report-prisma-a4-v4.html`.
4. Regere e valide os artefatos (`scripts/validar_artefato.py`,
   `scripts/gerar_workbook.py`, `scripts/gerar_relatorio.py`,
   `scripts/render_report.py` — este último já injeta `tokens.css` antes de
   `assets/report.css` automaticamente).
