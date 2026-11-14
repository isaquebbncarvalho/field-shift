# Instruções para agentes de código (Claude Code e similares)

## O projeto

Protótipo do desafio NASA Space Apps 2026 "Field Shift: Adapting Farms with NASA Data". Ferramenta de apoio à decisão que compara rotações de cultura no Cerrado (soja + segunda safra) usando o histórico de clima da NASA POWER, uma base agronômica em JSON e as prioridades do produtor. Leia `README.md` e `docs/metodo.md` antes de mudar qualquer lógica.

Prazo: hackathon de 48 horas (14 e 15/11/2026). Prefira o simples que funciona.

## Regras que não mudam

1. **O motor de regras decide a nota.** `fieldshift/motor.py` é determinístico. Texto (modelo fixo ou IA) só explica; nunca escolhe rotação.
2. **Toda nota tem evidência.** Se adicionar critério, adicione a `Evidencia` correspondente com fonte. Há teste para isso.
3. **Nunca invente número.** Valor agronômico novo entra em `data/conhecimento/culturas.json` com `"validado": false` e `fonte_sugerida`. Quem valida é a pessoa de agronomia do time.
4. **Demo funciona sem internet.** Novos pontos são baixados antes com `scripts/baixar_dados.py`. Não coloque chamada de rede no caminho da demo sem cache.
5. **Português** em textos de interface, comentários e docs.

## Comandos

```bash
pip install -r requirements.txt
python -m pytest -q                     # tem que passar antes de qualquer commit
streamlit run app/streamlit_app.py      # app em http://localhost:8501
python scripts/baixar_dados.py LAT LON  # cachear um ponto novo
```

Para testar o app sem navegador:

```python
from streamlit.testing.v1 import AppTest
at = AppTest.from_file("app/streamlit_app.py", default_timeout=120).run()
assert not at.exception
```

## Mapa do código

- `fieldshift/power.py`: cliente da API NASA POWER com cache (`data/cache/`, fora do git).
- `fieldshift/indicadores.py`: início/fim das chuvas, veranicos, calor, tendência (Mann-Kendall). Critérios em `Criterios`.
- `fieldshift/conhecimento.py`: carrega `data/conhecimento/*.json`.
- `fieldshift/motor.py`: simula a 2ª safra ano a ano e calcula as 4 notas (renda, solo, água, risco).
- `fieldshift/explicar.py`: frases em português a partir do resultado.
- `fieldshift/locais.py`: municípios de exemplo com dados em `data/exemplo/`.
- `app/streamlit_app.py`: interface.

## Streamlit

- O script roda de novo a cada interação: dados e indicadores usam `st.cache_data`.
- Use `width="stretch"` (não `use_container_width`).
- Estilo fica no bloco `<style>` do topo do app e em `.streamlit/config.toml`. Evite visual genérico: nada de gradiente decorativo, emoji como ícone de seção ou cards todos iguais.

## Definição de pronto

Testes passando, `AppTest` sem exceção, e o resultado conferido à mão em pelo menos um município. Mudou critério ou valor agronômico? Registre em `docs/validacao.md`.

## Ferramentas

O `.mcp.json` traz dois servidores MCP de dados da NASA (Space Data Atlas e Earthdata, oficial). Skills recomendadas e como instalar: `setup/ferramentas.md`.
