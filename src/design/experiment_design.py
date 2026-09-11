"""
Desenho do Experimento — LAB02 (IA vs. Codificação Manual)
Issue: #5

Este arquivo formaliza, em formato estruturado, o desenho do experimento
(hipóteses, variáveis, tratamentos, ameaças à validade), servindo como
fonte única de verdade que os scripts de análise da S03 podem importar
diretamente, em vez de duplicar essas definições em texto solto.
"""

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# A) Hipóteses (nula e alternativa) por RQ
# ---------------------------------------------------------------------------

HIPOTESES = {
    "RQ1_tempo": {
        "H0": "Não há diferença no tempo até passar nos testes (time-to-green) "
              "entre resolver o kata com assistente de IA e sem.",
        "H1": "O uso do assistente de IA reduz o tempo até passar nos testes.",
    },
    "RQ2_defeitos": {
        "H0": "Não há diferença na taxa de sucesso (% de testes passando ao "
              "final do time-box) entre os dois tratamentos.",
        "H1": "O uso do assistente de IA aumenta a taxa de sucesso.",
    },
    "RQ3_estrutura": {
        "H0": "Não há diferença na complexidade ciclomática média nem na "
              "duplicação de código entre os dois tratamentos.",
        "H1": "O uso do assistente de IA altera a complexidade ciclomática "
              "e/ou a duplicação de código produzido.",
    },
    "RQ_extra_prompts": {
        "H0": "O número de prompts trocados com a IA não se correlaciona "
              "com o tempo até passar nos testes nem com a taxa de sucesso.",
        "H1": "Mais prompts indicam maior dificuldade, correlacionando-se "
              "negativamente (ou nulamente) com tempo/taxa de sucesso — "
              "hipótese informal: correlação negativa fraca ou nula.",
    },
}


# ---------------------------------------------------------------------------
# B) Variáveis dependentes (DVs)
# ---------------------------------------------------------------------------

VARIAVEIS_DEPENDENTES = [
    {"nome": "time_to_green_seg", "descricao": "Tempo até passar em todos os testes de aceitação (segundos); trial que atinge o time-box sem sucesso é registrado como censurado em 2100s (35min), não descartado."},
    {"nome": "taxa_sucesso_pct", "descricao": "% de testes de aceitação passando ao final do time-box"},
    {"nome": "testes_falhando_abs", "descricao": "Número absoluto de testes falhando ao final do tempo"},
    {"nome": "complexidade_ciclomatica_media", "descricao": "Radon cc — complexidade ciclomática média por função"},
    {"nome": "duplicacao_pct", "descricao": "% de linhas duplicadas (jscpd ou equivalente)"},
    {"nome": "loc", "descricao": "Linhas de código — métrica de controle, usada para normalizar complexidade/duplicação"},
    {"nome": "indice_manutenibilidade", "descricao": "Radon mi — Maintainability Index (opcional/aprofundamento)"},
    {"nome": "num_prompts", "descricao": "Número de prompts/interações com o Claude no trial (apenas tratamento 'com_ia'); usada na RQ extra"},
]


# ---------------------------------------------------------------------------
# C) Variável independente (IV)
# ---------------------------------------------------------------------------

VARIAVEL_INDEPENDENTE = {
    "nome": "uso_assistente_ia",
    "niveis": ["com_ia", "sem_ia"],
    "descricao": "Se o assistente de IA (Claude, versão gratuita) esteve habilitado durante a resolução do kata",
}


# ---------------------------------------------------------------------------
# D) Tratamentos
# ---------------------------------------------------------------------------

TRATAMENTOS = ["com_ia", "sem_ia"]


# ---------------------------------------------------------------------------
# E) Objetos experimentais (katas)
# ---------------------------------------------------------------------------

KATAS = ["k1", "k2", "k3", "k4", "k5", "k6"]
LINGUAGEM = "Python"
FERRAMENTA_METRICAS = "Radon (cc, mi) + jscpd (duplicação)"
ASSISTENTE_IA = "Claude (versão gratuita)"


# ---------------------------------------------------------------------------
# F) Tipo de projeto experimental
# ---------------------------------------------------------------------------

DESENHO_EXPERIMENTAL = {
    "tipo": "crossover / within-subject, contrabalançado",
    "justificativa": (
        "Cada integrante resolve todos os 6 katas (3 com IA, 3 sem), em ordem "
        "contrabalançada, controlando a variação individual de habilidade — "
        "cada pessoa serve como seu próprio controle."
    ),
}


# ---------------------------------------------------------------------------
# G) Quantidade de medições
# ---------------------------------------------------------------------------

QUANTIDADE_MEDICOES = {
    "katas_por_integrante": 6,
    "trials_com_ia_por_integrante": 3,
    "trials_sem_ia_por_integrante": 3,
    "integrantes": 3,
    "total_trials_grupo": 18,
}


# ---------------------------------------------------------------------------
# H) Ameaças à validade
# ---------------------------------------------------------------------------

AMEACAS_VALIDADE = [
    {
        "tipo": "Efeito de aprendizado",
        "descricao": "Resolver vários katas em sequência pode gerar familiaridade crescente com o formato de enunciado/testes, favorecendo os katas resolvidos por último.",
        "mitigacao": "Ordem contrabalançada entre integrantes (cada um resolve os katas em ordem diferente).",
    },
    {
        "tipo": "Familiaridade prévia com a ferramenta de IA",
        "descricao": "Integrantes com mais experiência prévia com o Claude podem ter vantagem artificial no tratamento 'com_ia'.",
        "mitigacao": "Mesma ferramenta de IA fixada para todo o grupo, reduzindo variação de familiaridade entre tratamentos dentro de cada pessoa.",
    },
    {
        "tipo": "Vazamento de solução já vista / memorização",
        "descricao": "Se os katas fossem exercícios famosos (ex.: LeetCode clássico), a IA poderia reproduzir uma solução memorizada do treinamento em vez de efetivamente 'ajudar', inflando artificialmente o desempenho do tratamento com IA.",
        "mitigacao": "Os 6 katas (k1-k6) são autorais do grupo, com cenários fictícios específicos, reduzindo o risco de correspondência com exercícios indexados publicamente.",
    },
    {
        "tipo": "Time-box não uniforme",
        "descricao": "Reduzir o time-box de forma desigual entre integrantes distorceria a comparabilidade entre grupos da turma.",
        "mitigacao": "Time-box fixo de 35 minutos por trial para todos os integrantes, sem exceções.",
    },
]


@dataclass
class DesenhoExperimento:
    hipoteses: dict = field(default_factory=lambda: HIPOTESES)
    variaveis_dependentes: list = field(default_factory=lambda: VARIAVEIS_DEPENDENTES)
    variavel_independente: dict = field(default_factory=lambda: VARIAVEL_INDEPENDENTE)
    tratamentos: list = field(default_factory=lambda: TRATAMENTOS)
    katas: list = field(default_factory=lambda: KATAS)
    desenho_experimental: dict = field(default_factory=lambda: DESENHO_EXPERIMENTAL)
    quantidade_medicoes: dict = field(default_factory=lambda: QUANTIDADE_MEDICOES)
    ameacas_validade: list = field(default_factory=lambda: AMEACAS_VALIDADE)


if __name__ == "__main__":
    desenho = DesenhoExperimento()
    print(f"Katas: {desenho.katas}")
    print(f"Tratamentos: {desenho.tratamentos}")
    print(f"Total de ameaças à validade documentadas: {len(desenho.ameacas_validade)}")
    print(f"Total de RQs com hipóteses formalizadas: {len(desenho.hipoteses)}")