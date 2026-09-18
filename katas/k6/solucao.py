def rotear_chamados(chamados: list[str], palavras_chave: dict) -> list[dict]:
    resultado = []

    for texto in chamados:
        texto_lower = texto.lower()
        categoria = "geral"

        for cat, palavras in palavras_chave.items():
            if any(palavra.lower() in texto_lower for palavra in palavras):
                categoria = cat
                break

        if "urgente" in texto_lower:
            urgencia = "alta"
        else:
            urgencia = "normal"

        resultado.append({
            "texto": texto,
            "categoria": categoria,
            "urgencia": urgencia
        })

    return sorted(resultado, key=lambda chamado: chamado["urgencia"] != "alta")