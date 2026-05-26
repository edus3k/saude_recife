# ============================================
# FILTROS GLOBAIS
# utils/filtros.py
# ============================================

import streamlit as st

# ============================================
# CRIAR FILTROS
# ============================================

def criar_filtros(dados):

    st.sidebar.header("🎛️ Filtros")

    # ========================================
    # ANOS
    # ========================================

    anos = sorted(

        dados["ano"]
        .dropna()
        .unique()

    )

    # ========================================
    # MESES
    # ========================================

    meses = sorted(

        dados["mes"]
        .dropna()
        .unique()

    )

    # ========================================
    # UNIDADES
    # ========================================

    unidades = sorted(

        dados["nome_unidade"]
        .dropna()
        .unique()

    )

    # ========================================
    # FILTROS SIDEBAR
    # ========================================

    ano_select = st.sidebar.multiselect(

        "Ano",

        anos,

        default=anos

    )

    mes_select = st.sidebar.multiselect(

        "Mês",

        meses,

        default=meses

    )

    unidade_select = st.sidebar.multiselect(

        "Unidades",

        unidades,

        default=unidades

    )

    # ========================================
    # TOP N
    # ========================================

    top_n = st.sidebar.slider(

        "Top Ranking",

        min_value=5,

        max_value=50,

        value=20

    )

    # ========================================
    # RETORNO
    # ========================================

    return {

        "anos": ano_select,

        "meses": mes_select,

        "unidades": unidade_select,

        "top_n": top_n

    }

# ============================================
# APLICAR FILTROS
# ============================================

def aplicar_filtros(dados, filtros):

    dados_filtrados = dados[

        (

            dados["ano"]
            .isin(filtros["anos"])

        )

        &

        (

            dados["mes"]
            .isin(filtros["meses"])

        )

        &

        (

            dados["nome_unidade"]
            .isin(filtros["unidades"])

        )

    ]

    return dados_filtrados

# ============================================
# FILTRO DE PERÍODO
# ============================================

def criar_periodo(dados):

    dados["periodo"] = (

        dados["ano"]
        .astype(str)

        + "-"

        +

        dados["mes"]
        .astype(str)
        .str.zfill(2)

    )

    return dados

# ============================================
# FILTRO PERSONALIZADO
# ============================================

def filtro_top_n(df, coluna, top_n=10):

    return (

        df

        .sort_values(
            coluna,
            ascending=False
        )

        .head(top_n)

    )

# ============================================
# FILTRO POR INTERVALO
# ============================================

def filtro_intervalo(

    dados,

    coluna,

    valor_min,

    valor_max

):

    return dados[

        (

            dados[coluna]
            >= valor_min

        )

        &

        (

            dados[coluna]
            <= valor_max

        )

    ]

# ============================================
# FILTRO TEXTO
# ============================================

def filtro_texto(

    dados,

    coluna,

    texto

):

    if texto == "":

        return dados

    return dados[

        dados[coluna]
        .astype(str)
        .str.contains(
            texto,
            case=False,
            na=False
        )

    ]