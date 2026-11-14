# O desafio

**Field Shift: Adapting Farms with NASA Data**: NASA Space Apps Challenge 2026. Dificuldade intermediária/avançada. Temas: Ciências da Terra, Software, Artes e Multimídia.

Página oficial: https://www.spaceappschallenge.org/2026/challenges/adapting-farms-with-nasa-data/

## Em resumo (paráfrase do enunciado)

Produtores do mundo todo lidam com temperatura subindo, chuva mudando de padrão, falta de água, eventos extremos e solo perdendo saúde. Isso dificulta escolher rotações que protejam o solo, economizem água e deixem a fazenda resiliente. O desafio pede uma **ferramenta de apoio à decisão** que use **observações da Terra feitas pela NASA**, junto com **informação local de solo, características das culturas e prioridades do produtor**, para ajudar a explorar estratégias de rotação que fortaleçam o solo e adaptem a fazenda às mudanças.

## Como o protótipo responde a cada parte

| Pede | Onde está |
|---|---|
| Observações da Terra da NASA | NASA POWER, 24 safras de dados diários (`fieldshift/power.py`) |
| Informação local de solo | Ainda não: próximo passo é SoilGrids ou análise de solo do produtor |
| Características das culturas | `data/conhecimento/culturas.json` |
| Prioridades do produtor | Controles de renda, solo, água e risco no app |
| Explorar rotações | Comparação de 6 rotações, 3 em destaque, com evidência |
| Adaptar a mudanças | Indicadores e tendência do início/fim das chuvas, veranico e calor |

## Datas

- Hackathon: 14 e 15/11/2026. Envio do projeto até 15/11, 23h59.
- Evento local: Hub Goiás Rio Verde. Apresentação para a banca no domingo.

## Critérios de avaliação

Confirmar no site do Space Apps e com a organização local. Historicamente a avaliação global considera impacto, criatividade, validade, relevância e apresentação.

## Pontos a confirmar com a organização

- Regra de declaração de uso de IA no envio.
- Formato da apresentação local (tempo, se precisa de slide ou demo ao vivo).
- Se o repositório precisa ser público no envio.
