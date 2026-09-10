# Métricas Estáticas (RQ3) — Ambiente e Script

**Responsável:** Henrique | **Issue:** #3 | **Sprint:** S01

## Dependências

```
pip install -r requirements.txt
```

> `jscpd` requer Node.js (≥ 16). Se `npx` estiver disponível, o script o baixa automaticamente na primeira execução. Caso contrário, instale globalmente: `npm install -g jscpd`.

## Métricas coletadas

| Campo | Ferramenta | Descrição |
|---|---|---|
| `loc` | Python nativo | Linhas físicas totais nos `.py` do diretório |
| `cc_mean` | Radon `cc` | Complexidade ciclomática média de funções/métodos |
| `mi_mean` | Radon `mi` | Maintainability Index médio dos arquivos (opcional) |
| `duplication_pct` | jscpd | % de linhas duplicadas |

Valores `-1.0` indicam ferramenta indisponível no ambiente.

## Uso

```bash
# Ver resultado sem gravar
python -m src.metrics --dir katas/K1/solucao --dry-run

# Gravar no CSV padrão (data/metrics.csv)
python -m src.metrics --dir katas/K1/solucao --trial-id Caio-K1-IA-1

# Gravar em CSV alternativo
python -m src.metrics --dir katas/K1/solucao --trial-id Caio-K1-IA-1 --output data/metrics.csv
```

## Saída

```
[metrics] trial_id     : Caio-K1-IA-1
[metrics] diretorio    : /abs/path/katas/K1/solucao
[metrics] loc          : 42
[metrics] cc_mean      : 2.3333
[metrics] mi_mean      : 68.1200
[metrics] duplication% : 0.0000
[metrics] csv          : data/metrics.csv
```

O CSV `data/metrics.csv` acumula uma linha por chamada, permitindo consolidação posterior no dashboard (S03).
