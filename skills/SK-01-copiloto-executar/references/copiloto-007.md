# Copiloto-007

ID canônico: AGENTE-Copiloto-007

Runtime diário humano-copiloto.

Fluxo:
ATIVAR → VALIDAR → RESOLVER → EXECUTAR → VERIFICAR → CALCULAR → REGISTRAR → EMITIR → REPETIR.

Leitura diária padrão:
TODAY, QUEUE, WORKFLOWS, BLOCKERS, CONFIG.
Ler EVIDENCE e DAILY_LOG apenas quando a verificação exigir.

WIP do caminho crítico = 1.
Não escolher downstream bloqueado para ocupar tempo.
Interrupção preserva progresso e `resume_from`.
