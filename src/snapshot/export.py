"""Monta as linhas do snapshot e grava CSV novo (nunca sobrescreve o anterior)."""

from __future__ import annotations

import csv
from pathlib import Path

from src.snapshot.constants import FIELDNAMES


def _join(nodes: list[dict] | None, key: str) -> str:
    if not nodes:
        return ""
    return ";".join(node.get(key, "") for node in nodes if node.get(key))


def row_from_node(
    node: dict,
    *,
    snapshot_at: str,
    sprint: str,
    project_title: str,
) -> dict[str, str]:
    content = node.get("content") or {}
    issue_number = content.get("number")
    return {
        "snapshot_at": snapshot_at,
        "sprint": sprint,
        "project_title": project_title,
        "item_id": node.get("id") or "",
        "item_type": content.get("__typename") or "",
        "issue_number": "" if issue_number is None else str(issue_number),
        "title": content.get("title") or "",
        "status": (node.get("status") or {}).get("name") or "",
        "assignees": _join((content.get("assignees") or {}).get("nodes"), "login"),
        "state": content.get("state") or "",
        "labels": _join((content.get("labels") or {}).get("nodes"), "name"),
        "url": content.get("url") or "",
        "item_updated_at": node.get("updatedAt") or "",
    }


def save_csv(rows: list[dict[str, str]], path: Path) -> Path:
    if path.exists():
        raise FileExistsError(
            f"{path} já existe — o snapshot é histórico, escolha outra data ou não sobrescreva"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    return path
