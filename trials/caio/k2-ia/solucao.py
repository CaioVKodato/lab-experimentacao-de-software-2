"""K2 — Escalonador de Turnos (trial com IA, issue #11).

API pública exigida pelos testes: `escalonar_turnos`.
A implementação separa modelo (Turno/Funcionario) e política de alocação
(EscalonadorDeTurnos) para deixar a regra do enunciado explícita e testável.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class Turno(str, Enum):
    MANHA = "manha"
    TARDE = "tarde"
    NOITE = "noite"

    @classmethod
    def valores(cls) -> tuple[str, ...]:
        return tuple(item.value for item in cls)


@dataclass(frozen=True, slots=True)
class Funcionario:
    nome: str
    preferencias: tuple[str, ...]

    @classmethod
    def from_dict(cls, bruto: Mapping) -> "Funcionario":
        nome = str(bruto.get("nome", "")).strip()
        preferencias = tuple(bruto.get("preferencias") or ())
        return cls(nome=nome, preferencias=preferencias)


class EscalonadorDeTurnos:
    """Aloca na ordem de chegada, respeitando preferência e limite por turno."""

    def __init__(self, limite_por_turno: int) -> None:
        self._limite = max(0, int(limite_por_turno))
        self._ocupacao: dict[str, list[str]] = {turno: [] for turno in Turno.valores()}

    def _tem_vaga(self, turno: str) -> bool:
        alocados = self._ocupacao.get(turno)
        if alocados is None:
            return False
        return len(alocados) < self._limite

    def tentar_alocar(self, funcionario: Funcionario) -> bool:
        if not funcionario.nome:
            return False
        for turno in funcionario.preferencias:
            if self._tem_vaga(turno):
                self._ocupacao[turno].append(funcionario.nome)
                return True
        return False

    def resultado(self) -> dict[str, list[str]]:
        return {turno: list(nomes) for turno, nomes in self._ocupacao.items()}


def escalonar_turnos(funcionarios: list, limite_por_turno: int) -> dict:
    """Coloca cada funcionário no primeiro turno preferido que ainda tem vaga.

    A ordem da lista de entrada é a ordem de alocação. Se nenhuma preferência
    tiver vaga, a pessoa fica de fora. As chaves manha/tarde/noite sempre saem
    no dicionário, mesmo vazias.
    """
    escala = EscalonadorDeTurnos(limite_por_turno)
    for item in funcionarios or ():
        escala.tentar_alocar(Funcionario.from_dict(item))
    return escala.resultado()
