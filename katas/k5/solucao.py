def encontrar_duplicatas(nomes: list) -> list:
    mapa_acentos = {
        "á": "a", "à": "a", "â": "a", "ã": "a",
        "é": "e", "ê": "e",
        "í": "i",
        "ó": "o", "ô": "o", "õ": "o",
        "ú": "u",
        "ç": "c",
        "Á": "a", "À": "a", "Â": "a", "Ã": "a",
        "É": "e", "Ê": "e",
        "Í": "i",
        "Ó": "o", "Ô": "o", "Õ": "o",
        "Ú": "u",
        "Ç": "c",
    }

    def normalizar(nome):
        nome = nome.lower()
        nome = nome.replace(" ", "")
        resultado = []
        for c in nome:
            resultado.append(mapa_acentos.get(c, c))
        return "".join(resultado)

    grupos = {}
    for nome in nomes:
        chave = normalizar(nome)
        grupos.setdefault(chave, []).append(nome)

    return [grupo for grupo in grupos.values() if len(grupo) > 1]