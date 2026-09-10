"""Exporta o board do Lab02 para snapshots/.

    python -m src.snapshot --sprint Lab02S01
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime

from src.snapshot.constants import PROJECT_NUMBER, PROJECT_OWNER, PROJECT_STATUS_FIELD, SNAPSHOTS_DIR
from src.snapshot.export import row_from_node, save_csv
from src.snapshot.query import fetch_board_items


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Snapshot do GitHub Projects v2 (Kanban).")
    parser.add_argument("--sprint", default="Lab02S01", help="Identificador da sprint")
    args = parser.parse_args(argv)

    now = datetime.now().astimezone()
    snapshot_at = now.isoformat(timespec="seconds")
    out_path = SNAPSHOTS_DIR / f"{args.sprint.lower()}-{now.date().isoformat()}.csv"

    print(
        f"[snapshot] lendo Project {PROJECT_OWNER}/{PROJECT_NUMBER} "
        f"(campo {PROJECT_STATUS_FIELD})..."
    )
    try:
        project_title, nodes = fetch_board_items()
        rows = [
            row_from_node(
                node,
                snapshot_at=snapshot_at,
                sprint=args.sprint,
                project_title=project_title,
            )
            for node in nodes
        ]
        save_csv(rows, out_path)
    except (RuntimeError, FileExistsError) as exc:
        print(f"Erro no snapshot: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"[snapshot] {len(rows)} itens → {out_path}")
    print(f"[snapshot] projeto={project_title!r} sprint={args.sprint}")


if __name__ == "__main__":
    main()
