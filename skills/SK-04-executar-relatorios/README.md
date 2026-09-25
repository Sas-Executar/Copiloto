> **SK-04** · **Jurisdição:** [MAESTRO — Orchestrator Operacional](../../MAESTRO.md) · **Macroáreas:** A10, A00 · **Ponto de entrada:** [`SKILL.md`](SKILL.md)
>
> **Objetivo:** Relatórios source-grounded: status report, relatório executivo A4, ~60 templates de negócio, Mapa-OS/PRISM e workbook Desk&Go.

# executar-relatorios

Skill EXECUTAR consolidada — cinco capacidades de geração de documentos, um só contrato de grounding, progressive disclosure. Consolida quatro skills antigas (`executar-status-report`, `executar-status-report-business-pack`, `executar-mapa-os`, `deskgo-business-workbook`) e adiciona uma quinta capacidade (relatório executivo A4).

Ponto de entrada: **`SKILL.md`**. Leia-o primeiro — ele roteia para a referência certa conforme o pedido, em vez de carregar tudo de uma vez.

## Capacidades

1. **Status report** — texto/documento vira relatório editorial *source-grounded*: JSON canônico + HTML pronto para impressão. Nunca inventa métrica, data ou owner não sustentado pela fonte.
2. **Relatório executivo A4** — diagnóstico → recomendação → roadmap para board, pronto para virar PDF. Template e tokens seguem o contrato `EXECUTAR-REPORT-PRINT-DS-001` v1.0 (Green/Azure/Neutral + IBM Plex).
3. **Pacote de templates de negócio** — ~75 documentos prontos (memo, proposta, SOP, RAID log, RACI, OKR, business case, postmortem, e-mails operacionais, workbooks) em `templates/`.
4. **Mapa-OS / PRISM** — mapa operacional com posição canônica, WIP=1, evidência classificada. Quatro projeções: `mapa_operacional` (padrão — leitura de retomada, documento A4 permanente ou variante compacta de uma folha), `agora_proximo_depois`, `status_terminal`, `prisma_7d` (plano semanal de 7 dias, A4 três faces).
5. **Workbook visual Desk&Go** — kit de 5 peças A4 em SVG, wireframes sob demanda, validador de placeholder/caixa/contraste/impressão.

## Estrutura

```
executar-relatorios/
├── SKILL.md                 # roteador — leia primeiro
├── references/               # documentação por capacidade (progressive disclosure)
│   ├── 00-90-*.md             núcleo do status report (contrato, schema, visual, impressão...)
│   ├── 100-110-*.md           roteamento e perfis do pacote de templates
│   ├── 200-*.md                contrato do relatório executivo (fonte de verdade em prosa)
│   ├── design-tokens.md       contrato de tokens, camadas raw→alias→componente, lacunas em aberto
│   ├── mapa-os/                arquitetura, contrato, projeções, prompts de ativação
│   └── workbook/                contrato das 5 peças, relatório extenso, visuais sob demanda
├── schemas/                  # JSON Schema de cada saída (report, mapa-os, prisma, tokens...)
├── scripts/                  # validação e renderização — sempre use estes, não hand-rolled
├── assets/
│   ├── report.css, source-reference.html
│   ├── templates/              status-report-prisma-a4-v4.html, executive-report-a4.html, peca-a4.svg...
│   └── tokens/                 tokens.json (fonte), tokens.css (gerado), temas.json
├── templates/                 os ~75 templates de negócio, por categoria
├── examples/ · evals/         exemplos reais e casos de teste
└── agents/openai.yaml         compatibilidade Mapa-OS para agentes não-Claude
```

## Tokens de design

`assets/tokens/tokens.json` é a fonte única (camadas raw → alias → componente, proveniência `FONTE`/`DECISAO`/`LACUNA` por item). `assets/tokens/tokens.css` é **gerado** a partir dele via `python3 scripts/tokens.py --css` — nunca edite o `.css` à mão.

Antes de qualquer artefato visual:

```bash
python3 scripts/tokens.py --contraste --lacunas
```

Um pequeno conjunto de aliases permanece intencionalmente `LACUNA` porque o contrato de tokens não os cobre (ex.: paleta categórica do wireframe) — ver `references/design-tokens.md`. Não invente valor para preencher uma lacuna.

## Scripts principais

| Script | Uso |
|---|---|
| `render_report.py` / `validate_report.py` | status report → JSON canônico + HTML |
| `render_prism.py` / `audit_prism.py` | Mapa-OS PRISM (plano semanal A4, 3 faces) |
| `render_mapa_operacional.py` | Mapa-OS operacional (documento A4 permanente, comprimento variável) |
| `validate_mapa.py` | valida saída do Mapa-OS contra `schemas/output.schema.json` |
| `list_templates.py` / `validate_templates.py` | catálogo e validação do pacote de ~75 templates |
| `gerar_workbook.py` / `gerar_relatorio.py` / `gerar_wireframe.py` | workbook Desk&Go (5 peças, relatório extenso, wireframe) |
| `validar_artefato.py` | valida placeholder/caixa/contraste/impressão de qualquer artefato visual |
| `tokens.py` | resolve tokens, gera CSS, checa contraste e lacunas |
| `validate_skill.py` | valida a estrutura do pacote e as referências de progressive disclosure |

## Regras não-negociáveis (todas as capacidades)

- Nunca invente fatos, datas, percentuais, owners, prazos, riscos ou estados não sustentados pela fonte. Ausência de informação é explícita (`null`, `Não identificado no documento`, `NAO_DETERMINADO`, `BLOCKED`), nunca um campo silenciosamente vazio.
- Separe extração de interpretação: normalizar → identificar fatos sustentados → mapear no schema → registrar proveniência → validar → só então renderizar.
- `existente ≠ completo ≠ aprovado ≠ implementado ≠ testado ≠ verificado ≠ publicado`.
- Nunca hardcode hex — use os tokens (`var(--exec-color-*)` ou o alias correspondente).

## Manutenção

`MERGE_NOTES.md` (na raiz da skill) registra o histórico completo: a consolidação das 4 skills antigas, a integração do contrato real de tokens, dois bugs reais encontrados e corrigidos pelo loop de avaliação, e as decisões de cada rodada. É changelog interno para humanos, não é lido em tempo de execução.

`executar-relatorios-workspace/` (diretório irmão desta skill) guarda a iteração 1 do loop de avaliação (skill-creator): 5 casos de teste, grading, benchmark (92% com skill vs 42% sem) e notas de análise.
