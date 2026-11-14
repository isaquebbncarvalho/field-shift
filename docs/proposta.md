# Field Shift: proposta de projeto

Rascunho pra discussão do time. Desafio: *Field Shift: Adapting Farms with NASA Data* (NASA Space Apps 2026, Rio Verde).

## Ideia em uma frase

Uma ferramenta em que o produtor informa o talhão e o que ele prioriza, e recebe 3 rotações de cultura comparadas, cada uma com o porquê, calculadas a partir do histórico de clima da NASA daquele ponto.

## A pergunta que o protótipo responde

> Com a chuva mudando, o milho safrinha ainda cabe neste talhão, ou sorgo, braquiária ou planta de cobertura é a rotação mais segura?

É uma dúvida real de quem planta soja no Cerrado, e o dado da NASA responde: dá pra medir se a estação chuvosa está começando mais tarde, terminando mais cedo ou ficando mais irregular.

## Como funciona

1. **Entrada do produtor**: localização do talhão, rotação atual, dados de solo (se tiver análise) e prioridades (produzir mais, proteger o solo, economizar água, reduzir risco).
2. **Dados da NASA**: o sistema busca o histórico de chuva, temperatura, radiação e umidade do solo daquele ponto.
3. **Indicadores**: início e fim da estação chuvosa em cada ano, frequência de veranicos, calor na fase crítica e tendência ao longo dos anos.
4. **Pontuação**: um motor de regras cruza os indicadores com a exigência de cada cultura e com as prioridades do produtor.
5. **Saída**: 3 rotações lado a lado (incluindo a atual), com nota, riscos, o dado que justificou cada ponto e o grau de incerteza.

**Regra de projeto:** quem decide a nota é o motor de regras, que é auditável. IA generativa, se entrar, só reescreve a explicação em linguagem simples. Ela não escolhe a rotação.

## Dados

| Fonte | O que entrega | Acesso |
|---|---|---|
| NASA POWER | Chuva, temperatura, radiação e umidade do solo por coordenada, série histórica diária | API aberta, sem login |
| HLS ou MODIS (NDVI) | Vegetação do talhão ao longo do tempo, mostra quando o solo fica descoberto | Earthdata Login (gratuito) |
| SMAP | Umidade do solo a 9 km | Earthdata Login, arquivos pesados (opcional) |
| SoilGrids | Estimativa de solo quando o produtor não tem análise | Aberto |
| ZARC (Embrapa) | Janelas oficiais de plantio por município, usado pra validar | Aberto |

**Limite conhecido:** o POWER trabalha em grade de cerca de 50 km. Ele descreve o clima da região do talhão, não diferencia talhões vizinhos. O que é específico do talhão vem do NDVI e do que o produtor informa.

## Base agronômica

Tabela pequena e bem feita, com 6 a 8 culturas do Cerrado: soja, milho safrinha, sorgo, braquiária, milheto, crotalária e consórcio milho com braquiária.

Para cada cultura: duração do ciclo, exigência de água, tolerância a veranico e calor, cobertura de solo que deixa, efeito no nitrogênio e janela de plantio.

Rotações comparadas no protótipo:

1. Soja e milho safrinha (a atual da maioria).
2. Soja e sorgo.
3. Soja e milho consorciado com braquiária.
4. Soja e planta de cobertura (crotalária ou milheto).

Começa como tabela simples. Se sobrar tempo, vira uma base em que cada regra aponta para a fonte que a sustenta.

## Interface

- Conversa guiada no estilo WhatsApp (o produtor já vive lá), com perguntas fixas e botões. No protótipo é uma tela web que simula o chat, sem integração real com o WhatsApp.
- Cartões comparando as 3 rotações e um gráfico do início e fim das chuvas ano a ano.
- Identidade visual própria e conteúdo real (mapa do talhão, números reais), sem cara de template.

## Stack do protótipo

- Núcleo em Python (pandas e SciPy): dados da NASA, indicadores e motor de regras.
- Interface em Streamlit, rodando local no notebook. Tudo gratuito, sem serviço externo.
- Código escrito com agentes de IA (Claude Code), com testes automáticos.
- O núcleo não depende da interface: se o time quiser outro front depois, ele reaproveita o motor.

## O que fica de fora do protótipo

- Integração real com WhatsApp.
- Recomendação de adubação, defensivo ou cultivar.
- Cobertura nacional. O recorte é o Cerrado, com um talhão de exemplo.
- Previsão do tempo. A ferramenta trabalha com histórico e tendência.

## Como a gente prova que funciona

- Comparar as janelas que o sistema calcula com as do ZARC para o mesmo município.
- Rodar em 2 ou 3 pontos com clima diferente e conferir se a recomendação muda no sentido esperado.
- Deixar registrado um log de validação pra mostrar no pitch.
- Aviso na tela: a ferramenta apoia a decisão, quem decide é o produtor com o agrônomo dele.

## Riscos e como tratar

| Risco | Tratamento |
|---|---|
| API lenta ou internet caindo na demo | Dados do talhão de exemplo baixados antes e guardados em cache, mais um vídeo gravado de reserva |
| Dado da NASA virar enfeite | Cada nota mostra qual indicador a gerou. Sem dado, sem nota |
| Regras agronômicas erradas | Base pequena, com fonte por regra, revisada por alguém da área |
| Escopo estourar | Uma pergunta, um talhão, uma tela. O resto é extra |
| Produtor sem análise de solo | SoilGrids como estimativa, marcado na tela como estimativa |

## Divisão sugerida

- **Dados**: baixar e tratar as séries, calcular os indicadores.
- **Regras e validação**: base agronômica, pontuação, conferência com o ZARC.
- **App**: tela de conversa, cartões e gráfico.
- **Pitch**: roteiro, vídeo de 30 segundos e apresentação.

## Cronograma

- **Sábado de manhã**: fechar escopo e papéis, ter o dado do POWER rodando pro talhão de exemplo.
- **Sábado à tarde**: indicadores e base agronômica prontos, primeira pontuação funcionando.
- **Sábado à noite**: tela ligada na pontuação, de ponta a ponta, mesmo feia.
- **Domingo de manhã**: validação, acabamento visual e vídeo de reserva.
- **Domingo à tarde**: parar de construir, ensaiar o pitch e enviar o projeto.

## Decisões em aberto

1. Qual talhão de exemplo usar, e se as coordenadas reais aparecem ou ficam aproximadas.
2. Confirmar a stack com o time (o repositório já roda em Python + Streamlit).
3. Se entra IA generativa na explicação ou se o texto é montado por modelo fixo.
4. Conferir a regra deste ano sobre declarar uso de IA no envio.
