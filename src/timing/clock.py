"""Regras de tempo e censura da RQ1.

Time-to-green é a métrica primária. Se o trial não passa em todos os testes
dentro do time-box, o tempo é registrado como 35 min e `censurado=true`.
Descartar esses trials enviesaria a comparação a favor do tratamento com
mais falhas (enunciado, RQ1).
"""

from __future__ import annotations

from src.timing.constants import TIMEBOX_SECONDS


def all_tests_passed(passando: int, totais: int) -> bool:
    if totais <= 0:
        return False
    return passando >= totais


def taxa_sucesso(passando: int, totais: int) -> float:
    if totais <= 0:
        return 0.0
    return round(passando / totais, 4)


def resolve_time(*, elapsed_s: float, passou_todos: bool) -> tuple[int, bool]:
    """Devolve (tempo_s, censurado) segundo o protocolo do laboratório.

    - Verde antes do time-box: tempo real, não censurado.
    - Sem verde (estouro ou encerramento antecipado): 35 min, censurado.
      Parar cedo sem sucesso não pode encolher o tempo — isso enviesaria a RQ1.
    """
    elapsed = max(0, int(round(elapsed_s)))
    if passou_todos and elapsed <= TIMEBOX_SECONDS:
        return elapsed, False
    return TIMEBOX_SECONDS, True


def seconds_to_minutes(tempo_s: int) -> float:
    return round(tempo_s / 60.0, 2)
