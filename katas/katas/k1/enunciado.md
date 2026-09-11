# K1 — Validador de Senha Corporativa

Implemente a função `validar_senha(senha: str) -> bool` no arquivo `solucao.py`.

## Regras da empresa fictícia "AcmeCorp"

Uma senha é considerada válida se, e somente se, atender a **todas** as regras abaixo:

1. Tem no mínimo 8 caracteres.
2. Contém pelo menos um dígito (0-9).
3. Contém pelo menos um símbolo do conjunto: `!@#$%&*`.
4. Não contém o mesmo caractere repetido 3 vezes seguidas (ex.: `"aaa"` é inválido, `"aab"` é válido).
5. Não contém espaços em branco.

## Exemplos

- `"Acme2024!"` → `True`
- `"acme"` → `False` (menos de 8 caracteres, sem dígito, sem símbolo)
- `"Acmeeee1!"` → `False` (três "e" seguidos)
- `"Acme 2024!"` → `False` (contém espaço)

## Entrega

Implemente apenas a função `validar_senha` em `solucao.py`. Não modifique `test_k1.py`.
