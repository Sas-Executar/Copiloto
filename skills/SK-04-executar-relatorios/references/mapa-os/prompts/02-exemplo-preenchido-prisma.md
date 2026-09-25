---
activation_numeric: "02"
activation_verbal: "/testar-mapa-prisma"
source_document_id: "1mQuvQNROujTe1SnrfbS19JKIRWz1USmhXRYJigg21aU"
---

> Uso: exemplo preenchido e exclusivamente ilustrativo para demonstrar a geração sem contaminar dados reais.

# PROMPT DE TESTE PREENCHIDO — MAPA-OS SEMANAL EM PRISMA A4

Use a skill $executar-mapa-os para transformar os dados abaixo em um Mapa-OS semanal, com projeção final Prisma A4 V4, pronto para impressão.

## 1. Configuração

- Modo: EXECUTAR

- Projeção: prisma_7d

- Projeto: Ativação do Ecossistema EXECUTAR

- Project ID: PRJ-EXEC-001

- Owner: Não determinado

- Semana: W37

- Período: 07/09/2026 a 13/09/2026

- Timezone: America/Sao_Paulo

- Idioma: português do Brasil

- Formato: A4 retrato, escala 100%

- Geometria: 210 × 297 mm

- Faces: 3 × 99 mm

## 2. Objetivo final

Fechar um pacote mínimo de lançamento com aplicação verificável, três vídeos de demonstração, presença pública e documentação operacional rastreável.

## 3. Problema

Os componentes principais existem em estados diferentes, mas ainda não formam um pacote único, verificado e pronto para operação pública.

## 4. Processo

Executar uma frente por vez, respeitando dependências e WIP=1. Registrar evidência antes de promover estados. Distribuir o trabalho entre Desenvolvimento, Criativo e Operacional sem criar estruturas paralelas.

## 5. Capacidade

- Segunda: 6 horas

- Terça: 6 horas

- Quarta: 6 horas

- Quinta: 6 horas

- Sexta: 6 horas

- Sábado: 2 horas de revisão

- Domingo: 1 hora de fechamento

- Capacidade total: 33 horas

- Restrição: somente uma ação pode permanecer ativa

- Blocos de segunda a sexta: Desenvolvimento 2h, Criativo 2h e Operacional 2h

## 6. Hierarquia operacional

### DLV-APP-001 — Aplicação pública verificável

- Nível: entrega

- Estado: ativa

- Critério de conclusão: aplicação acessível e cenário multiusuário aprovado sem bloqueio crítico

- Prazo original: 08/09/2026

- Previsão atual: 08/09/2026

- Prioridade: crítica

### FLW-APP-001 — Validação técnica

### ACT-APP-001 — Implementar pacote técnico

- Estado: implementado

- Dependências: nenhuma

### - Evidência: EVID-001

- Critério: build concluído sem erro

### ACT-APP-002 — Executar teste público e multiusuário

- Estado: ativa

- Dependência: ACT-APP-001

- Evidência exigida: registro do teste funcional

- Critério: cenário passa sem bloqueio crítico

- Prazo: 08/09/2026

- Prioridade: crítica

### ACT-APP-003 — Registrar correções e decisão de liberação

- Estado: não iniciada

- Dependência: ACT-APP-002

- Evidência exigida: relatório de correções e decisão registrada

- Prazo: 09/09/2026

### DLV-VID-001 — Três vídeos de demonstração concluídos

- Nível: entrega

- Estado: existente

- Critério de conclusão: três vídeos finais acessíveis

- Prazo: 10/09/2026

- Prioridade: alta

### FLW-VID-001 — Produção audiovisual

### ACT-VID-001 — Revisar os três roteiros

- Estado: existente

- Dependência: ACT-APP-002

- Evidência exigida: três roteiros finais

### ACT-VID-002 — Gravar as três demonstrações

- Estado: não iniciada

- Dependência: ACT-VID-001

- Evidência exigida: três arquivos brutos

### ACT-VID-003 — Editar e exportar os vídeos

- Estado: não iniciada

- Dependência: ACT-VID-002

- Evidência exigida: três arquivos finais

### DLV-WEB-001 — Presença pública publicada

- Nível: entrega

- Estado: existente

- Critério de conclusão: landing page e canal público acessíveis

- Prazo: 11/09/2026

- Prioridade: alta

### FLW-WEB-001 — Publicação

### ACT-WEB-001 — Revisar conteúdo da landing page

- Estado: existente

- Dependência: ACT-APP-002

- Evidência exigida: versão revisada

### ACT-WEB-002 — Publicar landing page

- Estado: não iniciada

- Dependência: ACT-WEB-001

- Evidência exigida: URL pública acessível

### ACT-WEB-003 — Executar teste de acesso

- Estado: não iniciada

- Dependência: ACT-WEB-002

- Evidência exigida: registro do teste

### DLV-OPS-001 — Runbook operacional validado

- Nível: entrega

- Estado: existente

- Critério de conclusão: procedimento de operação e retomada validado

- Prazo: 13/09/2026

- Prioridade: média

### FLW-OPS-001 — Evidências e fechamento

### ACT-OPS-001 — Consolidar evidências da semana

- Estado: não iniciada

- Dependências: ACT-APP-003, ACT-VID-003 e ACT-WEB-003

- Evidência exigida: índice das evidências

### ACT-OPS-002 — Validar runbook de retomada

- Estado: não iniciada

- Dependência: ACT-OPS-001

- Evidência exigida: registro da simulação de retomada

### ACT-OPS-003 — Emitir fechamento e próximo estado

- Estado: não iniciada

- Dependência: ACT-OPS-002

- Evidência exigida: status report final

## 7. Evidências disponíveis

EVID-001

- Classe: D_INTERNO

- Descrição: registro do build concluído sem erro

- Origem: pipeline interno

- Sustenta: ACT-APP-001

- Estado sustentado: implementado

- Não sustenta: testado, verificado ou publicado

## 8. Bloqueios e lacunas

- Nenhum bloqueio confirmado para ACT-APP-002.

- Não existe evidência de teste público ou multiusuário.

- Não existem arquivos finais dos três vídeos.

- Não existe URL pública validada.

- Owner formal não determinado.

## 9. Distribuição semanal pretendida

- Dia 01 — revisar posição, preparar cenário e iniciar validação técnica

- Dia 02 — executar teste público e registrar correções

- Dia 03 — revisar roteiros e gravar demonstrações

- Dia 04 — editar vídeos e revisar landing page

- Dia 05 — publicar landing page e testar acesso

- Dia 06 — consolidar evidências e revisar pendências

- Dia 07 — validar runbook, fechar a semana e definir o próximo estado

A distribuição é uma projeção. Dependências e evidências continuam sendo a fonte da elegibilidade.

## 10. Regras obrigatórias

Preserve a estrutura:

Projeto → Entrega/Dia Lógico → Fluxo → Ação

Aplique:

1 entrega ativa → 1 fluxo ativo → 1 ação ativa

Considere que:

- Dia Lógico não é uma data;

- calendário é uma projeção;

- dependências governam elegibilidade;

- Agora/Próximo/Depois não criam objetos paralelos;

- existente ≠ completo ≠ aprovado ≠ implementado ≠ testado ≠ verificado ≠ publicado;

- “feito” não substitui evidência;

- item bloqueado não pode ser escolhido como próxima ação;

- prazo original e previsão atual são campos distintos;

- inferência não pode ser apresentada como fato.

Se houver mais de uma ação elegível, use:

1. dependências satisfeitas;

2. caminho crítico informado;

3. maior valor declarado;

4. prazo mais próximo;

5. similaridade com a ação ativa.

Se ainda houver empate, registre EXIGE_HUMANO.

## 11. Resultado esperado

Antes de renderizar:

1. construa o objeto canônico conforme schemas/output.schema.json;

2. valide hierarquia, IDs, dependências e WIP;

3. mantenha ACT-APP-002 como única ação Agora, caso permaneça elegível;

4. não promova a aplicação de implementada para testada ou verificada;

5. organize os demais objetos em Próximo e Depois;

6. gere o payload conforme schemas/prism-report.schema.json.

## 12. Arquivos obrigatórios

Crie efetivamente:

- mapa-os-PRJ-EXEC-001-W37.json;

- mapa-os-PRJ-EXEC-001-W37-prisma-payload.json;

- mapa-os-PRJ-EXEC-001-W37-prisma.html;

- mapa-os-PRJ-EXEC-001-W37-placeholders.json.

Use o template interno assets/templates/status-report-prisma-a4-v4.html.

## 13. Validação

Execute:

python scripts/validate_mapa.py mapa-os-PRJ-EXEC-001-W37.json

python scripts/render_prism.py mapa-os-PRJ-EXEC-001-W37-prisma-payload.json mapa-os-PRJ-EXEC-001-W37-prisma.html --tokens mapa-os-PRJ-EXEC-001-W37-placeholders.json

python scripts/audit_prism.py

Confirme:

- schema válido;

- WIP=1;

- dependências válidas;

- estados sustentados;

- exatamente 100 placeholders resolvidos;

- nenhum placeholder residual;

- namespaces DOC_*, EPIC_*, CALENDAR_* e RESULT_*;

- geometria 210 × 297 mm;

- três faces de 99 mm;

- HTML pronto para impressão em escala 100%.

Se algum texto exceder o limite do schema, condense sem perder IDs, datas, critérios, estados ou evidências. Não altere CSS, tipografia, grid, margens, paddings ou dimensões.

## 14. Entrega final

Comece com DOCUMENT READER · VALU-MODE V3.

Entregue os quatro arquivos para download e um relatório final PASS ou BLOCKED.

Informe:

- posição operacional;

- próxima ação;

- evidência necessária;

- bloqueios e lacunas;

- arquivos gerados;

- validações executadas;

- nível realmente alcançado.

Não responda apenas com explicações ou código no chat.

Não declare a aplicação testada ou verificada sem a evidência correspondente.

Não declare “inspecionado em impressão” sem inspeção visual ou física.
