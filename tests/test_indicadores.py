import numpy as np
import pandas as pd

from fieldshift.indicadores import (
    fim_chuvas,
    indicadores_por_safra,
    inicio_chuvas,
    tendencia,
)


def serie_sintetica(inicio="2010-10-10", fim="2011-03-31", mm=10.0, falso_inicio=None):
    datas = pd.date_range("2010-07-01", "2011-06-30", freq="D")
    chuva = pd.Series(0.0, index=datas)
    chuva[inicio:fim] = mm
    if falso_inicio:
        chuva[falso_inicio] = 40.0
    df = pd.DataFrame({"chuva_mm": chuva, "temp_max_c": 30.0})
    return df


def test_inicio_e_fim_em_estacao_bem_definida():
    df = serie_sintetica()
    assert inicio_chuvas(df["chuva_mm"], 2010) == pd.Timestamp("2010-10-10")
    assert fim_chuvas(df["chuva_mm"], 2010) == pd.Timestamp("2011-04-01")


def test_falso_inicio_e_ignorado():
    df = serie_sintetica(falso_inicio="2010-09-05")
    assert inicio_chuvas(df["chuva_mm"], 2010) == pd.Timestamp("2010-10-10")


def test_sem_chuva_nao_define_inicio():
    df = serie_sintetica(mm=0.0)
    assert pd.isna(inicio_chuvas(df["chuva_mm"], 2010))


def test_indicadores_por_safra_monta_linha():
    df = serie_sintetica()
    ind = indicadores_por_safra(df, 2010, 2010)
    assert len(ind) == 1
    linha = ind.iloc[0]
    assert linha["safra"] == "2010/11"
    assert linha["duracao_dias"] == (pd.Timestamp("2011-04-01") - pd.Timestamp("2010-10-10")).days
    assert linha["maior_veranico_dias"] == 0


def test_tendencia_detecta_queda():
    anos = pd.Series(range(2001, 2025))
    valores = pd.Series(1500 - 15 * np.arange(24) + np.random.default_rng(1).normal(0, 20, 24))
    t = tendencia(valores, anos, "chuva")
    assert t.inclinacao_por_decada < -100
    assert t.significativa
