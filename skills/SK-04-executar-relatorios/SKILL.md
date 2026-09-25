---
name: executar-relatorios
description: >
  Skill EXECUTAR consolidada, cinco capacidades com progressive disclosure:
  (1) status report — texto vira relatório editorial source-grounded, JSON
  canônico + HTML de impressão; (2) relatório executivo A4 — diagnóstico,
  recomendação e roadmap para board, pronto para PDF; (3) ~60 templates de
  negócio (memo, proposta, SOP, RAID, RACI, OKR, business case, postmortem,
  e-mails, workbooks); (4) Mapa-OS/PRISM — mapa operacional semanal,
  Agora/Próximo/Depois, WIP=1, projeção Prisma A4; (5) workbook visual
  Desk&Go — 5 peças A4 em SVG, wireframes, validador de contraste/impressão.
  Ative para status report, relatório executivo/para o board,
  memo/proposta/SOP/RAID/RACI/OKR/business case/postmortem, e-mail de
  status/kickoff, Mapa-OS, centro de comando, Agora-Próximo-Depois, Prisma
  (ou atalhos 00/01/02), workbook, Desk&Go, as 5 peças,
  fundação/GTM/roadmap/kanban/canvas, ou conferir SVG/HTML antes da gráfica.
  Substitui executar-status-report, executar-status-report-business-pack,
  executar-mapa-os, deskgo-business-workbook.
---

# EXECUTAR Relatórios

Skill única, quatro capacidades, um só contrato de grounding. Leia apenas o
que a tarefa exige — não carregue toda a árvore de `references/` de uma vez.

**Camada de tokens de design: resolvida.** `assets/tokens/tokens.json`
contém os valores reais do contrato `EXECUTAR-REPORT-PRINT-DS-001` v1.0
(Green/Azure/Neutral + IBM Plex — ver `references/200-executive-report-print-contract.md`),
publicados como `assets/tokens/tokens.css`. Use sempre o alias
(`var(--exec-color-*)` ou, no template PRISM, o nome sem prefixo) — nunca um
hex literal. Um pequeno conjunto de aliases herdados permanece
intencionalmente indefinido porque o contrato não os cobre (ver "Lacunas em
aberto" em `references/design-tokens.md`); se o pedido exigir exatamente um
desses, pergunte ou entregue em modo grayscale/estrutural e diga por quê —
nunca invente o valor.

## Núcleo não-negociável (vale para as quatro capacidades)

- Nunca invente fatos, datas, percentuais, owners, prazos, progresso, riscos,
  ações, requisitos, integrações, evidências ou estados não sustentados pela
  fonte.
- Represente ausência de informação explicitamente: `Não identificado no
  documento`, `null`, `NAO_DETERMINADO` ou `BLOCKED`, conforme o schema em uso
  — nunca um campo vazio silencioso nem um valor inventado para preencher.
- Separe extração de interpretação: normalizar → identificar fatos
  sustentados → mapear no schema → registrar proveniência → validar → só
  então renderizar.
- Não calcule percentuais nem derive datas a não ser que estejam explícitos
  ou sejam exatamente deriváveis de numerador/denominador ou base explícita.
- Não rotule trabalho inferido como concluído. `existente ≠ completo ≠
  aprovado ≠ implementado ≠ testado ≠ verificado ≠ publicado`.
- Não reconcilie conflitos entre fontes silenciosamente — registre o
  conflito (`quality.conflicts` no status report; conflito registrado e não
  resolvido no Mapa-OS).
- Preserve o idioma da fonte, salvo pedido explícito de tradução.
- Mantenha o sistema visual editorial e utilizável em escala de cinza: forte
  hierarquia, whitespace, traços finos, acento contido — nunca dashboard
  decorativo denso.
- Evite quebra de blocos críticos entre páginas impressas onde for prático.
- Campo vazio nunca tem o peso de dado real — três estados (`blank`/`empty`/
  `filled`), nunca só cor para distinguir (não sobrevive a fotocópia).
- Não envie mensagens, publique, faça deploy ou altere sistemas externos sem
  solicitação e autorização específicas.

## Passo 1 — identifique a capacidade

| O pedido fala de… | Capacidade | Leia antes |
|---|---|---|
| status report, converter documento/texto em relatório, sintetizar como report, progresso/riscos/ações de um projeto, report por e-mail (HTML/PDF) | Status report | `references/00-operating-contract.md`, `references/20-report-schema.md`, `references/30-information-mapping.md`, `references/120-email-html.md` |
| relatório executivo A4 para impressão/PDF, "one-pager para diretoria", diagnóstico → recomendação → roadmap, matriz evidência-implicação-ação, capa própria, cabeçalho/rodapé paginado | Relatório executivo (impressão) | `references/200-executive-report-print-contract.md`, `assets/templates/executive-report-a4.html` |
| memo, proposta, SOP, RAID log, RACI, OKR, business case, postmortem, e-mail operacional, brief, ADR, PRD/FRD, kanban, roadmap, retro, canvas — qualquer artefato de negócio fora do status report padrão | Pacote de templates de negócio | `references/100-business-template-routing.md`, `references/110-renderer-profiles.md`, `templates/catalog.json` |
| Mapa-OS, mapa operacional, centro de comando, retomada, Agora/Próximo/Depois, plano semanal Prisma, status EXECUTAR, ou os atalhos 00/01/02 | Mapa-OS / PRISM | `references/mapa-os/architecture-executar.md`, `references/mapa-os/mapa-os-contract.md`, `references/mapa-os/activation-index.md` |
| workbook, Desk&Go, "as 5 peças", Fundação/GTM/Roadmap/Kanban/Canvas, relatório longo de ciclo, painel/comparativo/cronograma numa folha, wireframe, conferir SVG/HTML antes da gráfica | Workbook visual | `references/workbook/contrato-workbook.md` (5 peças), `references/workbook/playbook-relatorios.md` (relatório extenso), `references/workbook/visuais-sob-demanda.md` (visual avulso), `references/workbook/placeholder-checkbox.md` (validação) |
| paleta, tema, "muda a cor", token, contraste, ajuste de stack visual | Contrato de tokens | `references/design-tokens.md` |

Pedido ambíguo ou que cruza duas capacidades: pergunte antes de gerar, ou
combine as referências indicadas — os arquivos não conflitam entre si (ex.:
um relatório de negócio com o visual do workbook lê os dois grupos).

## Passo 2 — capacidade 1: status report

Sempre leia `references/00-operating-contract.md`, `references/20-report-schema.md`,
`references/30-information-mapping.md`. Leia `references/10-input-normalization.md`
para entrada ruidosa/heterogênea. Leia `references/40-visual-system.md`,
`references/50-html-css-architecture.md`, `references/60-print-rules.md` para
saída HTML visual. Leia `references/70-quality-gates.md` e
`references/80-edge-cases.md` antes da entrega final ou quando a confiança
for baixa.

Fluxo: ingerir (IDs estáveis `S01`, `S02`…) → normalizar
(`scripts/normalize_text.py`) → extrair fatos classificados → mapear no
schema → comprimir preservando incerteza → montar JSON canônico
(`schemas/report.schema.json`, validar com `scripts/validate_report.py`) →
renderizar (`scripts/render_report.py saida.html [--email saida.email.html]`,
template `assets/templates/status-report-v1.html` + `tokens.css` + `report.css`) →
validar saída final (`references/70-quality-gates.md`).

Envio por e-mail (HTML no corpo ou PDF anexo, à escolha): perfil `email` em
`references/120-email-html.md`. O `.email.html` é gerado dos tokens por
`scripts/build_email.py` — nunca à mão, nunca com `var()` nem hex solto.

Ordem de leitura na saída HTML: `header → progresso → profundidade →
ontem/hoje/amanhã → agora → properties → tags → footer`.

## Passo 3 — capacidade 2: pacote de templates de negócio

Quando o pedido for um artefato de negócio diferente do status report
padrão, leia `references/100-business-template-routing.md` e
`references/110-renderer-profiles.md`, e escolha o template mais estreito em
`templates/catalog.json`. Categorias disponíveis em `templates/`: `customer/`,
`emails/`, `execution/`, `reports/`, `strategy/`, `workbooks/`, `writing/`.

Preserve as mesmas regras de grounding, proveniência, dado ausente e
validação do status report. Use `scripts/list_templates.py` para inspecionar
o catálogo e `scripts/validate_templates.py` para manutenção do pacote.

## Passo 4 — capacidade 3: Mapa-OS / PRISM

### Ativação simples

- `00`, `/ajuda-mapa` ou "não sei por onde começar" → menu curto de três
  opções (ver `references/mapa-os/activation-index.md`).
- `01`, `/criar-mapa-semanal` ou "quero criar meu mapa da semana" → roteiro
  de `references/mapa-os/prompts/01-prompt-mestre-prisma.md`.
- `02`, `/testar-mapa-prisma` ou "quero ver um exemplo" → exemplo ilustrativo
  em `references/mapa-os/prompts/02-exemplo-preenchido-prisma.md` — nunca
  misture esses dados a um projeto real.

Os IDs numéricos só ativam o roteador quando a mensagem for exatamente 00,
01 ou 02, ou vier com prefixo explícito "Mapa" (ex.: "Mapa 01"). Números em
datas, semanas ou texto corrido não são comandos.

### Antes de operar

Leia sempre `references/mapa-os/architecture-executar.md` e
`references/mapa-os/mapa-os-contract.md`. Leia
`references/mapa-os/projections.md` só ao emitir uma projeção visual/
imprimível. Leia `references/mapa-os/source-audit.md` para distinguir corpus
canônico de protótipos.

### Invariantes

Posição é estado operacional. Dia Lógico é entrega, não data de calendário.
Passagem de tempo não altera estado sozinha. WIP operacional é `1 entrega →
1 fluxo → 1 ação`. Dependências válidas governam elegibilidade — ordem
numérica é só preferencial. Atraso preserva o prazo original e recebe
previsão atual separada, nunca sobrescrevendo um pelo outro.

### Evidência

Classifique com `A_OBSERVADO`, `B_PRIMARIO`, `C_PUBLICADO`, `D_INTERNO` ou
`E_INFERIDO`. Nunca apresente inferência como observação, dado primário ou
fonte publicada.

### Saída

Objeto compatível com `schemas/output.schema.json`, validado com
`scripts/validate_mapa.py`. Projeções: `mapa_operacional` (padrão),
`agora_proximo_depois`, `status_terminal`, `prisma_7d`. Para `prisma_7d`,
construa o payload conforme `schemas/prism-report.schema.json` e renderize
com `python scripts/render_prism.py payload.json output.html` usando o
template imutável `assets/templates/status-report-prisma-a4-v4.html` (A4
retrato, três faces de 99mm, placeholders `DOC_*`/`EPIC_*`/`CALENDAR_*`/
`RESULT_*`). Não edite HTML/CSS para acomodar conteúdo — condense
semanticamente ou retorne erro de fit. Quando `mapa_operacional` precisa
virar um documento A4 permanente (fonte grande e estruturada, não um plano
de sete dias — ex.: um control plane com dezenas de macroáreas), use
`python scripts/render_mapa_operacional.py payload.json output.html`; ao
contrário do `prisma_7d`, o conteúdo é gerado dinamicamente a partir do
payload, sem placeholders fixos. Ver `references/mapa-os/projections.md`.

## Passo 5 — capacidade 4: workbook visual (Desk&Go)

Seis regras valem para todo entregável visual, mesmo quando o pedido parece
simples — detalhe completo em `references/workbook/`:

1. Campo vazio nunca tem o peso de dado real (`blank`/`empty`/`filled`,
   três sinais juntos — itálico, cor mais leve, texto sentinela).
2. Caixa de marcar tem mínimo físico: lado ≥ 3,5mm, traço ≥ 0,25mm.
3. Cor só dentro do bloco de tokens — nunca hex literal num atributo.
   Camadas raw → alias → componente; componente consome só o alias. **Hoje
   essa camada é placeholder — ver aviso no topo deste arquivo.**
4. Medida de origem de imagem/extração nunca vira mm em silêncio — toda
   medida física é decisão registrada com a base do cálculo.
5. Papel nunca sugere ação de tela impossível no papel.
6. Valor-destaque nunca carrega a metodologia junto (número grande numa
   linha, regra de cálculo em outra, menor).

```bash
# workbook: 5 peças A4, determinístico, validado antes de mover
python3 scripts/gerar_workbook.py --output-dir out/ --tema <tema>

# relatório extenso a partir de spec JSON
python3 scripts/gerar_relatorio.py --spec spec.json --saida rel.html

# wireframe antes da peça final
python3 scripts/gerar_wireframe.py --catalogo --saida catalogo.svg

# validação — sempre, mesmo para artefato de terceiro
python3 scripts/validar_artefato.py out/*.svg --modo branco
python3 scripts/tokens.py --tema <tema> --contraste --lacunas
```

`--tema` exige que `assets/tokens/tokens.json` e (se houver mais de um tema)
`assets/tokens/temas.json` existam — hoje eles não existem, só os schemas.
Não invente valores para rodar o gerador; explique ao usuário que o passo
aguarda o contrato de tokens.

Entrega: workbook sempre em zip único (nunca peças soltas); relatório e
visual avulso como arquivo direto.

## Suporte

### Schemas
`schemas/report.schema.json`, `schemas/activation.schema.json`,
`schemas/input.schema.json`, `schemas/output.schema.json`,
`schemas/prism-report.schema.json`, `assets/tokens/tokens.schema.json`,
`assets/tokens/temas.schema.json`.

### Scripts
Status report: `normalize_text.py`, `validate_report.py`, `render_report.py`,
`validate_skill.py`, `list_templates.py`, `validate_templates.py`. Mapa-OS:
`validate_mapa.py`, `audit_prism.py`, `render_prism.py`,
`render_mapa_operacional.py`, `simple_schema.py`.
Workbook: `tokens.py`, `validar_artefato.py`, `gerar_workbook.py`,
`gerar_relatorio.py`, `gerar_wireframe.py`.

### Assets
`assets/report.css`, `assets/source-reference.html`,
`assets/templates/status-report-prisma-a4-v4.html`,
`assets/templates/peca-a4.svg`, `assets/templates/relatorio-exemplo.html`,
`assets/templates/executive-report-a4.html` (relatório executivo A4),
`assets/tokens/` (tokens resolvidos — ver acima), `assets/data/`.

### Exemplos e evals
`examples/` (status report + `mapa-os-*` prefixados), `evals/evals.json`,
`evals/mapa-os-cases.jsonl`.

### Compatibilidade entre agentes
`agents/openai.yaml` documenta a mesma capacidade Mapa-OS para agentes
não-Claude — mantido como referência, não como caminho de execução nesta
skill.

## Manutenção

`MERGE_NOTES.md` na raiz desta skill registra as decisões de consolidação
(o que veio de qual pacote, onde ficou um marcador `A DEFINIR`). Não é lido
em tempo de execução — é changelog interno para humanos.
