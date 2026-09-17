# K2 — Escalonador de Turnos Simples

Implemente a função `escalonar_turnos(funcionarios: list[dict], limite_por_turno: int) -> dict` no arquivo `solucao.py`.

## Entrada

`funcionarios` é uma lista de dicionários, cada um no formato:
```python
{"nome": "Ana", "preferencias": ["manha", "tarde", "noite"]}
```
A lista `preferencias` está em ordem de prioridade (primeira opção é a preferida).

`limite_por_turno` é um inteiro com o número máximo de pessoas permitidas em cada turno.

## Regra de alocação

Para cada funcionário, na ordem em que aparece na lista de entrada, aloque-o no primeiro turno de sua lista de preferências que ainda não atingiu o `limite_por_turno`. Se **nenhuma** preferência do funcionário tiver vaga disponível, ele fica de fora (não aparece no resultado).

## Saída

Um dicionário no formato:
```python
{"manha": ["Ana", "Bruno"], "tarde": ["Carla"], "noite": []}
```

As três chaves (`"manha"`, `"tarde"`, `"noite"`) devem sempre existir no resultado, mesmo que vazias.

## Exemplo

```python
funcionarios = [
    {"nome": "Ana", "preferencias": ["manha", "tarde"]},
    {"nome": "Bruno", "preferencias": ["manha", "noite"]},
    {"nome": "Carla", "preferencias": ["manha"]},
]
escalonar_turnos(funcionarios, limite_por_turno=1)
# {"manha": ["Ana"], "tarde": [], "noite": ["Bruno"]}
# Carla ficou de fora: "manha" já tinha 1 pessoa (limite) e ela não tinha outra preferência.
```

## Entrega

Implemente apenas `escalonar_turnos` em `solucao.py`. Não modifique `test_k2.py`.
