from solucao import rotear_chamados

PALAVRAS_CHAVE = {
    "bug": ["erro", "travando", "quebrado", "falha"],
    "duvida": ["como", "onde", "ajuda"],
    "elogio": ["parabéns", "excelente", "ótimo"],
}


def test_caso_exemplo():
    chamados = [
        "Como faço para exportar meu relatório?",
        "URGENTE: sistema travando toda hora",
        "Parabéns pelo produto, excelente trabalho!",
    ]
    resultado = rotear_chamados(chamados, PALAVRAS_CHAVE)
    assert resultado[0]["categoria"] == "bug"
    assert resultado[0]["urgencia"] == "alta"
    assert resultado[1]["categoria"] == "duvida"
    assert resultado[1]["urgencia"] == "normal"
    assert resultado[2]["categoria"] == "elogio"
    assert resultado[2]["urgencia"] == "normal"


def test_categoria_geral_quando_sem_palavra_chave():
    resultado = rotear_chamados(["texto aleatório sem relacao"], PALAVRAS_CHAVE)
    assert resultado[0]["categoria"] == "geral"
    assert resultado[0]["urgencia"] == "normal"


def test_ordem_prioridade_categorias():
    # contém palavras de "bug" e "duvida"; deve escolher a primeira categoria no dict = "bug"
    resultado = rotear_chamados(["como corrigir esse erro?"], PALAVRAS_CHAVE)
    assert resultado[0]["categoria"] == "bug"


def test_case_insensitive():
    resultado = rotear_chamados(["ERRO CRÍTICO no sistema"], PALAVRAS_CHAVE)
    assert resultado[0]["categoria"] == "bug"


def test_urgencia_case_insensitive():
    resultado = rotear_chamados(["Urgente, preciso de ajuda"], PALAVRAS_CHAVE)
    assert resultado[0]["urgencia"] == "alta"


def test_lista_vazia():
    assert rotear_chamados([], PALAVRAS_CHAVE) == []


def test_ordenacao_estavel_por_urgencia():
    chamados = [
        "chamado normal 1 - como funciona",
        "chamado urgente - erro grave urgente",
        "chamado normal 2 - parabéns",
    ]
    resultado = rotear_chamados(chamados, PALAVRAS_CHAVE)
    textos_em_ordem = [c["texto"] for c in resultado]
    assert textos_em_ordem[0] == "chamado urgente - erro grave urgente"
    assert textos_em_ordem[1] == "chamado normal 1 - como funciona"
    assert textos_em_ordem[2] == "chamado normal 2 - parabéns"


def test_dicionario_palavras_chave_vazio():
    resultado = rotear_chamados(["qualquer coisa"], {})
    assert resultado[0]["categoria"] == "geral"
