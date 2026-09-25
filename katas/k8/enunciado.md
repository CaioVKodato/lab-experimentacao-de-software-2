# K8 — Calculadora de Multa de Biblioteca

Implemente a função `calcular_multa(dias_atraso: int, tipo_usuario: str) -> float` no arquivo `solucao.py`.

## Regras da biblioteca "LivroFácil"

1. A multa por atraso é de R$1,50 por dia, para qualquer tipo de usuário.
2. `tipo_usuario` pode ser `"aluno"`, `"professor"` ou `"externo"`.
3. Se `dias_atraso` for 0 ou negativo, a multa é R$0,00.
4. Tipos de usuário diferentes de `"aluno"`, `"professor"` ou `"externo"` devem levantar `ValueError`.

## Exemplos

```python
calcular_multa(0, "aluno")       # sem atraso -> 0.0
calcular_multa(5, "aluno")       # 5 dias -> 7.5
calcular_multa(10, "externo")    # 10 dias -> 15.0
```

## Entrega

Implemente apenas `calcular_multa` em `solucao.py`. Não modifique `test_k8.py`.
