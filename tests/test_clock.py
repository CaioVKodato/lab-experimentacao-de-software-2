"""Regras da RQ1: time-to-green e censura em 35 min."""

from __future__ import annotations

import unittest

from src.timing.clock import resolve_time, taxa_sucesso
from src.timing.constants import TIMEBOX_SECONDS
from src.timing.schema import build_trial


class ClockTests(unittest.TestCase):
    def test_green_antes_do_timebox_nao_censura(self) -> None:
        tempo, censurado = resolve_time(elapsed_s=12 * 60, passou_todos=True)
        self.assertEqual(tempo, 720)
        self.assertFalse(censurado)

    def test_sem_verde_sempre_censura_em_35(self) -> None:
        tempo, censurado = resolve_time(elapsed_s=10 * 60, passou_todos=False)
        self.assertEqual(tempo, TIMEBOX_SECONDS)
        self.assertTrue(censurado)

    def test_estouro_do_timebox_sem_verde(self) -> None:
        tempo, censurado = resolve_time(elapsed_s=40 * 60, passou_todos=False)
        self.assertEqual(tempo, TIMEBOX_SECONDS)
        self.assertTrue(censurado)

    def test_taxa_normaliza_katas_com_n_diferente(self) -> None:
        self.assertEqual(taxa_sucesso(3, 4), 0.75)
        self.assertEqual(taxa_sucesso(0, 0), 0.0)


class TrialTests(unittest.TestCase):
    def test_manual_nao_aceita_prompts(self) -> None:
        with self.assertRaises(ValueError):
            build_trial(
                integrante="Caio",
                kata="K2",
                tratamento="Manual",
                ordem=2,
                elapsed_s=100,
                testes_passando=1,
                testes_totais=1,
                iniciado_em="",
                encerrado_em="",
                n_prompts=2,
            )

    def test_trial_incompleto_vai_para_csv_como_censurado(self) -> None:
        trial = build_trial(
            integrante="Caio",
            kata="K1",
            tratamento="IA",
            ordem=1,
            elapsed_s=600,
            testes_passando=2,
            testes_totais=5,
            iniciado_em="",
            encerrado_em="",
            n_prompts=4,
            assistente="ChatGPT",
        )
        self.assertTrue(trial.censurado)
        self.assertEqual(trial.tempo_s, TIMEBOX_SECONDS)
        self.assertEqual(trial.taxa_sucesso, 0.4)
        self.assertEqual(trial.n_prompts, "4")


if __name__ == "__main__":
    unittest.main()
