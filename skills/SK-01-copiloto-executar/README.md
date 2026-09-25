# SK-01 · copiloto-executar

> **Jurisdição:** [MAESTRO — Orchestrator Operacional](../../MAESTRO.md) · **Macroáreas:** A00, A09 · **Ponto de entrada:** [`SKILL.md`](SKILL.md)

## Objetivo
Operar a rotina diária EXECUTAR sobre **uma única fonte de verdade** (`EXECUTAR_CONTROL_CENTER` / `00_AGORA`), sem criar plano, fila, sprint, gate ou estado paralelo.

## Funções
| Comando | Função |
|---|---|
| `/bomdia` | Valida o fechamento anterior, resolve o trabalho liberado e emite o dia |
| `/agora` | Mostra só o objeto atual, DoD, evidência esperada e próxima ação |
| `/estado` | Progresso derivado, sprint/C72, gate, bloqueios, posição |
| `/fechardia` | Valida resultado + evidência, registra `resume_from` e fecha o dia |
| `/replanejamento` | Recalcula só o subgrafo afetado |

Fluxo: `ATIVAR → VALIDAR → RESOLVER → EXECUTAR → VERIFICAR → CALCULAR → REGISTRAR → EMITIR → REPETIR`. `CONCLUÍDO` exige DoD + evidência + verificação; caminho crítico com WIP=1.

## Estrutura
- `references/` — commands, copiloto-007, produtividade, operacoes, orchestrator, legado
- `references/contracts/` — schemas de entrada/saída do orquestrador, command-router, drive-bindings, preflight, state-contract, testes
- `scripts/validate_skill.py` — validação estrutural
