def validar_senha(senha: str) -> bool:
    if len(senha) < 8:
        return False
    if " " in senha:
        return False
    tem_digito = False
    tem_simbolo = False
    for i in range(len(senha)):
        c = senha[i]
        if c.isdigit():
            tem_digito = True
        if c in "!@#$%&*":
            tem_simbolo = True
        if i >= 2 and senha[i] == senha[i - 1] == senha[i - 2]:
            return False
    return tem_digito and tem_simbolo
