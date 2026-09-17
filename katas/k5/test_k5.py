from solucao import encontrar_duplicatas


def _to_sets(grupos):
    return sorted([sorted(g) for g in grupos])


def test_caso_exemplo():
    resultado = encontrar_duplicatas(["João Silva", "joao silva", "Ana", "ANA ", "Bruno"])
    esperado = [["João Silva", "joao silva"], ["Ana", "ANA "]]
    assert _to_sets(resultado) == _to_sets(esperado)


def test_sem_duplicatas():
    resultado = encontrar_duplicatas(["Ana", "Bruno", "Carla"])
    assert resultado == []


def test_lista_vazia():
    assert encontrar_duplicatas([]) == []


def test_espacos_no_meio():
    resultado = encontrar_duplicatas(["Ana Paula", "Ana  Paula", "AnaPaula"])
    esperado = [["Ana Paula", "Ana  Paula", "AnaPaula"]]
    assert _to_sets(resultado) == _to_sets(esperado)


def test_grupo_triplo():
    resultado = encontrar_duplicatas(["Jose", "JOSE", "jose ", "Maria"])
    esperado = [["Jose", "JOSE", "jose "]]
    assert _to_sets(resultado) == _to_sets(esperado)


def test_acentos_diversos():
    resultado = encontrar_duplicatas(["São Paulo", "sao paulo", "Conceição", "conceicao"])
    esperado = [["São Paulo", "sao paulo"], ["Conceição", "conceicao"]]
    assert _to_sets(resultado) == _to_sets(esperado)


def test_nomes_identicos_sem_variacao():
    resultado = encontrar_duplicatas(["Ana", "Ana"])
    assert _to_sets(resultado) == _to_sets([["Ana", "Ana"]])


def test_um_unico_nome():
    assert encontrar_duplicatas(["Ana"]) == []
