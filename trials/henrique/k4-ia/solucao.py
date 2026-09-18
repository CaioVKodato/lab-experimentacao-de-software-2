"""K4 — Calculadora de Descontos em Cascata (trial com IA, issue #18)."""


def aplicar_descontos(preco: float, descontos: list[dict]) -> float:
    """Aplica descontos em cascata sobre o preço, cada um sobre o valor já reduzido.

    Desconto fixo nunca deixa o preço negativo. Resultado arredondado em 2 casas.
    """
    atual = preco
    for desconto in descontos:
        tipo = desconto.get("tipo")
        valor = desconto.get("valor", 0)
        if tipo == "percentual":
            atual = atual * (1 - valor / 100)
        elif tipo == "fixo":
            atual = max(0.0, atual - valor)
    return round(atual, 2)
