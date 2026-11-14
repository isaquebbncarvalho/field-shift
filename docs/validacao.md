# Log de validação

Registro do que foi conferido, com que fonte e qual o resultado. É o argumento de validade do pitch: atualize sempre que mudar critério ou valor agronômico.

## Rodada 0 — saída inicial do protótipo (14/11/2026, madrugada)

Dados: NASA POWER, safras 2001/02 a 2024/25. Pesos padrão (renda 4, solo 3, água 1, risco 4). Base agronômica ainda **não validada**.

| Município | Chuva anual média (mm) | Início mediano das chuvas | Fim mediano | Safras com início definido | Chuva na estação, tendência por década | Milho safrinha com problema: últimas 10 (série toda) | Melhor rotação |
|---|---|---|---|---|---|---|---|
| Rio Verde – GO | 1191 | 16/10 | 21/04 | 24/24 | −157 mm (p=0,006) | 50% (29%) | Soja → sorgo (7,0) |
| Jataí – GO | 1304 | 12/10 | 25/04 | 24/24 | −328 mm (p<0,001) | 60% (29%) | Soja → sorgo (6,6) |
| Sorriso – MT | 1502 | 01/10 | 27/04 | 24/24 | −304 mm (p<0,001) | 30% (17%) | Soja → milho + braquiária (7,0) |
| Luís Eduardo Magalhães – BA | 1026 | 31/10 | 17/04 | 22/24 | −155 mm (p=0,041) | 90% (75%) | Soja → braquiária (5,6) |

### O que bate com a realidade

- Rio Verde: início mediano em meados de outubro, coerente com a época de plantio da soja na região.
- Sorriso, maior polo de milho safrinha do país, sai com o menor risco para o milho entre os quatro. O oeste da Bahia, onde a safrinha de milho é pouco praticada, sai com o maior.
- As safras ruins que o modelo aponta em Goiás coincidem com anos de seca conhecidos: 2020/21 (chuva atrasada e safrinha de 2021 com perdas) e 2023/24 (El Niño, calor extremo).

### Avisos antes de citar números no pitch

1. **Chuva total provavelmente subestimada.** A média anual do POWER em Rio Verde (1191 mm) parece abaixo do que se espera para a região. Conferir com a normal climatológica de uma estação do INMET próxima. Se o POWER subestima, o risco de falta de água fica superestimado para todas as culturas.
2. **Tendências fortes demais pedem desconfiança.** Quedas de 300 mm por década em Jataí e Sorriso são grandes. Parte pode ser real (secas recentes), parte pode vir de mudança na fonte do dado ao longo da série. Antes de afirmar, comparar com GPM IMERG ou estação. No pitch, falar em "a série da NASA indica queda" e mostrar o teste, sem vender o número exato como certeza.
3. **Base agronômica sem validação.** Todos os valores de `culturas.json` são de partida.

## Próximas conferências

| # | O quê | Como | Responsável | Status |
|---|---|---|---|---|
| 1 | Janelas de plantio de soja e milho 2ª safra em Rio Verde | Comparar com o ZARC do município | Agronomia | pendente |
| 2 | Valores de `culturas.json` | Revisão linha a linha, preencher fonte | Agronomia | pendente |
| 3 | Chuva anual do POWER | Comparar com normal do INMET | Dados | pendente |
| 4 | Tendência de chuva | Repetir com GPM IMERG no mesmo ponto | Dados | pendente |
| 5 | Sensibilidade | Mudar ±20% a chuva mínima do milho e ver se o ranking muda | Dados | pendente |
