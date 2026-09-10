"""Constantes do módulo de métricas estáticas (RQ3)."""

from __future__ import annotations

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
METRICS_CSV = DATA_DIR / "metrics.csv"

FIELDNAMES = (
    "trial_id",
    "diretorio",
    "loc",
    "cc_mean",
    "mi_mean",
    "duplication_pct",
    "coletado_em",
)
