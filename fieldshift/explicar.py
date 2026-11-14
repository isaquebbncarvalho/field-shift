"""Explicação em linguagem simples, montada por modelo fixo a partir da evidência.

Não usa IA e não decide nada: só descreve o que o motor de regras calculou.
"""

from __future__ import annotations

from .indicadores import Tendencia
from .motor import CRITERIOS, Avaliacao


def _num(x: float, casas: int = 1) -> str:
    return f"{x:.{casas}f}".replace(".", ",")


def explicar_rotacao(av: Avaliacao, prioridades: dict[str, float], atual: bool) -> str:
    pesados = sorted(CRITERIOS, key=lambda k: prioridades.get(k, 0), reverse=True)
    melhor = max(pesados[:3], key=lambda k: av.notas[k])
    pior = min(pesados[:3], key=lambda k: av.notas[k])
    partes = [
        f"**{av.nome}** ficou com nota **{_num(av.nota_geral)}**"
        + (" (é a sua rotação atual)." if atual else "."),
        f"Ponto forte: {CRITERIOS[melhor].lower()} ({_num(av.notas[melhor])}).",
    ]
    if pior != melhor:
        partes.append(f"Ponto fraco: {CRITERIOS[pior].lower()} ({_num(av.notas[pior])}).")
    if av.falha_recente >= 0.4:
        partes.append(
            f"Atenção: em {av.falha_recente:.0%} das últimas safras a 2ª safra teria problema "
            "por falta de chuva ou plantio fora da janela."
        )
    elif av.falha_recente <= 0.1:
        partes.append("Clima recente favorável para essa 2ª safra.")
    return " ".join(partes)


def _sentido(t: Tendencia, positivo: str, negativo: str) -> str:
    return positivo if t.inclinacao_por_decada > 0 else negativo


def explicar_clima(tendencias: dict[str, Tendencia], local: str, periodo: str) -> list[str]:
    frases = []
    t = tendencias.get("chuva_estacao_mm")
    if t:
        base = (
            f"Chuva na estação chuvosa em {local} ({periodo}): "
            f"{_sentido(t, 'subiu', 'caiu')} cerca de {abs(t.inclinacao_por_decada):.0f} mm por década"
        )
        frases.append(base + (" — tendência estatisticamente significativa." if t.significativa else " — sem tendência significativa."))
    t = tendencias.get("fim_dia_safra")
    if t:
        frases.append(
            f"Fim das chuvas: {_sentido(t, 'mais tarde', 'mais cedo')} em cerca de "
            f"{abs(t.inclinacao_por_decada):.0f} dias por década"
            + (" (significativo)." if t.significativa else " (não significativo).")
        )
    t = tendencias.get("dias_calor")
    if t:
        frases.append(
            f"Dias com máxima acima do limite: {_sentido(t, 'aumentaram', 'diminuíram')} cerca de "
            f"{abs(t.inclinacao_por_decada):.0f} por década"
            + (" (significativo)." if t.significativa else " (não significativo).")
        )
    return frases
