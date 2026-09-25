# Relatórios regenerados — M2.1 Risco Cognitivo

Regenerados em 2026-09-25 sobre os tokens da skill `executar-relatorios`
(`skills/SK-04-executar-relatorios`, contrato EXECUTAR-REPORT-PRINT-DS-001). Nenhum hex fora do
bloco `TOKENS` gerado; tipografia IBM Plex.

| Arquivo | Origem (IDX) | Como regenerar |
|---|---|---|
| `MAP-REPORT-STATUS-001.json` | IDX 08 | JSON canônico `EXECUTAR_STATUS_REPORT_V1` (valores da fonte, com proveniência) |
| `MAP-REPORT-STATUS-001.html` / `.pdf` | IDX 08 | `python3 skills/SK-04-executar-relatorios/scripts/render_report.py <json> <html> --email <email.html>` |
| `MAP-REPORT-STATUS-001.email.html` | IDX 08 | idem, perfil e-mail (CSS inline) |
| `processo-trabalho-formulario-semana.html` / `.pdf` | IDX 03 | estilo migrado para aliases; `tokens.py --sincronizar <html>` após mudar tokens |

> `quality.conflicts` do IDX 08: título e tríade falam da campanha de lançamento, mas as
> propriedades descrevem a consolidação do código SaaS. Mantido como na fonte; decidir antes de circular.
