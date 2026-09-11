# Seleção e Validação dos Katas — S01

Issue: #4

## Critérios de escolha

- Dificuldade equivalente (mesmo time-box de 35 min faz sentido para todos)
- Baixa indexação (evitar katas clássicos de LeetCode/HackerRank, reduzindo risco de a IA reproduzir solução memorizada)
- Número de testes conhecido (usado depois para calcular a taxa de sucesso na RQ2)

## Tabela de katas

| Kata | Ideia | Nº de testes | Justificativa de equivalência de dificuldade | Justificativa de baixa indexação |
|---|---|---|---|---|
| K1 — Validador de Senha Corporativa | Validar string contra regras compostas (tamanho, dígito, símbolo, repetição, espaço) | 10 | Lógica condicional simples sobre string, sem estrutura de dados complexa — mesmo nível de K3/K4 | Regras fictícias da "AcmeCorp"; a combinação específica de critérios não replica nenhum exercício clássico conhecido |
| K2 — Escalonador de Turnos Simples | Alocar itens em categorias respeitando limite e ordem de preferência | 7 | Envolve iteração + estrutura de dados (dict/list), nível intermediário comparável aos demais | Cenário de escala de turnos com regra de prioridade própria, não é um problema padrão de livros/plataformas |
| K3 — Parser de Log de Pedidos | Parsing de string delimitada + agregação, com tratamento de linhas inválidas | 8 | Parsing + agregação é comparável em esforço a K1/K2, com foco em tratamento de exceção manual | Formato de log e regras de exclusão são autorais, não seguem um dataset ou exercício público conhecido |
| K4 — Calculadora de Descontos em Cascata | Aplicar sequência de operações numéricas com regra de não-negatividade | 9 | Lógica matemática simples com regra de negócio, equivalente em complexidade aos outros | Regra de "desconto em cascata" com dois tipos (percentual/fixo) é uma combinação específica do grupo, não um kata padrão |
| K5 — Detector de Duplicatas Aproximadas | Normalização manual de string (case, espaços, acentos) para comparação | 8 | Exige implementação manual de lógica que normalmente vem pronta em bibliotecas — nível equivalente aos demais | Proibição explícita de usar libs de fuzzy matching prontas reduz o espaço de soluções memorizadas pela IA |
| K6 — Roteador de Chamados de Suporte | Classificação por regras + ordenação por critério secundário (urgência) | 8 | Combina classificação e ordenação, complexidade comparável ao conjunto | Categorias e regras de urgência são fictícias e configuráveis, não seguem taxonomia de nenhum sistema real conhecido |

## Artefato de código

Katas implementados em `katas/k1` a `katas/k6`, cada um com `enunciado.md`, `solucao.py` (stub) e `test_kX.py` (testes de aceitação via pytest).

Commit: https://github.com/CaioVKodato/lab-experimentacao-de-software-2/commit/e03591857a80a14a4827f0c0f0e833b4662a18d1
