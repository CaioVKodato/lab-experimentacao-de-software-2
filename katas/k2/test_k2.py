from solucao import escalonar_turnos


def test_alocacao_simples():
    funcionarios = [
        {"nome": "Ana", "preferencias": ["manha", "tarde"]},
        {"nome": "Bruno", "preferencias": ["manha", "noite"]},
        {"nome": "Carla", "preferencias": ["manha"]},
    ]
    resultado = escalonar_turnos(funcionarios, limite_por_turno=1)
    assert resultado == {"manha": ["Ana"], "tarde": [], "noite": ["Bruno"]}


def test_funcionario_sem_vaga_fica_de_fora():
    funcionarios = [
        {"nome": "Ana", "preferencias": ["manha"]},
        {"nome": "Bruno", "preferencias": ["manha"]},
    ]
    resultado = escalonar_turnos(funcionarios, limite_por_turno=1)
    assert resultado["manha"] == ["Ana"]
    assert "Bruno" not in resultado["manha"] + resultado["tarde"] + resultado["noite"]


def test_todas_chaves_presentes_mesmo_vazias():
    resultado = escalonar_turnos([], limite_por_turno=2)
    assert set(resultado.keys()) == {"manha", "tarde", "noite"}
    assert resultado == {"manha": [], "tarde": [], "noite": []}


def test_limite_respeitado():
    funcionarios = [
        {"nome": f"P{i}", "preferencias": ["manha"]} for i in range(5)
    ]
    resultado = escalonar_turnos(funcionarios, limite_por_turno=3)
    assert len(resultado["manha"]) == 3


def test_ordem_de_preferencia_respeitada():
    funcionarios = [
        {"nome": "Ana", "preferencias": ["manha"]},
        {"nome": "Bruno", "preferencias": ["manha", "tarde"]},
    ]
    resultado = escalonar_turnos(funcionarios, limite_por_turno=1)
    assert resultado["manha"] == ["Ana"]
    assert resultado["tarde"] == ["Bruno"]


def test_nao_duplica_pessoa_em_dois_turnos():
    funcionarios = [{"nome": "Ana", "preferencias": ["manha", "tarde", "noite"]}]
    resultado = escalonar_turnos(funcionarios, limite_por_turno=1)
    total_alocacoes = sum(resultado[turno].count("Ana") for turno in resultado)
    assert total_alocacoes == 1


def test_limite_zero_ninguem_alocado():
    funcionarios = [{"nome": "Ana", "preferencias": ["manha"]}]
    resultado = escalonar_turnos(funcionarios, limite_por_turno=0)
    assert resultado == {"manha": [], "tarde": [], "noite": []}
