# Lab02 — Assistentes de IA vs. codificação manual

Repositório do **Laboratório 02** — experimento controlado (crossover within-subject).

Disciplina: Laboratório de Experimentação de Software  
Curso: Engenharia de Software · 6º período · Noite  
Professor: Danilo Maia

## Integrantes

- [CaioVKodato](https://github.com/CaioVKodato) (Caio)
- [Henrique-volponi](https://github.com/Henrique-volponi) (Henrique)
- [Kjonps](https://github.com/Kjonps) (Jonas Martins)

## GitHub Projects

Board Kanban (Projects v2), vinculado ao repositório:  
https://github.com/users/CaioVKodato/projects/7  

Aba Projects do repo:  
https://github.com/CaioVKodato/lab-experimentacao-de-software-2/projects

Colunas e WIP iguais ao Lab01: `Backlog → To Do → Doing → Review → Done`, **WIP = 6** em Doing (~2 por pessoa).

## Decisões fixas do grupo

| Item | Valor |
|------|--------|
| Linguagem | Python 3 |
| Métricas estáticas | Radon (`cc`, `mi`) + jscpd (duplicação) + LOC |
| Assistente de IA | **um só para todos os trials** (definir na S01 e travar no desenho) |
| Katas | 6, dificuldade comparável, baixa indexação (Jonas valida) |
| Time-box | 35 min/trial (censurado em 35 min se não ficar verde) |
| Desenho | Crossover within-subject, contrabalanceado |
| Inferência | Wilcoxon pareado; descritivo = mediana + IQR |

## Divisão por sprint

Cada integrante precisa ser **Assignee** de pelo menos uma Issue **com artefato commitado** em **S01, S02 e S03**. Commits devem citar `#N` da Issue.

### S01 — Desenho + preparação (Caio começa)

| Issue | Assignee | Artefato esperado |
|-------|----------|-------------------|
| Estrutura do repo, labels e Kanban | **Caio** | README, pastas, Project |
| Script de cronometragem / coleta de tempo | **Caio** | `src/timing/` + CSV de trials |
| Ambiente + métricas estáticas (Radon/jscpd) | **Henrique** | `requirements.txt`, `src/metrics/` |
| Seleção das 6 katas + testes de aceitação | **Jonas** | `katas/` com testes |
| Hipóteses, GQM e ameaças à validade | **Jonas** | `docs/s01/desenho-do-experimento.md` |
| Snapshot do Kanban S01 | **Caio** | `snapshots/lab02s01-AAAA-MM-DD.csv` |

### S02 — Execução (18 trials)

Cada um resolve as **6 katas** (3 com IA, 3 sem), ordem contrabalanceada. **Uma Issue por trial**, Assignee = quem executou.

| Integrante | Ordem | Tratamentos |
|------------|-------|-------------|
| Caio | K1→K2→K3→K4→K5→K6 | IA, Manual, IA, Manual, IA, Manual |
| Henrique | K4→K5→K6→K1→K2→K3 | Manual, IA, Manual, IA, Manual, IA |
| Jonas | K6→K5→K4→K3→K2→K1 | IA, Manual, Manual, IA, IA, Manual |

Isso dá 9 trials IA + 9 Manual e espalha o efeito de aprendizado.

### S03 — Análise + dashboard

| Issue | Assignee | Artefato |
|-------|----------|----------|
| Wilcoxon RQ1 (tempo) e RQ2 (defeitos) | **Caio** | `src/analysis/` + `docs/s03/caio/` |
| Análise RQ3 (Radon/jscpd/LOC) | **Henrique** | `src/analysis/` + `docs/s03/henrique/` |
| Dashboard (Pandas/Matplotlib/Seaborn) | **Jonas** | `src/dashboard/` + figuras |
| Snapshot do Kanban S03 | **Jonas** | `snapshots/lab02s03-AAAA-MM-DD.csv` |

### Relatório Final

| Issue | Assignee | Seções |
|-------|----------|--------|
| Introdução + hipóteses | **Caio** | (i) |
| Metodologia reproduzível | **Henrique** | (ii) |
| Resultados, discussão, link do repo | **Jonas** | (iii)(iv)(v) |

## Como registrar as Issues

1. Convide Henrique e Jonas como collaborators (eles precisam **aceitar** o convite).
2. Autentique o GitHub CLI com escopos de repo + Projects:

```powershell
gh auth login --scopes "repo,project,read:project"
```

3. Rode o script (cria **só as 6 Issues da S01**, o Project e os cards).

No **Git Bash** (barra invertida some — use assim):

```bash
powershell.exe -File scripts/criar_issues.ps1
```

No **PowerShell**:

```powershell
.\scripts\criar_issues.ps1
```

Issues de S02, S03 e do relatório entram nas sprints seguintes.

4. No Project: Status = Backlog / To Do / Doing / Review / Done; WIP = 6 em Doing.
5. Todo commit cita a Issue, por exemplo: `#2 script de cronometragem`.

## Coleta de trials (S01 · Caio · #2)

Pacote `src/timing` — só biblioteca padrão. Time-box 35 min; trial sem verde é **censurado em 35 min**, nunca descartado. Resumo usa mediana e IQR.

```text
python -m src.timing proximo --integrante Caio
python -m src.timing start --integrante Caio
python -m src.timing finish --passando 8 --totais 8 --prompts 3
python -m src.timing record --integrante Caio --minutos 18.4 --passando 8 --totais 8
python -m src.timing resumo
python -m unittest discover -s tests
```

Documentação: [`docs/s01/caio/coleta_tempo.md`](docs/s01/caio/coleta_tempo.md)  
CSV: `data/trials.csv` (real) · `data/trials.example.csv` (linhas de exemplo)

## Snapshot do Kanban (S01 · Caio · #6)

```text
python -m src.snapshot --sprint Lab02S01
```

Gera `snapshots/lab02s01-AAAA-MM-DD.csv` (arquivo novo). Ver [`docs/s01/caio/snapshot_kanban.md`](docs/s01/caio/snapshot_kanban.md).

## Estrutura

```text
.
├── katas/                      # Jonas — 6 exercícios + testes
├── src/
│   ├── timing/                 # Caio — RQ1/RQ2 (clock, schema, protocol, store)
│   ├── snapshot/               # Caio — foto do Projects v2
│   └── metrics/                # Henrique — Radon / jscpd / LOC
├── data/                       # trials.csv
├── docs/s01/caio/              # uso da coleta e do snapshot
├── snapshots/                  # um CSV novo por sprint
├── tests/                      # censura, taxa de sucesso, mediana
├── scripts/criar_issues.ps1
└── README.md
```
