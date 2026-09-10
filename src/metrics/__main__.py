"""CLI para coleta de métricas estáticas (RQ3).

Uso (na raiz do repositório):
    python -m src.metrics --dir katas/K1/solucao
    python -m src.metrics --dir katas/K1/solucao --trial-id Caio-K1-IA-1
    python -m src.metrics --dir katas/K1/solucao --trial-id Caio-K1-IA-1 --output data/metrics.csv
    python -m src.metrics --dir katas/K1/solucao --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.metrics.collector import collect_metrics
from src.metrics.constants import METRICS_CSV
from src.metrics.store import append_metrics


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Coleta métricas estáticas de um diretório de trial (RQ3)."
    )
    parser.add_argument("--dir", required=True, help="Diretório com o código do trial")
    parser.add_argument(
        "--trial-id",
        default="",
        help="Identificador do trial (ex: Caio-K1-IA-1)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help=f"CSV de saída (padrão: {METRICS_CSV})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Exibe resultado sem gravar CSV",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    directory = Path(args.dir)
    if not directory.is_dir():
        print(f"Erro: {directory!r} não é um diretório válido", file=sys.stderr)
        sys.exit(1)

    output = Path(args.output) if args.output else METRICS_CSV

    try:
        row = collect_metrics(directory, trial_id=args.trial_id)
    except Exception as exc:
        print(f"Erro ao coletar métricas: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"[metrics] trial_id     : {row.trial_id or '(sem id)'}")
    print(f"[metrics] diretorio    : {row.diretorio}")
    print(f"[metrics] loc          : {row.loc}")
    print(f"[metrics] cc_mean      : {row.cc_mean:.4f}")
    if row.mi_mean >= 0:
        print(f"[metrics] mi_mean      : {row.mi_mean:.4f}")
    else:
        print("[metrics] mi_mean      : indisponível")
    if row.duplication_pct >= 0:
        print(f"[metrics] duplication% : {row.duplication_pct:.4f}")
    else:
        print("[metrics] duplication% : indisponível (jscpd/Node.js não encontrado)")

    if not args.dry_run:
        append_metrics(row, path=output)
        print(f"[metrics] csv          : {output}")
    else:
        print("[metrics] dry-run: resultado não gravado em CSV")


if __name__ == "__main__":
    main()
