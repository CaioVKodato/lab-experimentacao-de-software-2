# K4 — Calculadora de Descontos em Cascata

Implemente a função `aplicar_descontos(preco: float, descontos: list[dict]) -> float` no arquivo `solucao.py`.

## Entrada

`preco` é o preço original (float, sempre positivo).

`descontos` é uma lista ordenada de dicionários, aplicados **na ordem em que aparecem**, cada um em um destes dois formatos:
```python
{"tipo": "percentual", "valor": 10}   # 10% de desconto sobre o preço atual
{"tipo": "fixo", "valor": 5.0}        # R$5,00 de desconto sobre o preço atual
```

## Regras

1. Cada desconto é aplicado sobre o preço **já reduzido** pelos descontos anteriores (cascata), não sobre o preço original.
2. Um desconto do tipo `"fixo"` nunca pode deixar o preço final negativo — se o valor do desconto for maior que o preço atual, o preço vira `0.0` (não fica negativo).
3. Um desconto do tipo `"percentual"` sempre reduz o preço proporcionalmente (nunca gera preço negativo por natureza).
4. O resultado final deve ser arredondado para 2 casas decimais.

## Exemplo

```python
aplicar_descontos(100.0, [
    {"tipo": "percentual", "valor": 10},  # 100 -> 90
    {"tipo": "fixo", "valor": 20},        # 90 -> 70
])
# 70.0

aplicar_descontos(10.0, [
    {"tipo": "fixo", "valor": 50},  # desconto maior que o preço
])
# 0.0
```

## Entrega

Implemente apenas `aplicar_descontos` em `solucao.py`. Não modifique `test_k4.py`.
