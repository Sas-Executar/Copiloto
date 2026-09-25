# EXECUTAR — Contrato de Design e Tokens para Relatórios Executivos

**ID:** EXECUTAR-REPORT-PRINT-DS-001  
**Versão:** 1.0  
**Área:** Design System / Relatórios / Impressão  
**Status:** READY_FOR_USE  
**Automação:** A4

## 1. Objetivo

Padronizar relatórios executivos impressos/PDF do ecossistema EXECUTAR usando a identidade visual mais madura já existente, sem criar uma segunda identidade ou um conjunto paralelo de tokens.

## 2. Fonte visual

Hierarquia de autoridade:

1. `Sas-Executar/Desyng-System-ecossitema.` → especificação visual e handoff.
2. `Sas-Executar/01-Executar-Echo/packages/design-tokens/` → implementação operacional dos tokens.
3. `Sas-Executar/01-Executar-Echo/packages/design-system/` → adaptação para componentes.
4. Showroom EXECUTAR → referência de composição, espaço negativo, superfícies, proporção de cor e hierarquia.

## 3. Tokens obrigatórios

### Cor
- Green 9: `#00BF63` — ação, progresso, prioridade.
- Green 11: `#007A45` — texto/acento acessível.
- Azure 9: `#1F93FF` — informação e navegação.
- Azure 11: `#0B6FD3` — texto/acento informativo acessível.
- Neutral 1: `#FFFFFF`.
- Neutral 2: `#F6F6F6`.
- Neutral 5: `#E4E4E4`.
- Neutral 10: `#7C7B7B`.
- Neutral 12: `#4B4A4A`.

Não introduzir cor crua quando houver token semântico equivalente.

### Tipografia
- Sans: IBM Plex Sans.
- Mono: IBM Plex Mono.
- Fallback de impressão: Helvetica Neue / Arial / sans-serif.

### Espaçamento
Escala base: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128 px.

### Raios
4, 8, 12, 16 px; pill = 999 px.

### Sombras
Discretas. Em impressão, preferência por borda/contraste de superfície em vez de profundidade pesada.

## 4. Gramática do showroom aplicada ao relatório

Preservar:
- alto espaço negativo;
- branco/cinza como área dominante;
- verde e Azure como acentos controlados;
- bordas finas;
- cards simples;
- hierarquia tipográfica forte;
- baixa densidade decorativa;
- um assunto/ação principal por composição.

Não transportar:
- navegação de produto;
- affordances interativas;
- componentes que só façam sentido em tela;
- decoração sem função executiva.

## 5. Gramática executiva do relatório

O documento deve seguir:

`pergunta executiva → resposta → evidência → implicação → recomendação → ação`

Regras:
- resposta principal no início da página;
- títulos devem expressar conclusão, não apenas tema;
- uma mensagem principal por página/bloco;
- métricas devem ter contexto;
- fatos, hipóteses e recomendações devem ser distinguíveis;
- detalhes secundários devem ir para apêndice;
- tabelas devem priorizar comparação e decisão;
- cor não substitui texto ou rótulo.

## 6. Contrato @page

- Formato: A4 retrato.
- Capa: página nomeada `cover`, margem zero.
- Miolo: página nomeada `report`.
- Margens do miolo: 15 mm superior, 16 mm laterais, 18 mm inferior.
- Cabeçalho: título curto do relatório + EXECUTAR.
- Rodapé: ID, versão, data e contador de páginas.
- `break-inside: avoid` para cards, tabelas, callouts, figuras e métricas.
- mínimo de 3 linhas para órfãs/viúvas.
- `print-color-adjust: exact`.

## 7. Componentes permitidos

- cover;
- eyebrow;
- answer-first;
- metric;
- card;
- callout;
- pill;
- tabela executiva;
- matriz evidência → implicação → ação;
- barra comparativa;
- roadmap em fases;
- bloco de riscos;
- bloco de decisão;
- nota de fonte.

## 8. Critério de aceite

PASS somente quando:
- identidade EXECUTAR preservada;
- nenhuma paleta paralela criada;
- A4 sem overflow horizontal;
- nenhum bloco importante cortado entre páginas;
- títulos e tabelas legíveis impressos;
- fontes e hipóteses registradas;
- cada página tiver mensagem executiva clara;
- verde/Azure usados de forma funcional, não ornamental;
- PDF/print preview revisado antes de RELEASED.

## 9. Arquivo de implementação

`EXECUTAR_Executive_Report_Print_Contract.html`

O arquivo é standalone e usa placeholders `{{...}}`. Pode ser preenchido por agente ou pipeline e então renderizado em navegador, Chromium, Prince, WeasyPrint ou mecanismo compatível com CSS paginado.
