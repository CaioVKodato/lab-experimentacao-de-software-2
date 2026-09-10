"""Constantes do protocolo de coleta (RQ1 e RQ2)."""

from __future__ import annotations

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
TRIALS_CSV = DATA_DIR / "trials.csv"
SESSION_PATH = DATA_DIR / ".session.json"

TIMEBOX_MINUTES = 35
TIMEBOX_SECONDS = TIMEBOX_MINUTES * 60

INTEGRANTES = ("Caio", "Henrique", "Jonas")
TRATAMENTOS = ("IA", "Manual")
KATAS = ("K1", "K2", "K3", "K4", "K5", "K6")

# Crossover contrabalanceado: 3 IA + 3 Manual por pessoa, 18 trials no total.
# Nunca descartar trial incompleto — censura em 35 min (enunciado).
CRONOGRAMA: dict[str, tuple[tuple[str, str], ...]] = {
    "Caio": (
        ("K1", "IA"),
        ("K2", "Manual"),
        ("K3", "IA"),
        ("K4", "Manual"),
        ("K5", "IA"),
        ("K6", "Manual"),
    ),
    "Henrique": (
        ("K4", "Manual"),
        ("K5", "IA"),
        ("K6", "Manual"),
        ("K1", "IA"),
        ("K2", "Manual"),
        ("K3", "IA"),
    ),
    "Jonas": (
        ("K6", "IA"),
        ("K5", "Manual"),
        ("K4", "Manual"),
        ("K3", "IA"),
        ("K2", "IA"),
        ("K1", "Manual"),
    ),
}

FIELDNAMES = (
    "trial_id",
    "integrante",
    "kata",
    "tratamento",
    "ordem",
    "iniciado_em",
    "encerrado_em",
    "tempo_s",
    "tempo_min",
    "censurado",
    "testes_passando",
    "testes_totais",
    "taxa_sucesso",
    "n_prompts",
    "assistente",
    "issue",
    "notas",
)
