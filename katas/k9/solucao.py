def calcular_pontos(valor_compra, dia_semana):
    dias_validos = {
        "segunda",
        "terca",
        "quarta",
        "quinta",
        "sexta",
        "sabado",
        "domingo",
    }

    dia_formatado = dia_semana.lower().strip()

    if dia_formatado not in dias_validos:
        raise ValueError(f"Dia da semana inválido: '{dia_semana}'")

    if valor_compra <= 0:
        return 0

    pontos = int(valor_compra // 10)

    # Regra da quarta-feira: pontos em dobro
    if dia_formatado == "quarta":
        pontos *= 2

    return pontos