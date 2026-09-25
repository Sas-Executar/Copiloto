> Texto extraído automaticamente de `DOC-GOV-001-business-docs-arquitetura-d01-d23.docx` (fonte original preservada ao lado).

Sim. Confirmei acesso direto ao Google Drive pela conta executar.leonardo@gmail.com e localizei a especificação que você estava lembrando.

A raiz Ecosistema Product Launch⁠ contém, neste momento, 24 pastas: 00__governanca-e-schema + D01–D23. Portanto, são 24 pastas no total, não 25. Não existe D24.

O que encontrei é mais importante: existem duas gerações dessa arquitetura documental.

A especificação mais detalhada está no arquivo GOV-SPEC-20260907-001__relatorio-integral-organizado__v01.md⁠. Ele contém explicitamente uma seção chamada “Família canônica dos 30 documentos”. Nela, a arquitetura original era:

16 áreas → 16 documentos macro + 14 documentos especializados = 30 documentos.

Por exemplo:

Área

Documento macro

Derivados/especializados localizados

D01 Gestão Empresarial

DDE — Documento de Direção Empresarial

TAP — Termo de Abertura; MNE — Modelo de Negócio; MRE — Mapa de Relações

D02 Jurídico/Riscos

DGRC — Governança, Riscos e Conformidade

MRC — Matriz de Riscos e Controles; PPT — Política de Privacidade e Termos

D03 Finanças

PFO — Plano Financeiro e Orçamentário

MFO — Modelo Financeiro

D04 Pessoas/RH

PPC — Plano de Pessoas e Capacidade

—

D05 Dados

EPGD — Estratégia e Plano de Gestão de Dados

DCM — Dicionário de Dados e Catálogo de Métricas

D06 Conhecimento

EGC — Estratégia de Gestão do Conhecimento

RMI — Registro Mestre de Identidades

D07 Execução

PEX — Plano de Execução

PIM — Plano de Implementação e Marcos

D08 Operações

MOP — Manual de Operações

RUN — Runbook Operacional

D09 Pesquisa

PPE — Plano de Pesquisa e Experimentação

DEB — Dossiê de Evidências e Base Científica

D10 Produto

DRP — Documento de Requisitos de Produto

PRD — Requisitos Integrados dos Produtos

D11 Experiência/Design

EEP — Especificação de Experiência e Projeto

DSI — Sistema de Design e Interface

D12 Engenharia

ETE — Especificação Técnica de Engenharia

—

D13 Mercado

DRM — Documento de Requisitos de Mercado

GTM — Plano de Entrada no Mercado e Lançamento

D14 Vendas

PCV — Plano Comercial e de Vendas

—

D15 Atendimento

PASC — Plano de Atendimento e Sucesso

—

D16 Mídias

PEM — Plano Estratégico de Mídias Sociais

—

Essa é exatamente a “série de especificações” que você estava procurando.

Há, porém, uma ressalva documental importante: o próprio relatório registra que os 16 documentos macro eram explicitamente documentados, enquanto os 14 especializados foram formalizados como classe E · Recomendada naquele momento. Ou seja, eles foram derivados da necessidade documentada de uma família de 30 documentos; não devem ser confundidos com os 16 macros originais.

Depois disso surgiu uma versão mais nova da governança. O documento GOVERNANCA⁠ estendeu o modelo para 23 áreas e definiu um documento macro para cada uma, incluindo:

D17 PEP, D18 PCE, D19 PAC, D20 PPR, D21 PWB, D22 DRL e D23 PBL.

Esse documento estabelece explicitamente a hierarquia:

Ecossistema → D01–D23 → Documento Macro → Documentos especializados → Workflows/Tarefas/Assets/Registros.

E há um ponto decisivo: ele também registra como próximo nível necessário do Master Index adicionar as colunas Subáreas, Documentos especializados, Repositório/Drive, Owner, Status e Dependências. Portanto, a arquitetura atual de 23 áreas ainda não incorporou completamente a antiga matriz dos documentos especializados ao Master Index novo.

Também confirmei isso nas extrações da própria pasta 00__governanca-e-schema⁠: 00_governanca-docx.csv registra essa pendência explicitamente, enquanto D06_progama-sas-diretorio-documental-xlsx.csv confirma o catálogo anterior de 16 áreas / 30 documentos.

Portanto, o estado real é:

SIM, existe a especificação das classes documentais. SIM, existe a relação área → documento macro → documentos especializados. Mas ela está dividida entre o modelo anterior D01–D16/30 documentos e a governança nova D01–D23.

O gap atual é bastante específico: falta fazer a reconciliação canônica dos 30 documentos antigos com as 23 áreas atuais, incluindo os documentos especializados de D17–D23. Esse é o ponto que precisa ser consolidado para termos finalmente um único MASTER DOCUMENT CLASS REGISTER sem ambiguidades.
