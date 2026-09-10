# K6 — Roteador de Chamados de Suporte

Implemente a função `rotear_chamados(chamados: list[str], palavras_chave: dict) -> list[dict]` no arquivo `solucao.py`.

## Entrada

`chamados` é uma lista de strings, cada uma o texto de um chamado de suporte.

`palavras_chave` é um dicionário mapeando categoria → lista de palavras-chave (case-insensitive), por exemplo:
```python
{
    "bug": ["erro", "quebrado", "falha", "travando"],
    "duvida": ["como", "onde", "ajuda"],
    "elogio": ["ótimo", "parabéns", "excelente"],
}
```

## Regras de classificação

1. Um chamado pertence à primeira categoria (na ordem em que aparece no dicionário `palavras_chave`) cuja alguma palavra-chave apareça no texto do chamado (case-insensitive, correspondência de substring).
2. Se nenhuma palavra-chave de nenhuma categoria for encontrada, o chamado é classificado como `"geral"`.
3. Urgência: se o texto do chamado contiver a palavra `"urgente"` (case-insensitive), a urgência é `"alta"`; caso contrário, `"normal"`.

## Saída

Uma lista de dicionários, na mesma ordem dos chamados de entrada, priorizada por urgência (`"alta"` primeiro, mantendo a ordem relativa original dentro de cada grupo de urgência — ordenação estável):
```python
[
    {"texto": "...", "categoria": "bug", "urgencia": "alta"},
    {"texto": "...", "categoria": "duvida", "urgencia": "normal"},
]
```

## Exemplo

```python
chamados = [
    "Como faço para exportar meu relatório?",
    "URGENTE: sistema travando toda hora",
    "Parabéns pelo produto, excelente trabalho!",
]
palavras_chave = {
    "bug": ["erro", "travando"],
    "duvida": ["como"],
    "elogio": ["parabéns"],
}
rotear_chamados(chamados, palavras_chave)
# [
#   {"texto": "URGENTE: sistema travando toda hora", "categoria": "bug", "urgencia": "alta"},
#   {"texto": "Como faço para exportar meu relatório?", "categoria": "duvida", "urgencia": "normal"},
#   {"texto": "Parabéns pelo produto, excelente trabalho!", "categoria": "elogio", "urgencia": "normal"},
# ]
```

## Entrega

Implemente apenas `rotear_chamados` em `solucao.py`. Não modifique `test_k6.py`.
