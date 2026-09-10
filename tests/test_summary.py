"""Resumo descritivo usa mediana/IQR, não média."""

from __future__ import annotations

import unittest

from src.timing.summary import by_treatment


class SummaryTests(unittest.TestCase):
    def test_mediana_ignora_outlier(self) -> None:
        rows = [
            {"tratamento": "IA", "tempo_s": "600", "taxa_sucesso": "1.0000", "censurado": "false"},
            {"tratamento": "IA", "tempo_s": "700", "taxa_sucesso": "1.0000", "censurado": "false"},
            {"tratamento": "IA", "tempo_s": "2100", "taxa_sucesso": "0.2000", "censurado": "true"},
            {"tratamento": "Manual", "tempo_s": "900", "taxa_sucesso": "1.0000", "censurado": "false"},
        ]
        blocks = {item["tratamento"]: item for item in by_treatment(rows)}
        self.assertEqual(blocks["IA"]["n"], 3)
        self.assertEqual(blocks["IA"]["censurados"], 1)
        self.assertEqual(blocks["IA"]["tempo_s_mediana"], 700)
        self.assertEqual(blocks["Manual"]["n"], 1)


if __name__ == "__main__":
    unittest.main()
