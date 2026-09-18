def aplicar_descontos(preco: float, descontos: list[dict]) -> float:
    for desconto in descontos:
        tipo = desconto["tipo"]
        valor = desconto["valor"]

        if tipo == "percentual":
            preco -= preco * (valor / 100)

        elif tipo == "fixo":
            preco -= valor
            if preco < 0:
                preco = 0.0

    return round(preco, 2)