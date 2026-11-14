"""Carrega a base agronômica (culturas e rotações) dos arquivos JSON."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

PASTA = Path(__file__).resolve().parent.parent / "data" / "conhecimento"


@dataclass(frozen=True)
class Cultura:
    id: str
    nome: str
    papel: str
    ciclo_dias: int
    observacoes: str = ""
    fonte_sugerida: str = ""
    validado: bool = False
    atraso_semeadura_dias: int = 0
    dias_criticos: int = 0
    chuva_min_fase_critica_mm: float = 0.0
    data_limite_semeadura: str = "12-31"
    economia_agua: int = 3
    tolerancia_seca: int = 3
    tolerancia_calor: int = 3
    cobertura_solo_seca: int = 3
    palhada: int = 3
    fixa_nitrogenio: bool = False
    renda_direta: int = 3


@dataclass(frozen=True)
class Rotacao:
    id: str
    nome: str
    verao: str
    segunda: str
    atual_padrao: bool = False


@dataclass
class Base:
    culturas: dict[str, Cultura] = field(default_factory=dict)
    rotacoes: list[Rotacao] = field(default_factory=list)

    def rotacao(self, rotacao_id: str) -> Rotacao:
        for r in self.rotacoes:
            if r.id == rotacao_id:
                return r
        raise KeyError(rotacao_id)

    @property
    def pendentes_validacao(self) -> list[str]:
        return [c.nome for c in self.culturas.values() if not c.validado]


def carregar_base(pasta: Path | None = None) -> Base:
    pasta = pasta or PASTA
    with open(pasta / "culturas.json", encoding="utf-8") as f:
        culturas = json.load(f)["culturas"]
    with open(pasta / "rotacoes.json", encoding="utf-8") as f:
        rotacoes = json.load(f)["rotacoes"]
    base = Base(
        culturas={c["id"]: Cultura(**c) for c in culturas},
        rotacoes=[Rotacao(**r) for r in rotacoes],
    )
    for r in base.rotacoes:
        for cid in (r.verao, r.segunda):
            if cid not in base.culturas:
                raise ValueError(f"Rotação {r.id} cita cultura inexistente: {cid}")
    return base
