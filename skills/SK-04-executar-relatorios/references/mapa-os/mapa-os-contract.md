# Contrato Mapa-OS

## Objetivo

Transformar material disperso em orientação operacional sem alterar a verdade do projeto. O Mapa-OS é uma projeção de leitura e execução, não um banco de dados concorrente.

## Classificação de fonte

| Classe | Uso | Autoridade |
|---|---|---|
| Norma/contrato | Define obrigação e gate | Determinística quando inequívoca |
| Decisão aprovada | Fecha alternativa registrada | Determinística dentro do escopo |
| Evidência | Sustenta estado ou resultado | Conforme origem e validade |
| Status | Declara estado atual | Deve ser confrontado com critérios/evidência |
| Plano | Expressa intenção, sequência ou prazo | Não prova conclusão |
| Template | Define forma de apresentação | Não define fatos do projeto |
| Exemplo | Ilustra comportamento | Nunca é fonte de verdade por si só |

## Autoridade de comportamento

- `DETERMINISTICO`: cálculo ou regra fixa sustentada.
- `INTERPRETATIVO`: síntese dentro de limites explícitos.
- `EXIGE_HUMANO`: conflito, empate ou mutação que requer decisão/autorização.
- `NAO_DETERMINADO`: lacuna declarada.

## Estado

Use os estados do material-fonte quando consistentes. Ao normalizar, preserve a diferença entre `existing`, `complete`, `approved`, `implemented`, `tested`, `verified` e `published`. Um estado superior exige evidência e critério próprios.

## Elegibilidade

Uma ação é elegível quando todas as dependências obrigatórias estão em estado suficiente, gates anteriores estão satisfeitos, não existe bloqueio ativo e há capacidade/autoridade quando exigida. Se mais de uma ação permanecer elegível, aplique somente a regra de precedência fornecida. Sem regra, retorne empate para decisão humana.

## Horizontes

- `Agora`: única ação ativa/elegível e seus bloqueios/evidência.
- `Próximo`: itens elegíveis após o fechamento válido de Agora.
- `Depois`: sequência dependente ou horizonte posterior; não recebe foco ativo.

Horizontes não mudam IDs, estados ou dependências.

## Cabeçalho documental

Inicie respostas substantivas com classe e ID, `DOCUMENT READER · VALU-MODE V3`, os campos ID/Tipo/Owner/Versão/Data/Fase/Projeto/PARA/Referência/3#, depois `RESUMO EXECUTIVO` com O quê/Por quê/Quem/Como e `3P+N · APLICAÇÃO` com Problema/Processo/Progresso/Next. Use exatamente três tags; não invente owner, projeto ou referência. Depois do bloco, limite o corpo a Resumo Executivo, Conclusão, Desenvolvimento e Próximos Passos, omitindo seções sem conteúdo real.
