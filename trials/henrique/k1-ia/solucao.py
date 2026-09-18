"""K1 — Validador de Senha Corporativa (trial com IA, issue #17)."""


_SIMBOLOS = frozenset("!@#$%&*")


def validar_senha(senha: str) -> bool:
    """Retorna True se a senha atender a todas as regras da AcmeCorp."""
    if len(senha) < 8:
        return False
    if not any(c.isdigit() for c in senha):
        return False
    if not any(c in _SIMBOLOS for c in senha):
        return False
    if any(c.isspace() for c in senha):
        return False
    for i in range(len(senha) - 2):
        if senha[i] == senha[i + 1] == senha[i + 2]:
            return False
    return True
