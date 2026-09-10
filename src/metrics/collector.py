"""Orquestrador: coleta LOC, CC, MI e duplicação de um diretório de trial."""

from __future__ import annotations

from pathlib import Path

from src.metrics.jscpd_runner import compute_duplication
from src.metrics.loc import count_loc
from src.metrics.radon_runner import compute_cc, compute_mi
from src.metrics.schema import MetricsRow
from src.metrics.store import now_iso


def collect_metrics(directory: Path, trial_id: str = "") -> MetricsRow:
    """Coleta todas as métricas estáticas do diretório e retorna um MetricsRow."""
    directory = directory.resolve()
    return MetricsRow(
        trial_id=trial_id,
        diretorio=str(directory),
        loc=count_loc(directory),
        cc_mean=compute_cc(directory),
        mi_mean=compute_mi(directory),
        duplication_pct=compute_duplication(directory),
        coletado_em=now_iso(),
    )
