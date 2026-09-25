"""
Dashboard de Visualização — LAB02 (IA vs. Codificação Manual)
Issue: #41

Lê data/trials.csv diretamente e recalcula RQ1, RQ2 e RQ3 do zero — não depende
dos relatórios intermediários das Issues B (#47) e C (#40), que podem estar
desatualizados em relação à versão mais recente do CSV (ex.: após correções de
dados). Isso garante que o painel final é sempre consistente com o dado atual.

Gera:
  - Um painel único (dashboard_s03.png) com 4 subplots: tempo, taxa de sucesso,
    complexidade ciclomática, duplicação — todos comparando IA vs. Manual
  - Um relatório textual (dashboard_s03.md) com estatística descritiva,
    testes de hipótese e transparência sobre completude dos dados

Uso:
    python3 src/analysis/dashboard_s03.py
"""

import os
import warnings
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = "data/trials.csv"
FIG_PATH = "docs/figures/s03/dashboard_s03.png"
REPORT_PATH = "docs/s03/dashboard_s03.md"

os.makedirs(os.path.dirname(FIG_PATH), exist_ok=True)
os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)

sns.set_style("whitegrid")
PALETA = {"IA": "#4c72b0", "Manual": "#c44e52"}
ORDEM = ["IA", "Manual"]


def carregar_dados(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def completude(df: pd.DataFrame, coluna: str) -> dict:
    total = len(df)
    validos = df[coluna].notna().sum()
    por_integrante = df.groupby("integrante")[coluna].apply(lambda s: s.notna().sum())
    return {"total": total, "validos": validos, "por_integrante": por_integrante.to_dict()}


def descritiva(df: pd.DataFrame, coluna: str) -> pd.DataFrame:
    d = df.dropna(subset=[coluna])
    if len(d) == 0:
        return None
    return d.groupby("tratamento")[coluna].agg(
        n="count", mediana="median", q1=lambda x: x.quantile(0.25),
        q3=lambda x: x.quantile(0.75)
    ).reindex(ORDEM)


def teste_dois_grupos(df: pd.DataFrame, coluna: str) -> dict:
    """Wilcoxon pareado por integrante (n pequeno, respeita within-subject) +
    Mann-Whitney não pareado (mais poder, ignora pareamento)."""
    d = df.dropna(subset=[coluna])
    resultado = {}

    pareado = d.groupby(["integrante", "tratamento"])[coluna].median().unstack()
    pareado = pareado.dropna()
    if len(pareado) >= 2 and "IA" in pareado.columns and "Manual" in pareado.columns:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                stat_w, p_w = stats.wilcoxon(pareado["IA"], pareado["Manual"])
            except ValueError:
                stat_w, p_w = np.nan, np.nan
        resultado["wilcoxon"] = {"n_pares": len(pareado), "p_valor": p_w}
    else:
        resultado["wilcoxon"] = None

    grupo_ia = d[d["tratamento"] == "IA"][coluna]
    grupo_manual = d[d["tratamento"] == "Manual"][coluna]
    if len(grupo_ia) >= 3 and len(grupo_manual) >= 3:
        stat_u, p_u = stats.mannwhitneyu(grupo_ia, grupo_manual, alternative="two-sided")
        resultado["mannwhitney"] = {"n_ia": len(grupo_ia), "n_manual": len(grupo_manual), "p_valor": p_u}
    else:
        resultado["mannwhitney"] = None

    return resultado


def fmt_p(p):
    if p is None or (isinstance(p, float) and np.isnan(p)):
        return "n/d"
    marca = " *" if p < 0.05 else ""
    return f"{p:.4f}{marca}"


def montar_painel(df: pd.DataFrame):
    fig, axes = plt.subplots(2, 2, figsize=(11, 9))

    specs = [
        (axes[0, 0], "tempo_s", "Tempo até passar nos testes (s)", "RQ1 — Tempo"),
        (axes[0, 1], "taxa_sucesso", "Taxa de sucesso", "RQ2 — Taxa de sucesso"),
        (axes[1, 0], "cc_mean", "Complexidade ciclomática média", "RQ3 — Complexidade"),
        (axes[1, 1], "duplicacao_pct", "% Duplicação de código", "RQ3 — Duplicação"),
    ]

    for ax, coluna, ylabel, titulo in specs:
        d = df.dropna(subset=[coluna])
        if len(d) == 0:
            ax.text(0.5, 0.5, "Sem dados", ha="center", va="center", transform=ax.transAxes)
            ax.set_title(titulo)
            continue
        sns.boxplot(data=d, x="tratamento", y=coluna, order=ORDEM, hue="tratamento",
                    palette=PALETA, legend=False, ax=ax)
        sns.stripplot(data=d, x="tratamento", y=coluna, order=ORDEM, ax=ax,
                       color="black", alpha=0.5, jitter=True, size=4)
        ax.set_title(f"{titulo}  (n={len(d)})")
        ax.set_ylabel(ylabel)
        ax.set_xlabel("")

    fig.suptitle("Dashboard S03 — LAB02: IA vs. Codificação Manual", fontsize=14, y=1.00)
    fig.tight_layout()
    fig.savefig(FIG_PATH, dpi=150, bbox_inches="tight")
    plt.close(fig)


def gerar_relatorio(df: pd.DataFrame) -> str:
    linhas = ["# Dashboard S03 — LAB02\n"]
    linhas.append("Painel consolidado recalculado diretamente de `data/trials.csv` (Issue #41).\n")

    linhas.append("## Completude dos dados\n")
    for coluna, nome in [("tempo_s", "tempo_s (RQ1)"), ("taxa_sucesso", "taxa_sucesso (RQ2)"),
                          ("cc_mean", "cc_mean (RQ3)"), ("duplicacao_pct", "duplicacao_pct (RQ3)")]:
        c = completude(df, coluna)
        linhas.append(f"- **{nome}**: {c['validos']}/{c['total']} trials preenchidos "
                       f"({c['por_integrante']})")
    linhas.append("")

    for coluna, nome_rq in [("tempo_s", "RQ1 — Tempo"), ("taxa_sucesso", "RQ2 — Taxa de sucesso"),
                             ("cc_mean", "RQ3 — Complexidade"), ("duplicacao_pct", "RQ3 — Duplicação")]:
        linhas.append(f"## {nome_rq}\n")
        desc = descritiva(df, coluna)
        if desc is None:
            linhas.append("Sem dados suficientes.\n")
            continue
        linhas.append(desc.to_markdown() + "\n")
        testes = teste_dois_grupos(df, coluna)
        if testes["wilcoxon"]:
            linhas.append(f"Wilcoxon pareado (n={testes['wilcoxon']['n_pares']} pares): "
                           f"p={fmt_p(testes['wilcoxon']['p_valor'])}")
        if testes["mannwhitney"]:
            linhas.append(f"Mann-Whitney (n={testes['mannwhitney']['n_ia']} vs "
                           f"{testes['mannwhitney']['n_manual']}): p={fmt_p(testes['mannwhitney']['p_valor'])}")
        linhas.append("")

    linhas.append("![Dashboard](../figures/s03/dashboard_s03.png)\n")
    linhas.append("\n*(marcado com \\* = p < 0.05)*")
    return "\n".join(linhas)


def main():
    df = carregar_dados(DATA_PATH)
    montar_painel(df)
    relatorio = gerar_relatorio(df)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(relatorio)
    print(f"Painel salvo em: {FIG_PATH}")
    print(f"Relatório salvo em: {REPORT_PATH}")


if __name__ == "__main__":
    main()