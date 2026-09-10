# K3 — Parser de Log de Pedidos

Implemente a função `analisar_pedidos(linhas: list[str]) -> dict` no arquivo `solucao.py`.

## Entrada

`linhas` é uma lista de strings, cada uma no formato:
```
ID|produto|quantidade|status
```
Exemplo: `"1|caneta|10|entregue"`

`status` pode ser: `"entregue"`, `"cancelado"` ou `"pendente"`.

Linhas malformadas (campos faltando, quantidade não numérica, status desconhecido) devem ser **ignoradas** silenciosamente (não contam em nenhuma métrica e não geram erro).

## Saída

Um dicionário no formato:
```python
{
    "total_por_produto": {"caneta": 25, "caderno": 5},  # soma de quantidade, apenas pedidos "entregue"
    "pedidos_cancelados": 3,          # contagem de linhas com status "cancelado"
    "produto_mais_pedido": "caneta",  # produto com maior total_por_produto; None se não houver nenhum entregue
}
```

## Exemplo

```python
linhas = [
    "1|caneta|10|entregue",
    "2|caderno|5|entregue",
    "3|caneta|15|entregue",
    "4|lapis|2|cancelado",
    "linha invalida sem pipes",
    "5|caneta|abc|entregue",
]
analisar_pedidos(linhas)
# {
#   "total_por_produto": {"caneta": 25, "caderno": 5},
#   "pedidos_cancelados": 1,
#   "produto_mais_pedido": "caneta",
# }
```

## Entrega

Implemente apenas `analisar_pedidos` em `solucao.py`. Não modifique `test_k3.py`.
