# Catálogo de documentos

Cada documento tem **ID estável**, classe e papel no ecossistema. O `.docx` original é preservado e, ao lado dele, há um `.md` com o texto extraído para leitura no GitHub.

| ID | Classe | Documento | Função | Skill/uso principal |
|---|---|---|---|---|
| DOC-GOV-001 | Governança | [Business Docs: arquitetura D01–D23](01-governanca/DOC-GOV-001-business-docs-arquitetura-d01-d23.md) | Estrutura das 24 pastas do Drive (00 + D01–D23) e as duas gerações da arquitetura documental (GOV-SPEC-20260907-001) | MAESTRO, SK-01 |
| DOC-PRM-001 | Prompt | [Prompt mestre: pré-preenchimento documental](02-prompts/DOC-PRM-001-prompt-mestre-pre-preenchimento.md) | Contrato `EXECUTAR-DOC-PREFILL-001`: 23 áreas, 37 documentos (23 macro + 14 especializados), rastreabilidade campo a campo | Origem do HUB-CP-002 |
| DOC-PRM-002 | Prompt | [Prompt do workbook integrado](02-prompts/DOC-PRM-002-prompt-workbook-integrado.md) | Inventariar o corpus, reconciliar conflitos e montar o Workbook Integrado de Governança e Operação | SK-04 |
| DOC-FRM-001 | Formulário | [Formulário mestre D01–D23](03-formularios/DOC-FRM-001-formulario-mestre-d01-d23.md) | Resumo executivo, JTBD, 5W2H e PDCPA por domínio; lacunas marcadas como LACUNA | SK-02, HUB |
| DOC-SCH-001 | Schema | [Schema YAML do SaaS Entrypoint](04-schemas/DOC-SCH-001-schema-yaml-saas-entrypoint.md) | Converte o 01_Formulario (94 campos, 17 domínios) em YAML preenchível por agente | HUB (SRC-01) |
| DOC-PRD-001 | Produto | [Checklist de product management](05-produto/DOC-PRD-001-checklist-product-management.md) | Fases do ciclo de produto, com entregáveis e questões de controle | A02, gates G02–G04 |
| HUB-CP-002 | Hub / fonte canônica | [EXECUTAR HUB Control Plane v2 (.xlsx)](06-hub/HUB-CP-002-executar-hub-control-plane-v2.xlsx) | Fonte primária de verdade (Release 1) | MAESTRO (todas) |
| HUB-MAP-001 | Hub / projeção | [Mapa operacional: payload PRISM](06-hub/HUB-MAP-001-mapa-operacional-prisma-payload.json) | Visão executiva do HUB para renderizar no SK-04 | SK-04 |

## Classes
`01-governanca` estrutura e regras · `02-prompts` contratos de agente · `03-formularios` entrada humana · `04-schemas` estruturas de dados · `05-produto` método de produto · `06-hub` fonte canônica e projeções.
