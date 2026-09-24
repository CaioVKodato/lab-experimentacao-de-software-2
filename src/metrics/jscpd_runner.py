"""Coleta de percentual de duplicação via jscpd (Node.js).

Usa jscpd@3.5.4 (compatível com Node 16). Em Windows chama ``npx.cmd``.
Analisa apenas ``solucao.py`` (cópia em diretório temporário), como exige a Issue #38.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

JSCPD_PACKAGE = "jscpd@3.5.4"


def _npx_cmd() -> str:
    return "npx.cmd" if os.name == "nt" else "npx"


def compute_duplication(directory: Path) -> float:
    """Percentual de linhas duplicadas no ``solucao.py`` do diretório.

    Retorna -1.0 se jscpd/Node.js não estiver disponível.
    """
    directory = Path(directory)
    solucao = directory / "solucao.py" if directory.is_dir() else directory
    if solucao.is_dir():
        solucao = solucao / "solucao.py"
    if not solucao.is_file():
        # fallback: primeiro .py que não seja teste
        candidates = [
            p for p in directory.rglob("*.py") if not p.name.startswith("test_")
        ] if directory.is_dir() else []
        if not candidates:
            return -1.0
        solucao = candidates[0]

    with tempfile.TemporaryDirectory() as tmpdir:
        work = Path(tmpdir) / "src"
        out = Path(tmpdir) / "report"
        work.mkdir()
        out.mkdir()
        shutil.copy(solucao, work / "solucao.py")

        cmd = [
            _npx_cmd(),
            "--yes",
            JSCPD_PACKAGE,
            str(work),
            "-f",
            "python",
            "-r",
            "json",
            "-o",
            str(out),
            "-s",
        ]
        try:
            completed = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180,
                check=False,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return -1.0

        report = out / "jscpd-report.json"
        if not report.exists():
            # jscpd às vezes não grava JSON quando não há clones: trata como 0%
            if completed.returncode == 0:
                return 0.0
            return -1.0

        try:
            data = json.loads(report.read_text(encoding="utf-8"))
            return round(float(data["statistics"]["total"]["percentage"]), 4)
        except (KeyError, ValueError, json.JSONDecodeError, TypeError):
            return -1.0
