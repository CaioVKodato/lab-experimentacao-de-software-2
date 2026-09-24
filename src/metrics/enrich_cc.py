"""Preenche ``cc_mean`` (Radon) em ``data/trials.csv`` para a RQ3.

Não reexecuta jscpd — só complexidade ciclomática média de ``solucao.py``.

Uso:
    python -m src.metrics.enrich_cc
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from src.metrics.constants import DATA_DIR
from src.metrics.radon_runner import compute_cc
from src.metrics.trial_sources import TRIAL_SOURCES

TRIALS_CSV = DATA_DIR / "trials.csv"


def enrich(path: Path = TRIALS_CSV, *, dry_run: bool = False) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    if "cc_mean" not in fieldnames:
        # coloca cc_mean depois de loc
        if "loc" in fieldnames:
            idx = fieldnames.index("loc") + 1
            fieldnames[idx:idx] = ["cc_mean"]
        else:
            fieldnames.append("cc_mean")

    by_id = {source.trial_id: source for source in TRIAL_SOURCES}
    for row in rows:
        source = by_id.get(row["trial_id"])
        if source is None:
            raise RuntimeError(f"trial_id desconhecido: {row['trial_id']}")
        cc = compute_cc(source.solucao.parent)
        row["cc_mean"] = f"{cc:.4f}"
        print(f"[enrich_cc] {row['trial_id']:24}  cc_mean={cc:.4f}")

    empty = [r["trial_id"] for r in rows if not str(r.get("cc_mean", "")).strip()]
    if empty:
        raise RuntimeError(f"cc_mean vazio: {empty}")

    if dry_run:
        print(f"[enrich_cc] dry-run: {len(rows)} linhas")
        return rows

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"[enrich_cc] {len(rows)} linhas -> {path}")
    return rows


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Preenche cc_mean no trials.csv (Issue #40).")
    parser.add_argument("--csv", type=Path, default=TRIALS_CSV)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        enrich(args.csv, dry_run=args.dry_run)
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
