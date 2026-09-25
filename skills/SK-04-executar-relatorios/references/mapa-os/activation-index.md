# Índice de ativação simples

Este índice existe para tornar a skill utilizável por pessoas que não conhecem Mapa-OS, schemas ou Prisma. Os comandos reduzem a entrada; não reduzem as validações nem autorizam a invenção de dados.

## Regra de reconhecimento

Reconheça um ID numérico somente quando a mensagem inteira for 00, 01 ou 02, ou quando o usuário escrever Mapa 00, Mapa 01 ou Mapa 02. Não trate números em datas, semanas, prazos ou IDs de projeto como comando.

## 00 · Ajuda

- ID verbal: /ajuda-mapa
- Frases equivalentes: “me ajude”, “não sei por onde começar”, “como faço meu mapa?”
- Resposta: apresente somente as opções 01 e 02, em linguagem simples, e peça que a pessoa envie o número ou descreva o que deseja.

## 01 · Criar mapa semanal

- ID verbal: /criar-mapa-semanal
- Frases equivalentes: “quero criar meu mapa da semana”, “montar meu plano semanal”, “gerar meu Prisma”
- Referência: [prompts/01-prompt-mestre-prisma.md](prompts/01-prompt-mestre-prisma.md)
- Resposta: inicie uma coleta progressiva. Primeiro confirme projeto, semana e objetivo; depois peça somente os fatos restantes que impedem a geração. Explique termos técnicos quando aparecerem.

## 02 · Testar exemplo Prisma

- ID verbal: /testar-mapa-prisma
- Frases equivalentes: “quero ver um exemplo”, “testar com dados de exemplo”, “como fica impresso?”
- Referência: [prompts/02-exemplo-preenchido-prisma.md](prompts/02-exemplo-preenchido-prisma.md)
- Resposta: gere a demonstração baseada no exemplo, identificando-a como ilustrativa. Não trate nomes, datas, estados ou evidências do exemplo como fonte de verdade de qualquer projeto.
