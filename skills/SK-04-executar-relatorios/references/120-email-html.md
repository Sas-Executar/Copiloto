# Perfil `email` — relatório enviado por e-mail (HTML ou PDF)

Quem envia é o Copiloto Operacional (`Sas-Executar/executar-Blog/apps/copiloto`, ADR-015), pelo
Resend, com as saídas desta skill. O remetente escolhe o formato por envio (`/status-report <tipo> html|pdf`
ou `formato:` da rotina):

| Formato | O que vai | Fonte |
|---|---|---|
| `html` | o relatório no corpo do e-mail + `text/plain` equivalente | `assets/templates/status-report-v1.email.html` |
| `pdf` | corpo curto (resumo + link) + anexo PDF A4 | `assets/templates/status-report-v1.html` impresso (`@page` A4) |

Os dois partem do **mesmo JSON canônico** (`EXECUTAR_STATUS_REPORT_V1`) e dos **mesmos placeholders**.
Número nenhum é recalculado no template.

## Regras do e-mail HTML

1. **Tokens resolvidos, nunca `var()`.** Clientes de e-mail (Outlook desktop, Gmail) ignoram custom
   properties. A fonte `status-report-v1.email.src.html` usa `var(--exec-*)`; `scripts/build_email.py`
   troca cada uma pelo valor de `assets/tokens/tokens.json` e grava `status-report-v1.email.html`.
   Nunca edite o `.email.html` à mão; `validate_skill.py` falha se ele estiver desatualizado.
2. **CSS inline e tabelas.** Layout em `<table role="presentation">` com largura 600 px e
   `max-width:100%`. Sem `<style>` dependente de classe, sem flex/grid, sem imagens obrigatórias.
3. **Sem fonte externa.** Pilha `exec-font-sans` / `exec-font-mono` (IBM Plex com fallback do sistema);
   nenhum `@import` ou `<link>`.
4. **Só aliases definidos.** Nenhuma `LACUNA` (ex.: `surface-inverse`) e nenhum hex fora do que o build
   gerou. Texto de marca usa `brand-strong` (5,4:1); `brand` é só preenchimento (barra, régua).
   Rótulos usam `ink-secondary-strong` (6:1); `ink-secondary`/`ink-muted` não servem para texto.
5. **Modo claro declarado** (`color-scheme: light`) para o cliente não inverter as cores do relatório.
6. **Preheader** oculto com o resumo (`{{PREHEADER}}`: percentual + próxima ação).
7. **Texto alternativo obrigatório.** Todo envio leva a parte `text/plain` com os mesmos números.
8. **Sem ID interno em conteúdo externo.** Relatórios para fora do time seguem a regra de IDs do blog
   (sem `FRC-xx`, `TP001`, `RC-KNW`, `ARTICLE-MASTER`).

## Regras do PDF

- Gerado do template de impressão (`status-report-v1.html`) com `@page{size:A4}` e
  `print-color-adjust: exact` nos blocos de cor (ver `60-print-rules.md`).
- No Worker, o PDF sai pelo Cloudflare Browser Rendering; localmente, por Playwright/Chromium.
- O PDF é anexado; o corpo do e-mail repete só título, percentual e próxima ação.

## Checagem

```bash
python3 scripts/build_email.py --checar
python3 scripts/tokens.py --contraste
python3 scripts/validate_skill.py
```
