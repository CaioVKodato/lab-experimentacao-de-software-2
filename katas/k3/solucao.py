def analisar_pedidos(linhas: list) -> dict:
    total_por_produto = {}
    pedidos_cancelados = 0

    for linha in linhas:
        partes = linha.split("|")
        if len(partes) != 4:
            continue
        _id, produto, quantidade_str, status = partes

        if status == "cancelado":
            pedidos_cancelados += 1
            continue

        if status != "entregue":
            continue

        try:
            quantidade = int(quantidade_str)
        except ValueError:
            continue

        total_por_produto[produto] = total_por_produto.get(produto, 0) + quantidade

    if total_por_produto:
        produto_mais_pedido = max(total_por_produto, key=total_por_produto.get)
    else:
        produto_mais_pedido = None

    return {
        "total_por_produto": total_por_produto,
        "pedidos_cancelados": pedidos_cancelados,
        "produto_mais_pedido": produto_mais_pedido,
    }