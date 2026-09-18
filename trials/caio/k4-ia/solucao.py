"""K4 — Calculadora de Descontos em Cascata (trial com IA, issue #12).

API pública exigida pelos testes: `aplicar_descontos`.
Cada tipo de desconto é uma política explícita; o calculador aplica a
cascata na ordem da lista e só arredonda o resultado final.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class TipoDesconto(str, Enum):
    PERCENTUAL = "percentual"
    FIXO = "fixo"


class PoliticaDesconto(ABC):
    @abstractmethod
    def aplicar(self, preco_atual: float) -> float:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class DescontoPercentual(PoliticaDesconto):
    percentual: float

    def aplicar(self, preco_atual: float) -> float:
        fator = max(0.0, 1.0 - (self.percentual / 100.0))
        return preco_atual * fator


@dataclass(frozen=True, slots=True)
class DescontoFixo(PoliticaDesconto):
    valor: float

    def aplicar(self, preco_atual: float) -> float:
        return max(0.0, preco_atual - self.valor)


def _politica_de(bruto: Mapping) -> PoliticaDesconto | None:
    tipo = str(bruto.get("tipo", "")).strip().lower()
    valor = float(bruto.get("valor", 0))
    if tipo == TipoDesconto.PERCENTUAL:
        return DescontoPercentual(percentual=valor)
    if tipo == TipoDesconto.FIXO:
        return DescontoFixo(valor=valor)
    return None


class CalculadoraCascata:
    """Aplica descontos em sequência sobre o preço já reduzido."""

    def __init__(self, preco_inicial: float) -> None:
        self._preco = max(0.0, float(preco_inicial))

    def aplicar_todos(self, descontos: list | tuple) -> float:
        for bruto in descontos or ():
            politica = _politica_de(bruto)
            if politica is None:
                continue
            self._preco = politica.aplicar(self._preco)
        return round(self._preco, 2)


def aplicar_descontos(preco: float, descontos: list) -> float:
    """Reduz o preço em cascata e devolve o valor arredondado em 2 casas.

    Desconto fixo não deixa o preço negativo (piso 0.0). Percentual reduz
    sobre o preço corrente, não sobre o original.
    """
    return CalculadoraCascata(preco).aplicar_todos(descontos)
