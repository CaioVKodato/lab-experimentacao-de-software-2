# K9 — Calculadora de Pontos de Fidelidade

Implemente a função `calcular_pontos(valor_compra: float, dia_semana: str) -> int` no arquivo `solucao.py`.

## Regras do programa "ClubeMais"

1. A cada R$10,00 gastos, o cliente ganha 1 ponto (arredondado para baixo).
2. `dia_semana` pode ser `"segunda"`, `"terca"`, `"quarta"`, `"quinta"`, `"sexta"`, `"sabado"` ou `"domingo"`.
3. Valores de `dia_semana` fora dessa lista devem levantar `ValueError`.
4. Se `valor_compra` for menor ou igual a zero, o cliente ganha 0 pontos.

## Exemplos

```python
calcular_pontos(50.0, "segunda")   # 50 / 10 -> 5 pontos
calcular_pontos(25.0, "quarta")    # 25 / 10 -> 2 pontos (arredondado p/ baixo)
calcular_pontos(0.0, "sexta")      # 0 pontos
```

## Entrega

Implemente apenas `calcular_pontos` em `solucao.py`. Não modifique `test_k9.py`.
