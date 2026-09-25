> Texto extraído automaticamente de `DOC-PRM-001-prompt-mestre-pre-preenchimento.docx` (fonte original preservada ao lado).

PROMPT MESTRE — PRÉ-PREENCHIMENTO DOCUMENTAL DO ECOSSISTEMA

A estrutura abaixo transforma o agente em um pré-preenchedor documental determinístico. Ela cobre as 23 áreas, os 23 documentos macro e os 14 documentos especializados já definidos, totalizando 37 documentos, com rastreabilidade campo a campo e sem completar lacunas por inferência silenciosa.

PROMPT MESTRE — PRÉ-PREENCHIMENTO DOCUMENTAL DO ECOSSISTEMA

prompt_contract:

id: "EXECUTAR-DOC-PREFILL-001"

version: "1.0"

area: "Governança Documental"

workflow: "Discovery > Evidence > Classification > Prefill > Conflict Resolution > Validation > Master Index"

owner: "A_DEFINIR"

status: "READY_FOR_EXECUTION"

automation_level: "A4"

objective:

primary: >

Ler integralmente o corpus documental disponível e realizar o

pré-preenchimento rastreável de todos os documentos canônicos

D01-D23 do Ecossistema Product Launch.

result: >

Entregar cada documento com todos os seus campos preenchidos

quando houver evidência, explicitamente marcados como A_DEFINIR

quando a informação não existir, e como CONFLITO quando houver

fontes incompatíveis.

prohibition:

- "Não inventar conteúdo."

- "Não preencher lacunas com conhecimento genérico."

- "Não transformar recomendação em decisão existente."

- "Não transformar documento existente em evidência de implementação."

- "Não tratar PRE_PREENCHIDO como APROVADO."

- "Não alterar IDs canônicos existentes."

corpus:

primary_root: "Ecosistema Product Launch"

governance_sources:

- "GOVERNANCA"

- "GOV-SPEC-20260907-001__relatorio-integral-organizado__v01.md"

- "00__governanca-e-schema/00_INDICE_EXTRACOES.csv"

- "00__governanca-e-schema/00_governanca-docx.csv"

- "00__governanca-e-schema/00_readme-governanca.csv"

precedence:

- priority: 1

source: "Fonte original ou documento canônico mais recente"

- priority: 2

source: "Documento macro/especializado da própria área"

- priority: 3

source: "Registros extraídos da área"

- priority: 4

source: "Documentos de áreas relacionadas"

- priority: 5

source: "Inferência formal explicitamente marcada DERIVED"

external_research:

allowed: true

rule: >

Pesquisa externa pode complementar requisitos legais, técnicos,

científicos ou de mercado, mas nunca substituir evidência interna

sobre decisões, estado, owner, orçamento, implementação ou aprovação.

external_content_status: "EXTERNAL_EVIDENCE"

canonical_hierarchy:

structure:

- "ECOSSISTEMA"

- "AREA_D01_D23"

- "DOCUMENTO_MACRO"

- "DOCUMENTO_ESPECIALIZADO"

- "WORKFLOW"

- "ENTREGAVEL"

- "TAREFA"

- "ACAO"

- "EVIDENCIA"

- "REGISTRO"

document_count:

macro_documents: 23

specialized_documents_defined: 14

total_documents_in_scope: 37

epistemic_model:

classes:

DIRECT:

definition: "Informação explicitamente registrada em fonte."

DERIVED:

definition: >

Conclusão necessária derivada de duas ou mais evidências

existentes, sem introduzir requisito externo.

EXTERNAL_EVIDENCE:

definition: "Informação proveniente de fonte externa identificada."

PROPOSED:

definition: >

Proposta nova produzida pelo agente. Nunca tratar como estado atual.

GAP:

definition: "Informação necessária, mas não encontrada."

CONFLICT:

definition: "Duas ou mais fontes apresentam valores incompatíveis."

field_status:

allowed:

- "FOUND"

- "DERIVED"

- "EXTERNAL"

- "CONFLICT"

- "NOT_FOUND"

not_found_value: "A_DEFINIR"

implementation_states:

allowed:

- "IDENTIFICADO"

- "PRE_PREENCHIDO"

- "ESPECIFICADO"

- "APROVADO"

- "EM_DESENVOLVIMENTO"

- "IMPLEMENTADO"

- "TESTADO"

- "VERIFICADO"

- "LIBERADO"

- "PUBLICADO"

rule: >

Nunca promover o estado apenas porque existe um arquivo ou texto.

O trabalho deste workflow termina em PRE_PREENCHIDO,

salvo evidência explícita de estado superior.

universal_field_contract:

required_for_every_field:

value: "valor encontrado ou A_DEFINIR"

status: "FOUND | DERIVED | EXTERNAL | CONFLICT | NOT_FOUND"

epistemic_class: "DIRECT | DERIVED | EXTERNAL_EVIDENCE | PROPOSED | GAP | CONFLICT"

confidence: "alta | media | baixa | n/a"

source_id: "arquivo/documento de origem"

source_locator: "seção, linha, aba, página, registro ou outro localizador"

evidence_excerpt: "síntese curta da evidência"

conflicting_sources: []

notes: ""

rule: >

Nenhum valor diferente de A_DEFINIR pode existir sem source_id

e source_locator, exceto conteúdo explicitamente marcado PROPOSED.

document_metadata:

required:

document_id: ""

document_name: ""

acronym: ""

domain_id: ""

domain_name: ""

version: "PREFILL-0.1"

owner: "A_DEFINIR"

document_status: "PRE_PREENCHIDO"

approval_status: "PENDENTE"

implementation_status: "NAO_PRESUMIR"

source_count: 0

evidence_coverage_percent: 0

conflict_count: 0

gap_count: 0

depends_on: []

blocks: []

source_files: []

last_verified_at: ""

INSTRUÇÃO OPERACIONAL AO AGENTE

Execute o processo abaixo sem solicitar ao usuário informações que possam ser recuperadas do corpus.

Primeiro, inventarie as fontes disponíveis e identifique para cada documento canônico quais fontes podem fornecer evidência.

Depois, processe uma área por vez, em ordem D01 → D23.

Para cada documento:

crie sua estrutura integral;

procure evidências para cada campo;

preencha somente o que estiver sustentado;

marque informação ausente como A_DEFINIR;

registre divergências como CONFLICT;

mantenha recomendações como PROPOSED;

calcule cobertura documental;

registre dependências;

gere lista consolidada de gaps;

gere evidência de rastreabilidade.

Não interrompa o workflow porque um campo está ausente.

A_DEFINIR é um resultado válido.

D01 — GESTÃO EMPRESARIAL

D01:

area_name: "Gestão Empresarial"

D01-DOC-DDE-001:

acronym: "DDE"

name: "Documento de Direção Empresarial"

purpose: "Fonte executiva principal de direção, identidade e governança empresarial."

required_sections:

identity:

fields:

- nome_do_ecossistema

- descricao_executiva

- contexto

- razao_de_existencia

- fase_atual

problem_and_opportunity:

fields:

- problema_central

- problemas_secundarios

- oportunidade

- evidencias_do_problema

purpose:

fields:

- proposito

- missao

- visao

- principios

- valores

strategic_direction:

fields:

- objetivos_estrategicos

- resultados_esperados

- prioridades

- nao_objetivos

- horizonte_temporal

ecosystem:

fields:

- produtos

- servicos

- marcas

- agentes

- plataformas

- unidades_de_negocio

governance:

fields:

- modelo_de_governanca

- papeis_decisorios

- direitos_de_decisao

- gates

- mecanismos_de_controle

stakeholders:

fields:

- stakeholders

- interesse

- influencia

- relacionamento

strategic_dependencies:

fields:

- dependencias

- restricoes

- premissas

risks:

fields:

- riscos_estrategicos

- mitigacoes_existentes

measurement:

fields:

- indicadores

- metas

- criterios_de_sucesso

decisions:

fields:

- decisoes_vigentes

- decisoes_pendentes

D01-DOC-TAP-001:

acronym: "TAP"

name: "Termo de Abertura do Ecossistema"

purpose: "Formalizar a autorização e os limites do programa/projeto."

required_sections:

identification:

fields:

- titulo

- justificativa

- contexto

- sponsor

- owner

objective:

fields:

- objetivo_geral

- objetivos_especificos

- resultado_final_esperado

scope:

fields:

- escopo_incluido

- escopo_excluido

- fronteiras

deliverables:

fields:

- entregaveis_principais

- definition_of_done

milestones:

fields:

- marcos

- datas_existentes

stakeholders:

fields:

- participantes

- papeis

- responsabilidades

constraints:

fields:

- restricoes

- premissas

- dependencias

resources:

fields:

- capacidade

- recursos

- orcamento

success:

fields:

- criterios_de_aceite

- indicadores_de_sucesso

risks:

fields:

- riscos_iniciais

approvals:

fields:

- aprovadores

- status_aprovacao

D01-DOC-MNE-001:

acronym: "MNE"

name: "Modelo de Negócio do Ecossistema"

required_sections:

customer:

fields:

- segmentos

- usuarios

- clientes

- problemas

- jtbd

value:

fields:

- propostas_de_valor

- beneficios

- diferenciadores

- alternativas_existentes

offerings:

fields:

- produtos

- servicos

- planos

- ofertas

channels:

fields:

- aquisicao

- distribuicao

- entrega

relationships:

fields:

- relacionamento_com_cliente

- comunidade

- suporte

revenue:

fields:

- fontes_de_receita

- precificacao

- recorrencia

costs:

fields:

- estrutura_de_custos

- capex

- opex

resources:

fields:

- recursos_chave

- capacidades_chave

activities:

fields:

- atividades_chave

partners:

fields:

- parceiros

- fornecedores

economics:

fields:

- margem

- cac

- ltv

- break_even

assumptions:

fields:

- hipoteses

- validacoes_pendentes

D01-DOC-MRE-001:

acronym: "MRE"

name: "Mapa de Relações do Ecossistema"

required_sections:

nodes:

fields:

- componentes

- produtos

- servicos

- agentes

- plataformas

relationships:

fields:

- origem

- destino

- tipo_de_relacao

- objetivo

flows:

fields:

- fluxo_de_valor

- fluxo_de_dados

- fluxo_de_conhecimento

- fluxo_comercial

- fluxo_de_feedback

interfaces:

fields:

- entradas

- saidas

- handoffs

dependencies:

fields:

- dependencias

- gargalos

loops:

fields:

- ciclos_de_aprendizado

- retroalimentacao

risks:

fields:

- falhas_de_integracao

- pontos_unicos_de_falha

D02 — JURÍDICO, RISCOS E CONFORMIDADE

D02:

D02-DOC-DGRC-001:

acronym: "DGRC"

name: "Documento de Governança, Riscos e Conformidade"

required_sections:

governance: [estrutura_juridica, papeis, autoridades, politicas]

obligations: [leis_aplicaveis, regulamentos, obrigacoes, licencas]

contracts: [contratos_existentes, contratos_necessarios, obrigacoes_contratuais]

privacy: [dados_pessoais, finalidades, bases_legais, direitos, retencao]

intellectual_property: [marcas, direitos_autorais, software, licencas]

risk_management: [riscos, controles, owners, resposta]

compliance: [controles, auditorias, evidencias, periodicidade]

incidents: [eventos_reportaveis, resposta, escalacao]

approvals: [aprovadores, gates_juridicos]

D02-DOC-MRC-001:

acronym: "MRC"

name: "Matriz de Riscos e Controles"

record_schema:

- risk_id

- categoria

- ativo_processo_afetado

- evento_de_risco

- causa

- impacto

- probabilidade

- severidade

- risco_inerente

- controles_existentes

- efetividade_controle

- risco_residual

- resposta

- owner

- trigger

- prazo

- evidencia

- status

D02-DOC-PPT-001:

acronym: "PPT"

name: "Política de Privacidade e Termos"

required_sections:

organization: [controlador, operador, contato]

collected_data: [categorias_de_dados, origem]

purposes: [finalidade, base_legal]

sharing: [terceiros, operadores, transferencia]

storage: [retencao, exclusao]

rights: [direitos_do_titular, canal_de_solicitacao]

cookies: [cookies, analytics, preferencias]

security: [medidas_de_seguranca]

terms: [elegibilidade, uso_permitido, uso_proibido]

liability: [limitacoes, responsabilidades]

ip: [propriedade_intelectual]

termination: [suspensao, encerramento]

updates: [alteracoes_da_politica]

D03 — FINANÇAS

D03:

D03-DOC-PFO-001:

acronym: "PFO"

name: "Plano Financeiro e Orçamentário"

required_sections:

assumptions: [premissas_financeiras, periodo, moeda]

revenue: [fontes, previsoes, recorrencia]

capex: [item, valor, periodo, justificativa]

opex: [categoria, valor, periodicidade]

budget: [orcamento_por_area, limite, realizado]

cashflow: [entradas, saidas, saldo]

runway: [caixa_disponivel, burn_rate, meses]

financing: [capital_proprio, divida, investimento]

pricing: [precos, descontos, impostos]

scenarios: [base, otimista, conservador]

controls: [aprovacao_de_gastos, conciliacao]

indicators: [receita, margem, burn, runway, resultado]

D03-DOC-MFO-001:

acronym: "MFO"

name: "Modelo Financeiro do Ecossistema"

required_sections:

model_inputs: [premissas, drivers]

revenue_model: [produto, unidade, volume, preco]

cost_model: [fixos, variaveis]

pnl: [receita, custos, margem, despesas, resultado]

cashflow: [operacional, investimento, financiamento]

unit_economics: [cac, ltv, arpu, churn, margem]

break_even: [ponto_de_equilibrio]

sensitivity: [variaveis_criticas, impacto]

scenarios: [cenario, premissas, resultado]

D04 — PESSOAS E RECURSOS HUMANOS

D04:

D04-DOC-PPC-001:

acronym: "PPC"

name: "Plano de Pessoas e Capacidade"

required_sections:

organization: [estrutura, equipes, funcoes]

roles: [papel, responsabilidades, autoridade]

raci: [atividade, responsavel, aprovador, consultado, informado]

people: [pessoa, funcao, disponibilidade]

competencies: [competencia, nivel, necessidade]

capacity: [horas_disponiveis, capacidade_liquida, restricoes]

workload: [demanda, capacidade, deficit]

gaps: [lacuna, impacto, prioridade]

hiring: [necessidades_futuras, perfil]

onboarding: [entrada, treinamento, acesso]

development: [formacao, capacitacao]

continuity: [dependencia_de_pessoa, substituicao]

metrics: [utilizacao, capacidade, turnover, gaps]

D05 — DADOS

D05:

D05-DOC-EPGD-001:

acronym: "EPGD"

name: "Estratégia e Plano de Gestão de Dados"

required_sections:

data_domains: [dominio, descricao, owner]

sources: [fonte, sistema, origem]

ingestion: [metodo, frequencia]

storage: [banco, repositorio, formato]

schemas: [schema, versao, contrato]

quality: [completude, validade, consistencia, unicidade]

lineage: [origem, transformacoes, destino]

access: [perfil, permissao]

security: [classificacao, protecao]

privacy: [dados_pessoais, finalidade]

lifecycle: [criacao, uso, retencao, descarte]

analytics: [datasets, indicadores]

governance: [owners, stewards, aprovacao]

D05-DOC-DCM-001:

acronym: "DCM"

name: "Dicionário de Dados e Catálogo de Métricas"

record_schema:

- metric_or_field_id

- nome

- tipo

- definicao

- formula

- unidade

- granularidade

- fonte

- tabela_dataset

- campo_evento

- dimensoes

- owner

- frequencia

- freshness

- regra_de_qualidade

- classificacao

- retencao

- consumidores

D06 — CONHECIMENTO E BUSCA CORPORATIVA

D06:

D06-DOC-EGC-001:

acronym: "EGC"

name: "Estratégia de Gestão do Conhecimento"

required_sections:

taxonomy: [dominios, subareas, classes_documentais]

ontology: [objetos, relacoes]

repositories: [repositorio, finalidade, owner]

sources_of_truth: [objeto, fonte_canonica]

identity: [padrao_de_ids, naming]

versioning: [versao, historico, supersede]

ingestion: [entrada, classificacao, processamento]

retrieval: [busca, filtros, indexacao]

curation: [revisao, aprovacao]

archival: [arquivamento, descarte]

crosslinking: [relacoes_entre_documentos]

governance: [owner, estado, evidencia]

D06-DOC-RMI-001:

acronym: "RMI"

name: "Registro Mestre de Identidades"

record_schema:

- canonical_id

- object_type

- domain_id

- subarea_id

- parent_id

- canonical_name

- aliases

- version

- status

- owner

- source

- evidence

- repository

- location

- depends_on

- blocks

- supersedes

- created_at

- updated_at

D07 — PRODUTIVIDADE E EXECUÇÃO

D07:

D07-DOC-PEX-001:

acronym: "PEX"

name: "Plano de Execução"

required_sections:

objectives: [objetivo, resultado]

deliverables: [entregavel, dod, evidencia]

portfolio: [projeto, prioridade, estado]

dependencies: [upstream, downstream]

capacity: [capacidade_bruta, fixa, liquida]

wip: [limite, trabalho_ativo]

backlog: [item, prioridade, elegibilidade]

schedule: [ciclo, data, marco]

gates: [gate, criterio, evidencia]

risks: [bloqueio, impacto, resposta]

verification: [criterio_de_aceite, evidencia]

progress: [planejado, realizado, restante]

D07-DOC-PIM-001:

acronym: "PIM"

name: "Plano de Implementação e Marcos"

required_sections:

implementation_strategy: [abordagem, ondas]

milestones: [marco, resultado, criterio]

work_packages: [pacote, entregavel]

dependencies: [dependencia, precondicao]

resources: [pessoa, sistema, recurso]

schedule: [inicio, fim, ciclo]

gates: [gate, entrada, saida]

rollout: [piloto, expansao]

handoff: [origem, destino, contrato]

verification: [teste, evidencia]

rollback: [condicao, procedimento]

D08 — OPERAÇÕES

D08:

D08-DOC-MOP-001:

acronym: "MOP"

name: "Manual de Operações"

required_sections:

operating_model: [servicos, processos]

process_inventory: [processo, objetivo, owner]

inputs: [entrada, origem]

procedures: [etapas, regra]

outputs: [saida, consumidor]

roles: [executor, aprovador]

controls: [controle, frequencia]

sla: [servico, meta]

handoffs: [origem, destino]

incidents: [tipo, resposta]

continuity: [backup, contingencia]

metrics: [volume, tempo, erro, qualidade]

D08-DOC-RUN-001:

acronym: "RUN"

name: "Runbook Operacional do Ecossistema"

runbook_schema:

- runbook_id

- nome

- objetivo

- trigger

- precondicoes

- sistemas

- credenciais_necessarias

- passos

- resultado_esperado

- verificacao

- evidencia

- excecoes

- rollback

- escalacao

- owner

- frequencia

D09 — PESQUISA E INOVAÇÃO

D09:

D09-DOC-PPE-001:

acronym: "PPE"

name: "Plano de Pesquisa e Experimentação"

required_sections:

question: [pergunta_de_pesquisa]

hypothesis: [hipotese, pressupostos]

evidence_review: [fontes_existentes, lacunas]

method: [metodo, desenho]

population: [publico, amostra]

variables: [independente, dependente, controle]

protocol: [procedimento]

experiment: [intervencao, comparacao]

measurement: [metricas, instrumentos]

analysis: [metodo_de_analise]

criteria: [sucesso, falha, inconclusivo]

results: [resultado, limitacoes]

decision: [decisao_derivada]

D09-DOC-DEB-001:

acronym: "DEB"

name: "Dossiê de Evidências e Base Científica"

record_schema:

- claim_id

- claim

- domain

- evidence_class

- source_id

- source_type

- citation

- locator

- publication_date

- population

- finding

- limitation

- contradictory_evidence

- supported_documents

- confidence

- status

D10 — GESTÃO DE PRODUTO

D10:

D10-DOC-DRP-001:

acronym: "DRP"

name: "Documento de Requisitos de Produto"

required_sections:

problem: [problema, evidencia, impacto]

audience: [usuarios, clientes, icp]

jtbd: [situacao, trabalho, outcome]

value: [proposta_de_valor]

goals: [objetivos, metricas]

scope: [incluido, excluido]

capabilities: [capacidade, beneficio]

requirements: [funcionais, nao_funcionais]

journeys: [jornadas, fluxos]

constraints: [restricoes]

dependencies: [dependencias]

acceptance: [criterios_de_aceite]

roadmap: [agora, proximo, depois]

risks: [risco, mitigacao]

D10-DOC-PRD-001:

acronym: "PRD"

name: "Requisitos Integrados dos Produtos"

product_schema:

- product_id

- product_name

- problem

- target_user

- jtbd

- goals

- non_goals

- use_cases

- user_stories

- functional_requirements

- non_functional_requirements

- user_flows

- states

- edge_cases

- integrations

- data_requirements

- analytics

- security

- privacy

- accessibility

- acceptance_criteria

- dependencies

- release_criteria

D11 — EXPERIÊNCIA E PROJETO

D11:

D11-DOC-EEP-001:

acronym: "EEP"

name: "Especificação de Experiência e Projeto"

required_sections:

user_research: [evidencias, necessidades]

personas: [perfil, contexto]

journeys: [etapa, acao, friccao]

information_architecture: [navegacao, hierarquia]

flows: [entrada, decisao, saida]

interaction: [comportamento, feedback]

states: [loading, vazio, erro, sucesso]

content: [microcopy, orientacao]

responsive: [mobile, tablet, desktop]

accessibility: [teclado, contraste, semantica, movimento]

prototype: [artefato, status]

validation: [teste, resultado]

D11-DOC-DSI-001:

acronym: "DSI"

name: "Sistema de Design e Interface"

required_sections:

foundations: [principios]

tokens: [cor, tipografia, espacamento, raio, sombra]

grid: [breakpoints, colunas]

components: [componente, variante, estado]

patterns: [navegacao, formulario, feedback]

icons: [biblioteca, regras]

motion: [duracao, easing, reduced_motion]

accessibility: [wcag, foco, contraste]

content_design: [voz, tom, nomenclatura]

governance: [versao, owner, contribuicao]

engineering_handoff: [package, tokens, storybook]

D12 — ENGENHARIA

D12:

D12-DOC-ETE-001:

acronym: "ETE"

name: "Especificação Técnica de Engenharia"

required_sections:

architecture: [visao_geral, diagramas]

repositories: [repositorio, branch, finalidade]

stack: [frameworks, linguagens, runtime]

applications: [app, responsabilidade]

packages: [package, responsabilidade]

interfaces: [api, eventos, webhooks]

data: [banco, schema, migracoes]

authentication: [auth, autorizacao]

integrations: [servico, contrato]

infrastructure: [hosting, storage, network]

environments: [local, preview, staging, production]

cicd: [build, test, deploy]

observability: [logs, metrics, errors]

performance: [budgets, limites]

security: [secrets, headers, rate_limit]

testing: [unitario, integracao, e2e]

deployment: [processo, release]

rollback: [condicao, procedimento]

adr_links: [decisoes_arquiteturais]

D13 — MERCADO E GERAÇÃO DE DEMANDA

D13:

D13-DOC-DRM-001:

acronym: "DRM"

name: "Documento de Requisitos de Mercado"

required_sections:

market: [definicao, tamanho, tendencia]

segments: [segmento, necessidade]

icp: [perfil, criterios, exclusoes]

demand: [sinais, problemas, procura]

alternatives: [concorrentes, substitutos]

positioning: [categoria, diferenciacao]

messaging: [problema, promessa, prova]

channels: [organico, pago, parceria]

acquisition: [estrategias]

pricing_signals: [disposicao_a_pagar, benchmarks]

evidence: [fontes, estudos]

risks: [riscos_de_mercado]

D13-DOC-GTM-001:

acronym: "GTM"

name: "Plano de Entrada no Mercado e Lançamento"

required_sections:

objectives: [objetivo_de_lancamento]

audience: [icp, segmentos]

positioning: [posicionamento, mensagem]

offer: [produto, plano, preco]

channels: [canal, funcao]

content: [ativos, campanha]

funnel: [awareness, consideration, conversion, retention]

campaign: [fase, atividade, ativo]

launch: [pre_launch, launch, post_launch]

sales_handoff: [marketing_para_vendas]

support_readiness: [atendimento, faq]

analytics: [metricas, eventos]

budget: [investimento]

experiments: [hipotese, teste]

gates: [go_no_go, criterio]

D14 — VENDAS

D14:

D14-DOC-PCV-001:

acronym: "PCV"

name: "Plano Comercial e de Vendas"

required_sections:

customer: [icp, segmentos]

offers: [produto, pacote]

pricing: [preco, desconto]

qualification: [criterios, scoring]

funnel: [lead, mql, sql, proposta, ganho]

process: [etapas, owner]

scripts: [abertura, descoberta, fechamento]

discovery: [perguntas, necessidades]

objections: [objecao, resposta]

proposals: [template, requisitos]

crm: [sistema, campos, etapas]

pipeline: [valor, probabilidade]

forecast: [periodo, receita]

targets: [quota, conversao]

handoff: [contrato, onboarding, customer_success]

metrics: [win_rate, ciclo, ticket]

D15 — ATENDIMENTO E SUCESSO DO CLIENTE

D15:

D15-DOC-PASC-001:

acronym: "PASC"

name: "Plano de Atendimento e Sucesso do Cliente"

required_sections:

service_model: [modelo, segmentos]

onboarding: [etapas, objetivo]

channels: [email, chat, outros]

service_hours: [horarios]

sla: [prioridade, prazo]

knowledge_base: [artigos, faq]

ticketing: [classificacao, fluxo]

escalation: [nivel, responsavel]

success_plan: [objetivo_do_cliente, marco]

health_score: [indicadores]

feedback: [coleta, tratamento]

satisfaction: [csat, nps]

retention: [renovacao, expansao]

churn: [sinais, resposta]

incident_communication: [mensagem, canal]

metrics: [tempo_resposta, resolucao, churn]

D16 — MÍDIAS SOCIAIS E DISTRIBUIÇÃO/ESTRATÉGIA

D16:

D16-DOC-PEM-001:

acronym: "PEM"

name: "Plano Estratégico de Mídias Sociais"

aliases:

- "Mídias Sociais e Distribuição Digital"

- "Mídias Sociais e Estratégias"

required_sections:

objectives: [objetivos]

audience: [publicos]

channels: [canal, funcao]

content_pillars: [pilar, tese]

formats: [artigo, video, carrossel, story, newsletter]

editorial_calendar: [data, tema, canal]

production: [pesquisa, texto, visual, revisao]

repurposing: [fonte, derivados]

distribution: [organico, comunidade, parceria]

cta: [cta, destino]

community: [resposta, moderacao]

measurement: [alcance, engajamento, clique, conversao]

governance: [owner, aprovacao]

brand_compliance: [voz, visual, claims]

D17 — EMPREGO E PORTFÓLIO

D17:

D17-DOC-PEP-001:

acronym: "PEP"

name: "Plano de Emprego e Portfólio"

required_sections:

objective: [objetivo_profissional, horizonte]

positioning: [proposta_profissional, especialidades]

target: [cargos, empresas, clientes, mercados]

competencies: [competencias, nivel, evidencia]

gaps: [lacuna, plano_de_desenvolvimento]

portfolio_inventory: [projeto, papel, resultado]

case_studies: [problema, acao, resultado, evidencia]

credentials: [formacao, certificacao]

assets: [curriculo, linkedin, site, portfolio]

applications: [oportunidade, status]

outreach: [contato, canal, proxima_acao]

interviews: [empresa, etapa, preparacao]

roadmap: [marcos, datas]

metrics: [aplicacoes, entrevistas, conversao]

D18 — CONTRATOS E SCHEMAS

D18:

D18-DOC-PCE-001:

acronym: "PCE"

name: "Plano de Contratos e Esquemas"

aliases:

- "Contratos e Esquemas"

- "Contratos e Schemas"

required_sections:

contract_inventory: [contrato, tipo, owner]

document_schemas: [documento, schema]

data_contracts: [producer, consumer, payload]

api_contracts: [endpoint, request, response]

event_contracts: [evento, propriedades]

workflow_contracts: [entrada, saida, gate]

handoff_contracts: [origem, destino, requisitos]

validation: [schema_validator, regra]

versioning: [versao, compatibilidade]

change_control: [mudanca, aprovacao]

registry: [id, localizacao]

testing: [contract_test, resultado]

deprecation: [objeto, prazo, substituto]

D19 — ASSETS E CTAs

D19:

D19-DOC-PAC-001:

acronym: "PAC"

name: "Plano de Assets e CTAs"

required_sections:

asset_inventory: [asset_id, nome, tipo]

purpose: [objetivo, campanha, produto]

source: [origem, documento_fonte]

format: [arquivo, dimensao, canal]

content: [headline, copy, visual]

variants: [variante, uso]

cta_catalog: [cta_id, texto, acao]

destination: [url, deep_link, formulario]

placement: [pagina, componente, canal]

tracking: [utm, evento, campanha]

accessibility: [alt_text, legibilidade]

ownership: [owner, aprovador]

status: [draft, aprovado, publicado]

reuse: [ativo_fonte, derivados]

D20 — PLATAFORMAS E REPOSITÓRIOS

D20:

D20-DOC-PPR-001:

acronym: "PPR"

name: "Plano de Plataformas e Repositórios"

required_sections:

systems: [plataforma, finalidade]

accounts: [conta, organizacao]

repositories: [repo, owner, finalidade]

branches: [branch, funcao, protecao]

directories: [path, responsabilidade]

environments: [local, preview, staging, production]

deployments: [app, plataforma, url, status]

domains: [dominio, destino]

integrations: [origem, destino, metodo]

permissions: [sistema, perfil, acesso]

secrets: [secret_name, localizacao_sem_valor]

source_of_truth: [objeto, repositorio]

backups: [objeto, estrategia]

recovery: [procedimento, rto, rpo]

maintenance: [rotina, owner]

D21 — WORKBOOK

D21:

D21-DOC-PWB-001:

acronym: "PWB"

name: "Plano de Workbooks"

required_sections:

workbook_catalog: [workbook_id, nome]

purpose: [objetivo, usuario]

source_data: [fonte, atualizacao]

sheets: [aba, finalidade]

fields: [campo, definicao]

formulas: [formula, logica]

inputs: [entrada, tipo]

outputs: [relatorio, indicador]

validation: [regra, erro]

visualization: [grafico, tabela]

printing: [formato, area_segura]

automation: [trigger, processo]

ownership: [owner, aprovador]

versioning: [versao, alteracao]

evidence: [fonte, rastreabilidade]

D22 — DECISION AND REGISTER LOG

D22:

D22-DOC-DRL-001:

acronym: "DRL"

name: "Decision and Register Log do Ecossistema"

decision_record_schema:

- decision_id

- title

- domain

- context

- problem

- decision_required

- options_considered

- evaluation_criteria

- selected_option

- rationale

- evidence

- owner

- decision_date

- effective_date

- status

- dependencies

- blocks

- consequences

- risks

- reversibility

- review_date

- supersedes

- superseded_by

register_types:

- decisions

- assumptions

- conflicts

- gaps

- risks

- issues

- changes

- approvals

- releases

- lessons_learned

D23 — BLUEPRINTS

D23:

D23-DOC-PBL-001:

acronym: "PBL"

name: "Plano de Blueprints"

required_sections:

blueprint_catalog: [blueprint_id, nome, dominio]

problem: [problema, evidencia]

objective: [resultado_esperado]

scope: [incluido, excluido]

architecture: [componentes, relacoes]

workflow: [entrada, etapas, saida]

user_flow: [ator, acao, estado]

data: [entidades, eventos]

interfaces: [api, ui, integracao]

dependencies: [tecnicas, operacionais]

constraints: [tecnicas, legais, ux]

contracts: [schemas, interfaces]

acceptance: [criterios]

prototype: [artefato, localizacao]

implementation: [repositorio, pacote, rota]

tests: [teste, resultado]

release_mapping: [release, gate]

evidence: [fontes, registros]

REGRAS DE PRÉ-PREENCHIMENTO

prefill_rules:

extraction:

- >

Para cada campo, procurar primeiro evidência na própria área.

- >

Depois procurar referências cruzadas em outras áreas.

- >

Não limitar a busca ao nome exato do campo; usar equivalentes

semânticos e relações documentais.

- >

Preservar o texto original quando for decisão, valor, ID,

número, nome ou requisito específico.

consolidation:

- >

Se múltiplas fontes disserem essencialmente a mesma coisa,

consolidar e citar todas as fontes relevantes.

- >

Se fontes apresentarem versões sucessivas claramente identificadas,

usar a mais recente e registrar a anterior como superseded.

- >

Se não houver evidência de supersessão, registrar CONFLICT.

derivation:

allowed: true

requirements:

- "mínimo de duas evidências compatíveis"

- "nenhum novo requisito introduzido"

- "classe epistemológica DERIVED"

- "justificativa explícita"

proposal:

allowed: true

condition: >

Somente quando o documento necessita estruturalmente de um item,

mas o corpus não contém a resposta.

output_rule: >

A resposta canônica permanece A_DEFINIR.

Qualquer sugestão deve aparecer separadamente em proposed_value.

state_control:

- "Documento encontrado != documento completo"

- "Documento completo != aprovado"

- "Código encontrado != implementado"

- "Deploy encontrado != verificado"

- "Asset encontrado != publicado"

- "Decisão proposta != decisão aprovada"

sensitive_values:

rule: >

Não reproduzir senhas, tokens, chaves privadas ou segredos.

Registrar apenas existência e localização segura.

SCHEMA DO CAMPO PRÉ-PREENCHIDO

Para cada campo de todos os documentos, produzir exatamente:

field:

field_id: "Dxx-DOC-XXX-001.SECTION.FIELD"

label: ""

value: "A_DEFINIR"

normalized_value: null

evidence_status: "NOT_FOUND"

epistemic_class: "GAP"

confidence: "n/a"

evidence:

- source_id: ""

source_title: ""

source_type: ""

locator: ""

support: ""

conflicts: []

derived_from: []

proposed_value: null

proposed_rationale: null

notes: ""

SCHEMA DE SAÍDA DE CADA DOCUMENTO

document_output:

metadata:

document_id: ""

document_name: ""

acronym: ""

domain_id: ""

version: "PREFILL-0.1"

owner: "A_DEFINIR"

status: "PRE_PREENCHIDO"

approval_status: "PENDENTE"

executive_summary:

what: ""

why: ""

who: ""

how: ""

fields: {}

dependencies:

depends_on: []

blocks: []

evidence_summary:

total_fields: 0

found: 0

derived: 0

external: 0

conflict: 0

not_found: 0

coverage_percent: 0

gaps: []

conflicts: []

human_decisions_required: []

sources: []

validation:

every_field_accounted_for: false

evidence_attached_to_every_non_gap: false

conflicts_explicit: false

unsupported_claims: 0

ids_preserved: false

MASTER INDEX FINAL

Além dos 37 documentos individuais, produzir:

master_document_register:

columns:

- domain_id

- domain_name

- document_id

- acronym

- document_name

- document_class

- parent_document_id

- source_folder

- source_files

- owner

- status

- approval_status

- evidence_coverage_percent

- gaps

- conflicts

- depends_on

- blocks

- next_action

Classificar:

document_class:

allowed:

- MACRO

- SPECIALIZED

RELATÓRIO DE GAPS

Produzir também:

gap_register:

- gap_id: ""

domain_id: ""

document_id: ""

field_id: ""

missing_information: ""

why_required: ""

searched_sources: []

can_be_researched_externally: false

requires_human_decision: false

blocks: []

next_action: ""

RELATÓRIO DE CONFLITOS

conflict_register:

- conflict_id: ""

domain_id: ""

document_id: ""

field_id: ""

issue: ""

source_a:

source: ""

value: ""

source_b:

source: ""

value: ""

impact: ""

resolution_rule: ""

requires_human_decision: true

CONTRATO DE ACEITE

O workflow somente pode ser declarado VERIFIED quando:

acceptance_criteria:

- "D01-D23 processados."

- "23 documentos macro presentes."

- "14 documentos especializados presentes."

- "37 documentos contabilizados."

- "Todos os campos possuem valor ou A_DEFINIR."

- "Todo valor encontrado possui evidência."

- "Toda derivação possui fontes e justificativa."

- "Toda divergência está no Conflict Register."

- "Nenhum GAP foi preenchido por invenção."

- "Todos os IDs canônicos foram preservados."

- "Master Document Register foi produzido."

- "Gap Register foi produzido."

- "Conflict Register foi produzido."

- "Dependências foram reconciliadas."

- "Nenhum documento PRE_PREENCHIDO foi tratado como APROVADO."

ORDEM DE EXECUÇÃO

execution_graph:

- id: "PF-00"

task: "Inventariar fontes"

output: "SOURCE_REGISTER"

gate: "fontes identificadas"

- id: "PF-01"

task: "Processar D01"

depends_on: ["PF-00"]

- id: "PF-02"

task: "Processar D02"

depends_on: ["PF-01"]

- id: "PF-03"

task: "Processar D03"

depends_on: ["PF-02"]

- id: "PF-04-23"

task: "Continuar sequencialmente até D23"

rule: "WIP = 1"

- id: "PF-24"

task: "Executar reconciliação cruzada"

depends_on: ["D01-D23 concluídos"]

- id: "PF-25"

task: "Gerar Master Document Register"

- id: "PF-26"

task: "Gerar Gap Register"

- id: "PF-27"

task: "Gerar Conflict Register"

- id: "PF-28"

task: "Executar QA e validação"

- id: "PF-29"

task: "Entregar pacote final"

FORMATO FINAL OBRIGATÓRIO

Entregar um único pacote lógico contendo:

00_MASTER_DOCUMENT_REGISTER

00_SOURCE_REGISTER

00_GAP_REGISTER

00_CONFLICT_REGISTER

D01 a D23

dentro de cada área, seu documento macro

dentro das áreas aplicáveis, seus documentos especializados

um PREFILL_REPORT consolidado

um VALIDATION_REPORT

um NEXT_ACTIONS_REGISTER

Não solicitar ao usuário o preenchimento inicial.

O objetivo deste workflow é justamente reduzir ao mínimo a carga humana.

Primeiro pesquise, extraia, reconcilie e pré-preencha tudo o que puder ser obtido documentalmente.

Somente depois apresente uma seção:

USER_ACTION_REQUIRED

Nela, consolide exclusivamente os campos que:

realmente dependem de decisão humana;

não podem ser determinados pelas fontes;

não podem ser resolvidos por pesquisa;

não podem ser derivados sem criar informação nova.

Agrupe essas decisões no menor número possível de perguntas.

A entrega final deve deixar cada um dos 37 documentos em estado:

PRE_PREENCHIDO

com rastreabilidade suficiente para posterior revisão, aprovação e promoção ao estado canônico.

A diferença central dessa versão é que o agente não recebe apenas os nomes DDE, TAP, MNE, MRE etc. Ele recebe o contrato de conteúdo de cada documento e de cada área, além da regra de como preencher, provar, marcar conflito e deixar lacunas explícitas. Isso permite transformar o corpus do Drive diretamente em um conjunto documental pré-preenchido sem depender de perguntas campo a campo.
