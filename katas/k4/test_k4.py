from solucao import aplicar_descontos


def test_cascata_percentual_depois_fixo():
    resultado = aplicar_descontos(100.0, [
        {"tipo": "percentual", "valor": 10},
        {"tipo": "fixo", "valor": 20},
    ])
    assert resultado == 70.0


def test_fixo_maior_que_preco_nao_fica_negativo():
    resultado = aplicar_descontos(10.0, [{"tipo": "fixo", "valor": 50}])
    assert resultado == 0.0


def test_sem_descontos():
    resultado = aplicar_descontos(100.0, [])
    assert resultado == 100.0


def test_apenas_percentual():
    resultado = aplicar_descontos(200.0, [{"tipo": "percentual", "valor": 50}])
    assert resultado == 100.0


def test_multiplos_percentuais_em_cascata():
    resultado = aplicar_descontos(100.0, [
        {"tipo": "percentual", "valor": 10},  # 90
        {"tipo": "percentual", "valor": 10},  # 81
    ])
    assert resultado == 81.0


def test_fixo_depois_percentual():
    resultado = aplicar_descontos(100.0, [
        {"tipo": "fixo", "valor": 20},         # 80
        {"tipo": "percentual", "valor": 25},   # 60
    ])
    assert resultado == 60.0


def test_arredondamento_duas_casas():
    resultado = aplicar_descontos(10.0, [{"tipo": "percentual", "valor": 33}])
    assert resultado == 6.7


def test_desconto_percentual_100_zera_preco():
    resultado = aplicar_descontos(50.0, [{"tipo": "percentual", "valor": 100}])
    assert resultado == 0.0


def test_preco_exato_apos_fixo():
    resultado = aplicar_descontos(20.0, [{"tipo": "fixo", "valor": 20}])
    assert resultado == 0.0
