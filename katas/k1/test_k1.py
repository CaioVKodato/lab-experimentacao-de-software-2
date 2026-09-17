from solucao import validar_senha


def test_senha_valida_completa():
    assert validar_senha("Acme2024!") is True


def test_senha_curta():
    assert validar_senha("Ac2!") is False


def test_sem_digito():
    assert validar_senha("Acmeacme!") is False


def test_sem_simbolo():
    assert validar_senha("Acme2024") is False


def test_caractere_repetido_3x():
    assert validar_senha("Acmeeee1!") is False


def test_caractere_repetido_2x_ok():
    assert validar_senha("Acmee2024!") is True


def test_contem_espaco():
    assert validar_senha("Acme 2024!") is False


def test_exatamente_8_caracteres():
    assert validar_senha("Ac2024!x") is True


def test_multiplos_simbolos():
    assert validar_senha("Ac2024!@#") is True


def test_string_vazia():
    assert validar_senha("") is False
