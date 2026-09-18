"""K6 — Roteador de Chamados de Suporte (trial sem IA, issue #22)."""


def rotear_chamados(chamados: list[str], palavras_chave: dict) -> list[dict]:
    """Classifica e ordena chamados por categoria e urgência.

    Cada chamado recebe a primeira categoria cujas palavras-chave apareçam no texto
    (case-insensitive). Sem correspondência → 'geral'. Contém 'urgente' → urgência 'alta'.
    Resultado ordenado: 'alta' primeiro, ordem relativa original preservada.
    """
    resultado = []
    for texto in chamados:
        texto_lower = texto.lower()

        categoria = "geral"
        for cat, palavras in palavras_chave.items():
            if any(p.lower() in texto_lower for p in palavras):
                categoria = cat
                break

        urgencia = "alta" if "urgente" in texto_lower else "normal"
        resultado.append({"texto": texto, "categoria": categoria, "urgencia": urgencia})

    return sorted(resultado, key=lambda c: 0 if c["urgencia"] == "alta" else 1)
