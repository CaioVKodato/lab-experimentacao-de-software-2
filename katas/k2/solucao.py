def escalonar_turnos(funcionarios: list[dict], limite_por_turno: int) -> dict:
    turnos = {
        "manha": [],
        "tarde": [],
        "noite": []
    }

    for funcionario in funcionarios:
        nome = funcionario["nome"]
        preferencias = funcionario["preferencias"]

        for turno in preferencias:
            if turno in turnos and len(turnos[turno]) < limite_por_turno:
                turnos[turno].append(nome)
                break

    return turnos