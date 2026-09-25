# RQ extra — Ambiguidade de conteúdo vs. desorganização estrutural do prompt

## Hipótese

H0: nem a ambiguidade de conteúdo (regra de negócio omitida do enunciado) nem a desorganização estrutural do prompt aumentam o número de prompts necessários até a IA convergir para uma solução correta.

H1: a ausência de uma regra de negócio arbitrária aumenta o número de prompts necessários; a desorganização estrutural do prompt, isoladamente, tem efeito menor ou nulo, desde que toda a informação necessária esteja presente.

## Metodologia

Foram desenhados três katas adicionais (k7, k8, k9), cada um com uma regra de negócio deliberadamente omitida do enunciado, revelada apenas pelos testes automatizados:

- **k7** (Calculadora de Tarifa de Estacionamento): regra oculta é a comparação de tipo de veículo ser case-insensitive.
- **k8** (Calculadora de Multa de Biblioteca): regra oculta é uma carência de 5 dias antes da multa começar a contar, exclusiva para usuários do tipo "professor".
- **k9** (Calculadora de Pontos de Fidelidade): regra oculta é a duplicação de pontos em compras realizadas às quartas-feiras.

Os três enunciados foram apresentados ao assistente de IA (Gemini) em formato **desorganizado e informal**, no registro de um estudante escrevendo rapidamente, sem estruturação lógica — texto corrido, informação fora de ordem, sem separação em tópicos ou exemplos formatados. Cada trial foi conduzido em uma conversa nova, sem histórico de tentativas anteriores. Quando a implementação inicial falhava nos testes ocultos, a mensagem de erro do pytest era repassada à IA de forma minimamente informativa (ex.: "o valor calculado veio pela metade do esperado"), sem revelar o nome do teste, o valor de entrada específico ou qualquer menção direta à regra de negócio.

O k7 foi executado em duas conversas independentes para verificar replicabilidade.

## Resultados

| Kata | Regra oculta | Natureza da regra | Prompts até convergir |
|---|---|---|---|
| k7 (execução 1) | Case-insensitive | Hábito defensivo de programação | 1 |
| k7 (execução 2, réplica) | Case-insensitive | Hábito defensivo de programação | 1 |
| k8 | Carência de 5 dias (professor) | Regra de negócio arbitrária | 2 |
| k9 | Dobro de pontos (quarta-feira) | Regra de negócio arbitrária | 2 |

![Prompts por kata](rq_extra_prompts_por_kata.png)

![Prompts médios por tipo de regra](rq_extra_por_tipo_regra.png)

## Discussão

O padrão observado foi consistente e replicável: quando a regra oculta coincidia com uma convenção defensiva de programação amplamente adotada (normalização de case em comparações de string), a IA implementou a solução correta **de primeira tentativa**, mesmo sem qualquer menção a isso no enunciado — o próprio código gerado trazia comentários como "padroniza a string para evitar problemas com maiúsculas/minúsculas", evidenciando que a decisão veio de hábito de boa prática, não de inferência sobre o contexto do problema. Esse resultado se replicou de forma idêntica em duas execuções independentes do k7.

Em contraste, quando a regra oculta era uma política de negócio genuinamente arbitrária — sem qualquer analogia com convenção de programação — a IA necessitou de uma rodada adicional de correção em ambos os casos testados (k8 e k9), mesmo com uma mensagem de erro deliberadamente vaga.

Esse achado sugere uma reformulação da hipótese original mais precisa do que "ambiguidade aumenta o número de prompts" de forma genérica: **o fator determinante não é a ambiguidade do prompt em si, mas se a informação omitida é ou não inferível a partir de convenções gerais de engenharia de software.** Regras de negócio específicas de domínio — que não têm por que ser adivinhadas por um sistema sem contexto adicional — geram fricção real na interação; convenções universais de código, mesmo quando omitidas do enunciado, tendem a ser aplicadas por padrão, neutralizando o efeito de ambiguidade pretendido.

Notavelmente, a **desorganização estrutural do prompt não parece ter sido o fator decisivo em nenhum dos três casos** — os três foram escritos no mesmo registro informal e desestruturado, e ainda assim k8 e k9 exigiram correção enquanto k7 não, em ambas as execuções. Isso é consistente com a hipótese de que a robustez a ruído estrutural do prompt é maior do que a robustez a lacunas de informação genuína, quando a informação omitida não é reconstruível por convenção.

## Limitações

O tamanho amostral é pequeno (3 katas, 4 trials no total, sendo 2 réplicas do mesmo kata), o que impede qualquer teste estatístico formal de significância — a conclusão aqui é qualitativa e descritiva, não inferencial. A mensagem de erro repassada à IA, embora deliberadamente vaga, ainda carrega alguma informação residual (ex.: "veio pela metade do esperado" sinaliza uma relação multiplicativa) que pode ter facilitado a correção mais do que um cenário de feedback totalmente opaco permitiria. Investigações futuras poderiam ampliar o número de katas por categoria e variar sistematicamente o nível de informação da mensagem de erro repassada.