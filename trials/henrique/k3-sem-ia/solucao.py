"""K3 — Parser de Log de Pedidos (trial sem IA, issue #21)."""


_STATUSES_VALIDOS = {"entregue", "cancelado", "pendente"}


def analisar_pedidos(linhas: list[str]) -> dict:
    """Analisa linhas de log no formato ID|produto|quantidade|status.

    Linhas malformadas, quantidade não numérica ou status desconhecido são ignoradas.
    Apenas pedidos com status 'entregue' somam no total por produto.
    """
    total_por_produto: dict[str, int] = {}
    pedidos_cancelados = 0

    for linha in linhas:
        partes = linha.split("|")
        if len(partes) != 4:
            continue
        _, produto, quantidade_str, status = partes
        if status not in _STATUSES_VALIDOS:
            continue
        try:
            quantidade = int(quantidade_str)
        except ValueError:
            continue

        if status == "entregue":
            total_por_produto[produto] = total_por_produto.get(produto, 0) + quantidade
        elif status == "cancelado":
            pedidos_cancelados += 1

    produto_mais_pedido = max(total_por_produto, key=total_por_produto.__getitem__) if total_por_produto else None

    return {
        "total_por_produto": total_por_produto,
        "pedidos_cancelados": pedidos_cancelados,
        "produto_mais_pedido": produto_mais_pedido,
    }
