import pytest
from solucao import calcular_tarifa


def test_dentro_da_tolerancia_carro():
    assert calcular_tarifa(10, "carro") == 0.0


def test_exatamente_15_min_tolerancia():
    assert calcular_tarifa(15, "carro") == 0.0


def test_uma_hora_cheia_carro():
    assert calcular_tarifa(75, "carro") == 8.0


def test_arredondamento_para_cima_carro():
    assert calcular_tarifa(76, "carro") == 16.0


def test_moto_duas_horas():
    assert calcular_tarifa(90, "moto") == 10.0


def test_moto_uma_hora():
    assert calcular_tarifa(70, "moto") == 5.0


def test_tipo_veiculo_invalido_levanta_erro():
    with pytest.raises(ValueError):
        calcular_tarifa(60, "caminhao")


def test_zero_minutos():
    assert calcular_tarifa(0, "carro") == 0.0


# --- Regra não descrita explicitamente no enunciado: a comparação do tipo
# de veículo deve ser case-insensitive (aceitar "Carro", "MOTO", "Moto" etc.)
def test_tipo_veiculo_maiusculo():
    assert calcular_tarifa(75, "CARRO") == 8.0


def test_tipo_veiculo_capitalizado():
    assert calcular_tarifa(90, "Moto") == 10.0
