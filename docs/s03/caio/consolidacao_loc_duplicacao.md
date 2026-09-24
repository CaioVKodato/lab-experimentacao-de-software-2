# Issue #38 — Consolidação LOC + duplicação (RQ3)

**Responsável:** Caio · **Sprint:** S03

## Onde entram as métricas

| Issue | O quê |
|-------|--------|
| **#38 (esta)** | Preenche `loc` e `duplicacao_pct` em `data/trials.csv` |
| **#40 (Issue C)** | Analisa RQ3 (CC/duplicação entre tratamentos) **usando** essas colunas |

Ou seja: o CSV é preenchido **aqui**; a análise estatística é a próxima tarefa.

## Fontes do ``solucao.py``

| Integrante | Caminho |
|------------|---------|
| Caio | `trials/caio/kX-ia/` ou `kX-manual/` |
| Henrique | `trials/henrique/kX-ia/` ou `kX-sem-ia/` |
| Jonas | `katas/kX/solucao.py` (PR #37) |

## Como rodar

```text
python -m src.metrics.consolidate
python -m src.metrics.consolidate --dry-run
```

Requisitos: Node.js + `npx` (usa `jscpd@3.5.4`, compatível com Node 16).

## Critério de pronto

- 18 linhas em `data/trials.csv`
- Colunas `loc` e `duplicacao_pct` sem célula vazia
- Tempo (RQ1) do Henrique/Jonas pode ainda estar vazio — isso não bloqueia a #38; bloqueia a #39 (Wilcoxon) até eles registrarem
