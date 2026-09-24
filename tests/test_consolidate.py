"""Testes da consolidação LOC (Issue #38)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.metrics.loc import count_solucao_loc
from src.metrics.trial_sources import TRIAL_SOURCES


class LocSolucaoTests(unittest.TestCase):
    def test_conta_so_solucao_nao_testes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "solucao.py").write_text("a\nb\nc\n", encoding="utf-8")
            (root / "test_x.py").write_text("x\n" * 50, encoding="utf-8")
            self.assertEqual(count_solucao_loc(root), 3)

    def test_dezoito_fontes_com_arquivo(self) -> None:
        self.assertEqual(len(TRIAL_SOURCES), 18)
        missing = [s.trial_id for s in TRIAL_SOURCES if not s.solucao.is_file()]
        self.assertEqual(missing, [])


class TrialsCsvColumnsTests(unittest.TestCase):
    def test_csv_tem_loc_e_duplicacao_nas_18_linhas(self) -> None:
        import csv

        path = Path("data/trials.csv")
        self.assertTrue(path.exists())
        with path.open(encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 18)
        for row in rows:
            self.assertTrue(row["loc"].strip(), msg=row["trial_id"])
            self.assertTrue(row["duplicacao_pct"].strip(), msg=row["trial_id"])


if __name__ == "__main__":
    unittest.main()
