"""Modelo de um trial e validação dos campos coletados."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from src.timing.clock import all_tests_passed, resolve_time, seconds_to_minutes, taxa_sucesso
from src.timing.constants import INTEGRANTES, KATAS, TRATAMENTOS


@dataclass(frozen=True)
class Trial:
    trial_id: str
    integrante: str
    kata: str
    tratamento: str
    ordem: int
    iniciado_em: str
    encerrado_em: str
    tempo_s: int
    tempo_min: float
    censurado: bool
    testes_passando: int
    testes_totais: int
    taxa_sucesso: float
    n_prompts: str
    assistente: str
    issue: str
    notas: str

    def to_row(self) -> dict[str, str]:
        row = asdict(self)
        row["censurado"] = "true" if self.censurado else "false"
        row["ordem"] = str(self.ordem)
        row["tempo_s"] = str(self.tempo_s)
        row["tempo_min"] = f"{self.tempo_min:.2f}"
        row["testes_passando"] = str(self.testes_passando)
        row["testes_totais"] = str(self.testes_totais)
        row["taxa_sucesso"] = f"{self.taxa_sucesso:.4f}"
        return row


def validate_ids(integrante: str, kata: str, tratamento: str, ordem: int) -> None:
    if integrante not in INTEGRANTES:
        raise ValueError(f"integrante inválido: {integrante!r} (use {INTEGRANTES})")
    if kata not in KATAS:
        raise ValueError(f"kata inválida: {kata!r} (use {KATAS})")
    if tratamento not in TRATAMENTOS:
        raise ValueError(f"tratamento inválido: {tratamento!r} (use {TRATAMENTOS})")
    if not 1 <= ordem <= 6:
        raise ValueError(f"ordem deve ser 1..6, recebido {ordem}")


def build_trial(
    *,
    integrante: str,
    kata: str,
    tratamento: str,
    ordem: int,
    elapsed_s: float,
    testes_passando: int,
    testes_totais: int,
    iniciado_em: str,
    encerrado_em: str,
    n_prompts: int | None = None,
    assistente: str = "",
    issue: str = "",
    notas: str = "",
) -> Trial:
    validate_ids(integrante, kata, tratamento, ordem)
    if testes_passando < 0 or testes_totais < 0:
        raise ValueError("contagem de testes não pode ser negativa")
    if testes_passando > testes_totais:
        raise ValueError("testes passando não pode exceder o total")
    if tratamento == "Manual" and n_prompts:
        raise ValueError("n_prompts só faz sentido no tratamento IA")

    passou = all_tests_passed(testes_passando, testes_totais)
    tempo_s, censurado = resolve_time(elapsed_s=elapsed_s, passou_todos=passou)
    prompts = "" if n_prompts is None else str(n_prompts)
    if tratamento == "IA" and not assistente:
        assistente = "a-definir"

    return Trial(
        trial_id=f"{integrante}-{kata}-{tratamento}-{ordem}",
        integrante=integrante,
        kata=kata,
        tratamento=tratamento,
        ordem=ordem,
        iniciado_em=iniciado_em,
        encerrado_em=encerrado_em,
        tempo_s=tempo_s,
        tempo_min=seconds_to_minutes(tempo_s),
        censurado=censurado,
        testes_passando=testes_passando,
        testes_totais=testes_totais,
        taxa_sucesso=taxa_sucesso(testes_passando, testes_totais),
        n_prompts=prompts,
        assistente=assistente if tratamento == "IA" else "",
        issue=issue,
        notas=notas,
    )
