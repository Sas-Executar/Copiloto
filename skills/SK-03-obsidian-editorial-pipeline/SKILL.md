---
name: obsidian-editorial-pipeline
description: "Opera a produção editorial faseada no Obsidian pela SOP-KP-001 (transformação → problema → público → perguntas → tese → inventário → MECE → escopo → sequência → outline → argumentos → evidências → claims → storyboard → brief visual → Content-Spec → artigo → visual → infográfico → vídeo → derivados → QA → operação). Use para criar, continuar, revisar, organizar ou empacotar ciclos editoriais completos — nunca pulando direto de um tema para produção. Compõe dinamicamente artigo, evidências, produto/solução (quando o CTA gerar um), vídeo, carrosséis, imagens, stories, newsletters, ebooks, CTAs, QA e operação (agendamento/publicação/medição/aprendizado)."
metadata:
  version: 2.3.0
---
# Obsidian Editorial Pipeline V2.3

## Objetivo
Transformar um ciclo editorial em um job operacional rastreável no Obsidian, avançando
por dependências reais (WIP=1) pelos 8 blocos da **SOP-KP-001**, sem exigir nada antes
da hora e sem quantizar progresso em degraus artificiais.

## O que mudou na V2.3 (correções estruturais)

1. **A trilha não começa em "tema validado".** Ela abre no Bloco A da SOP-KP-001 —
   transformação (S01) e só depois problema canônico (S02) — e segue os 8 blocos
   reais: Estratégia & Problema → Conhecimento & Evidência → Conteúdo Master →
   Produto/Solução (condicional) → Design & Visual → Derivados e Distribuição →
   QA & Governança → Operação. Nunca pular para pesquisa ou produção com o problema
   ainda em aberto.
2. **O formulário inicial não exige `problem_id` (nem tese, evidência, artigo ou
   assets).** Definir o problema é uma das primeiras tarefas da SOP, não um
   pré-requisito para abrir o job. O YAML/JSON de entrada identifica apenas o
   `pack_id` do ciclo e, opcionalmente, overrides já conhecidos (`cycle_title`,
   `asset_plan`, `produto_esperado`). Tudo o mais nasce dentro da trilha, na etapa
   certa — ver `schemas/editorial-form.schema.json`.
3. **O Bloco D (Produto/Solução) é condicional e nunca presumido.** Ele só habilita
   quando o operador registra explicitamente `produto_esperado = true` (a decisão
   é tomada em S17, ao fechar o artigo master — nunca antes, nunca por inferência).
   Quando ativo, ele nunca trava nem substitui os blocos principais: é formalizado
   (PRD→FRD→UX→Agent Spec→Tech Spec→ADR→Data→NFR→Safety→MVP) e fica estacionado como
   subprojeto do pack, sem consumir o eixo editorial e sem gerar código.
4. **Progresso é real, não quantizado.** `percent = 100 × etapas_habilitadas_concluídas
   ÷ etapas_habilitadas`, um número contínuo — não mais os degraus fixos 0/33/66/99/100
   da V2.2. Ao concluir a última etapa habilitada, a interface mostra **"Pronto para
   gerar ZIP"** (não "99%" nem "100%"). Só depois que o ZIP é gerado e os hashes do
   manifesto são conferidos o ciclo vira **"100% Empacotado"**.
5. **Cada etapa tem exatamente um entregável ativo.** Toda página de etapa segue a
   mesma anatomia 1:1: Agora → Entregue isto → Gancho para o tema → Preencha aqui
   (vazio) → Evidência → Pronto quando (um único critério) → Contexto de referência
   (recolhido, nunca pré-preenchido) → Próximo passo (um único avanço possível). Ver
   `references/ux-hig-obsidian.md`.
6. **O gancho de cada etapa é personalizado pelo tema escolhido, sem pré-preencher
   a resposta.** `cycle_title` (o tema/título de trabalho informado no formulário
   inicial) é interpolado na pergunta-guia de cada etapa (`config/process-v03.json`
   → campo `gancho`), para que o operador nunca abra uma etapa sem saber o que
   produzir para o seu tema específico — mas a área "Preencha aqui" continua
   nascendo vazia; o gancho pergunta, nunca responde.

## Fontes de verdade
1. Pedido e decisões explícitas do usuário para o ciclo atual (inclui `produto_esperado`).
2. **SOP-KP-001** — processo canônico único. Resumo operacional em
   `references/sop-kp-001.md`; blocos, etapas, dependências, artefato e critério de
   pronto de cada etapa em `config/process-v03.json`.
3. Formulário de entrada fornecido pelo usuário; na ausência de campos opcionais, usar
   os defaults de `config/process-v03.json` (`default_assets`) e `schemas/editorial-form.schema.json`.
4. Estado existente do ciclo em `00-Sistema/estado-do-ciclo.json`.
5. Templates e referências desta skill (forma/estilo — nunca gates; ver `references/source-precedence.md`).

Se houver conflito, aplicar `references/source-precedence.md`. Nunca inventar
`problem_id`, owner, aprovação, evidência, fonte, data, URL, status ou a decisão
`produto_esperado`.

## Inferir operação
- `CREATE`: há um `pack_id` novo e não há job existente para ele.
- `CONTINUE`: há job existente, ou pedido para prosseguir/atualizar/decidir o Bloco D.
- `PACKAGE`: pedido de ZIP/handoff, ou todas as etapas habilitadas estão `DONE`
  (estado `PRONTO_PARA_EMPACOTAR`).
Não exigir comandos rígidos. Aceitar instruções naturais e combinações de entregáveis.

## Experiência obrigatória no Obsidian
- Tudo que o operador vê e preenche deve estar em português.
- Todo ciclo possui um único entry point: `00 - COMEÇAR AQUI.md`.
- O operador atravessa o ciclo por wikilinks internos sem voltar à árvore.
- Toda etapa mostra **Anterior · Começar aqui · Painel · Próxima**, o bloco (A–H) e
  o único critério de pronto desta etapa.
- Imagens aceitam `![[arquivo.png]]` e link do Drive; vídeos possuem campo explícito
  para URL do Google Drive.
- `99 - FINALIZAR E GERAR ZIP.md` é o ponto final operacional.
- Antes de empacotar um vault preenchido manualmente, executar `scripts/sincronizar_obsidian.py`.
- Consulte `references/navegacao-obsidian.md` e `references/ux-hig-obsidian.md`.

## Executar

1. Ler integralmente o pedido do usuário, o job existente (se houver) e qualquer
   documento de referência fornecido (ex.: um knowledge pack anterior). Não copiar
   conteúdo já preenchido de um documento de referência para dentro dos campos de
   execução de uma etapa nova — o campo de preenchimento nasce sempre vazio; o
   documento de referência vira, no máximo, uma etapa concluída no histórico ou um
   link em "Contexto de referência".
2. **Criar o job com o formulário mínimo.** Normalizar a entrada segundo
   `schemas/editorial-form.schema.json` (`scripts/normalize_form.py` se necessário).
   O único campo obrigatório é `pack_id`. Nunca perguntar por `problem_id`, tese,
   evidências ou artigo neste passo — eles nascem em S02, S05, S12 e S17.
3. `scripts/create_job.py` monta a camada técnica em `00-Sistema/`, calcula quais
   etapas ficam habilitadas (asset com quantidade 0 vira `SKIPPED`; Bloco D fica
   `PENDING`/desabilitado até a decisão de `produto_esperado`) e gera
   `00 - COMEÇAR AQUI.md`, `01 - PAINEL DO CICLO.md`, a trilha `02 - TRILHA/`,
   `98 - CHECKLIST FINAL.md` e `99 - FINALIZAR E GERAR ZIP.md`.
4. Selecionar somente um nó elegível por vez (`scripts/next_action.py`). Não iniciar
   o próximo nó enquanto existir `IN_PROGRESS` (WIP=1).
5. Produzir o artefato do nó — e só ele — com a estrutura da etapa (Agora → Entregue
   isto → Preencha aqui → Evidência → Pronto quando → Contexto → Próximo passo).
   Adaptar o conteúdo real ao entregável pedido, sem criar seções extras nem
   antecipar entregáveis de etapas futuras.
6. Registrar output e evidência. `DONE` exige output existente + evidência
   verificável + o único critério de pronto da etapa marcado — nunca a existência
   do arquivo sozinha como prova.
7. **Ao concluir S17 (artigo master)**, registrar explicitamente a decisão do Bloco D:
   `scripts/update_step.py JOB S17 --done --output ... --evidence ... --produto-esperado true|false`.
   Sem essa decisão, S18 fica bloqueada — mas o Bloco E nunca fica bloqueado por causa
   dela (regra da SOP: Bloco D nunca trava o eixo principal).
8. Recalcular estado a cada mudança (`scripts/update_step.py` já faz isso): estado
   `PLANEJANDO` → `EM_ANDAMENTO` → `PRONTO_PARA_EMPACOTAR` → `EMPACOTADO`, com
   `percent` sempre = etapas habilitadas concluídas ÷ total habilitado.
9. Antes de gerar o ZIP, executar `scripts/validate_job.py`. Corrigir erros.
10. Em `PRONTO_PARA_EMPACOTAR`, executar `scripts/build_production_zip.py`. Isso é o
    que marca `packaged=true` e muda o estado para `EMPACOTADO` — nunca declarar
    "100%" antes disso.
11. Só marcar `handoff_accepted` quando houver evidência explícita de aceite por
    quem recebe o pacote fora desta skill (ex.: outra equipe/Fase 2 de um Process
    Doc de marca mais amplo). Empacotado ≠ aceito por terceiros.

## Modelo editorial canônico
Cadeia de blocos: **A Estratégia & Problema → B Conhecimento & Evidência → C
Conteúdo Master → D Produto/Solução (condicional) → E Design & Visual → F Derivados
e Distribuição → G QA & Governança → H Operação.** Cadeia final de qualquer pack:
`artigo → visuais → infográfico → vídeo → derivados → QA → agendamento →
publicação → medição → aprendizado`. Evidência e raciocínio ficam ligados ao
problema (S02); todo asset herda `problem_id`, `solution_id` (se houver Bloco D),
`evidence_refs` e `cta_id`. Um asset deve ter uma próxima ação principal.

## Regras de controle
- WIP=1.
- Não publicar, agendar, enviar ou contatar terceiros sem autorização explícita —
  mesmo dentro do Bloco H (Operação), que é parte do ciclo mas não dispensa aprovação.
- Não refazer pesquisa já sustentada apenas porque muda o formato do asset (Bloco F
  reutiliza o Knowledge Master).
- Não tratar arquivo existente como prova de conclusão — só o critério de pronto
  marcado + evidência real.
- Não marcar claim como [E1] sem fonte identificável; [FW] nunca vira [E1].
- Não presumir a decisão `produto_esperado`. Sem evidência suficiente para um Top N
  (Bloco D) ou para sustentar um claim (Bloco B), nunca preencher artificialmente —
  marcar como pendente/insuficiente.
- Capturar nova ideia durante WIP na fila/backlog; não interromper o nó ativo.
- Quando faltar aprovação humana, preparar tudo e usar `USER_ACTION_REQUIRED`.
- Em falha parcial, registrar efeitos já produzidos e evitar duplicidade.

## Ferramentas locais
```bash
python3 scripts/normalize_form.py FORMULARIO --out normalized-form.json   # opcional; só pack_id é obrigatório
python3 scripts/create_job.py normalized-form.json --out JOB_DIR
python3 scripts/next_action.py JOB_DIR
python3 scripts/update_step.py JOB_DIR S01 --start
python3 scripts/update_step.py JOB_DIR S01 --done --output CAMINHO --evidence "descrição/arquivo"
python3 scripts/update_step.py JOB_DIR S17 --done --output CAMINHO --evidence "..." --produto-esperado true   # ou false
python3 scripts/sincronizar_obsidian.py JOB_DIR
python3 scripts/atualizar_navegacao.py JOB_DIR
python3 scripts/validate_job.py JOB_DIR
python3 scripts/build_production_zip.py JOB_DIR --out pacote.zip
python3 scripts/verify_package.py pacote.zip
```

## Entrega ao usuário
Informar bloco atual, nó executado, artefatos criados/alterados, evidência,
bloqueios e próxima ação — sempre em termos de "etapas habilitadas concluídas / total"
(nunca um percentual quantizado). Em `PACKAGE`, entregar o ZIP e o relatório de
verificação, deixando claro que "Empacotado" é um estado técnico desta skill, não
aceite por terceiros. Não alegar aceite/handoff sem evidência registrada.
