"""Protocolo de um trial: start, finish e registro a posteriori."""

from __future__ import annotations

from datetime import datetime

from src.timing.constants import CRONOGRAMA
from src.timing.schema import Trial, build_trial, validate_ids
from src.timing.store import (
    append_trial,
    clear_session,
    now_iso,
    read_session,
    read_trials,
    write_session,
)


def planned_step(integrante: str, ordem: int) -> tuple[str, str]:
    steps = CRONOGRAMA.get(integrante)
    if not steps:
        raise ValueError(f"sem cronograma para {integrante!r}")
    return steps[ordem - 1]


def next_ordem(integrante: str) -> int:
    done = {int(row["ordem"]) for row in read_trials() if row.get("integrante") == integrante}
    for ordem in range(1, 7):
        if ordem not in done:
            return ordem
    raise ValueError(f"{integrante} já tem os 6 trials no CSV")


def start(
    *,
    integrante: str,
    kata: str | None = None,
    tratamento: str | None = None,
    ordem: int | None = None,
    issue: str = "",
    assistente: str = "",
) -> dict:
    if read_session():
        raise RuntimeError("já existe um trial em andamento; use `finish` ou `cancel`")

    ordem = ordem or next_ordem(integrante)
    planned_kata, planned_trat = planned_step(integrante, ordem)
    kata = kata or planned_kata
    tratamento = tratamento or planned_trat
    validate_ids(integrante, kata, tratamento, ordem)

    if (kata, tratamento) != (planned_kata, planned_trat):
        raise ValueError(
            f"ordem {ordem} de {integrante} no cronograma é "
            f"{planned_kata}/{planned_trat}, não {kata}/{tratamento}"
        )

    session = {
        "integrante": integrante,
        "kata": kata,
        "tratamento": tratamento,
        "ordem": ordem,
        "issue": issue,
        "assistente": assistente,
        "iniciado_em": now_iso(),
    }
    write_session(session)
    return session


def _elapsed_seconds(iniciado_em: str, encerrado_em: str) -> float:
    start_dt = datetime.fromisoformat(iniciado_em)
    end_dt = datetime.fromisoformat(encerrado_em)
    return (end_dt - start_dt).total_seconds()


def finish(
    *,
    testes_passando: int,
    testes_totais: int,
    n_prompts: int | None = None,
    notas: str = "",
) -> Trial:
    session = read_session()
    if not session:
        raise RuntimeError("nenhum trial em andamento; use `start` ou `record`")

    encerrado_em = now_iso()
    trial = build_trial(
        integrante=session["integrante"],
        kata=session["kata"],
        tratamento=session["tratamento"],
        ordem=int(session["ordem"]),
        elapsed_s=_elapsed_seconds(session["iniciado_em"], encerrado_em),
        testes_passando=testes_passando,
        testes_totais=testes_totais,
        iniciado_em=session["iniciado_em"],
        encerrado_em=encerrado_em,
        n_prompts=n_prompts,
        assistente=session.get("assistente") or "",
        issue=session.get("issue") or "",
        notas=notas,
    )
    append_trial(trial)
    clear_session()
    return trial


def record(
    *,
    integrante: str,
    testes_passando: int,
    testes_totais: int,
    elapsed_s: float,
    kata: str | None = None,
    tratamento: str | None = None,
    ordem: int | None = None,
    n_prompts: int | None = None,
    assistente: str = "",
    issue: str = "",
    notas: str = "",
) -> Trial:
    """Registra um trial já cronometrado (celular, IDE, etc.)."""
    ordem = ordem or next_ordem(integrante)
    planned_kata, planned_trat = planned_step(integrante, ordem)
    trial = build_trial(
        integrante=integrante,
        kata=kata or planned_kata,
        tratamento=tratamento or planned_trat,
        ordem=ordem,
        elapsed_s=elapsed_s,
        testes_passando=testes_passando,
        testes_totais=testes_totais,
        iniciado_em="",
        encerrado_em=now_iso(),
        n_prompts=n_prompts,
        assistente=assistente,
        issue=issue,
        notas=notas,
    )
    append_trial(trial)
    return trial


def cancel() -> None:
    if not read_session():
        raise RuntimeError("nenhum trial em andamento")
    clear_session()
