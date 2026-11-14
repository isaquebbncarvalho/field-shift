"""Pontos de exemplo com dados da NASA já baixados em data/exemplo.

Coordenadas aproximadas da sede de cada município (não de propriedades).
Servem para a demo funcionar sem internet e para comparar climas diferentes.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .power import EXEMPLO_DIR, baixar_power, ler_csv


@dataclass(frozen=True)
class Local:
    id: str
    nome: str
    lat: float
    lon: float

    @property
    def arquivo_exemplo(self) -> Path:
        return EXEMPLO_DIR / f"{self.id}_2000-2025.csv.gz"


LOCAIS = [
    Local("rio-verde-go", "Rio Verde – GO", -17.79, -50.92),
    Local("jatai-go", "Jataí – GO", -17.88, -51.72),
    Local("sorriso-mt", "Sorriso – MT", -12.55, -55.71),
    Local("luis-eduardo-magalhaes-ba", "Luís Eduardo Magalhães – BA", -12.09, -45.80),
]


def carregar_local(local: Local) -> pd.DataFrame:
    if local.arquivo_exemplo.exists():
        return ler_csv(local.arquivo_exemplo)
    return baixar_power(local.lat, local.lon, 2000, 2025)


def carregar_coordenada(lat: float, lon: float) -> pd.DataFrame:
    for local in LOCAIS:
        if abs(local.lat - lat) < 0.01 and abs(local.lon - lon) < 0.01:
            return carregar_local(local)
    return baixar_power(lat, lon, 2000, 2025)
