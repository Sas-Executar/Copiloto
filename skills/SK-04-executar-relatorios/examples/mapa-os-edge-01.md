# Limite — duas ações elegíveis sem precedência

## Entrada

Duas ações não bloqueadas possuem dependências satisfeitas, mas a fonte não define prioridade, valor, prazo decisivo ou outra regra de desempate.

## Esperado

`next_action = null`, issue de autoridade com severidade `blocking` e classificação `EXIGE_HUMANO`. O restante do mapa continua disponível.

## Proibido

Escolher uma das ações por ordem de aparição ou preferência do modelo.
