# Roteiro do pitch (esqueleto)

Ajustar ao tempo que a organização der. Base para 4 minutos.

## 1. Problema (30 s)

Em Rio Verde, quase todo mundo planta soja e depois milho safrinha. A safrinha depende da chuva que sobra depois da colheita da soja. Quando a chuva acaba mais cedo, o milho perde. A pergunta de todo produtor em fevereiro: planto milho ou vou de algo mais seguro?

## 2. O que a NASA mostra (45 s)

Abrir o app em Rio Verde. Mostrar o quadro "O que mudou no clima" e o gráfico de início e fim das chuvas ano a ano. Citar 2020/21 e 2023/24 como safras que a ferramenta marca e que todo produtor da região lembra.

Cuidado: falar em "a série da NASA indica", sem vender o número da tendência como certeza (ver avisos em `validacao.md`).

## 3. A ferramenta (1 min 30 s)

- O produtor escolhe o local, a rotação atual e o que prioriza.
- Mostrar os 3 cartões: a rotação atual e as duas melhores alternativas.
- Abrir "De onde vem essa nota": cada número tem a fonte.
- Mexer no peso de renda e mostrar a recomendação mudando. A decisão continua do produtor.
- Trocar para Sorriso-MT: o milho safrinha volta a fazer sentido. Mesma regra, clima diferente, resposta diferente.

## 4. Por que confiar (45 s)

- Quem decide é um motor de regras auditável, não uma IA.
- Validação: janelas conferidas com o ZARC, valores agronômicos revisados (citar quem revisou), coerência com a realidade de 4 regiões.
- Limites ditos de frente: resolução regional, não prevê o tempo, não substitui o agrônomo.

## 5. Próximos passos (30 s)

- Solo do talhão (SoilGrids ou análise do produtor).
- Chuva de maior resolução (GPM IMERG) e cobertura do solo por satélite (NDVI).
- Entrega por conversa no WhatsApp, onde o produtor já está.

## Perguntas prováveis da banca

| Pergunta | Resposta curta |
|---|---|
| Por que POWER e não imagem de satélite? | Precisamos de 24 anos de clima diário por ponto; o POWER entrega isso aberto. Imagem entra para ver o talhão, como próximo passo. |
| Como sabem que os números agronômicos estão certos? | Base revisada por agronomia com fonte por linha; ver log de validação. |
| A tendência de queda é real? | A série indica e o teste estatístico confirma na série; estamos cruzando com estação e IMERG antes de afirmar o tamanho. |
| E se o produtor discordar? | Ele muda os pesos e vê o efeito. A ferramenta mostra as consequências, não decide. |
