def analisar_pedidos(linhas: list) -> dict:
    total_por_produto = {}
    pedidos_cancelados = 0
    for linha in linhas:
        partes = linha.split("|")
        if len(partes) != 4:
            continue
        _id, produto, quantidade, status = partes
        if status not in ("entregue", "cancelado", "pendente"):
            continue
        try:
            n = int(quantidade)
        except ValueError:
            continue
        if status == "cancelado":
            pedidos_cancelados += 1
        elif status == "entregue":
            if produto not in total_por_produto:
                total_por_produto[produto] = 0
            total_por_produto[produto] += n
    produto_mais_pedido = None
    maior = -1
    for produto, total in total_por_produto.items():
        if total > maior:
            maior = total
            produto_mais_pedido = produto
    return {
        "total_por_produto": total_por_produto,
        "pedidos_cancelados": pedidos_cancelados,
        "produto_mais_pedido": produto_mais_pedido,
    }
