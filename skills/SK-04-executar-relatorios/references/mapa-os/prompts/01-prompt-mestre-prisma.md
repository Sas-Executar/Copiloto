---
activation_numeric: "01"
activation_verbal: "/criar-mapa-semanal"
source_document_id: "1k9QU8SiSCcBIp5XI33EtYyGftj5-op76NB7ZEhS3uNA"
---

> Uso: roteiro mestre reutilizável para coletar os dados do usuário e gerar o Mapa-OS semanal em Prisma A4.

# PROMPT MESTRE — MAPA-OS SEMANAL EM PRISMA A4

Use a skill $executar-mapa-os para transformar as informações abaixo em um Mapa-OS de uma semana, projetado no modo Prisma A4 V4, pronto para impressão.

## 1. Objetivo da execução

Produza uma visão operacional semanal que permita:

1. reconhecer o objetivo central da semana;

2. localizar a posição atual do projeto;

3. distinguir o que está concluído, ativo, bloqueado e ainda não iniciado;

4. identificar uma única próxima ação elegível;

5. organizar o trabalho nos horizontes Agora, Próximo e Depois;

6. apresentar sete dias de execução;

7. registrar os entregáveis e as evidências necessárias;

8. gerar o HTML final do Prisma A4.

## 2. Modo solicitado

- Skill: $executar-mapa-os

- Modo operacional: EXECUTAR

- Projeção final: prisma_7d

- Período: [DATA INICIAL] a [DATA FINAL]

- Semana: [WXX]

- Timezone: [TIMEZONE]

- Idioma: português do Brasil

- Formato físico: A4 retrato

- Escala de impressão: 100%

- Geometria obrigatória: 210 × 297 mm

- Faces obrigatórias: 3 faces de 99 mm

- Template: assets/templates/status-report-prisma-a4-v4.html

## 3. Fonte de verdade

Use somente:

- os dados escritos neste prompt;

- os documentos anexados nesta conversa;

- as evidências explicitamente indicadas;

- as regras e os arquivos internos da skill.

Não transforme exemplos internos da skill em fatos deste projeto.

Não invente owner, datas, capacidade, progresso, dependências, entregáveis, estados ou evidências.

Quando uma informação não estiver disponível, registre NAO_DETERMINADO.

Pergunte somente quando a ausência impedir obrigatoriamente a geração do relatório.

## 4. Regras operacionais obrigatórias

Preserve a estrutura:

Projeto → Entrega/Dia Lógico → Fluxo → Ação

Aplique WIP operacional:

1 entrega ativa → 1 fluxo ativo → 1 ação ativa

Considere que:

- Dia Lógico é uma entrega, não uma data;

- calendário é apenas uma projeção;

- passagem do tempo não altera o estado;

- dependências governam a elegibilidade;

- Agora/Próximo/Depois não criam objetos paralelos;

- existente ≠ completo ≠ aprovado ≠ implementado ≠ testado ≠ verificado ≠ publicado;

- a afirmação “feito” não substitui evidência;

- prazo original e previsão atual são campos diferentes;

- item bloqueado não pode ser selecionado como próxima ação;

- inferência não pode ser apresentada como fato observado.

Se houver mais de uma ação elegível, use esta ordem:

1. dependências satisfeitas;

2. caminho crítico informado;

3. maior valor declarado;

4. prazo mais próximo;

5. similaridade com a ação ativa.

Se ainda houver empate, não escolha arbitrariamente. Registre EXIGE_HUMANO.

## 5. Dados do projeto

### Identidade

- Projeto: [NOME DO PROJETO]

- ID do projeto: [PROJECT_ID]

- Owner: [OWNER OU NÃO DETERMINADO]

- Objetivo final: [OBJETIVO FINAL]

- Estado atual: [ESTADO SUPORTADO]

- Período da semana: [PERÍODO]

### Problema

[PROBLEMA QUE A SEMANA DEVE RESOLVER]

### Processo

[MÉTODO, ROTINA OU ESTRATÉGIA DE EXECUÇÃO]

### Progresso sustentado

[O QUE JÁ EXISTE, FOI IMPLEMENTADO, TESTADO OU VERIFICADO]

### Capacidade

- Segunda: [HORAS]

- Terça: [HORAS]

- Quarta: [HORAS]

- Quinta: [HORAS]

- Sexta: [HORAS]

- Sábado: [HORAS]

- Domingo: [HORAS]

- Restrições fixas: [RESTRIÇÕES]

### Entregas, fluxos e ações

Para cada objeto, informe:

- ID;

- nível: entrega, fluxo ou ação;

- título;

- parent ID;

- estado;

- dependências;

- critério de conclusão;

- evidência exigida;

- prazo original;

- previsão atual;

- bloqueios;

- valor ou prioridade, quando houver.

Dados:

[COLE AQUI AS ENTREGAS, FLUXOS E AÇÕES]

### Evidências disponíveis

[LISTE ID, DESCRIÇÃO, ORIGEM E OBJETO SUSTENTADO]

### Bloqueios e conflitos

[LISTE OS BLOQUEIOS, CONFLITOS OU LACUNAS]

### Rotina ou distribuição desejada

[DESCREVA A ROTINA SEMANAL, CASO EXISTA]

## 6. Construção do Mapa-OS

Antes de renderizar:

1. inventarie as fontes;

2. classifique norma, plano, decisão, status, evidência, template e exemplo;

3. construa o objeto canônico conforme schemas/output.schema.json;

4. valide IDs, pais e dependências;

5. valide WIP=1;

6. valide evidências e estados;

7. determine a posição atual;

8. selecione uma única próxima ação;

9. organize Agora, Próximo e Depois;

10. distribua os objetos pelos sete dias sem alterar a estrutura canônica.

## 7. Construção do Prisma

Gere um payload conforme schemas/prism-report.schema.json.

O Prisma deve conter:

### Face 01 — Épica

- uma épica semanal;

- intenção;

- progresso sustentado;

- exatamente quatro KPIs.

### Face 02 — Execução

- exatamente sete dias;

- número, dia da semana, data, título, foco e tracks;

- dias 01–06 com até dois tracks visíveis;

- dia 07 com até três tracks;

- nenhuma lista extensa ou parágrafo dentro dos cartões.

### Face 03 — Resultado

- um entregável principal;

- exatamente quatro entregáveis de apoio;

- estado sustentado de cada entregável;

- próximo estado operacional;

- rastreabilidade curta.

Se faltarem dados para algum campo obrigatório, não invente. Registre a lacuna e solicite somente a informação necessária.

## 8. Política de texto e fit

Se algum texto exceder o limite do schema:

1. remova redundância;

2. use substantivos e verbos precisos;

3. preserve IDs, datas, quantidades, critérios, milestones e estados;

4. mova detalhes do título para a descrição;

5. retorne erro de fit se a condensação causar perda semântica.

Nunca altere:

- CSS;

- tipografia;

- margens;

- paddings;

- grid;

- dimensões;

- altura das faces;

- namespaces dos placeholders.

## 9. Arquivos obrigatórios

Crie efetivamente:

1. mapa-os-[PROJECT_ID]-[WXX].json

Objeto canônico validado.

2. mapa-os-[PROJECT_ID]-[WXX]-prisma-payload.json

Payload conforme o schema Prisma.

3. mapa-os-[PROJECT_ID]-[WXX]-prisma.html

HTML final preenchido e pronto para impressão.

4. mapa-os-[PROJECT_ID]-[WXX]-placeholders.json

Mapa dos 100 placeholders resolvidos.

Não entregue apenas instruções, pseudocódigo ou HTML dentro da resposta. Entregue os arquivos para download.

## 10. Validações obrigatórias

Execute:

python scripts/validate_mapa.py mapa-os-[PROJECT_ID]-[WXX].json

python scripts/render_prism.py mapa-os-[PROJECT_ID]-[WXX]-prisma-payload.json mapa-os-[PROJECT_ID]-[WXX]-prisma.html --tokens mapa-os-[PROJECT_ID]-[WXX]-placeholders.json

python scripts/audit_prism.py

Confirme:

- schema válido;

- WIP válido;

- dependências válidas;

- estados sustentados;

- evidências rastreáveis;

- exatamente 100 placeholders;

- nenhum placeholder residual;

- somente namespaces DOC_*, EPIC_*, CALENDAR_* e RESULT_*;

- geometria A4 preservada;

- três faces de 99 mm preservadas.

## 11. Resposta final

Comece com DOCUMENT READER · VALU-MODE V3.

Informe:

- posição operacional;

- única próxima ação;

- evidência necessária;

- bloqueios ou lacunas;

- arquivos gerados;

- resultado da validação;

- nível realmente alcançado: criado, validado ou renderizado.

Não declare “inspecionado em impressão” sem inspeção visual ou física correspondente.
