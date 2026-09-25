# Normal 01 — retomada operacional

## Entrada

Plano com uma entrega ativa, duas ações sequenciais e evidência de que a primeira foi implementada.

## Esperado

A skill preserva `implementado ≠ verificado`, mantém WIP=1 e seleciona a verificação como única próxima ação. A saída de referência está em `normal-output.json`.

## Proibido

Declarar a entrega publicada ou verificada antes do teste.
