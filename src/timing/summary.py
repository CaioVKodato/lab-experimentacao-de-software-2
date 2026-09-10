"""Resumo descritivo da RQ1/RQ2: mediana e IQR (não média)."""

from __future__ import annotations

from statistics import median

from src.timing.constants import TRATAMENTOS
from src.timing.store import read_trials


def _iqr(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    ordered = sorted(values)
    mid = len(ordered) // 2
    lower = ordered[:mid]
    upper = ordered[mid:] if len(ordered) % 2 == 0 else ordered[mid + 1 :]
    if not lower or not upper:
        return 0.0
    return round(median(upper) - median(lower), 4)


def by_treatment(rows: list[dict[str, str]] | None = None) -> list[dict[str, float | int | str]]:
    rows = rows if rows is not None else read_trials()
    out: list[dict[str, float | int | str]] = []
    for tratamento in TRATAMENTOS:
        subset = [row for row in rows if row.get("tratamento") == tratamento]
        tempos = [float(row["tempo_s"]) for row in subset if row.get("tempo_s")]
        taxas = [float(row["taxa_sucesso"]) for row in subset if row.get("taxa_sucesso")]
        censurados = sum(1 for row in subset if row.get("censurado") == "true")
        out.append(
            {
                "tratamento": tratamento,
                "n": len(subset),
                "censurados": censurados,
                "tempo_s_mediana": median(tempos) if tempos else 0.0,
                "tempo_s_iqr": _iqr(tempos),
                "taxa_sucesso_mediana": median(taxas) if taxas else 0.0,
                "taxa_sucesso_iqr": _iqr(taxas),
            }
        )
    return out
