# Relatórios regenerados — S0 Programa, governança e operações

| Arquivo | Origem (IDX) | Como regenerar |
|---|---|---|
| `mapa-os-executar-skills.json` | IDX 04 | Mapa-OS (valida com `validate_mapa.py`: PASS) |
| `mapa-os-executar-skills-prisma-payload.json` | IDX 06 | payload PRISM |
| `mapa-os-executar-skills-prisma.html` / `.pdf` | IDX 02 + PDF impresso | `python3 skills/SK-04-executar-relatorios/scripts/render_prism.py <payload> <html>` — template Prisma V4 agora sobre tokens (IBM Plex, sem hex fora do bloco `TOKENS`) |
