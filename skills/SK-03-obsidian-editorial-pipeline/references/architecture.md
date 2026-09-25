# Arquitetura V2.3

```text
CICLO/
├── 00 - COMEÇAR AQUI.md
├── 01 - PAINEL DO CICLO.md
├── 98 - CHECKLIST FINAL.md
├── 99 - FINALIZAR E GERAR ZIP.md
├── 00-Sistema/
│   ├── ciclo.json
│   ├── estado-do-ciclo.json
│   └── manifesto-de-producao.json   (só depois de empacotar)
├── 02 - TRILHA/                      (uma página por etapa, 8 blocos A–H)
├── 03 - ARQUIVOS/
└── 04 - FONTES/
```

Nenhuma página de etapa é um arquivo estático copiado de `assets/templates/`:
a V2.3 gera cada página programaticamente a partir de `config/process-v03.json`
(`scripts/navegacao.py:render_step_page`), garantindo que todas as 42 etapas
sigam exatamente a mesma anatomia 1:1 (ver `references/ux-hig-obsidian.md`).
