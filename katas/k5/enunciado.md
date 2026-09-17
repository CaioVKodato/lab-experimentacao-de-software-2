# K5 — Detector de Duplicatas Aproximadas

Implemente a função `encontrar_duplicatas(nomes: list[str]) -> list[list[str]]` no arquivo `solucao.py`.

## Regra de similaridade (normalização manual — não use bibliotecas de fuzzy matching)

Dois nomes são considerados "o mesmo" se, após normalização, ficarem idênticos. A normalização consiste em:

1. Converter para minúsculas.
2. Remover espaços extras no início, fim, e no meio (múltiplos espaços viram nenhum espaço — ou seja, remova todos os espaços da string).
3. Remover acentos (ex.: `"João"` → `"joao"`, `"ANA"` → `"ana"`).

Você deve implementar a remoção de acentos manualmente (um mapeamento de caracteres acentuados para não-acentuados é suficiente; cubra ao menos á, à, â, ã, é, ê, í, ó, ô, õ, ú, ç e suas versões maiúsculas).

## Entrada e Saída

Dada uma lista de nomes (strings), retorne uma lista de **grupos** de nomes originais (na forma como apareceram na entrada) que são duplicatas entre si. Nomes sem nenhuma duplicata não aparecem no resultado. A ordem dos grupos e dos nomes dentro de cada grupo não importa para os testes (serão comparados como conjuntos).

## Exemplo

```python
encontrar_duplicatas(["João Silva", "joao silva", "Ana", "ANA ", "Bruno"])
# [["João Silva", "joao silva"], ["Ana", "ANA "]]
# "Bruno" não aparece pois não tem duplicata.
```

## Entrega

Implemente apenas `encontrar_duplicatas` em `solucao.py`. Não modifique `test_k5.py`. Não use bibliotecas externas de fuzzy matching (ex.: `fuzzywuzzy`, `rapidfuzz`) — apenas string manipulation da biblioteca padrão.
