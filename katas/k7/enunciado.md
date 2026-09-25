# K7 — Calculadora de Tarifa de Estacionamento

Implemente a função `calcular_tarifa(minutos_permanencia: int, tipo_veiculo: str) -> float` no arquivo `solucao.py`.

## Regras do estacionamento "ParkFácil"

1. Tarifa por hora: `"carro"` = R$8,00/hora; `"moto"` = R$5,00/hora.
2. Os primeiros 15 minutos de permanência são gratuitos (tolerância), independente do tipo de veículo.
3. Após a tolerância, o tempo é sempre arredondado **para cima** em horas cheias (ex.: 61 minutos de permanência cobrável contam como 2 horas).
4. Tipos de veículo inválidos (diferentes de `"carro"` ou `"moto"`) devem levantar `ValueError`.

## Exemplos

```python
calcular_tarifa(10, "carro")   # 10 min, dentro da tolerância -> 0.0
calcular_tarifa(15, "carro")   # exatamente 15 min -> 0.0
calcular_tarifa(75, "carro")   # 75 - 15 = 60 min cobráveis -> 1 hora -> 8.0
calcular_tarifa(90, "moto")    # 90 - 15 = 75 min cobráveis -> arredonda p/ 2h -> 10.0
```

## Entrega

Implemente apenas `calcular_tarifa` em `solucao.py`. Não modifique `test_k7.py`.
