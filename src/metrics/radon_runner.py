"""Coleta de complexidade ciclomática (CC) e Maintainability Index (MI) via Radon."""

from __future__ import annotations

from pathlib import Path


def compute_cc(directory: Path) -> float:
    """Complexidade ciclomática média de todas as funções/métodos no diretório.

    Retorna 0.0 se não houver blocos ou se Radon não estiver instalado.
    """
    try:
        from radon.complexity import cc_visit
    except ImportError:
        return 0.0

    scores: list[float] = []
    for py_file in sorted(directory.rglob("*.py")):
        try:
            code = py_file.read_text(encoding="utf-8", errors="replace")
            blocks = cc_visit(code)
            scores.extend(float(b.complexity) for b in blocks)
        except Exception:
            pass
    return round(sum(scores) / len(scores), 4) if scores else 0.0


def compute_mi(directory: Path) -> float:
    """Maintainability Index médio dos arquivos .py no diretório.

    Retorna -1.0 se Radon não estiver instalado ou nenhum arquivo for analisável.
    """
    try:
        from radon.metrics import mi_visit
    except ImportError:
        return -1.0

    values: list[float] = []
    for py_file in sorted(directory.rglob("*.py")):
        try:
            code = py_file.read_text(encoding="utf-8", errors="replace")
            mi = mi_visit(code, multi=True)
            values.append(float(mi))
        except Exception:
            pass
    return round(sum(values) / len(values), 4) if values else -1.0
