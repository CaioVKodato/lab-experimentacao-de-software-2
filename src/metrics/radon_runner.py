"""Coleta de complexidade ciclomática (CC) e Maintainability Index (MI) via Radon."""

from __future__ import annotations

from pathlib import Path


def _solucao_path(directory: Path) -> Path | None:
    directory = Path(directory)
    solucao = directory / "solucao.py" if directory.is_dir() else directory
    if solucao.is_file() and solucao.name == "solucao.py":
        return solucao
    if directory.is_dir():
        candidate = directory / "solucao.py"
        if candidate.is_file():
            return candidate
    return None


def compute_cc(directory: Path) -> float:
    """Complexidade ciclomática média das funções/métodos de ``solucao.py``.

    Retorna 0.0 se não houver blocos ou se Radon não estiver instalado.
    """
    try:
        from radon.complexity import cc_visit
    except ImportError:
        return 0.0

    solucao = _solucao_path(directory)
    if solucao is None:
        return 0.0

    try:
        code = solucao.read_text(encoding="utf-8", errors="replace")
        blocks = cc_visit(code)
        scores = [float(b.complexity) for b in blocks]
    except Exception:
        return 0.0
    return round(sum(scores) / len(scores), 4) if scores else 0.0


def compute_mi(directory: Path) -> float:
    """Maintainability Index de ``solucao.py``.

    Retorna -1.0 se Radon não estiver instalado ou o arquivo for inanalisável.
    """
    try:
        from radon.metrics import mi_visit
    except ImportError:
        return -1.0

    solucao = _solucao_path(directory)
    if solucao is None:
        return -1.0

    try:
        code = solucao.read_text(encoding="utf-8", errors="replace")
        return round(float(mi_visit(code, multi=True)), 4)
    except Exception:
        return -1.0
