def validar_senha(senha: str) -> bool:
    if len(senha) < 8:
        return False
    if " " in senha:
        return False
    if not any(c.isdigit() for c in senha):
        return False
    simbolos = set("!@#$%&*")
    if not any(c in simbolos for c in senha):
        return False
    for i in range(len(senha) - 2):
        if senha[i] == senha[i+1] == senha[i+2]:
            return False
    return True