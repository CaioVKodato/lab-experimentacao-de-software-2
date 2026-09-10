"""Contagem de linhas de código (LOC) para arquivos Python."""

from __future__ import annotations

from pathlib import Path


def count_loc(directory: Path) -> int:
    """Total de linhas físicas em arquivos .py do diretório (inclusive linhas em branco)."""
    total = 0
    for py_file in sorted(directory.rglob("*.py")):
        try:
            total += len(py_file.read_text(encoding="utf-8", errors="replace").splitlines())
        except OSError:
            pass
    return total
