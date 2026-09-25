# Arquitetura EXECUTAR — invariantes

## Hierarquia

```text
MACRO = PROJETO
MESO  = ENTREGA / DIA LÓGICO
MICRO = FLUXO DE TRABALHO
ÁTOMO = AÇÃO
```

## Regras

- Posição = estado.
- Dia Lógico é entrega, não data. Calendário é projeção de capacidade.
- WIP operacional = 1 entrega ativa → 1 fluxo ativo → 1 ação ativa.
- A ordem dos Dias Lógicos é preferencial. Dependências válidas governam elegibilidade.
- O projeto encerra somente quando entregas obrigatórias, gates e evidências exigidas estiverem concluídos.
- Uma entrega pode ter N fluxos e um fluxo pode ter N ações. O número três é referência de template.

## Modos

`MODO MAPA` mostra o universo do projeto, relações e categorias. `MODO EXECUTAR` mostra somente entrega, fluxo e ação ativos, evidência, gate e próximo mergulho.

```text
ENTREGA → _INICIAR → FLUXO → AÇÃO → EVIDÊNCIA → GATE
        → PRÓXIMO FLUXO ELEGÍVEL → _FEITO
```

## Erros proibidos

- interpretar `DIA-01` como data;
- avançar estado por passagem do tempo;
- fechar etapa sem evidência quando o contrato a exige;
- deixar o modelo escolher arbitrariamente entre itens empatados;
- introduzir Scrum, Kanban ou outra estrutura como fonte concorrente.
