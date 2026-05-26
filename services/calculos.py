# ============================================
# CÁLCULOS E MÉTRICAS
# services/calculos.py
# ============================================

import pandas as pd
import numpy as np

# ============================================
# PACIENTES POR MÉDICO
# ============================================

def calcular_pacientes_por_medico(dados):

    dados["pacientes_por_medico"] = (

        dados["total_atendimentos"]

        /

        dados["total_medicos"]
        .replace(0, 1)

    )

    return dados

# ============================================
# PRESSÃO LEITOS
# ============================================

def calcular_pressao_leitos(dados):

    dados["pressao_leitos"] = (

        dados["total_atendimentos"]

        /

        dados["qtd_leitos"]
        .replace(0, 1)

    )

    return dados

# ============================================
# TEMPO ESPERA
# ============================================

def calcular_tempo_espera(dados):

    dados["tempo_espera"] = (

        dados["pacientes_por_medico"]

        * 12

    )

    return dados

# ============================================
# SCORE QUALIDADE
# ============================================

def calcular_score_qualidade(dados):

    dados["score_qualidade"] = (

        (

            1000

            /

            (

                dados[
                    "pacientes_por_medico"
                ] + 1

            )

        )

        +

        (

            500

            /

            (

                dados[
                    "pressao_leitos"
                ] + 1

            )

        )

    )

    return dados

# ============================================
# SCORE EFICIÊNCIA
# ============================================

def calcular_score_eficiencia(dados):

    dados["atendimento_por_profissional"] = (

        dados["total_atendimentos"]

        /

        dados["total_profissionais"]
        .replace(0, 1)

    )

    dados["score_eficiencia"] = (

        dados[
            "atendimento_por_profissional"
        ]

        * 0.7

        +

        dados[
            "score_qualidade"
        ]

        * 0.3

    )

    return dados

# ============================================
# ÍNDICE SOBRECARGA
# ============================================

def calcular_indice_sobrecarga(dados):

    dados["indice_sobrecarga"] = (

        dados[
            "pacientes_por_medico"
        ] * 0.4

        +

        dados[
            "pressao_leitos"
        ] * 0.3

        +

        dados[
            "tempo_espera"
        ] * 0.3

    )

    return dados

# ============================================
# SCORE ESTRUTURAL
# ============================================

def calcular_score_estrutura(dados):

    dados["score_estrutura"] = (

        dados["qtd_leitos"] * 0.4

        +

        dados["qtd_salas"] * 0.3

        +

        dados["qtd_equipamentos"] * 0.3

    )

    return dados

# ============================================
# SCORE GERAL
# ============================================

def calcular_score_geral(dados):

    dados["score_geral"] = (

        dados["score_qualidade"] * 0.4

        +

        dados["score_eficiencia"] * 0.3

        +

        dados["score_estrutura"] * 0.3

    )

    return dados

# ============================================
# STATUS OPERACIONAL
# ============================================

def calcular_status_operacional(dados):

    condicoes = [

        dados["score_qualidade"] >= 80,

        dados["score_qualidade"] >= 60,

        dados["score_qualidade"] >= 40

    ]

    resultados = [

        "Excelente",

        "Bom",

        "Atenção"

    ]

    dados["status_operacional"] = np.select(

        condicoes,

        resultados,

        default="Crítico"

    )

    return dados

# ============================================
# VARIAÇÃO PERCENTUAL
# ============================================

def calcular_variacao_percentual(

    dados,

    coluna,

    groupby=None

):

    if groupby:

        dados[
            f"{coluna}_variacao"
        ] = (

            dados

            .groupby(groupby)[coluna]

            .pct_change()

            * 100

        )

    else:

        dados[
            f"{coluna}_variacao"
        ] = (

            dados[coluna]

            .pct_change()

            * 100

        )

    return dados

# ============================================
# MÉDIA MÓVEL
# ============================================

def calcular_media_movel(

    dados,

    coluna,

    janela=3

):

    dados[
        f"{coluna}_media_movel"
    ] = (

        dados[coluna]

        .rolling(janela)

        .mean()

    )

    return dados

# ============================================
# NORMALIZAÇÃO
# ============================================

def normalizar_coluna(

    dados,

    coluna

):

    minimo = dados[coluna].min()

    maximo = dados[coluna].max()

    dados[
        f"{coluna}_normalizado"
    ] = (

        (

            dados[coluna]

            - minimo

        )

        /

        (

            maximo - minimo

        )

    )

    return dados

# ============================================
# CLASSIFICAÇÃO QUARTIL
# ============================================

def classificar_quartil(

    dados,

    coluna

):

    dados[
        f"{coluna}_quartil"
    ] = pd.qcut(

        dados[coluna],

        q=4,

        labels=[

            "Baixo",

            "Médio",

            "Alto",

            "Muito Alto"

        ]

    )

    return dados

# ============================================
# CALCULAR TODAS MÉTRICAS
# ============================================

def calcular_metricas(dados):

    dados = calcular_pacientes_por_medico(dados)

    dados = calcular_pressao_leitos(dados)

    dados = calcular_tempo_espera(dados)

    dados = calcular_score_qualidade(dados)

    dados = calcular_score_eficiencia(dados)

    dados = calcular_indice_sobrecarga(dados)

    dados = calcular_score_estrutura(dados)

    dados = calcular_score_geral(dados)

    dados = calcular_status_operacional(dados)

    return dados

# ============================================
# RESUMO ESTATÍSTICO
# ============================================

def resumo_estatistico(

    dados,

    colunas

):

    return (

        dados[colunas]

        .describe()

        .transpose()

    )

# ============================================
# TOP INDICADORES
# ============================================

def top_indicadores(

    dados,

    coluna,

    top_n=10,

    ascendente=False

):

    return (

        dados

        .sort_values(

            coluna,

            ascending=ascendente

        )

        .head(top_n)

    )

# ============================================
# AGREGAÇÃO TEMPORAL
# ============================================

def agregacao_temporal(

    dados,

    coluna_data,

    metricas

):

    return (

        dados

        .groupby(
            coluna_data,
            as_index=False
        )

        .agg(metricas)

    )

# ============================================
# AGREGAÇÃO UNIDADE
# ============================================

def agregacao_unidade(

    dados,

    metricas

):

    return (

        dados

        .groupby(
            "nome_unidade",
            as_index=False
        )

        .agg(metricas)

    )

# ============================================
# CORRELAÇÃO
# ============================================

def calcular_correlacao(

    dados,

    colunas

):

    return dados[colunas].corr()

# ============================================
# DETECTAR OUTLIERS
# ============================================

def detectar_outliers(

    dados,

    coluna

):

    q1 = dados[coluna].quantile(0.25)

    q3 = dados[coluna].quantile(0.75)

    iqr = q3 - q1

    limite_inferior = q1 - 1.5 * iqr

    limite_superior = q3 + 1.5 * iqr

    dados["outlier"] = (

        (dados[coluna] < limite_inferior)

        |

        (dados[coluna] > limite_superior)

    )

    return dados

# ============================================
# SCORE PERCENTUAL
# ============================================

def score_percentual(

    dados,

    coluna

):

    total = dados[coluna].sum()

    dados[
        f"{coluna}_percentual"
    ] = (

        dados[coluna]

        / total

    ) * 100

    return dados