"""
src/analysis/analyze_s03.py
Análise estatística RQ1/RQ2 (tempo, taxa) e RQ3 (estrutura) — Sprint S03

RQ1/RQ2: Issue #47 (Henrique)
RQ3: Issue #40 (Caio) — ver também ``python -m src.analysis.rq3``
"""

from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from src.analysis.rq3 import main as run_rq3

ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "trials.csv"
FIGURES_DIR = ROOT / "docs" / "figures" / "s03"
REPORT_FILE = ROOT / "docs" / "s03" / "analise_estatistica_s03.md"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

CORES = {"IA": "#2196F3", "Manual": "#F44336"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def rank_biserial(x, y):
    nx, ny = len(x), len(y)
    u, _ = stats.mannwhitneyu(x, y, alternative="two-sided")
    return 1 - (2 * u) / (nx * ny)


def interpret_r(r):
    r = abs(r)
    if r < 0.1:
        return "negligível"
    if r < 0.3:
        return "pequeno"
    if r < 0.5:
        return "médio"
    return "grande"


# ---------------------------------------------------------------------------
# Carga
# ---------------------------------------------------------------------------

def load_data():
    df = pd.read_csv(DATA_FILE)
    df.columns = df.columns.str.strip()
    df["tratamento"] = df["tratamento"].str.strip()
    df["integrante"] = df["integrante"].str.strip()
    df["tempo_s"] = pd.to_numeric(df["tempo_s"], errors="coerce")
    df["taxa_sucesso"] = pd.to_numeric(df["taxa_sucesso"], errors="coerce")
    return df


# ---------------------------------------------------------------------------
# RQ1 — Tempo
# ---------------------------------------------------------------------------

def analise_rq1(df):
    df_t = df.dropna(subset=["tempo_s"])
    n_ok = len(df_t)
    print(f"\n{'='*60}\nRQ1 — Tempo até passar nos testes\n{'='*60}")
    print(f"Trials com tempo registrado: {n_ok}/{len(df)}")

    if n_ok == 0:
        print("Sem dados de tempo. Análise RQ1 ignorada.")
        return None, None, None

    ia = df_t[df_t["tratamento"] == "IA"]["tempo_s"].values
    manual = df_t[df_t["tratamento"] == "Manual"]["tempo_s"].values

    print(f"\nIA     n={len(ia)}: mediana={np.median(ia):.0f}s  média={np.mean(ia):.0f}s  DP={np.std(ia, ddof=1):.0f}s")
    print(f"Manual n={len(manual)}: mediana={np.median(manual):.0f}s  média={np.mean(manual):.0f}s  DP={np.std(manual, ddof=1):.0f}s")

    if len(ia) < 3 or len(manual) < 3:
        print("Amostra insuficiente para teste — apenas descritiva.")
        return ia, manual, None

    u, p = stats.mannwhitneyu(ia, manual, alternative="two-sided")
    r = rank_biserial(ia, manual)
    print(f"\nMann-Whitney U={u:.1f}  p={p:.4f}  r={r:.3f} [{interpret_r(r)}]")
    print(f"AVISO: n={len(ia)+len(manual)} trials — inferência muito limitada.")
    if p < 0.05:
        print("Resultado: diferenca significativa (alfa=0.05).")
    else:
        print("Resultado: sem evidencia de diferenca significativa (alfa=0.05).")

    return ia, manual, {"U": u, "p": p, "r": r, "n_ia": len(ia), "n_manual": len(manual)}


# ---------------------------------------------------------------------------
# RQ2 — Taxa de sucesso
# ---------------------------------------------------------------------------

def analise_rq2(df):
    df_tx = df.dropna(subset=["taxa_sucesso"])
    print(f"\n{'='*60}\nRQ2 — Taxa de sucesso\n{'='*60}")
    print(f"Trials com taxa_sucesso: {len(df_tx)}/{len(df)}")

    if df_tx.empty:
        print("Sem dados de taxa de sucesso.")
        return None, None, None

    ia = df_tx[df_tx["tratamento"] == "IA"]["taxa_sucesso"].values
    manual = df_tx[df_tx["tratamento"] == "Manual"]["taxa_sucesso"].values

    print(f"\nIA     n={len(ia)}: mediana={np.median(ia):.4f}  média={np.mean(ia):.4f}")
    print(f"Manual n={len(manual)}: mediana={np.median(manual):.4f}  média={np.mean(manual):.4f}")

    todos = np.concatenate([ia, manual])
    if np.std(todos) == 0:
        print("Variância zero — todos os trials: 100% de sucesso. Teste não aplicável.")
        return ia, manual, None

    u, p = stats.mannwhitneyu(ia, manual, alternative="two-sided")
    r = rank_biserial(ia, manual)
    print(f"\nMann-Whitney U={u:.1f}  p={p:.4f}  r={r:.3f} [{interpret_r(r)}]")
    return ia, manual, {"U": u, "p": p, "r": r}


# ---------------------------------------------------------------------------
# Figuras
# ---------------------------------------------------------------------------

def plot_boxplot_tempo(ia, manual):
    if ia is None:
        return
    fig, ax = plt.subplots(figsize=(6, 5))
    bp = ax.boxplot([ia, manual], patch_artist=True,
                    medianprops=dict(color="black", linewidth=2))
    ax.set_xticklabels(["Com IA", "Manual"])
    bp["boxes"][0].set_facecolor(CORES["IA"])
    bp["boxes"][1].set_facecolor(CORES["Manual"])
    for i, (dados, cor) in enumerate(zip([ia, manual], CORES.values()), start=1):
        jitter = np.random.default_rng(42).uniform(-0.08, 0.08, len(dados))
        ax.scatter(i + jitter, dados, color=cor, edgecolors="white", s=70, zorder=3, alpha=0.85)
    ax.set_ylabel("Tempo (segundos)")
    ax.set_title("RQ1 — Tempo até passar nos testes")
    plt.tight_layout()
    path = FIGURES_DIR / "rq1_boxplot_tempo.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Figura: {path}")


def plot_barras_taxa(ia, manual):
    if ia is None:
        return
    fig, ax = plt.subplots(figsize=(6, 4))
    medias = [np.mean(ia) * 100, np.mean(manual) * 100]
    erros = [np.std(ia, ddof=1) * 100 if len(ia) > 1 else 0,
             np.std(manual, ddof=1) * 100 if len(manual) > 1 else 0]
    bars = ax.bar(["Com IA", "Manual"], medias, yerr=erros, capsize=5,
                  color=list(CORES.values()), edgecolor="white", width=0.5)
    ax.set_ylim(0, 115)
    ax.set_ylabel("Taxa de sucesso média (%)")
    ax.set_title("RQ2 — Taxa de sucesso nos testes")
    for bar, val in zip(bars, medias):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                f"{val:.1f}%", ha="center", va="bottom")
    plt.tight_layout()
    path = FIGURES_DIR / "rq2_barras_taxa_sucesso.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Figura: {path}")


def plot_strip_por_integrante(df):
    df_t = df.dropna(subset=["tempo_s"])
    if df_t.empty:
        return
    fig, ax = plt.subplots(figsize=(7, 5))
    integrantes = sorted(df_t["integrante"].unique())
    rng = np.random.default_rng(42)
    for i, nome in enumerate(integrantes):
        sub = df_t[df_t["integrante"] == nome]
        for _, row in sub.iterrows():
            cor = CORES[row["tratamento"]]
            marker = "o" if row["tratamento"] == "IA" else "s"
            ax.scatter(i + rng.uniform(-0.1, 0.1), row["tempo_s"],
                       color=cor, marker=marker, s=80, zorder=3, alpha=0.85)
    ax.set_xticks(range(len(integrantes)))
    ax.set_xticklabels(integrantes)
    ax.set_ylabel("Tempo (segundos)")
    ax.set_title("RQ1 — Tempo por integrante e tratamento")
    ax.legend(handles=[
        mpatches.Patch(color=CORES["IA"], label="Com IA"),
        mpatches.Patch(color=CORES["Manual"], label="Manual"),
    ])
    plt.tight_layout()
    path = FIGURES_DIR / "rq1_strip_por_integrante.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Figura: {path}")


# ---------------------------------------------------------------------------
# Relatório
# ---------------------------------------------------------------------------

def gerar_relatorio(df, stats_rq1, stats_rq2):
    df_t = df.dropna(subset=["tempo_s"])
    df_tx = df.dropna(subset=["taxa_sucesso"])

    def fmt_stats(grp):
        return f"mediana={np.median(grp):.0f}s  média={np.mean(grp):.0f}s  DP={np.std(grp, ddof=1):.0f}s" if len(grp) > 1 else f"n={len(grp)}"

    rq1_ia = df_t[df_t["tratamento"] == "IA"]["tempo_s"].values if not df_t.empty else np.array([])
    rq1_manual = df_t[df_t["tratamento"] == "Manual"]["tempo_s"].values if not df_t.empty else np.array([])
    rq2_ia = df_tx[df_tx["tratamento"] == "IA"]["taxa_sucesso"].values if not df_tx.empty else np.array([])
    rq2_manual = df_tx[df_tx["tratamento"] == "Manual"]["taxa_sucesso"].values if not df_tx.empty else np.array([])

    rq1_teste = (
        f"Mann-Whitney U={stats_rq1['U']:.1f}, p={stats_rq1['p']:.4f}, "
        f"r={stats_rq1['r']:.3f} ({interpret_r(stats_rq1['r'])})"
        if stats_rq1 else "Não aplicável — amostra insuficiente ou dados ausentes."
    )
    rq2_teste = (
        f"Mann-Whitney U={stats_rq2['U']:.1f}, p={stats_rq2['p']:.4f}, "
        f"r={stats_rq2['r']:.3f} ({interpret_r(stats_rq2['r'])})"
        if stats_rq2 else "Não aplicável — variância zero (100% de sucesso em todos os trials) ou dados ausentes."
    )

    md = f"""# Análise Estatística — RQ1 e RQ2 (S03)

**Responsável:** Henrique Volponi · **Issue:** #47

---

## Dados utilizados

| Coluna | Trials completos |
|--------|-----------------|
| `tempo_s` | {len(df_t)}/{len(df)} |
| `taxa_sucesso` | {len(df_tx)}/{len(df)} |

> **Limitação:** apenas o integrante Caio possui tempo registrado. Henrique e Jonas ainda não registraram seus tempos (ver notas em `data/trials.csv`). A análise de RQ1 reflete somente os 6 trials do Caio (3 IA, 3 Manual).

---

## RQ1 — Tempo até passar nos testes (time-to-green)

**H0:** não há diferença no tempo entre os tratamentos.
**H1:** o uso de IA reduz o tempo até passar nos testes.

### Estatísticas descritivas

| Tratamento | n | Mediana (s) | Média (s) | DP (s) |
|-----------|---|------------|----------|--------|
| Com IA | {len(rq1_ia)} | {np.median(rq1_ia):.0f} | {np.mean(rq1_ia):.0f} | {np.std(rq1_ia, ddof=1):.0f} |
| Manual | {len(rq1_manual)} | {np.median(rq1_manual):.0f} | {np.mean(rq1_manual):.0f} | {np.std(rq1_manual, ddof=1):.0f} |

### Teste estatístico

{rq1_teste}

### Interpretação

Com apenas {len(df_t)} trials com tempo registrado, qualquer conclusão é preliminar. Os dados do Caio indicam que os tempos com IA (mediana {np.median(rq1_ia):.0f}s) e sem IA (mediana {np.median(rq1_manual):.0f}s) foram similares, sem diferença estatisticamente significativa. A análise completa depende do preenchimento dos tempos de Henrique e Jonas.

### Visualizações

![Boxplot tempo](../figures/s03/rq1_boxplot_tempo.png)

![Strip por integrante](../figures/s03/rq1_strip_por_integrante.png)

---

## RQ2 — Taxa de sucesso nos testes

**H0:** não há diferença na taxa de sucesso entre os tratamentos.
**H1:** o uso de IA aumenta a taxa de sucesso.

### Estatísticas descritivas

| Tratamento | n | Média (%) |
|-----------|---|----------|
| Com IA | {len(rq2_ia)} | {np.mean(rq2_ia)*100:.1f}% |
| Manual | {len(rq2_manual)} | {np.mean(rq2_manual)*100:.1f}% |

### Teste estatístico

{rq2_teste}

### Interpretação

Todos os trials com dados registrados atingiram 100% de taxa de sucesso nos dois tratamentos. Não há variância para detectar diferença — não é possível rejeitar nem confirmar H0 com esses dados. Isso indica que os katas, dentro do time-box de 35 min, foram resolvíveis com ou sem IA para os participantes que completaram os trials.

### Visualização

![Barras taxa de sucesso](../figures/s03/rq2_barras_taxa_sucesso.png)

---

## Resumo

| RQ | Resultado | Tamanho de efeito | Conclusão |
|----|----------|------------------|-----------|
| RQ1 — Tempo | {"p=" + f"{stats_rq1['p']:.4f}" if stats_rq1 else "n/a"} | {"r=" + f"{stats_rq1['r']:.3f}" if stats_rq1 else "n/a"} | Não significativo — dados insuficientes |
| RQ2 — Taxa | n/a | n/a | Variância zero — análise inviável |

> Análise deverá ser refeita após preenchimento completo de `tempo_s` para Henrique e Jonas.
"""

    REPORT_FILE.write_text(md, encoding="utf-8")
    print(f"\nRelatório: {REPORT_FILE}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    df = load_data()
    ia_t, manual_t, stats_rq1 = analise_rq1(df)
    ia_tx, manual_tx, stats_rq2 = analise_rq2(df)
    plot_boxplot_tempo(ia_t, manual_t)
    plot_barras_taxa(ia_tx, manual_tx)
    plot_strip_por_integrante(df)
    gerar_relatorio(df, stats_rq1, stats_rq2)
    print("\n--- RQ3 (Issue #40) ---")
    run_rq3()
    print("\nAnalise concluida (RQ1/RQ2/RQ3).")


if __name__ == "__main__":
    main()
