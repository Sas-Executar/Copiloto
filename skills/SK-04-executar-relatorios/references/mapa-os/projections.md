# Projeções do Mapa-OS

Toda projeção lê o mesmo `mapa_os` validado. Nenhuma projeção cria objeto, promove estado, resolve conflito ou reordena dependências por estética.

## mapa_operacional

Mostre posição, progresso sustentado, ação Agora, critério de conclusão, evidência necessária, bloqueios, itens Próximo/Depois e a pergunta: “A prova descrita existe?”.

Existem duas formas de saída para esta projeção, conforme o que a fonte sustenta:

- **Leitura de retomada** (texto/JSON simples): resposta direta na conversa, sem template fixo.
- **Documento A4 permanente** (quando a fonte é grande e estruturada — ex.: um control plane com dezenas de macroáreas/domínios/documentos, não um projeto de sete dias): use `scripts/render_mapa_operacional.py` com `assets/templates` gerado dinamicamente a partir do payload (não há 100 placeholders fixos como no `prisma_7d` — o conteúdo tem comprimento variável, então o script itera sobre o payload e monta o HTML por seção). Estrutura mínima do payload: `meta`, `visao_geral` (resumo + números-chave), `como_ler_a_planilha` (passos), `mapa_operacional.macroareas` (nome, finalidade_executiva, domínios, quantidade_de_campos, aba_de_preenchimento, situação), `estrutura_da_planilha`, `pontos_de_atencao`, `legenda_executiva`, `fonte_e_rastreabilidade`. Reaproveita os mesmos tokens/componentes visuais do `executive-report-a4.html` (card, metric, callout, pill, section-head, table) — mesma identidade EXECUTAR, sem paleta paralela.

  ```bash
  python scripts/render_mapa_operacional.py payload.json output.html
  ```

  Este documento é permanente/de referência, não um plano de execução — não force nele uma estrutura de dias ou semana; isso é o `prisma_7d`, abaixo.

  **Variante compacta (uma folha A4):** quando o pedido é por uma visão geral
  de uma folha só (não o documento de referência completo em várias
  páginas), reaproveite o mesmo template e schema do `prisma_7d`
  (`assets/templates/status-report-prisma-a4-v4.html` +
  `schemas/prism-report.schema.json`) remapeando a semântica dos campos —
  o template é sobre estrutura visual (3 faces, KPIs, 7 blocos, hero +
  4 itens), não sobre "semana": nada nele exige que `calendar.days` sejam
  dias do calendário. Mapeamento: `epic` = visão geral da fonte (não
  "épica"); `epic.intent` = como interpretar; `kpis` = 4 números
  estruturais (contagens, não situação operacional — conflitos/gates não
  entram aqui); `calendar.days` = até 7 blocos de navegação/agrupamento
  temático (não dias — reescreva `weekday`/`date` como rótulo+rastreio
  curto, ex. `weekday:"ÁREA"`, `date:"A02-A04"`); `deliverables.hero` =
  como operar/usar a fonte; `deliverables.items` = as camadas de uso (ex.
  entrada, consulta, rastreio, governança); `deliverables.next` = pontos
  que exigem atenção/decisão; `deliverables.trace` = fonte e abas.

  O template tem três rótulos de canto fixos ("FACE 01 · ÉPICA", "FACE 02 ·
  EXECUÇÃO", "FACE 03 · RESULTADO") que não vêm do payload — são texto
  estático do arquivo imutável. Para uma leitura não-semanal eles ficam
  incoerentes com o conteúdo; ajuste-os no HTML já renderizado (não no
  template-fonte) para casar com os três `eyebrow` do payload, por exemplo:

  ```python
  html = html.replace("FACE 01 · ÉPICA", "FACE 01 · " + epic_eyebrow)
  html = html.replace("FACE 02 · EXECUÇÃO", "FACE 02 · " + calendar_eyebrow)
  html = html.replace("FACE 03 · RESULTADO", "FACE 03 · " + deliverables_eyebrow)
  ```

## agora_proximo_depois

Agrupe por horizonte, preservando IDs e prazos. Um prazo original vencido permanece registrado; uma nova previsão é outro campo. O bloco Agora recebe WIP=1.

## status_terminal

Síntese compacta: header, progresso por profundidade, posição atual, 3P+N, riscos, prevenção, evidências e tags. Percentuais exigem numerador/denominador explícitos.

## prisma_7d

Use somente quando houver dados suficientes para sete dias ou quando o usuário autorizar planejamento desses sete dias. Converta o Mapa-OS em payload conforme `schemas/prism-report.schema.json`: Face 01 com uma épica, intenção, progresso e quatro KPIs; Face 02 com sete dias; Face 03 com um entregável principal, quatro entregáveis de apoio e próximo estado.

O template `assets/templates/status-report-prisma-a4-v4.html` é fixo. Os 100 placeholders pertencem apenas aos namespaces `DOC_*`, `EPIC_*`, `CALENDAR_*` e `RESULT_*`. Não reintroduza tokens legados.

Quando um campo exceder `maxLength`, remova redundância e condense sem perder IDs, datas, quantidades, milestones ou qualificadores de estado. Nunca reduza tipografia, margens, paddings ou faces. Se não couber sem perda, retorne erro de fit.

```bash
python scripts/render_prism.py payload.json output.html
python scripts/audit_prism.py
```
