"""Motor de regras: cruza os indicadores da NASA com a base agronômica e as
prioridades do produtor e devolve uma nota por rotação, com a evidência de cada
número.

Regra de projeto: quem decide a nota é este motor, que é determinístico e
auditável. Texto gerado (por modelo fixo ou IA) só explica o resultado.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .conhecimento import Base, Cultura, Rotacao

CRITERIOS = {
    "renda": "Renda esperada",
    "solo": "Proteção do solo",
    "agua": "Economia de água",
    "risco": "Segurança climática",
}

PRIORIDADES_PADRAO = {"renda": 4, "solo": 3, "agua": 1, "risco": 4}

SAFRAS_RECENTES = 10
INTERVALO_COLHEITA_PLANTIO_DIAS = 1
# Numa safra "com problema" a lavoura perde parte da produção, não toda.
# 0,5 = metade da renda esperada. Valor de partida, a validar.
PERDA_EM_SAFRA_PROBLEMA = 0.5


@dataclass
class Evidencia:
    criterio: str
    texto: str
    fonte: str


@dataclass
class Avaliacao:
    rotacao: Rotacao
    cultura: Cultura
    notas: dict[str, float]
    nota_geral: float
    por_safra: pd.DataFrame
    falha_total: float
    falha_recente: float
    n_safras: int
    n_recentes: int
    evidencias: list[Evidencia] = field(default_factory=list)

    @property
    def nome(self) -> str:
        return self.rotacao.nome


def _data_limite(ano_safra: int, mm_dd: str) -> pd.Timestamp:
    return pd.Timestamp(f"{ano_safra + 1}-{mm_dd}")


def simular_segunda_safra(
    df: pd.DataFrame, ind: pd.DataFrame, soja: Cultura, cultura: Cultura
) -> pd.DataFrame:
    """Para cada safra, estima a semeadura da 2ª safra e checa janela e água."""
    chuva = df["chuva_mm"]
    linhas = []
    for _, s in ind.iterrows():
        linha = {"safra": s["safra"], "ano": s["ano"]}
        if pd.isna(s["inicio_chuvas"]):
            linha.update(
                semeadura_soja=pd.NaT,
                semeadura_segunda=pd.NaT,
                chuva_fase_critica_mm=np.nan,
                janela_umida_dias=np.nan,
                fora_da_janela=True,
                agua_insuficiente=True,
                falha=True,
                motivo="estação chuvosa sem início definido",
            )
            linhas.append(linha)
            continue
        sem_soja = s["inicio_chuvas"] + pd.Timedelta(days=soja.atraso_semeadura_dias)
        colheita = sem_soja + pd.Timedelta(days=soja.ciclo_dias)
        sem_seg = colheita + pd.Timedelta(days=INTERVALO_COLHEITA_PLANTIO_DIAS)
        limite = _data_limite(int(s["ano"]), cultura.data_limite_semeadura)
        fora = bool(sem_seg > limite)
        fim_critico = sem_seg + pd.Timedelta(days=cultura.dias_criticos - 1)
        chuva_critica = float(chuva[sem_seg:fim_critico].sum())
        pouca_agua = bool(chuva_critica < cultura.chuva_min_fase_critica_mm)
        motivos = []
        if fora:
            motivos.append("semeadura depois do limite")
        if pouca_agua:
            motivos.append("pouca chuva na fase crítica")
        linha.update(
            semeadura_soja=sem_soja,
            semeadura_segunda=sem_seg,
            chuva_fase_critica_mm=chuva_critica,
            janela_umida_dias=(s["fim_chuvas"] - sem_seg).days if pd.notna(s["fim_chuvas"]) else np.nan,
            fora_da_janela=fora,
            agua_insuficiente=pouca_agua,
            falha=fora or pouca_agua,
            motivo="; ".join(motivos) if motivos else "ok",
        )
        linhas.append(linha)
    return pd.DataFrame(linhas)


def _nota_solo(c: Cultura) -> float:
    n = 5 if c.fixa_nitrogenio else 1
    return round((0.5 * c.cobertura_solo_seca + 0.3 * c.palhada + 0.2 * n) * 2, 1)


def _fmt_data(d: pd.Timestamp) -> str:
    return d.strftime("%d/%m") if pd.notna(d) else "—"


def _dia_mediano(datas: pd.Series) -> pd.Timestamp:
    """Data mediana ignorando o ano (usa dia do ano agrícola)."""
    datas = datas.dropna()
    if datas.empty:
        return pd.NaT
    ref = []
    for d in datas:
        ano = d.year if d.month >= 7 else d.year - 1
        ref.append((d - pd.Timestamp(f"{ano}-07-01")).days)
    mediana = float(np.median(ref))
    return pd.Timestamp("2001-07-01") + pd.Timedelta(days=mediana)


def avaliar_rotacao(
    df: pd.DataFrame,
    ind: pd.DataFrame,
    base: Base,
    rotacao: Rotacao,
    prioridades: dict[str, float] | None = None,
    fonte: str = "NASA POWER",
) -> Avaliacao:
    prioridades = prioridades or PRIORIDADES_PADRAO
    soja = base.culturas[rotacao.verao]
    cultura = base.culturas[rotacao.segunda]
    sim = simular_segunda_safra(df, ind, soja, cultura)

    recentes = sim.tail(SAFRAS_RECENTES)
    falha_total = float(sim["falha"].mean()) if len(sim) else float("nan")
    falha_recente = float(recentes["falha"].mean()) if len(recentes) else float("nan")

    notas = {
        "risco": round(10 * (1 - falha_recente), 1),
        "agua": float(2 * cultura.economia_agua),
        "solo": _nota_solo(cultura),
        "renda": round(2 * cultura.renda_direta * (1 - PERDA_EM_SAFRA_PROBLEMA * falha_recente), 1),
    }
    pesos = {k: float(prioridades.get(k, 0)) for k in CRITERIOS}
    soma = sum(pesos.values()) or 1.0
    geral = round(sum(notas[k] * pesos[k] for k in CRITERIOS) / soma, 1)

    periodo = f"{sim['safra'].iloc[0]}–{sim['safra'].iloc[-1]}" if len(sim) else "—"
    periodo_rec = f"{recentes['safra'].iloc[0]}–{recentes['safra'].iloc[-1]}" if len(recentes) else "—"
    n_falhas_rec = int(recentes["falha"].sum())
    n_agua_rec = int(recentes["agua_insuficiente"].sum())
    n_fora_rec = int(recentes["fora_da_janela"].sum())
    chuva_med = float(recentes["chuva_fase_critica_mm"].median())
    p20, p80 = (
        np.nanpercentile(recentes["chuva_fase_critica_mm"], [20, 80])
        if recentes["chuva_fase_critica_mm"].notna().any()
        else (np.nan, np.nan)
    )
    sem_med = _dia_mediano(recentes["semeadura_segunda"])
    limite_txt = cultura.data_limite_semeadura[3:] + "/" + cultura.data_limite_semeadura[:2]

    evid = [
        Evidencia(
            "risco",
            f"Em {n_falhas_rec} das últimas {len(recentes)} safras ({periodo_rec}) a {cultura.nome.lower()} "
            f"teria problema: {n_agua_rec} por chuva abaixo de {cultura.chuva_min_fase_critica_mm:.0f} mm "
            f"nos {cultura.dias_criticos} dias após a semeadura e {n_fora_rec} por semeadura depois do limite "
            f"({limite_txt}). Na série inteira ({periodo}) a taxa de problema foi {falha_total:.0%}.",
            f"{fonte} (chuva diária) + base agronômica",
        ),
        Evidencia(
            "risco",
            f"Semeadura estimada da 2ª safra: mediana {_fmt_data(sem_med)}, considerando soja de "
            f"{soja.ciclo_dias} dias semeada {soja.atraso_semeadura_dias} dias após o início das chuvas. "
            f"Chuva na fase crítica: mediana {chuva_med:.0f} mm (20% dos anos abaixo de {p20:.0f} mm, "
            f"20% acima de {p80:.0f} mm).",
            f"{fonte} (chuva diária)",
        ),
        Evidencia(
            "solo",
            f"Cobertura na seca {cultura.cobertura_solo_seca}/5, palhada {cultura.palhada}/5"
            + (", fixa nitrogênio" if cultura.fixa_nitrogenio else "")
            + ".",
            "Base agronômica" + ("" if cultura.validado else " (valor inicial, a validar)"),
        ),
        Evidencia(
            "agua",
            f"Economia de água {cultura.economia_agua}/5 e tolerância a seca {cultura.tolerancia_seca}/5.",
            "Base agronômica" + ("" if cultura.validado else " (valor inicial, a validar)"),
        ),
        Evidencia(
            "renda",
            f"Potencial de renda direta {cultura.renda_direta}/5, descontado pelo risco climático recente "
            f"({falha_recente:.0%} de safras com problema, cada uma perdendo "
            f"{PERDA_EM_SAFRA_PROBLEMA:.0%} da renda).",
            "Base agronômica + " + fonte,
        ),
    ]

    return Avaliacao(
        rotacao=rotacao,
        cultura=cultura,
        notas=notas,
        nota_geral=geral,
        por_safra=sim,
        falha_total=falha_total,
        falha_recente=falha_recente,
        n_safras=len(sim),
        n_recentes=len(recentes),
        evidencias=evid,
    )


def comparar(
    df: pd.DataFrame,
    ind: pd.DataFrame,
    base: Base,
    prioridades: dict[str, float] | None = None,
    fonte: str = "NASA POWER",
) -> list[Avaliacao]:
    """Avalia todas as rotações e devolve da maior para a menor nota."""
    avaliacoes = [avaliar_rotacao(df, ind, base, r, prioridades, fonte) for r in base.rotacoes]
    return sorted(avaliacoes, key=lambda a: a.nota_geral, reverse=True)


def selecionar_tres(avaliacoes: list[Avaliacao], atual_id: str) -> list[Avaliacao]:
    """As duas melhores alternativas mais a rotação atual do produtor."""
    atual = next(a for a in avaliacoes if a.rotacao.id == atual_id)
    outras = [a for a in avaliacoes if a.rotacao.id != atual_id][:2]
    return sorted([atual, *outras], key=lambda a: a.nota_geral, reverse=True)
