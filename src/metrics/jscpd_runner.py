"""Coleta de percentual de duplicação via jscpd (Node.js)."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


def compute_duplication(directory: Path) -> float:
    """Percentual de linhas duplicadas no diretório via npx jscpd.

    Retorna -1.0 se jscpd/Node.js não estiver disponível ou timeout.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            subprocess.run(
                [
                    "npx", "--yes", "jscpd",
                    str(directory),
                    "--reporters", "json",
                    "--output", tmpdir,
                    "--silent",
                ],
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return -1.0

        report = Path(tmpdir) / "jscpd-report.json"
        if not report.exists():
            return -1.0

        try:
            data = json.loads(report.read_text(encoding="utf-8"))
            return round(float(data["statistics"]["total"]["percentage"]), 4)
        except (KeyError, ValueError, json.JSONDecodeError):
            return -1.0
