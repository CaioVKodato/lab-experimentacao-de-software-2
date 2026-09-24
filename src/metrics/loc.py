"""Contagem de linhas de código (LOC) para arquivos Python."""

from __future__ import annotations

from pathlib import Path


def count_loc_file(path: Path) -> int:
    """Linhas físicas de um único arquivo (inclusive em branco)."""
    try:
        return len(path.read_text(encoding="utf-8", errors="replace").splitlines())
    except OSError:
        return 0


def count_loc(directory: Path) -> int:
    """Total de linhas físicas em arquivos .py do diretório (inclusive em branco)."""
    total = 0
    for py_file in sorted(Path(directory).rglob("*.py")):
        total += count_loc_file(py_file)
    return total


def count_solucao_loc(directory: Path) -> int:
    """LOC apenas de ``solucao.py`` (métrica exigida pela Issue #38 / RQ3)."""
    solucao = Path(directory) / "solucao.py"
    if solucao.is_file():
        return count_loc_file(solucao)
    return 0
