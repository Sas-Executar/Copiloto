# UX HIG adaptado ao Obsidian (V2.3)

## Objetivo
Transformar o vault em uma interface operacional 1:1 — cada tela é uma etapa com
exatamente um entregável ativo, não uma árvore de documentos para explorar.

## Princípios
1. **Uma tela = um único entregável ativo.** Nunca duas decisões abertas na mesma etapa.
2. **Localização explícita.** Toda etapa mostra ciclo, bloco (A–H), etapa e progresso real.
3. **Ação principal evidente.** O preenchimento aparece antes do contexto de apoio.
4. **Divulgação progressiva.** Contexto de referência fica recolhido e nunca é copiado para dentro da área de preenchimento — só linkado.
5. **Navegação previsível.** Anterior · Início · Painel · Próxima em todas as etapas; a etapa mostra sempre um único próximo passo possível.
6. **Feedback de estado consistente.** Pendente, em andamento, concluída, não aplicável e bloqueada usam a mesma linguagem em toda a trilha.
7. **Reconhecimento > memória.** A tela mostra o entregável e o único critério de pronto — não uma lista de checkboxes genéricos.
8. **Português primeiro.** IDs técnicos (S01, TP-XXX.PROBLEM.V1) ficam em propriedades/metadados e no rótulo do entregável, não substituem o texto operacional.
9. **WIP=1.** Só a etapa elegível atual é promovida; nunca duas etapas em andamento.
10. **Sem plugin obrigatório.** O núcleo usa Markdown, Callouts, Wikilinks, embeds e CSS snippet nativos.
11. **Progresso é real, não quantizado.** O percentual é etapas habilitadas concluídas ÷ total — nunca degraus fixos (0/33/66/99/100). Concluir a última etapa mostra "Pronto para gerar ZIP", não "100%".

## Anatomia de cada etapa (1:1 — nada além disto)
1. Navegação (Anterior · Início · Painel · Próxima).
2. Título humano + bloco (A–H).
3. **AGORA** — uma frase: o que fazer.
4. **ENTREGUE ISTO** — o entregável ativo desta etapa, e só ele.
5. **PREENCHA AQUI** — área de trabalho vazia (`[PREENCHER]`); nunca vem pré-preenchida com conteúdo de referência ou de exemplo.
6. **EVIDÊNCIA** — vazia até o operador preencher.
7. **PRONTO QUANDO** — um único critério de pronto, objetivo e verificável.
8. **CONTEXTO DE REFERÊNCIA** — recolhível, aponta (por link) para os artefatos de etapas anteriores relevantes; nunca duplica o conteúdo já preenchido dentro da área de execução.
9. **PRÓXIMO PASSO** — um único avanço possível a partir daqui.

## Regra de densidade
A primeira dobra não contém a trilha inteira nem o histórico completo. Esses ficam
no Painel do ciclo ou em callout recolhível (`> [!contexto]-`).
