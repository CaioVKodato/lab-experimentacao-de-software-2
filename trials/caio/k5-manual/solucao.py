ACENTOS = {
    "á": "a",
    "à": "a",
    "â": "a",
    "ã": "a",
    "é": "e",
    "ê": "e",
    "í": "i",
    "ó": "o",
    "ô": "o",
    "õ": "o",
    "ú": "u",
    "ç": "c",
}


def _normalizar(nome):
    s = nome.lower().replace(" ", "")
    saida = ""
    for c in s:
        if c in ACENTOS:
            saida += ACENTOS[c]
        else:
            saida += c
    return saida


def encontrar_duplicatas(nomes: list) -> list:
    grupos = {}
    for nome in nomes:
        chave = _normalizar(nome)
        if chave not in grupos:
            grupos[chave] = []
        grupos[chave].append(nome)
    resultado = []
    for chave in grupos:
        if len(grupos[chave]) >= 2:
            resultado.append(grupos[chave])
    return resultado
