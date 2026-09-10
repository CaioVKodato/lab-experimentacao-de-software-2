"""Persistência do CSV de métricas estáticas."""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

from src.metrics.constants import FIELDNAMES, METRICS_CSV
from src.metrics.schema import MetricsRow


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def ensure_csv(path: Path = METRICS_CSV) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.stat().st_size == 0:
        with path.open("w", newline="", encoding="utf-8") as handle:
            csv.DictWriter(handle, fieldnames=FIELDNAMES).writeheader()
    return path


def read_metrics(path: Path = METRICS_CSV) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_metrics(row: MetricsRow, path: Path = METRICS_CSV) -> Path:
    ensure_csv(path)
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writerow(row.to_row())
    return path
