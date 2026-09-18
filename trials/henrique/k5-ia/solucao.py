"""K5 — Detector de Duplicatas Aproximadas (trial com IA, issue #19)."""

import unicodedata
from collections import defaultdict


def _normalizar(nome: str) -> str:
    """Lowercase, remove espaços e acentos."""
    sem_espacos = nome.lower().replace(" ", "")
    return unicodedata.normalize("NFD", sem_espacos).encode("ascii", "ignore").decode("ascii")


def encontrar_duplicatas(nomes: list[str]) -> list[list[str]]:
    """Retorna grupos de nomes que são duplicatas após normalização.

    Nomes sem duplicata ficam de fora do resultado.
    """
    grupos: dict[str, list[str]] = defaultdict(list)
    for nome in nomes:
        grupos[_normalizar(nome)].append(nome)
    return [grupo for grupo in grupos.values() if len(grupo) >= 2]
