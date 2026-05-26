# ============================================
# QUERIES ANALÍTICAS
# services/queries.py
# ============================================

import pandas as pd

from services.database import (
    executar_query
)

from utils.constantes import (
    PAPE_FILE,
    PFPE_FILE,
    STPE_FILE
)

# ============================================
# QUERY BASE INTEGRADA
# ============================================

def query_base_integrada(

    filtro=""

):

    query = f"""

    WITH pape AS (

        SELECT

            CAST(pa_coduni AS VARCHAR)
                AS unidade,

            ano,
            mes,

            COUNT(*)
                AS total_atendimentos

        FROM read_parquet('{PAPE_FILE}')

        {filtro}

        GROUP BY 1,2,3

    ),

    pfpe AS (

        SELECT

            CAST(cnes AS VARCHAR)
                AS unidade,

            COUNT(*)
                AS total_profissionais,

            COUNT(*) FILTER (

                WHERE cpf_cnpj IS NOT NULL

            )
                AS total_medicos

        FROM read_parquet('{PFPE_FILE}')

        GROUP BY 1

    ),

    stpe AS (

        SELECT

            CAST(cnes AS VARCHAR)
                AS unidade,

            COUNT(*)
                AS qtd_leitos,

            COUNT(*)
                AS qtd_salas,

            COUNT(*)
                AS qtd_equipamentos

        FROM read_parquet('{STPE_FILE}')

        GROUP BY 1

    )

    SELECT

        p.unidade,

        p.ano,
        p.mes,

        p.total_atendimentos,

        COALESCE(
            f.total_profissionais,
            0
        ) AS total_profissionais,

        COALESCE(
            f.total_medicos,
            0
        ) AS total_medicos,

        COALESCE(
            s.qtd_leitos,
            0
        ) AS qtd_leitos,

        COALESCE(
            s.qtd_salas,
            0
        ) AS qtd_salas,

        COALESCE(
            s.qtd_equipamentos,
            0
        ) AS qtd_equipamentos

    FROM pape p

    LEFT JOIN pfpe f
        ON p.unidade = f.unidade

    LEFT JOIN stpe s
        ON p.unidade = s.unidade

    """

    return executar_query(query)

# ============================================
# QUERY RANKING
# ============================================

def query_ranking(

    dados,

    top_n=20

):

    ranking = (

        dados

        .groupby(
            "nome_unidade",
            as_index=False
        )

        .agg({

            "score_qualidade":
                "mean",

            "total_atendimentos":
                "sum",

            "total_profissionais":
                "mean",

            "qtd_leitos":
                "mean"

        })

        .sort_values(

            "score_qualidade",

            ascending=False

        )

        .head(top_n)

    )

    return ranking

# ============================================
# QUERY EFICIÊNCIA
# ============================================

def query_eficiencia(

    dados,

    top_n=20

):

    eficiencia = (

        dados

        .groupby([

            "ano",
            "mes",
            "nome_unidade"

        ], as_index=False)

        .agg({

            "total_atendimentos":
                "sum",

            "total_profissionais":
                "mean",

            "total_medicos":
                "mean",

            "tempo_espera":
                "mean",

            "score_qualidade":
                "mean"

        })

    )

    eficiencia[
        "atendimento_por_profissional"
    ] = (

        eficiencia[
            "total_atendimentos"
        ]

        /

        eficiencia[
            "total_profissionais"
        ]
        .replace(0, 1)

    )

    eficiencia[
        "score_eficiencia"
    ] = (

        eficiencia[
            "atendimento_por_profissional"
        ]

        * 0.7

        +

        eficiencia[
            "score_qualidade"
        ]

        * 0.3

    )

    return (

        eficiencia

        .sort_values(

            "score_eficiencia",

            ascending=False

        )

        .head(top_n)

    )

# ============================================
# QUERY SOBRECARGA
# ============================================

def query_sobrecarga(

    dados,

    top_n=20

):

    sobrecarga = (

        dados

        .groupby([

            "ano",
            "mes",
            "nome_unidade"

        ], as_index=False)

        .agg({

            "total_atendimentos":
                "sum",

            "total_profissionais":
                "mean",

            "total_medicos":
                "mean",

            "tempo_espera":
                "mean",

            "pacientes_por_medico":
                "mean",

            "pressao_leitos":
                "mean"

        })

    )

    sobrecarga[
        "indice_sobrecarga"
    ] = (

        sobrecarga[
            "pacientes_por_medico"
        ] * 0.4

        +

        sobrecarga[
            "pressao_leitos"
        ] * 0.3

        +

        sobrecarga[
            "tempo_espera"
        ] * 0.3

    )

    return (

        sobrecarga

        .sort_values(

            "indice_sobrecarga",

            ascending=False

        )

        .head(top_n)

    )

# ============================================
# QUERY EVOLUÇÃO
# ============================================

def query_evolucao(

    dados

):

    evolucao = (

        dados

        .groupby([

            "ano",
            "mes"

        ], as_index=False)

        .agg({

            "total_atendimentos":
                "sum",

            "score_qualidade":
                "mean",

            "tempo_espera":
                "mean"

        })

    )

    evolucao["periodo"] = (

        evolucao["ano"]
        .astype(str)

        + "-"

        +

        evolucao["mes"]
        .astype(str)
        .str.zfill(2)

    )

    return evolucao

# ============================================
# QUERY QUALIDADE X DEMANDA
# ============================================

def query_qualidade_demanda(

    dados

):

    return (

        dados

        .groupby(
            "nome_unidade",
            as_index=False
        )

        .agg({

            "total_atendimentos":
                "sum",

            "score_qualidade":
                "mean",

            "tempo_espera":
                "mean",

            "qtd_leitos":
                "mean"

        })

    )

# ============================================
# QUERY RESUMO EXECUTIVO
# ============================================

def query_resumo(

    dados

):

    resumo = {

        "total_atendimentos":

            int(
                dados[
                    "total_atendimentos"
                ].sum()
            ),

        "total_profissionais":

            int(
                dados[
                    "total_profissionais"
                ].sum()
            ),

        "total_medicos":

            int(
                dados[
                    "total_medicos"
                ].sum()
            ),

        "total_leitos":

            int(
                dados[
                    "qtd_leitos"
                ].sum()
            ),

        "score_medio":

            round(

                dados[
                    "score_qualidade"
                ].mean(),

                2

            ),

        "tempo_espera":

            round(

                dados[
                    "tempo_espera"
                ].mean(),

                1

            )

    }

    return resumo

# ============================================
# QUERY TOP UNIDADES
# ============================================

def query_top_unidades(

    dados,

    coluna,

    top_n=10

):

    return (

        dados

        .groupby(
            "nome_unidade",
            as_index=False
        )

        .agg({

            coluna:
                "mean"

        })

        .sort_values(

            coluna,

            ascending=False

        )

        .head(top_n)

    )

# ============================================
# QUERY COMPARATIVO
# ============================================

def query_comparativo(

    dados,

    coluna

):

    return (

        dados

        .pivot_table(

            index="periodo",

            columns="nome_unidade",

            values=coluna,

            aggfunc="mean"

        )

        .fillna(0)

    )

# ============================================
# QUERY HEATMAP
# ============================================

def query_heatmap(

    dados,

    coluna

):

    heatmap = (

        dados

        .pivot_table(

            index="nome_unidade",

            columns="mes",

            values=coluna,

            aggfunc="mean"

        )

        .fillna(0)

    )

    return heatmap

# ============================================
# QUERY CORRELAÇÃO
# ============================================

def query_correlacao(

    dados,

    colunas

):

    return (

        dados[colunas]

        .corr()

    )

# ============================================
# QUERY OUTLIERS
# ============================================

def query_outliers(

    dados,

    coluna

):

    q1 = dados[coluna].quantile(0.25)

    q3 = dados[coluna].quantile(0.75)

    iqr = q3 - q1

    limite_inferior = q1 - 1.5 * iqr

    limite_superior = q3 + 1.5 * iqr

    return dados[

        (

            dados[coluna]
            < limite_inferior

        )

        |

        (

            dados[coluna]
            > limite_superior

        )

    ]

# ============================================
# QUERY STATUS OPERACIONAL
# ============================================

def query_status_operacional(

    dados

):

    return (

        dados

        .groupby(
            "status_operacional",
            as_index=False
        )

        .agg({

            "nome_unidade":
                "count"

        })

        .rename(columns={

            "nome_unidade":
                "quantidade"

        })

    )

# ============================================
# QUERY DISTRIBUIÇÃO
# ============================================

def query_distribuicao(

    dados,

    coluna

):

    return dados[coluna]