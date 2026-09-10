"""Coleta de métricas estáticas de código (RQ3): CC, MI, duplicação, LOC."""

from src.metrics.collector import collect_metrics
from src.metrics.schema import MetricsRow

__all__ = ["MetricsRow", "collect_metrics"]
