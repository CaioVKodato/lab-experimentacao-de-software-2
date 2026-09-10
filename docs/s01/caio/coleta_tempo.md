# Coleta de tempo e defeitos (S01 · Caio · #2)

Módulo `src/timing`. Cobre as métricas das **RQ1** e **RQ2** no momento do trial.

## O que é medido

| RQ | Campo no CSV | Regra |
|----|----------------|-------|
| RQ1 | `tempo_s` / `tempo_min` | Time-to-green. Se não passar em todos os testes, **censurado em 35 min** |
| RQ1 | `censurado` | `true` se o trial não ficou verde; **nunca descartar** a linha |
| RQ2 | `testes_passando` / `testes_totais` / `taxa_sucesso` | Taxa normaliza katas com N de testes diferente |
| RQ1 expl. | `n_prompts` | Opcional; só no tratamento IA |
| Controle | `integrante`, `kata`, `tratamento`, `ordem` | Cronograma contrabalanceado |

Agregação descritiva: **mediana e IQR**, não média (`python -m src.timing resumo`).

## Fluxo de um trial (S02)

```text
python -m src.timing proximo --integrante Caio
python -m src.timing start --integrante Caio --issue 2
# ... resolve a kata até os testes passarem, ou até 35 min
python -m src.timing finish --passando 8 --totais 8 --prompts 3
```

Se o cronômetro foi externo (celular):

```text
python -m src.timing record --integrante Caio --minutos 18.4 --passando 8 --totais 8
```

Sem verde, o script grava `tempo_min=35.00` e `censurado=true`, mesmo que a sessão tenha durado menos — parar cedo sem sucesso não pode encolher o tempo da RQ1.

## Cronograma já embutido

O `start` sem `--kata` / `--tratamento` puxa a linha do crossover:

| Integrante | 1 | 2 | 3 | 4 | 5 | 6 |
|------------|---|---|---|---|---|---|
| Caio | K1 IA | K2 Manual | K3 IA | K4 Manual | K5 IA | K6 Manual |
| Henrique | K4 Manual | K5 IA | K6 Manual | K1 IA | K2 Manual | K3 IA |
| Jonas | K6 IA | K5 Manual | K4 Manual | K3 IA | K2 IA | K1 Manual |

## Arquivos

- Planilha real: `data/trials.csv` (só cabeçalho até a S02)
- Exemplo de linhas: `data/trials.example.csv`
- Sessão em andamento: `data/.session.json` (não versionar)
