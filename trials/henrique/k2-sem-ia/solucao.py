"""K2 — Escalonador de Turnos Simples (trial com IA, issue #20)."""


def escalonar_turnos(funcionarios: list[dict], limite_por_turno: int) -> dict:
    """Aloca cada funcionário no primeiro turno preferido com vaga disponível.

    Funcionários sem vaga em nenhuma preferência ficam de fora do resultado.
    As chaves manha/tarde/noite sempre existem, mesmo que vazias.
    """
    resultado: dict[str, list[str]] = {"manha": [], "tarde": [], "noite": []}
    for func in funcionarios:
        nome = func.get("nome", "")
        for turno in func.get("preferencias", []):
            if turno in resultado and len(resultado[turno]) < limite_por_turno:
                resultado[turno].append(nome)
                break
    return resultado
