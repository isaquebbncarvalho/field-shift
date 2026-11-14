# Método

Tudo o que o protótipo calcula, em linguagem de gente. Cada número aqui pode (e deve) ser questionado pela banca; a resposta está neste arquivo.

## 1. Dados de clima

- Fonte: NASA POWER, série diária por ponto, comunidade agroclimatológica (AG).
- Variáveis: chuva corrigida (`PRECTOTCORR`), temperatura média, máxima e mínima, radiação solar, umidade do solo superficial e na zona de raiz, umidade do ar.
- Período: 2000 a 2025. Safras analisadas: 2001/02 a 2024/25.
- Resolução: cerca de 0,5 grau (~50 km). Descreve o clima da região, não do talhão.

## 2. Safra

Uma safra vai de 1º de julho de um ano a 30 de junho do seguinte, rotulada "2023/24".

## 3. Início da estação chuvosa

Primeiro dia, a partir de 1º de setembro, que cumpre as três condições:

1. Chove pelo menos 1 mm no dia.
2. Os 5 dias a partir dele somam pelo menos 30 mm.
3. Nos 30 dias seguintes não há sequência de 7 ou mais dias secos (menos de 1 mm).

A condição 3 evita o "falso início": aquela chuva forte de setembro seguida de seca, que leva quem planta cedo a replantar. Se nada cumprir as condições até 31/12, a safra fica "sem início definido" e conta como problema.

Conferência: em Rio Verde-GO a mediana dá 16/10, coerente com a prática local de plantio de soja em outubro.

## 4. Fim da estação chuvosa

Primeiro dia, a partir de 15 de fevereiro, que abre um período de 20 dias com menos de 10 mm de chuva somados. Se isso não acontece até 30/06, o fim fica em 30/06.

## 5. Indicadores por safra

- Duração da estação (dias entre início e fim).
- Chuva total na estação.
- Maior veranico (maior sequência de dias secos dentro da estação) e número de veranicos de 10 dias ou mais.
- Dias de calor: dias com máxima de 34 °C ou mais dentro da estação.

## 6. Tendência

Para cada indicador, inclinação de uma reta ao longo das safras (expressa por década) e teste de Mann-Kendall (tau de Kendall). Só chamamos de "tendência significativa" quando p < 0,05 e há pelo menos 10 safras.

## 7. Simulação da segunda safra (ano a ano)

Para cada safra e cada rotação:

1. Soja semeada 5 dias depois do início das chuvas, ciclo de 115 dias.
2. A segunda cultura é semeada 1 dia depois da colheita da soja.
3. **Problema de janela:** semeadura depois da data limite da cultura (ex.: milho safrinha 05/03).
4. **Problema de água:** chuva nos dias críticos após a semeadura abaixo do mínimo da cultura (ex.: milho, menos de 250 mm nos 70 dias após semear).
5. A safra "tem problema" se tiver qualquer um dos dois.

Os valores por cultura estão em `data/conhecimento/culturas.json`.

## 8. Notas (0 a 10)

| Nota | Como é calculada |
|---|---|
| Segurança climática | 10 × (1 − fração de safras com problema nas últimas 10) |
| Renda esperada | 2 × potencial de renda da cultura (1 a 5) × (1 − 0,5 × fração de safras com problema). Numa safra com problema a lavoura perde metade da renda, não toda. |
| Proteção do solo | 2 × (0,5 × cobertura na seca + 0,3 × palhada + 0,2 × nitrogênio), com nitrogênio = 5 se a cultura fixa e 1 se não |
| Economia de água | 2 × nota de economia de água da cultura (1 a 5) |

**Nota geral:** média ponderada das quatro, com os pesos que o produtor escolhe nos controles (0 a 5). Padrão: renda 4, solo 3, água 1, risco 4.

A tela mostra a rotação atual do produtor e as duas alternativas de maior nota.

## 9. O que a ferramenta não faz

- Não prevê o tempo da próxima safra. Usa histórico e tendência.
- Não recomenda cultivar, adubação ou defensivo.
- Não diferencia talhões vizinhos (limite da resolução do dado).
- Não substitui o agrônomo. O aviso aparece na tela.

## 10. Pontos que a pessoa de agronomia precisa validar

- Ciclo da soja (115 dias) e atraso de semeadura (5 dias).
- Para cada segunda safra: dias críticos, chuva mínima, data limite de semeadura e as notas de 1 a 5.
- A perda de 50% da renda em safra com problema.
- Os critérios de início e fim das chuvas, comparando com o ZARC do município.
