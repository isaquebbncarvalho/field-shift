"""Checagens de sanidade com os dados reais da NASA guardados em data/exemplo."""

import numpy as np

from fieldshift.indicadores import indicadores_por_safra
from fieldshift.locais import LOCAIS, carregar_local


def test_exemplos_existem_e_tem_serie_completa():
    for local in LOCAIS:
        df = carregar_local(local)
        assert df.index.min().year <= 2001
        assert df.index.max().year >= 2025
        assert df["chuva_mm"].isna().mean() < 0.01


def test_rio_verde_inicio_mediano_das_chuvas_em_outubro():
    df = carregar_local(LOCAIS[0])
    ind = indicadores_por_safra(df, 2001, 2024)
    mediana = np.nanmedian(ind["inicio_dia_safra"])  # 1 = 1º de julho
    # 1º/out = dia 93, 31/out = dia 123
    assert 93 <= mediana <= 123
