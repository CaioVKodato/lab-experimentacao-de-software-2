"""GitHub Projects v2 do Lab02 (mesmo contrato de colunas do Lab01)."""

from __future__ import annotations

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SNAPSHOTS_DIR = ROOT_DIR / "snapshots"

PROJECT_OWNER = "CaioVKodato"
PROJECT_NUMBER = 7
PROJECT_STATUS_FIELD = "Status"

FIELDNAMES = (
    "snapshot_at",
    "sprint",
    "project_title",
    "item_id",
    "item_type",
    "issue_number",
    "title",
    "status",
    "assignees",
    "state",
    "labels",
    "url",
    "item_updated_at",
)

QUERY = """
query BoardSnapshot($login: String!, $number: Int!, $first: Int!, $after: String, $statusField: String!) {
  user(login: $login) {
    projectV2(number: $number) {
      title
      url
      items(first: $first, after: $after) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          updatedAt
          content {
            __typename
            ... on Issue {
              number
              title
              state
              url
              assignees(first: 10) { nodes { login } }
              labels(first: 10) { nodes { name } }
            }
            ... on DraftIssue { title }
            ... on PullRequest {
              number
              title
              state
              url
            }
          }
          status: fieldValueByName(name: $statusField) {
            ... on ProjectV2ItemFieldSingleSelectValue { name }
          }
        }
      }
    }
  }
}
"""
