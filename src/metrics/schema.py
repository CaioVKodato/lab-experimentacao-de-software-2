"""Modelo de uma linha de métricas estáticas."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class MetricsRow:
    trial_id: str
    diretorio: str
    loc: int
    cc_mean: float
    mi_mean: float
    duplication_pct: float
    coletado_em: str

    def to_row(self) -> dict[str, str]:
        row = asdict(self)
        row["loc"] = str(self.loc)
        row["cc_mean"] = f"{self.cc_mean:.4f}"
        row["mi_mean"] = f"{self.mi_mean:.4f}"
        row["duplication_pct"] = f"{self.duplication_pct:.4f}"
        return row
