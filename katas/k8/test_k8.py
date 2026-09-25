import pytest
from solucao import calcular_multa


def test_sem_atraso_aluno():
    assert calcular_multa(0, "aluno") == 0.0


def test_atraso_negativo():
    assert calcular_multa(-3, "aluno") == 0.0


def test_aluno_5_dias():
    assert calcular_multa(5, "aluno") == 7.5


def test_externo_10_dias():
    assert calcular_multa(10, "externo") == 15.0


def test_tipo_usuario_invalido():
    with pytest.raises(ValueError):
        calcular_multa(5, "visitante")


def test_aluno_1_dia():
    assert calcular_multa(1, "aluno") == 1.5


# --- Regra não descrita explicitamente no enunciado: professores têm uma
# tolerância de 5 dias de carência antes da multa começar a contar.
def test_professor_dentro_da_carencia():
    assert calcular_multa(5, "professor") == 0.0


def test_professor_exatamente_no_limite_da_carencia():
    assert calcular_multa(6, "professor") == 1.5


def test_professor_apos_carencia():
    assert calcular_multa(10, "professor") == 7.5
