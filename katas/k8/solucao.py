def calcular_multa(dias_atraso: int, tipo_usuario: str) -> float:
    tipo = tipo_usuario.strip().lower()
    
    tipos_validos = ["aluno", "professor", "externo"]
    if tipo not in tipos_validos:
        raise ValueError(f"Tipo de usuário inválido: '{tipo_usuario}'.")
    
    if dias_atraso <= 0:
        return 0.0

    # Professores têm 5 dias de carência
    dias_carencia = 5 if tipo == "professor" else 0
    dias_cobrancao = dias_atraso - dias_carencia

    if dias_cobrancao <= 0:
        return 0.0

    return dias_cobrancao * 1.50