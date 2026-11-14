"""Cliente da API NASA POWER (série diária por ponto) com cache em disco.

A API é aberta, sem login, e devolve chuva, temperatura, radiação e umidade do
solo para qualquer coordenada. A grade é de cerca de 0,5 grau (~50 km), então o
dado descreve o clima da REGIÃO do talhão, não diferencia talhões vizinhos.

Docs: https://power.larc.nasa.gov/docs/services/api/
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import requests

POWER_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

# Parâmetro da NASA -> nome da coluna no projeto.
PARAMETROS = {
    "PRECTOTCORR": "chuva_mm",
    "T2M": "temp_media_c",
    "T2M_MAX": "temp_max_c",
    "T2M_MIN": "temp_min_c",
    "ALLSKY_SFC_SW_DWN": "radiacao_mj_m2",
    "GWETTOP": "umidade_solo_sup",
    "GWETROOT": "umidade_solo_raiz",
    "RH2M": "umidade_ar_pct",
}

VALOR_AUSENTE = -999.0
RAIZ = Path(__file__).resolve().parent.parent
CACHE_DIR = RAIZ / "data" / "cache"
EXEMPLO_DIR = RAIZ / "data" / "exemplo"


def json_para_df(dados: dict) -> pd.DataFrame:
    """Converte a resposta JSON da API em DataFrame diário indexado por data."""
    parametros = dados["properties"]["parameter"]
    df = pd.DataFrame(parametros)
    df.index = pd.to_datetime(df.index, format="%Y%m%d")
    df.index.name = "data"
    df = df.rename(columns=PARAMETROS)
    df = df.replace(VALOR_AUSENTE, float("nan"))
    colunas = [c for c in PARAMETROS.values() if c in df.columns]
    return df[colunas].sort_index()


def _arquivo_cache(lat: float, lon: float, ano_inicio: int, ano_fim: int, pasta: Path) -> Path:
    return pasta / f"power_{lat:.2f}_{lon:.2f}_{ano_inicio}-{ano_fim}.csv.gz"


def salvar_csv(df: pd.DataFrame, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(caminho, compression="gzip")


def ler_csv(caminho: Path) -> pd.DataFrame:
    df = pd.read_csv(caminho, index_col="data", parse_dates=["data"], compression="gzip")
    return df.sort_index()


def baixar_power(
    lat: float,
    lon: float,
    ano_inicio: int = 2001,
    ano_fim: int = 2025,
    pasta_cache: Path | None = None,
    timeout: int = 180,
) -> pd.DataFrame:
    """Baixa a série diária do POWER para um ponto, usando cache se existir.

    O cache evita depender da internet na hora da demo: rode
    `python scripts/baixar_dados.py` antes do evento.
    """
    pasta = pasta_cache or CACHE_DIR
    arquivo = _arquivo_cache(lat, lon, ano_inicio, ano_fim, pasta)
    if arquivo.exists():
        return ler_csv(arquivo)

    params = {
        "parameters": ",".join(PARAMETROS.keys()),
        "community": "AG",
        "latitude": f"{lat:.4f}",
        "longitude": f"{lon:.4f}",
        "start": f"{ano_inicio}0101",
        "end": f"{ano_fim}1231",
        "format": "JSON",
    }
    resposta = requests.get(POWER_URL, params=params, timeout=timeout)
    resposta.raise_for_status()
    df = json_para_df(resposta.json())
    salvar_csv(df, arquivo)
    return df


def carregar_json(caminho: Path) -> pd.DataFrame:
    """Lê uma resposta da API salva em disco (útil para testes e demos)."""
    with open(caminho, encoding="utf-8") as f:
        return json_para_df(json.load(f))
