"""Indicadores agroclimáticos por safra a partir da série diária do POWER.

Uma safra vai de 1º de julho do ano Y a 30 de junho de Y+1 e é rotulada "Y/Y+1".

Todos os critérios ficam em `Criterios` para que o time possa ajustar e
justificar cada número no pitch. Os valores padrão foram conferidos contra a
série de Rio Verde-GO (início mediano das chuvas em meados de outubro) e devem
ser validados com o ZARC da Embrapa. Ver docs/metodo.md.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats


@dataclass(frozen=True)
class Criterios:
    # Início da estação chuvosa: primeiro dia, a partir de 1º/set, em que caem
    # pelo menos `inicio_chuva_mm` em `inicio_janela_dias` dias (com chuva no
    # próprio dia) e que NÃO é seguido de veranico de `inicio_veranico_dias`
    # ou mais nos `inicio_checagem_dias` seguintes (evita "falso início").
    inicio_busca: str = "09-01"
    inicio_limite: str = "12-31"
    inicio_chuva_mm: float = 30.0
    inicio_janela_dias: int = 5
    inicio_veranico_dias: int = 7
    inicio_checagem_dias: int = 30

    # Fim da estação chuvosa: primeiro dia, a partir de 15/fev, que abre um
    # período de `fim_janela_dias` dias com menos de `fim_chuva_mm` de chuva.
    fim_busca: str = "02-15"
    fim_janela_dias: int = 20
    fim_chuva_mm: float = 10.0

    # Dia seco: chuva abaixo deste valor.
    dia_seco_mm: float = 1.0

    # Veranico: sequência de dias secos dentro da estação chuvosa.
    veranico_min_dias: int = 10

    # Calor: dias com máxima igual ou acima deste valor dentro da estação.
    calor_limite_c: float = 34.0


CRITERIOS_PADRAO = Criterios()


def rotulo_safra(ano_inicio: int) -> str:
    return f"{ano_inicio}/{str(ano_inicio + 1)[-2:]}"


def _maior_sequencia_seca(valores: np.ndarray, limite: float) -> int:
    maior = atual = 0
    for v in valores:
        atual = atual + 1 if v < limite else 0
        maior = max(maior, atual)
    return maior


def _sequencias_secas(valores: np.ndarray, limite: float, minimo: int) -> int:
    contagem = atual = 0
    for v in valores:
        if v < limite:
            atual += 1
        else:
            if atual >= minimo:
                contagem += 1
            atual = 0
    if atual >= minimo:
        contagem += 1
    return contagem


def inicio_chuvas(chuva: pd.Series, ano: int, c: Criterios = CRITERIOS_PADRAO) -> pd.Timestamp:
    trecho = chuva[f"{ano}-{c.inicio_busca}":f"{ano}-{c.inicio_limite}"]
    # Precisa de dados além do limite para checar veranico depois do início.
    extendido = chuva[f"{ano}-{c.inicio_busca}":].iloc[: len(trecho) + c.inicio_checagem_dias]
    v = extendido.to_numpy()
    for i in range(len(trecho)):
        if v[i] < c.dia_seco_mm:
            continue
        if v[i : i + c.inicio_janela_dias].sum() < c.inicio_chuva_mm:
            continue
        seguinte = v[i + 1 : i + c.inicio_checagem_dias]
        if len(seguinte) < c.inicio_checagem_dias - 1:
            break
        if _maior_sequencia_seca(seguinte, c.dia_seco_mm) < c.inicio_veranico_dias:
            return trecho.index[i]
    return pd.NaT


def fim_chuvas(chuva: pd.Series, ano: int, c: Criterios = CRITERIOS_PADRAO) -> pd.Timestamp:
    trecho = chuva[f"{ano + 1}-{c.fim_busca}":f"{ano + 1}-06-30"]
    v = trecho.to_numpy()
    for i in range(len(v) - c.fim_janela_dias + 1):
        if v[i : i + c.fim_janela_dias].sum() < c.fim_chuva_mm:
            return trecho.index[i]
    return trecho.index[-1] if len(trecho) else pd.NaT


def indicadores_por_safra(
    df: pd.DataFrame,
    ano_inicio: int | None = None,
    ano_fim: int | None = None,
    c: Criterios = CRITERIOS_PADRAO,
) -> pd.DataFrame:
    """Uma linha por safra com início/fim das chuvas, veranicos, calor e chuva total."""
    chuva = df["chuva_mm"]
    primeiro = ano_inicio or int(df.index.min().year)
    ultimo = ano_fim or int(df.index.max().year) - 1
    linhas = []
    for ano in range(primeiro, ultimo + 1):
        if chuva[f"{ano}-07-01":f"{ano + 1}-06-30"].count() < 330:
            continue  # safra com dados incompletos
        ini = inicio_chuvas(chuva, ano, c)
        fim = fim_chuvas(chuva, ano, c)
        linha = {
            "safra": rotulo_safra(ano),
            "ano": ano,
            "inicio_chuvas": ini,
            "fim_chuvas": fim,
            "inicio_definido": pd.notna(ini),
        }
        if pd.notna(ini) and pd.notna(fim) and fim > ini:
            # A estação vai do início até a véspera do fim (o fim já é o 1º dia seco).
            estacao = df.loc[ini : fim - pd.Timedelta(days=1)]
            v = estacao["chuva_mm"].to_numpy()
            linha.update(
                duracao_dias=(fim - ini).days,
                chuva_estacao_mm=float(np.nansum(v)),
                maior_veranico_dias=_maior_sequencia_seca(v, c.dia_seco_mm),
                n_veranicos=_sequencias_secas(v, c.dia_seco_mm, c.veranico_min_dias),
                dias_calor=int((estacao["temp_max_c"] >= c.calor_limite_c).sum()),
            )
        else:
            linha.update(
                duracao_dias=np.nan,
                chuva_estacao_mm=np.nan,
                maior_veranico_dias=np.nan,
                n_veranicos=np.nan,
                dias_calor=np.nan,
            )
        linhas.append(linha)
    resultado = pd.DataFrame(linhas)
    if resultado.empty:
        return resultado
    # Dia do ano agrícola (1 = 1º de julho) para comparar datas entre safras.
    resultado["inicio_dia_safra"] = [
        (d - pd.Timestamp(f"{a}-07-01")).days + 1 if pd.notna(d) else np.nan
        for d, a in zip(resultado["inicio_chuvas"], resultado["ano"])
    ]
    resultado["fim_dia_safra"] = [
        (d - pd.Timestamp(f"{a}-07-01")).days + 1 if pd.notna(d) else np.nan
        for d, a in zip(resultado["fim_chuvas"], resultado["ano"])
    ]
    return resultado


@dataclass(frozen=True)
class Tendencia:
    variavel: str
    inclinacao_por_decada: float
    p_valor: float
    n_safras: int

    @property
    def significativa(self) -> bool:
        return self.n_safras >= 10 and self.p_valor < 0.05


def tendencia(serie: pd.Series, anos: pd.Series, nome: str) -> Tendencia:
    """Tendência linear (por década) com teste de Mann-Kendall via tau de Kendall."""
    validos = serie.notna() & anos.notna()
    x = anos[validos].astype(float).to_numpy()
    y = serie[validos].astype(float).to_numpy()
    if len(x) < 3:
        return Tendencia(nome, float("nan"), float("nan"), len(x))
    inclinacao = float(np.polyfit(x, y, 1)[0]) * 10
    _, p = stats.kendalltau(x, y)
    return Tendencia(nome, inclinacao, float(p), len(x))


def resumo_tendencias(ind: pd.DataFrame) -> dict[str, Tendencia]:
    variaveis = {
        "inicio_dia_safra": "Início das chuvas (dias)",
        "fim_dia_safra": "Fim das chuvas (dias)",
        "duracao_dias": "Duração da estação (dias)",
        "chuva_estacao_mm": "Chuva na estação (mm)",
        "maior_veranico_dias": "Maior veranico (dias)",
        "dias_calor": "Dias de calor extremo",
    }
    return {
        chave: tendencia(ind[chave], ind["ano"], nome)
        for chave, nome in variaveis.items()
        if chave in ind
    }


def data_safra(ano: int, dia_safra: float) -> pd.Timestamp:
    """Converte dia do ano agrícola de volta para data."""
    return pd.Timestamp(f"{ano}-07-01") + pd.Timedelta(days=float(dia_safra) - 1)
