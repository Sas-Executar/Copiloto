# CLAUDE.md: agente permanente de governança EXECUTAR

Este repositório é o **espelho estrutural (Release 2)** do programa EXECUTAR. A **fonte primária (Release 1)** é `_source/EXECUTAR_HUB_Control_Plane_v2.xlsx`, ou o que vier a substituí-la como fonte única. O agente opera sob o [MAESTRO](MAESTRO.md) (`ORC-MAESTRO-001`), e as skills de `skills/` executam o trabalho especializado.

## Regras invioláveis
1. **A planilha manda.** Se o GitHub e a planilha divergirem, abra uma issue `type:conflict` com as duas versões e a fonte. Nunca resolva a divergência em silêncio a favor do GitHub.
2. **Fechar não é aprovar.** Uma issue fechada só rastreia execução (documento criado ou PR aberto). Aprovação é a label `approval:pendente` → `approval:aprovado`, e muda **somente** por ação humana explícita, nunca automaticamente.
3. **WIP = 1.** No máximo uma tarefa em andamento por vez. Não abra frentes de execução paralelas.
4. **IDs canônicos são imutáveis.** `macroarea_id`, `domain_id`, `portfolio_id`, `artifact_id`, `template_id`, `gate_id`, `gap_id` e `conflict_id` são usados literalmente. Nunca renumere nem abrevie.
5. **Nada de inventar.** Owner `A_DEFINIR` significa issue sem assignee. Não crie relação template↔gate nem portfólio↔macroárea enquanto `GAP-DEP-01` estiver aberto: use `gate:tbd`.
6. **Nenhum segredo** em arquivo ou issue. Registre apenas a existência e o local seguro.
7. Saída humana sempre em pt-BR.

## Esquema de IDs e hierarquia
`PROGRAMA (EXECUTAR) → MACROÁREAS (A00–A12) → DOMÍNIOS (D0, D01–D23) ↕ PORTFÓLIO (S0, M0–M16) → ARTEFATOS (Dxx-DOC-XXX-001) → CAMPOS → DEPENDÊNCIAS → GATES (G00–G11) → DOCUMENTOS FINAIS (Axx/Mx/S0/EXECUTAR-FINAL-001)`

| Eixo | Epic | Sub-issues |
|---|---|---|
| Programa | `EXECUTAR-FINAL-001` | 33 Epics, gaps, conflitos |
| Macroárea (13) | `[EPIC MACROÁREA] Axx` | documentos canônicos `Dxx-DOC-*` + `Axx-FINAL-001` |
| Portfólio (20) | `[EPIC PORTFÓLIO] Mx/S0` | 20 templates `TPL-*` (só PRODUCT_INITIATIVE) + `Mx-FINAL-001` |

Arquivos:
- `governanca/<Axx-slug>/<Dxx-slug>/<artifact_id>-<slug>.md`: stubs com front-matter `id`, `status`, `approval`, `owner`, `issue_url`
- `portfolio/<pid-slug>/`: conteúdo de cada iniciativa

O mapa de issues fica em `_bootstrap/manifest-*.json` (chave → número da issue).

## Labels (use somente estas)
- `type:program-epic` · `type:macroarea-epic` · `type:portfolio-epic` · `type:document` · `type:final-dossier` · `type:gap` · `type:conflict`
- `area:A00` … `area:A12`
- `doc-class:macro` · `doc-class:specialized`
- `epistemic:direct` · `epistemic:derived` · `epistemic:external` · `epistemic:proposed` · `epistemic:gap` · `epistemic:conflict`
- `approval:pendente` · `approval:aprovado`
- `automation:A0` … `automation:A4`
- `gate:G00` … `gate:G11` · `gate:tbd`
- `priority:alta` · `priority:media` · `priority:baixa`
- `requires-human-decision`

## Procedimentos

### ADD_TASK
Quando o usuário pedir para adicionar uma tarefa:
1. Identifique o Epic correto (macroárea ou portfólio). Uma tarefa **nunca fica solta**; se o Epic for ambíguo, pergunte.
2. Crie a issue com título `[TIPO] <ID> — <descrição>` e as labels obrigatórias: `type:*`, `area:*` ou o portfólio, `approval:pendente` e `gate:*` ou `gate:tbd`.
3. Vincule a issue como sub-issue do Epic.
4. Responda com o número e o link da issue.

### STATUS_QUERY
Quando perguntarem sobre tarefas ou status:
1. Consulte o estado **real** no GitHub (`list_issues`, `search_issues`, sub-issues do Epic). Nunca responda de memória.
2. Responda com: abertas/fechadas por Epic, `approval:aprovado` × `pendente`, bloqueios (`requires-human-decision`) e a próxima ação única (WIP = 1).

### RECEBER_BRUTO
Quando o usuário entregar conteúdo bruto de uma iniciativa (ex.: Blog/M2) ou de uma área:
1. Classifique cada trecho pelo ID canônico: artefato, template ou campo.
2. Distribua o conteúdo nos stubs de `governanca/...` ou em `portfolio/<pid>/<template_id>.md`, marcando a origem e a classe epistêmica.
3. Atualize o front-matter: `status`, e `issue_url` quando faltar.
4. Comente em cada sub-issue de documento afetada o que entrou e de onde veio, e **feche** a issue (execução). **Não** altere `approval`.
5. Lacunas viram `A_DEFINIR` mais uma issue `type:gap`. Divergências viram `type:conflict`.
6. Commit com mensagem clara. Só siga para a próxima iniciativa quando o usuário indicar.

### VERIFICAR_ESPELHO
Antes de qualquer lote de alterações, releia a planilha e compare as contagens: 13 macroáreas, 24 domínios, 20 portfólios, 20 templates, 12 gates, 37 artefatos, 34 documentos finais. Se houver divergência, abra uma issue `type:conflict` e continue só com o que não foi afetado.
