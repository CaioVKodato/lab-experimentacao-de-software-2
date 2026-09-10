"""Persistência do CSV de trials e da sessão em andamento."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from src.timing.constants import FIELDNAMES, SESSION_PATH, TRIALS_CSV
from src.timing.schema import Trial


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def ensure_csv(path: Path = TRIALS_CSV) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.stat().st_size == 0:
        with path.open("w", newline="", encoding="utf-8") as handle:
            csv.DictWriter(handle, fieldnames=FIELDNAMES).writeheader()
    return path


def read_trials(path: Path = TRIALS_CSV) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_trial(trial: Trial, path: Path = TRIALS_CSV) -> Path:
    ensure_csv(path)
    existing = read_trials(path)
    if any(row.get("trial_id") == trial.trial_id for row in existing):
        raise ValueError(f"trial já registrado: {trial.trial_id}")
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writerow(trial.to_row())
    return path


def write_session(payload: dict, path: Path = SESSION_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_session(path: Path = SESSION_PATH) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def clear_session(path: Path = SESSION_PATH) -> None:
    if path.exists():
        path.unlink()
