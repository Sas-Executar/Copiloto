Tarefa: criar issues no GitHub, repo owner=sas-executar repo=copiloto, usando as ferramentas MCP (carregue antes via ToolSearch "select:mcp__github__issue_write,mcp__github__sub_issue_write").

Entrada: BATCH (lista JSON de objetos {key,title,labels,body,parent}), MANIFEST (arquivo de saída desta rodada), PARENTS (arquivos de manifest já existentes; lidos para resolver pais).
Um manifest é um objeto JSON: key -> {"number":N,"id":ID,"url":URL}. `number` é o último segmento da url.

Para CADA item, na ordem do arquivo, um de cada vez:
1. Se a key já está em MANIFEST ou em algum arquivo de PARENTS, pule (sem duplicatas).
2. Troque o texto literal "{GAPDEP}" no body por "#<number de GAP-DEP-01>" (procure-o em manifest-01.json).
3. Chame issue_write com method="create", title, body e labels exatamente como dados. NÃO passe parent_issue_number (ele quebra a criação automática de labels). Não use assignees.
4. Se parent não for nulo, resolva o number do pai pelos manifests (inclusive entradas criadas antes neste lote) e chame sub_issue_write method="add", issue_number=<number do pai>, sub_issue_id=<id da nova issue>.
5. Grave a entrada no MANIFEST imediatamente (reescreva o arquivo JSON completo), para que o progresso sobreviva a uma interrupção. Se o vínculo com o pai falhar, grave "link_error":msg.
Se uma chamada falhar, tente de novo uma vez; se falhar de novo, registre "error":msg e siga para o próximo item. Pare somente se 3 falhas seguidas tiverem a mesma causa, e relate essa causa.
Resposta final: quantas issues foram criadas, quantas foram vinculadas, os erros e o intervalo de números usado.
