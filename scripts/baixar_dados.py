"""Baixa e guarda em cache a série da NASA POWER para usar sem internet.

Uso:
    python scripts/baixar_dados.py                 # todos os locais de exemplo
    python scripts/baixar_dados.py -17.79 -50.92   # um ponto qualquer

Os 4 locais de exemplo já vêm no repositório (data/exemplo). Use este script
para o talhão de vocês ou para novos municípios, ANTES da demo.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from fieldshift.locais import LOCAIS  # noqa: E402
from fieldshift.power import baixar_power, salvar_csv  # noqa: E402


def main(argv: list[str]) -> None:
    if len(argv) == 2:
        lat, lon = float(argv[0]), float(argv[1])
        df = baixar_power(lat, lon, 2000, 2025)
        print(f"OK: {len(df)} dias para ({lat}, {lon}) guardados em data/cache/")
        return
    for local in LOCAIS:
        if local.arquivo_exemplo.exists():
            print(f"já existe: {local.nome}")
            continue
        df = baixar_power(local.lat, local.lon, 2000, 2025)
        salvar_csv(df, local.arquivo_exemplo)
        print(f"baixado: {local.nome} ({len(df)} dias)")


if __name__ == "__main__":
    main(sys.argv[1:])
