# Precedência de fontes (V2.3)

1. Dados e decisões explícitas do usuário para o ciclo atual (inclui a decisão `produto_esperado`).
2. **SOP-KP-001** (`references/sop-kp-001.md` + `config/process-v03.json`): fonte canônica única de blocos, gates, dependências e critério de pronto. Substitui o antigo Process Doc V02.
3. Estado e evidências já registrados no ciclo (`00-Sistema/estado-do-ciclo.json`).
4. Templates e referências desta skill (`references/ux-hig-obsidian.md`, `references/visual-system-v1.md` etc.) para forma/estilo — nunca para gates.

Nunca inventar `problem_id`, owner, aprovação, evidência, fonte, data ou URL. Se um
documento externo do usuário (Process Doc de marca, knowledge pack anterior) divergir
da SOP-KP-001 em gates ou ordem de etapas, registrar a divergência explicitamente e
tratá-la como decisão de governança separada — nunca silenciosamente ignorar uma das
duas fontes.
