import pytest
from solucao import calcular_pontos


def test_segunda_50_reais():
    assert calcular_pontos(50.0, "segunda") == 5


def test_arredondamento_para_baixo():
    assert calcular_pontos(25.0, "quinta") == 2


def test_valor_zero():
    assert calcular_pontos(0.0, "sexta") == 0


def test_valor_negativo():
    assert calcular_pontos(-10.0, "sabado") == 0


def test_dia_semana_invalido():
    with pytest.raises(ValueError):
        calcular_pontos(50.0, "feriado")


def test_domingo_normal():
    assert calcular_pontos(30.0, "domingo") == 3


# --- Regra não descrita explicitamente no enunciado: compras feitas na
# quarta-feira rendem o dobro de pontos (promoção "quarta em dobro").
def test_quarta_dobra_pontos():
    assert calcular_pontos(50.0, "quarta") == 10


def test_quarta_com_arredondamento():
    assert calcular_pontos(25.0, "quarta") == 4


def test_quarta_valor_zero_continua_zero():
    assert calcular_pontos(0.0, "quarta") == 0
