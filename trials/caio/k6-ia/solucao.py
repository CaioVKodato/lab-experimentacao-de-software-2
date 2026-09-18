"""K6 — Roteador de Chamados de Suporte (trial com IA, issue #13).

API pública exigida pelos testes: `rotear_chamados`.
A classificação (categoria + urgência) fica separada da ordenação estável
por urgência, para a regra do enunciado ficar explícita.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Sequence


class Urgencia(str, Enum):
    ALTA = "alta"
    NORMAL = "normal"

    @property
    def prioridade(self) -> int:
        return 0 if self is Urgencia.ALTA else 1


class Categoria:
    GERAL = "geral"


@dataclass(frozen=True, slots=True)
class ChamadoRoteado:
    texto: str
    categoria: str
    urgencia: Urgencia

    def para_dict(self) -> dict[str, str]:
        return {
            "texto": self.texto,
            "categoria": self.categoria,
            "urgencia": self.urgencia.value,
        }


def _contem(texto_normalizado: str, termo: str) -> bool:
    return termo.casefold() in texto_normalizado


class ClassificadorDeChamados:
    def __init__(self, palavras_chave: Mapping[str, Sequence[str]]) -> None:
        self._regras = tuple(
            (categoria, tuple(palavras or ()))
            for categoria, palavras in (palavras_chave or {}).items()
        )

    def _categoria(self, texto_normalizado: str) -> str:
        for categoria, palavras in self._regras:
            if any(_contem(texto_normalizado, palavra) for palavra in palavras):
                return categoria
        return Categoria.GERAL

    def _urgencia(self, texto_normalizado: str) -> Urgencia:
        if _contem(texto_normalizado, "urgente"):
            return Urgencia.ALTA
        return Urgencia.NORMAL

    def classificar(self, texto: str) -> ChamadoRoteado:
        normalizado = texto.casefold()
        return ChamadoRoteado(
            texto=texto,
            categoria=self._categoria(normalizado),
            urgencia=self._urgencia(normalizado),
        )


class RoteadorDeChamados:
    def __init__(self, palavras_chave: Mapping[str, Sequence[str]]) -> None:
        self._classificador = ClassificadorDeChamados(palavras_chave)

    def rotear(self, chamados: Sequence[str]) -> list[dict[str, str]]:
        classificados = [self._classificador.classificar(texto) for texto in chamados or ()]
        classificados.sort(key=lambda chamado: chamado.urgencia.prioridade)
        return [chamado.para_dict() for chamado in classificados]


def rotear_chamados(chamados: list, palavras_chave: dict) -> list:
    """Classifica cada chamado e devolve a lista com urgência alta primeiro.

    Categoria = primeira chave do dicionário cuja palavra aparece no texto
    (substring, sem distinguir maiúsculas). Sem match → "geral".
    A ordenação por urgência é estável.
    """
    return RoteadorDeChamados(palavras_chave).rotear(chamados)
