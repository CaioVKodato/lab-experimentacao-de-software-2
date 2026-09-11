# Desenho do Experimento — Hipóteses, GQM e Ameaças à Validade

Issue: #5
Artefato de código correspondente: `src/design/experiment_design.py` (fonte estruturada usada pelos scripts de análise da S03)

## Goal (GQM)

Analisar o uso de assistentes de IA generativa na resolução de tarefas de programação, comparando seu efeito frente à codificação manual, com respeito a tempo de resolução, qualidade funcional (defeitos) e qualidade estrutural do código produzido, do ponto de vista do grupo pesquisador, no contexto de katas de dificuldade equivalente resolvidos sob condições controladas (crossover within-subject, time-boxed).

## Hipóteses (H0/H1) por RQ

**RQ1 — Tempo:** H0: não há diferença no time-to-green entre tratamentos. H1: o uso de IA reduz o tempo até passar nos testes.

**RQ2 — Defeitos:** H0: não há diferença na taxa de sucesso entre tratamentos. H1: o uso de IA aumenta a taxa de sucesso.

**RQ3 — Estrutura:** H0: não há diferença em complexidade ciclomática nem duplicação entre tratamentos. H1: o uso de IA altera essas métricas.

**RQ extra — Prompts:** H0: nº de prompts não se correlaciona com tempo/taxa de sucesso. H1 (hipótese informal): correlação negativa fraca ou nula — mais prompts tende a indicar mais dificuldade, não necessariamente mais velocidade.

## Variáveis

- **Independente:** uso do assistente de IA (`com_ia` / `sem_ia`)
- **Dependentes:** time_to_green, taxa de sucesso, nº de testes falhando, complexidade ciclomática média, % duplicação, LOC (controle), índice de manutenibilidade (opcional), nº de prompts (RQ extra)

## Tratamentos e objetos experimentais

2 tratamentos (`com_ia`, `sem_ia`), aplicados sobre 6 katas autorais (k1-k6, ver `docs/s01/jonas/selecao_validacao_katas_s01.md`), em Python, com métricas via Radon (cc, mi) e jscpd (duplicação). Assistente de IA fixado: Claude (versão gratuita).

## Tipo de projeto experimental

Crossover / within-subject, contrabalançado: cada integrante resolve todos os 6 katas (3 com IA, 3 sem), em ordem contrabalançada entre integrantes, servindo como seu próprio controle — reduz variação individual de habilidade.

## Quantidade de medições

6 katas × 3 integrantes = 18 trials no total do grupo (9 com IA, 9 sem IA).

## Ameaças à validade

1. **Efeito de aprendizado** — familiaridade crescente com o formato dos katas ao longo da sessão. Mitigação: ordem contrabalançada entre integrantes.
2. **Familiaridade prévia com a ferramenta de IA** — vantagem artificial pra quem já usa Claude com frequência. Mitigação: mesma ferramenta fixada pra todo o grupo.
3. **Vazamento de solução já vista / memorização** — katas famosos poderiam ser "resolvidos de cor" pela IA. Mitigação: katas autorais (k1-k6), cenários fictícios específicos do grupo, baixa indexação pública.
4. **Time-box não uniforme** — reduzir o tempo de forma desigual distorceria a comparação entre grupos da turma. Mitigação: 35 minutos fixos por trial, sem exceção.