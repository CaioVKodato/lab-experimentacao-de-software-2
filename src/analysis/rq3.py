"""
Análise RQ3 — estrutura do código (CC, duplicação, LOC).

Issue #40. Usa ``data/trials.csv`` com ``loc``, ``duplicacao_pct`` e ``cc_mean``.
Normaliza complexidade por LOC (cc_por_kloc = cc_mean / loc * 1000).

Uso:
    python -m src.analysis.rq3
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "trials.csv"
FIGURES_DIR = ROOT / "docs" / "figures" / "s03"
REPORT_FILE = ROOT / "docs" / "s03" / "caio" / "analise_rq3.md"

CORES = {"IA": "#2196F3", "Manual": "#F44336"}


def rank_biserial(x, y) -> float:
    nx, ny = len(x), len(y)
    u, _ = stats.mannwhitneyu(x, y, alternative="two-sided")
    return 1 - (2 * u) / (nx * ny)


def interpret_r(r: float) -> str:
    r = abs(r)
    if r < 0.1:
        return "negligivel"
    if r < 0.3:
        return "pequeno"
    if r < 0.5:
        return "medio"
    return "grande"


def iqr(values: np.ndarray) -> float:
    if len(values) < 2:
        return 0.0
    q75, q25 = np.percentile(values, [75, 25])
    return float(q75 - q25)


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE)
    df.columns = df.columns.str.strip()
    for col in ("loc", "cc_mean", "duplicacao_pct"):
        if col not in df.columns:
            raise RuntimeError(
                f"coluna {col!r} ausente em {DATA_FILE}. "
                "Rode: python -m src.metrics.consolidate && python -m src.metrics.enrich_cc"
            )
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["loc", "cc_mean", "duplicacao_pct"]).copy()
    df = df[df["loc"] > 0]
    df["cc_por_kloc"] = df["cc_mean"] / df["loc"] * 1000.0
    return df


def descricao(series: pd.Series) -> dict:
    values = series.dropna().values.astype(float)
    return {
        "n": len(values),
        "mediana": float(np.median(values)) if len(values) else float("nan"),
        "iqr": iqr(values),
        "media": float(np.mean(values)) if len(values) else float("nan"),
    }


def comparar(ia: np.ndarray, manual: np.ndarray) -> dict | None:
    if len(ia) < 3 or len(manual) < 3:
        return None
    if np.std(np.concatenate([ia, manual])) == 0:
        return {"U": float("nan"), "p": float("nan"), "r": 0.0, "nota": "variancia zero"}
    u, p = stats.mannwhitneyu(ia, manual, alternative="two-sided")
    r = rank_biserial(ia, manual)
    return {"U": float(u), "p": float(p), "r": float(r), "nota": interpret_r(r)}


def split_tratamentos(df: pd.DataFrame, col: str) -> tuple[np.ndarray, np.ndarray]:
    ia = df[df["tratamento"] == "IA"][col].values.astype(float)
    manual = df[df["tratamento"] == "Manual"][col].values.astype(float)
    return ia, manual


def plot_boxplot(ia, manual, *, ylabel: str, title: str, filename: str) -> Path:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 5))
    bp = ax.boxplot([ia, manual], patch_artist=True, medianprops=dict(color="black", linewidth=2))
    ax.set_xticklabels(["Com IA", "Manual"])
    bp["boxes"][0].set_facecolor(CORES["IA"])
    bp["boxes"][1].set_facecolor(CORES["Manual"])
    rng = np.random.default_rng(42)
    for i, (dados, cor) in enumerate(zip([ia, manual], CORES.values()), start=1):
        jitter = rng.uniform(-0.08, 0.08, len(dados))
        ax.scatter(i + jitter, dados, color=cor, edgecolors="white", s=60, zorder=3, alpha=0.85)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.tight_layout()
    path = FIGURES_DIR / filename
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"[rq3] figura: {path}")
    return path


def _fmt_teste(stats_dict: dict | None) -> str:
    if not stats_dict:
        return "Nao aplicavel — amostra insuficiente (n < 3 por tratamento)."
    if stats_dict.get("nota") == "variancia zero":
        return "Nao aplicavel — variancia zero entre os tratamentos."
    return (
        f"Mann-Whitney U={stats_dict['U']:.1f}, p={stats_dict['p']:.4f}, "
        f"r={stats_dict['r']:.3f} ({stats_dict['nota']})"
    )


def _conclusao(stats_dict: dict | None, metrica: str) -> str:
    if not stats_dict or stats_dict.get("nota") == "variancia zero":
        return f"Sem evidencia inferencial para diferenca em {metrica}."
    if stats_dict["p"] < 0.05:
        return f"Diferenca significativa em {metrica} (alfa=0.05)."
    return f"Sem evidencia de diferenca significativa em {metrica} (alfa=0.05)."


def gerar_relatorio(df: pd.DataFrame, resultados: dict) -> Path:
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    d_loc_ia = descricao(df[df["tratamento"] == "IA"]["loc"])
    d_loc_man = descricao(df[df["tratamento"] == "Manual"]["loc"])
    d_cc_ia = descricao(df[df["tratamento"] == "IA"]["cc_mean"])
    d_cc_man = descricao(df[df["tratamento"] == "Manual"]["cc_mean"])
    d_n_ia = descricao(df[df["tratamento"] == "IA"]["cc_por_kloc"])
    d_n_man = descricao(df[df["tratamento"] == "Manual"]["cc_por_kloc"])
    d_dup_ia = descricao(df[df["tratamento"] == "IA"]["duplicacao_pct"])
    d_dup_man = descricao(df[df["tratamento"] == "Manual"]["duplicacao_pct"])

    md = f"""# RQ3 — Análise de estrutura do código (S03)

**Responsável:** Caio · **Issue:** #40

Depende da Issue #38 (`loc`, `duplicacao_pct`) e do enriquecimento `cc_mean` (Radon).

---

## Goal / hipóteses

**H0:** não há diferença na complexidade ciclomática média nem na duplicação entre tratamentos.
**H1:** o uso de assistente de IA altera complexidade e/ou duplicação.

LOC entra como **métrica de controle** (código de IA tende a ser mais verboso). A complexidade também é reportada normalizada: `cc_por_kloc = cc_mean / loc * 1000`.

## Dados

| Coluna | Trials |
|--------|--------|
| `loc` | {df['loc'].notna().sum()}/{len(df)} |
| `cc_mean` | {df['cc_mean'].notna().sum()}/{len(df)} |
| `duplicacao_pct` | {df['duplicacao_pct'].notna().sum()}/{len(df)} |

N = {len(df)} trials (9 IA + 9 Manual). Inferência: Mann-Whitney (amostras independentes por tratamento); descritivo: **mediana + IQR**.

---

## LOC (controle)

| Tratamento | n | Mediana | IQR |
|------------|---|---------|-----|
| Com IA | {d_loc_ia['n']} | {d_loc_ia['mediana']:.1f} | {d_loc_ia['iqr']:.1f} |
| Manual | {d_loc_man['n']} | {d_loc_man['mediana']:.1f} | {d_loc_man['iqr']:.1f} |

{_fmt_teste(resultados['loc'])}

{_conclusao(resultados['loc'], 'LOC')}

![Boxplot LOC](../../figures/s03/rq3_boxplot_loc.png)

---

## Complexidade ciclomática média (Radon `cc`)

| Tratamento | n | Mediana CC | IQR |
|------------|---|------------|-----|
| Com IA | {d_cc_ia['n']} | {d_cc_ia['mediana']:.3f} | {d_cc_ia['iqr']:.3f} |
| Manual | {d_cc_man['n']} | {d_cc_man['mediana']:.3f} | {d_cc_man['iqr']:.3f} |

{_fmt_teste(resultados['cc_mean'])}

{_conclusao(resultados['cc_mean'], 'complexidade ciclomática')}

### Normalizada por LOC (`cc_por_kloc`)

| Tratamento | n | Mediana | IQR |
|------------|---|---------|-----|
| Com IA | {d_n_ia['n']} | {d_n_ia['mediana']:.3f} | {d_n_ia['iqr']:.3f} |
| Manual | {d_n_man['n']} | {d_n_man['mediana']:.3f} | {d_n_man['iqr']:.3f} |

{_fmt_teste(resultados['cc_por_kloc'])}

{_conclusao(resultados['cc_por_kloc'], 'CC normalizada por LOC')}

![Boxplot CC](../../figures/s03/rq3_boxplot_cc.png)

![Boxplot CC/KLOC](../../figures/s03/rq3_boxplot_cc_por_kloc.png)

---

## Duplicação (`duplicacao_pct`, jscpd)

| Tratamento | n | Mediana (%) | IQR |
|------------|---|-------------|-----|
| Com IA | {d_dup_ia['n']} | {d_dup_ia['mediana']:.4f} | {d_dup_ia['iqr']:.4f} |
| Manual | {d_dup_man['n']} | {d_dup_man['mediana']:.4f} | {d_dup_man['iqr']:.4f} |

{_fmt_teste(resultados['duplicacao_pct'])}

{_conclusao(resultados['duplicacao_pct'], 'duplicacao')}

> Katas curtas (um único `solucao.py`) frequentemente resultam em 0% de duplicação no jscpd (sem clones >= 5 linhas). Isso limita a sensibilidade da comparação — LOC e CC carregam mais sinal neste N.

![Boxplot duplicacao](../../figures/s03/rq3_boxplot_duplicacao.png)

---

## Resumo RQ3

| Métrica | Teste | Conclusão |
|---------|-------|-----------|
| LOC (controle) | {_fmt_teste(resultados['loc'])} | {_conclusao(resultados['loc'], 'LOC')} |
| CC média | {_fmt_teste(resultados['cc_mean'])} | {_conclusao(resultados['cc_mean'], 'CC')} |
| CC / KLOC | {_fmt_teste(resultados['cc_por_kloc'])} | {_conclusao(resultados['cc_por_kloc'], 'CC/KLOC')} |
| Duplicação % | {_fmt_teste(resultados['duplicacao_pct'])} | {_conclusao(resultados['duplicacao_pct'], 'duplicacao')} |

### Interpretação geral

A comparação IA vs Manual na estrutura do código usa os 18 trials com métricas estáticas. LOC controla verbosidade; CC é olhada crua e normalizada. Duplicação via jscpd em arquivos pequenos tende a zero — interpretar com cautela. Preferimos mediana/IQR e Mann-Whitney dado o N reduzido (consistente com o desenho do laboratório).
"""
    REPORT_FILE.write_text(md, encoding="utf-8")
    print(f"[rq3] relatorio: {REPORT_FILE}")
    return REPORT_FILE


def main() -> None:
    df = load_data()
    print(f"[rq3] trials validos: {len(df)} (IA={sum(df.tratamento=='IA')}, Manual={sum(df.tratamento=='Manual')})")

    resultados = {}
    for col in ("loc", "cc_mean", "cc_por_kloc", "duplicacao_pct"):
        ia, manual = split_tratamentos(df, col)
        desc_ia, desc_man = descricao(pd.Series(ia)), descricao(pd.Series(manual))
        print(
            f"[rq3] {col}: IA mediana={desc_ia['mediana']:.4f} IQR={desc_ia['iqr']:.4f} | "
            f"Manual mediana={desc_man['mediana']:.4f} IQR={desc_man['iqr']:.4f}"
        )
        resultados[col] = comparar(ia, manual)

    ia_loc, man_loc = split_tratamentos(df, "loc")
    ia_cc, man_cc = split_tratamentos(df, "cc_mean")
    ia_n, man_n = split_tratamentos(df, "cc_por_kloc")
    ia_d, man_d = split_tratamentos(df, "duplicacao_pct")

    plot_boxplot(ia_loc, man_loc, ylabel="LOC", title="RQ3 — LOC (controle)", filename="rq3_boxplot_loc.png")
    plot_boxplot(ia_cc, man_cc, ylabel="CC media (Radon)", title="RQ3 — Complexidade ciclomatica", filename="rq3_boxplot_cc.png")
    plot_boxplot(ia_n, man_n, ylabel="CC / KLOC", title="RQ3 — CC normalizada por LOC", filename="rq3_boxplot_cc_por_kloc.png")
    plot_boxplot(ia_d, man_d, ylabel="Duplicacao (%)", title="RQ3 — Duplicacao (jscpd)", filename="rq3_boxplot_duplicacao.png")

    gerar_relatorio(df, resultados)
    print("[rq3] concluido.")


if __name__ == "__main__":
    main()
