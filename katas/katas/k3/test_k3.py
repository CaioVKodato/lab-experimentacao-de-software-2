from solucao import analisar_pedidos


def test_caso_exemplo_completo():
    linhas = [
        "1|caneta|10|entregue",
        "2|caderno|5|entregue",
        "3|caneta|15|entregue",
        "4|lapis|2|cancelado",
        "linha invalida sem pipes",
        "5|caneta|abc|entregue",
    ]
    resultado = analisar_pedidos(linhas)
    assert resultado["total_por_produto"] == {"caneta": 25, "caderno": 5}
    assert resultado["pedidos_cancelados"] == 1
    assert resultado["produto_mais_pedido"] == "caneta"


def test_lista_vazia():
    resultado = analisar_pedidos([])
    assert resultado["total_por_produto"] == {}
    assert resultado["pedidos_cancelados"] == 0
    assert resultado["produto_mais_pedido"] is None


def test_apenas_cancelados():
    linhas = ["1|caneta|10|cancelado", "2|caderno|5|cancelado"]
    resultado = analisar_pedidos(linhas)
    assert resultado["pedidos_cancelados"] == 2
    assert resultado["total_por_produto"] == {}
    assert resultado["produto_mais_pedido"] is None


def test_status_desconhecido_ignorado():
    linhas = ["1|caneta|10|em_transito"]
    resultado = analisar_pedidos(linhas)
    assert resultado["total_por_produto"] == {}
    assert resultado["pedidos_cancelados"] == 0


def test_quantidade_nao_numerica_ignorada():
    linhas = ["1|caneta|dez|entregue"]
    resultado = analisar_pedidos(linhas)
    assert resultado["total_por_produto"] == {}


def test_campos_faltando_ignorado():
    linhas = ["1|caneta|10"]
    resultado = analisar_pedidos(linhas)
    assert resultado["total_por_produto"] == {}
    assert resultado["pedidos_cancelados"] == 0


def test_pendente_nao_conta_no_total():
    linhas = ["1|caneta|10|pendente"]
    resultado = analisar_pedidos(linhas)
    assert resultado["total_por_produto"] == {}
    assert resultado["pedidos_cancelados"] == 0


def test_empate_produto_mais_pedido_retorna_algum_valido():
    linhas = ["1|caneta|10|entregue", "2|caderno|10|entregue"]
    resultado = analisar_pedidos(linhas)
    assert resultado["produto_mais_pedido"] in ("caneta", "caderno")
