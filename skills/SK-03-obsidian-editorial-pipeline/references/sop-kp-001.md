# SOP-KP-001 — Processo canônico (referência operacional)

Fonte canônica: **SOP-KP-001 — Processo Definitivo de Produção de Knowledge Pack Editorial**
(status DEFINITIVO, baseado na primeira aplicação completa — TP-001).

Esta skill implementa a SOP-KP-001 como o único workflow de gates. Ela substitui,
a partir da V2.3, o antigo Process Doc V02 (que começava direto em "tema validado"
e pulava as etapas reais de estratégia/conhecimento). Qualquer divergência entre
esta skill e a SOP-KP-001 é bug desta skill, não do processo.

## Unidade operacional
`1 problema → 1 knowledge pack → 1 solução (quando houver) → N assets → distribuição → métricas → aprendizado`

## Princípios de governança invariantes
- **Fator ≠ Vulnerabilidade ≠ Exposição ≠ Risco** (ou o equivalente do domínio do pack). Presença de um elemento nunca é anunciada como conclusão automática.
- **Um conceito → um ID canônico.** `problem_id` é o pivô do schema; todo asset herda `problem_id`, `solution_id` (se houver), `evidence_refs` e `cta_id`.
- **Classificação de evidência obrigatória**: toda afirmação do artigo recebe [E1] evidência primária, [E2] norma/guia oficial, [S] síntese sustentada ou [FW] constructo do framework. Uma afirmação [FW] nunca vira [E1].
- **Produto emergente fica estacionado.** Se o CTA de um pack gerar uma ferramenta/produto, ele é formalizado (Bloco D) mas nunca consome o eixo editorial principal nem vira código sem decisão explícita.
- **Sem evidência suficiente, nunca preencher artificialmente.** Marcar como pendente/insuficiente é um resultado válido.
- **Aprendizado nunca apaga histórico.** Toda atualização de catálogo/claim/decisão se soma ao registro anterior.

## Os 8 blocos (`config/process-v03.json`)

| Bloco | Nome | Regra de abertura |
|---|---|---|
| A | Estratégia & Problema | Ponto de partida de todo ciclo. Nunca pular para pesquisa/produção sem as 5 etapas fechadas. |
| B | Conhecimento & Evidência | Só abre com o Bloco A fechado. Nenhuma redação começa sem matriz de evidências + claims autorizados fechados. |
| C | Conteúdo Master | Storyboard → brief visual → Content-Spec → artigo master. Decide aqui (S17) se o Bloco D abre. |
| D | Produto/Solução (**condicional**) | Só habilita com decisão explícita `produto_esperado = true`. Nunca trava nem substitui A/B/C — é um ramo lateral que se formaliza e fica estacionado. |
| E | Design & Visual | Abre com o artigo aprovado (não depende do Bloco D). |
| F | Derivados e Distribuição | Reutiliza o Knowledge Master; nunca refaz pesquisa. |
| G | QA & Governança | Checklist mínimo antes de qualquer publicação. |
| H | Operação | Agendamento → publicação → medição → aprendizado. Fecha o ciclo. |

## Regra estrutural mais importante da V2.3

A trilha **não começa em "tema validado"**. O primeiro artefato de qualquer ciclo é a
transformação (S01), seguida do problema canônico (S02) — e é em **S02**, não na
criação do job, que o `problem_id` nasce. Exigir `problem_id` no formulário inicial
seria pedir o resultado de uma etapa antes de ela ser executada; a V2.3 corrige isso.

## Gate entre blocos

Não avançar de um bloco para o seguinte sem as etapas do bloco anterior registradas
como concluídas. O Bloco D é a única exceção formal ao "um bloco de cada vez": ele
pode abrir no meio do fluxo (tipicamente ao fechar o artigo master, S17) mas nunca
trava a abertura do Bloco E.

## Definition of Done do ciclo

Um ciclo está completo quando todas as etapas **habilitadas** (Bloco D incluído ou
excluído por decisão explícita) estão `DONE` — a interface mostra **"Pronto para
gerar ZIP"**. O ciclo só é **"100% Empacotado"** depois que o ZIP é gerado e os
hashes do manifesto são conferidos (`build_production_zip.py` + `verify_package.py`).
Aceite de terceiros fora desta skill (ex.: publicação por outra equipe) é um fato
separado e exige evidência própria — nunca presumir.
