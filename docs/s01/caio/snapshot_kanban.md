# Snapshot do Kanban (S01 · Caio · #6)

Módulo `src/snapshot`. O Projects v2 não guarda histórico de coluna; cada execução gera um **CSV novo** em `snapshots/` (base dos Labs 04 e 05).

```text
python -m src.snapshot --sprint Lab02S01
```

Saída: `snapshots/lab02s01-AAAA-MM-DD.csv`. Não sobrescrever arquivo antigo.

Requer `gh` autenticado com `read:project`:

```text
gh auth login --scopes "repo,project,read:project"
```

Colunas iguais às do Lab01: `snapshot_at`, `sprint`, `issue_number`, `title`, `status`, `assignees`, `state`, `labels`, `url`.
