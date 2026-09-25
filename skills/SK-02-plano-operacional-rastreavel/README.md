# SK-02 · plano-operacional-rastreavel

> **Jurisdição:** [MAESTRO — Orchestrator Operacional](../../MAESTRO.md) · **Macroáreas:** A09, A00 · **Ponto de entrada:** [`SKILL.md`](SKILL.md)

## Objetivo
Gerar o **plano operacional mensal rastreável** de qualquer cliente/projeto com o motor de evidência proprietário: IDs estáveis, hierarquia de fontes, classificação `FACT / DECISION / ASSUMPTION / GAP / CONFLICT` e limite normativo ISO 9001 / 10005 / 10006 / 21502 / 31000 / 10075-2.

## Funções
1. **Intake**: formulário interativo (`assets/formulario-intake.html`).
2. **Normalização e evidência**: aplica `references/motor-evidencia-fontes.md`.
3. **Limite normativo**: `references/normas-fixas-iso.md`.
4. **Construção do plano** em 7 fases internas.
5. **Pacote de 4 entregáveis**, sempre gerados juntos: documento interno, roadmap do cliente, schema de tarefas Linear (CSV) e calendário one-page.
6. **Juiz validador**: `scripts/validar_plano.py`, obrigatório entre o entregável #1 e os demais.

## Estrutura
- `references/`: schemas do documento interno, dos entregáveis e do CSV de tarefas; fontes vivas; prompt self-contained
- `assets/formulario-intake.html`
- `scripts/validar_plano.py`
