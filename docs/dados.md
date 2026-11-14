# Dados

## Em uso no protótipo

### NASA POWER (principal)

- API diária por ponto, sem login e sem chave: `https://power.larc.nasa.gov/api/temporal/daily/point`
- Parâmetros: `PRECTOTCORR, T2M, T2M_MAX, T2M_MIN, ALLSKY_SFC_SW_DWN, GWETTOP, GWETROOT, RH2M`, comunidade `AG`.
- Valor ausente: `-999` (convertido para vazio no código).
- Já baixado em `data/exemplo/` para Rio Verde, Jataí, Sorriso e Luís Eduardo Magalhães (2000–2025).
- Documentação: https://power.larc.nasa.gov/docs/services/api/

Exemplo direto no navegador:

```
https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR&community=AG&latitude=-17.79&longitude=-50.92&start=20240101&end=20240131&format=JSON
```

## Para evoluir (se sobrar tempo)

| Fonte | Para quê | Acesso |
|---|---|---|
| GPM IMERG (chuva diária ~10 km) | Conferir e melhorar a chuva do POWER | Earthdata Login (gratuito) |
| HLS ou MODIS NDVI | Ver quando o solo do talhão fica descoberto | Earthdata Login |
| SMAP (umidade do solo 9 km) | Conferir umidade do solo | Earthdata Login, arquivos pesados |
| SoilGrids | Estimar textura do solo sem análise | Aberto |
| ZARC (MAPA/Embrapa) | Validar janelas de plantio por município | Aberto |
| INMET (estações) | Validar chuva do POWER | Aberto |

Criar conta no Earthdata: https://urs.earthdata.nasa.gov/users/new

A biblioteca Python `earthaccess` busca e baixa esses produtos depois do login. Exemplos prontos para cada dataset: https://spacedata.swapniltamse.com/challenges/field-shift-adapting-farms/

## Regra

Dado novo entra primeiro em cache (`scripts/baixar_dados.py` ou um script em `scripts/`) e só depois no app. A demo não pode depender de download ao vivo.
