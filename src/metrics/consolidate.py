"""Consolida LOC e % de duplicação nos 18 trials → ``data/trials.csv``.

Issue #38 (S03): métricas estruturais exigidas pela RQ3.

Uso (na raiz do repositório):
    python -m src.metrics.consolidate
    python -m src.metrics.consolidate --dry-run
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from src.metrics.constants import DATA_DIR
from src.metrics.jscpd_runner import compute_duplication
from src.metrics.loc import count_solucao_loc
from src.metrics.trial_sources import TRIAL_SOURCES, TrialSource

TRIALS_CSV = DATA_DIR / "trials.csv"

BASE_FIELDS = (
    "trial_id",
    "integrante",
    "kata",
    "tratamento",
    "ordem",
    "iniciado_em",
    "encerrado_em",
    "tempo_s",
    "tempo_min",
    "censurado",
    "testes_passando",
    "testes_totais",
    "taxa_sucesso",
    "n_prompts",
    "assistente",
    "issue",
    "notas",
)

METRIC_FIELDS = ("loc", "duplicacao_pct")
FIELDNAMES = BASE_FIELDS + METRIC_FIELDS


def _empty_row(source: TrialSource) -> dict[str, str]:
    row = {field: "" for field in FIELDNAMES}
    row.update(
        {
            "trial_id": source.trial_id,
            "integrante": source.integrante,
            "kata": source.kata,
            "tratamento": source.tratamento,
            "ordem": str(source.ordem),
            "issue": source.issue,
            "notas": "tempo ainda nao registrado pelo integrante; LOC/duplicacao preenchidos na Issue #38",
        }
    )
    return row


def _read_existing(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        return {row["trial_id"]: row for row in csv.DictReader(handle) if row.get("trial_id")}


def _measure(source: TrialSource) -> tuple[int, float]:
    if not source.solucao.is_file():
        raise FileNotFoundError(f"solucao ausente: {source.solucao}")
    directory = source.solucao.parent
    loc = count_solucao_loc(directory)
    duplication = compute_duplication(directory)
    if duplication < 0:
        raise RuntimeError(
            f"jscpd indisponivel para {source.trial_id} "
            "(precisa Node.js + npx; jscpd@3.5.4)"
        )
    return loc, duplication


def consolidate(path: Path = TRIALS_CSV, *, dry_run: bool = False) -> list[dict[str, str]]:
    existing = _read_existing(path)
    rows: list[dict[str, str]] = []

    for source in TRIAL_SOURCES:
        row = dict(existing.get(source.trial_id) or _empty_row(source))
        # garante chaves novas mesmo em CSV antigo
        for field in FIELDNAMES:
            row.setdefault(field, "")
        loc, duplication = _measure(source)
        row["loc"] = str(loc)
        row["duplicacao_pct"] = f"{duplication:.4f}"
        # metadados canônicos
        row["integrante"] = source.integrante
        row["kata"] = source.kata
        row["tratamento"] = source.tratamento
        row["ordem"] = str(source.ordem)
        row["issue"] = source.issue or row.get("issue", "")
        rows.append(row)
        try:
            rel = source.solucao.relative_to(DATA_DIR.parent)
        except ValueError:
            rel = source.solucao
        print(
            f"[consolidate] {source.trial_id:24}  "
            f"loc={loc:4d}  duplicacao={duplication:7.4f}%  <- {rel}"
        )

    missing = [s.trial_id for s in TRIAL_SOURCES if not s.solucao.is_file()]
    if missing:
        raise RuntimeError(f"solucoes faltando: {missing}")

    empty = [r["trial_id"] for r in rows if not r.get("loc") or not r.get("duplicacao_pct")]
    if empty:
        raise RuntimeError(f"celulas vazias apos consolidacao: {empty}")

    if dry_run:
        print(f"[consolidate] dry-run: {len(rows)} linhas (nao gravou {path})")
        return rows

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"[consolidate] {len(rows)} linhas -> {path}")
    return rows


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Preenche loc e duplicacao_pct em data/trials.csv (Issue #38)."
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=TRIALS_CSV,
        help=f"CSV de trials (padrao: {TRIALS_CSV})",
    )
    parser.add_argument("--dry-run", action="store_true", help="Mede sem gravar")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    try:
        consolidate(args.csv, dry_run=args.dry_run)
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
