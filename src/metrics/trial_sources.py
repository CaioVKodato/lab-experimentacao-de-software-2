"""Registro dos 18 trials S02 → caminho do ``solucao.py``.

Caio: ``trials/caio/...``
Henrique: ``trials/henrique/...``
Jonas: soluções commitadas em ``katas/kX/solucao.py`` (PR #37).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.metrics.constants import ROOT_DIR


@dataclass(frozen=True)
class TrialSource:
    trial_id: str
    integrante: str
    kata: str
    tratamento: str
    ordem: int
    issue: str
    solucao: Path


def _p(*parts: str) -> Path:
    return ROOT_DIR.joinpath(*parts)


# Tratamentos reais (pasta/issue), não o cronograma teórico da S01.
TRIAL_SOURCES: tuple[TrialSource, ...] = (
    # Caio — 3 IA + 3 Manual
    TrialSource("Caio-K2-IA-1", "Caio", "K2", "IA", 1, "11", _p("trials", "caio", "k2-ia", "solucao.py")),
    TrialSource("Caio-K4-IA-2", "Caio", "K4", "IA", 2, "12", _p("trials", "caio", "k4-ia", "solucao.py")),
    TrialSource("Caio-K6-IA-3", "Caio", "K6", "IA", 3, "13", _p("trials", "caio", "k6-ia", "solucao.py")),
    TrialSource("Caio-K1-Manual-4", "Caio", "K1", "Manual", 4, "14", _p("trials", "caio", "k1-manual", "solucao.py")),
    TrialSource("Caio-K3-Manual-5", "Caio", "K3", "Manual", 5, "15", _p("trials", "caio", "k3-manual", "solucao.py")),
    TrialSource("Caio-K5-Manual-6", "Caio", "K5", "Manual", 6, "16", _p("trials", "caio", "k5-manual", "solucao.py")),
    # Henrique — pastas kX-ia / kX-sem-ia
    TrialSource("Henrique-K1-IA-4", "Henrique", "K1", "IA", 4, "17", _p("trials", "henrique", "k1-ia", "solucao.py")),
    TrialSource("Henrique-K2-Manual-5", "Henrique", "K2", "Manual", 5, "20", _p("trials", "henrique", "k2-sem-ia", "solucao.py")),
    TrialSource("Henrique-K3-Manual-6", "Henrique", "K3", "Manual", 6, "21", _p("trials", "henrique", "k3-sem-ia", "solucao.py")),
    TrialSource("Henrique-K4-IA-1", "Henrique", "K4", "IA", 1, "18", _p("trials", "henrique", "k4-ia", "solucao.py")),
    TrialSource("Henrique-K5-IA-2", "Henrique", "K5", "IA", 2, "19", _p("trials", "henrique", "k5-ia", "solucao.py")),
    TrialSource("Henrique-K6-Manual-3", "Henrique", "K6", "Manual", 3, "22", _p("trials", "henrique", "k6-sem-ia", "solucao.py")),
    # Jonas — soluções em katas/kX (PR #37); tratamentos do cronograma S01
    TrialSource("Jonas-K6-IA-1", "Jonas", "K6", "IA", 1, "23", _p("katas", "k6", "solucao.py")),
    TrialSource("Jonas-K5-Manual-2", "Jonas", "K5", "Manual", 2, "24", _p("katas", "k5", "solucao.py")),
    TrialSource("Jonas-K4-Manual-3", "Jonas", "K4", "Manual", 3, "25", _p("katas", "k4", "solucao.py")),
    TrialSource("Jonas-K3-IA-4", "Jonas", "K3", "IA", 4, "26", _p("katas", "k3", "solucao.py")),
    TrialSource("Jonas-K2-IA-5", "Jonas", "K2", "IA", 5, "27", _p("katas", "k2", "solucao.py")),
    TrialSource("Jonas-K1-Manual-6", "Jonas", "K1", "Manual", 6, "28", _p("katas", "k1", "solucao.py")),
)
