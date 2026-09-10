"""Leitura paginada do Project v2 via `gh api graphql`."""

from __future__ import annotations

import json
import subprocess

from src.snapshot.constants import (
    PROJECT_NUMBER,
    PROJECT_OWNER,
    PROJECT_STATUS_FIELD,
    QUERY,
)


def _gh_graphql(variables: dict) -> dict:
    cmd = [
        "gh",
        "api",
        "graphql",
        "-f",
        f"query={QUERY}",
        "-f",
        f"login={variables['login']}",
        "-F",
        f"number={variables['number']}",
        "-F",
        f"first={variables['first']}",
        "-f",
        f"statusField={variables['statusField']}",
    ]
    if variables.get("after"):
        cmd.extend(["-f", f"after={variables['after']}"])

    completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise RuntimeError(
            "falha ao ler o GitHub Projects. "
            "Rode `gh auth login --scopes \"repo,project,read:project\"`. "
            f"Detalhe: {detail}"
        )
    body = json.loads(completed.stdout)
    if body.get("errors"):
        raise RuntimeError(body["errors"])
    return body


def fetch_board_items() -> tuple[str, list[dict]]:
    items: list[dict] = []
    after: str | None = None
    project_title = ""

    while True:
        body = _gh_graphql(
            {
                "login": PROJECT_OWNER,
                "number": PROJECT_NUMBER,
                "first": 50,
                "after": after,
                "statusField": PROJECT_STATUS_FIELD,
            }
        )
        user = (body.get("data") or {}).get("user") or {}
        project = user.get("projectV2")
        if not project:
            raise RuntimeError(
                f"Project v2 não encontrado: {PROJECT_OWNER}/{PROJECT_NUMBER}"
            )

        project_title = project.get("title") or project_title
        connection = project["items"]
        for node in connection.get("nodes") or []:
            if node:
                items.append(node)

        page_info = connection["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        after = page_info["endCursor"]

    return project_title, items
