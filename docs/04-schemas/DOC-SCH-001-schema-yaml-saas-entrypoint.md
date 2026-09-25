> Texto extraído automaticamente de `DOC-SCH-001-schema-yaml-saas-entrypoint.docx` (fonte original preservada ao lado).

Schema YAML — EXECUTAR Projeto SaaS Entrypoint

Conversão de 01_Formulario (94 campos, 17 domínios) em YAML preenchível por agente de IA, para uso fora do Excel e reimportação posterior.

Let me look at the actual spreadsheet content first.This is exactly the kind of structured hub I need the full form data for. Let me read the actual 01_Formulario sheet with openpyxl to get every row/ID/field precisely, plus check the fill-color convention mentioned in the readme.Columns: B=ID, C=Campo, D=O que preencher, E=Resposta, F=Exemplo. Let me pull full data plus fill colors to detect editable rows vs section headers.Good, I have the full picture. Let me get the rest of the rows (all 17 domains) so I capture every field.All 94 fields across 17 domains, matching the readme. Now let's check output sheet 09_Indice_IDs (reverse map) to confirm field categories/types, then build the YAML schema files.All 94 fields confirmed, exactly matching the readme's domain groupings. Now I have everything needed. Let me build the YAML schema — one clean, agent-fillable YAML per domain would bloat things; better as one master YAML file with all 17 domains nested, matching IDs, instructions and examples, plus a fillable resposta: null for each. Let's build it programmatically to avoid transcription errors.94 fields total, all 17 domains confirmed. Now let's check how output sheets reference these (INDEX/MATCH by ID) to make sure the YAML id values are the canonical keys the workbook expects, and check 09_Indice_IDs quickly.Confirmed — IDs like 1.1, 1.2 are the canonical keys, and each maps to a specific output sheet. Let me capture the full "aparece em" mapping to embed in the YAML (useful metadata for round-tripping into the xlsx).All 94 map cleanly. Now let's build the deliverables: a master YAML schema (all 17 domains) plus a per-domain split for convenience, and a small Python writer script that can push filled YAML back into the xlsx's 01_Formulario sheet (column E) and recalc.Now let's also split per-domain YAML files (useful for an agent to fill one domain at a time / smaller context windows), and a small round-trip writer script.All 17 files generated, 94 fields total. Let's verify one file's content looks right, then write the round-trip loader script.Clean. Now build the round-trip writer script that reads filled YAML(s) and writes back into 01_Formulario column E, matching by ID, then recalculates.Now let's test the round trip works end to end with sample filled data, and add a README explaining the whole system.Works correctly. Let's clean up the test file and write a README, then package everything into a zip for delivery.Todos os 94 campos dos 17 domínios de 01_Formulario foram convertidos, mantendo id, campo, instrução e exemplo originais e deixando resposta: null como o único campo editável pelo agente.

Entreguei:

hub_completo.schema.yaml — tudo num arquivo só

17 YAMLs por domínio (01_negocio_gtm.yaml ... 17_prompt_engineering_comandos.yaml) — para preencher em lotes menores

preencher_xlsx.py — script que lê os YAMLs preenchidos e escreve de volta na coluna "Resposta" da aba 01_Formulario, casando por id, sem sobrescrever respostas já existentes (a menos que peça --overwrite)

README.md — explica o fluxo completo, incluindo o lembrete de rodar recalc.py (LibreOffice) depois, já que o openpyxl não recalcula as fórmulas INDEX/MATCH das abas 02-09 sozinho

Cada campo também traz aparece_em, mapeado da aba 09_Indice_IDs, indicando em qual aba de saída aquele dado será consumido — útil se quiser validar o preenchimento antes de reimportar.

Arquivos

hub_completo.schema.yaml — todos os 17 domínios e 94 campos num único arquivo. Use quando o agente tem contexto suficiente para preencher tudo de uma vez, ou para versionar o estado completo do hub em um só lugar.

01_negocio_gtm.yaml … 17_prompt_engineering_comandos.yaml — os mesmos 94 campos divididos um arquivo por domínio. Use para preencher em lotes menores (uma sessão de agente por domínio, revisão humana por partes, etc).

preencher_xlsx.py — script que lê os YAMLs preenchidos e escreve as respostas de volta na aba 01_Formularioda planilha original.

Formato de cada campo

- id: '1.1'                    # chave estável — NÃO alterar

campo: Problema central      # rótulo do campo — NÃO alterar

instrucao: Descreva em 1 frase o problema que o produto resolve.

exemplo: 'Ex: Equipes técnicas perdem contexto...'   # referência de formato, não copiar

aparece_em: 02_Visao_Geral   # aba de saída que consome este campo via INDEX/MATCH

resposta: null               # <- ÚNICO campo que o agente preenche

resposta aceita uma string ou uma lista de strings (itens viram linhas separadas por \n ao reimportar).

id, campo, instrucao, exemplo e aparece_em são somente leitura — servem para o agente entender o que preencher e para o script localizar a célula certa na hora de reimportar. Não renumerar nem reescrever.

Fluxo de trabalho

Um agente de IA (ou você) preenche resposta: nos YAMLs — no arquivo único ou nos arquivos por domínio, um de cada vez.

Rode o script de reimportação:python preencher_xlsx.py \

EXECUTAR_projetosaasentrypoint_EXPANDIDO.xlsx \

hub_preenchido.xlsx \

hub_completo.schema.yaml

Ou, preenchendo por domínios:python preencher_xlsx.py \

EXECUTAR_projetosaasentrypoint_EXPANDIDO.xlsx \

hub_preenchido.xlsx \

01_negocio_gtm.yaml 02_produto.yaml 03_arquitetura_full_stack.yaml

O script escreve cada resposta na coluna Resposta (coluna E) da aba 01_Formulario, casando pelo id. Por padrão ele não sobrescreve células que já têm uma resposta na planilha original — passe --overwrite como último argumento para forçar.

As abas 02 a 09 são fórmulas INDEX/MATCH contra 01_Formulario — elas recalculam sozinhas, mas o openpyxl não recalcula fórmulas ao salvar. Depois de gerar hub_preenchido.xlsx, rode o recalculador da skill xlsx para forçar o LibreOffice a recalcular e gravar os valores:python scripts/recalc.py hub_preenchido.xlsx

(esse script faz parte da skill xlsx deste ambiente — sem ele, as abas derivadas mostram fórmulas sem valor até serem abertas no Excel.)

Por que YAML e não JSON

Comentários e blocos de texto multilinha (instrucao, resposta longas) ficam legíveis sem escapar aspas.

null explícito marca claramente "ainda não preenchido" — fácil de grep (grep -c "resposta: null") para medir progresso de preenchimento, o equivalente à fórmula =COUNTA(E6:E151)&" / 94" que já existe na aba01_Formulario.
