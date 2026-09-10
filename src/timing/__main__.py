"""CLI da coleta de trials.

Uso (na raiz do repositório):
    python -m src.timing proximo --integrante Caio
    python -m src.timing start --integrante Caio
    python -m src.timing finish --passando 8 --totais 8
    python -m src.timing record --integrante Caio --segundos 842 --passando 8 --totais 8
    python -m src.timing list
    python -m src.timing resumo
"""

from __future__ import annotations

import argparse
import json
import sys

from src.timing.constants import CRONOGRAMA, TIMEBOX_MINUTES, TRIALS_CSV
from src.timing.protocol import cancel, finish, next_ordem, planned_step, record, start
from src.timing.store import read_session, read_trials
from src.timing.summary import by_treatment


def _add_common_ids(parser: argparse.ArgumentParser, *, require_integrante: bool) -> None:
    parser.add_argument("--integrante", required=require_integrante, choices=sorted(CRONOGRAMA))
    parser.add_argument("--kata", default=None)
    parser.add_argument("--tratamento", default=None, choices=("IA", "Manual"))
    parser.add_argument("--ordem", type=int, default=None)
    parser.add_argument("--issue", default="", help="Número da Issue do trial no GitHub")
    parser.add_argument("--assistente", default="", help="Nome/versão do assistente (só IA)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            f"Coleta de trials do Lab02 (time-box {TIMEBOX_MINUTES} min). "
            "Trial sem verde vira censurado em 35 min — nunca é descartado."
        )
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_next = sub.add_parser("proximo", help="Mostra o próximo trial do cronograma")
    p_next.add_argument("--integrante", required=True, choices=sorted(CRONOGRAMA))

    p_start = sub.add_parser("start", help="Inicia o cronômetro de um trial")
    _add_common_ids(p_start, require_integrante=True)

    p_fin = sub.add_parser("finish", help="Encerra o trial em andamento e grava o CSV")
    p_fin.add_argument("--passando", type=int, required=True)
    p_fin.add_argument("--totais", type=int, required=True)
    p_fin.add_argument("--prompts", type=int, default=None)
    p_fin.add_argument("--notas", default="")

    p_rec = sub.add_parser("record", help="Registra um trial já cronometrado")
    _add_common_ids(p_rec, require_integrante=True)
    p_rec.add_argument("--passando", type=int, required=True)
    p_rec.add_argument("--totais", type=int, required=True)
    p_rec.add_argument("--segundos", type=float, default=None)
    p_rec.add_argument("--minutos", type=float, default=None)
    p_rec.add_argument("--prompts", type=int, default=None)
    p_rec.add_argument("--notas", default="")

    sub.add_parser("status", help="Mostra o trial em andamento")
    sub.add_parser("cancel", help="Descarta a sessão em andamento (não grava CSV)")
    sub.add_parser("list", help="Lista os trials do CSV")
    sub.add_parser("resumo", help="Mediana e IQR por tratamento (não use média)")
    return parser


def _print_trial(trial) -> None:
    flag = "CENSURADO 35min" if trial.censurado else "time-to-green"
    print(
        f"[timing] {trial.trial_id}  {trial.tempo_min:.2f} min  "
        f"{trial.testes_passando}/{trial.testes_totais}  {flag}"
    )
    print(f"[timing] csv: {TRIALS_CSV}")


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    try:
        if args.cmd == "proximo":
            ordem = next_ordem(args.integrante)
            kata, tratamento = planned_step(args.integrante, ordem)
            print(f"{args.integrante} ordem {ordem}/6 -> {kata} / {tratamento}")
            return

        if args.cmd == "start":
            session = start(
                integrante=args.integrante,
                kata=args.kata,
                tratamento=args.tratamento,
                ordem=args.ordem,
                issue=args.issue,
                assistente=args.assistente,
            )
            print(
                f"[timing] cronômetro ligado: {session['integrante']} "
                f"{session['kata']} {session['tratamento']} ordem {session['ordem']}"
            )
            print(f"[timing] iniciado_em {session['iniciado_em']}")
            print(f"[timing] time-box {TIMEBOX_MINUTES} min — ao estourar, use finish mesmo sem verde")
            return

        if args.cmd == "finish":
            trial = finish(
                testes_passando=args.passando,
                testes_totais=args.totais,
                n_prompts=args.prompts,
                notas=args.notas,
            )
            _print_trial(trial)
            return

        if args.cmd == "record":
            if args.segundos is None and args.minutos is None:
                raise ValueError("informe --segundos ou --minutos")
            elapsed = args.segundos if args.segundos is not None else args.minutos * 60
            trial = record(
                integrante=args.integrante,
                kata=args.kata,
                tratamento=args.tratamento,
                ordem=args.ordem,
                elapsed_s=elapsed,
                testes_passando=args.passando,
                testes_totais=args.totais,
                n_prompts=args.prompts,
                assistente=args.assistente,
                issue=args.issue,
                notas=args.notas,
            )
            _print_trial(trial)
            return

        if args.cmd == "status":
            session = read_session()
            if not session:
                print("[timing] nenhum trial em andamento")
                return
            print(json.dumps(session, indent=2, ensure_ascii=False))
            return

        if args.cmd == "cancel":
            cancel()
            print("[timing] sessão descartada (CSV intacto)")
            return

        if args.cmd == "list":
            rows = read_trials()
            if not rows:
                print(f"[timing] CSV vazio: {TRIALS_CSV}")
                return
            for row in rows:
                print(
                    f"{row['trial_id']:24}  {row['tempo_min']:>6} min  "
                    f"{row['testes_passando']}/{row['testes_totais']}  "
                    f"censurado={row['censurado']}"
                )
            return

        if args.cmd == "resumo":
            print("tratamento  n  cens  tempo_mediana_s  IQR_s  taxa_mediana  IQR_taxa")
            for block in by_treatment():
                print(
                    f"{block['tratamento']:<10} {block['n']:>2}  {block['censurados']:>4}  "
                    f"{block['tempo_s_mediana']:>14}  {block['tempo_s_iqr']:>5}  "
                    f"{block['taxa_sucesso_mediana']:>12}  {block['taxa_sucesso_iqr']}"
                )
            return
    except (ValueError, RuntimeError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
