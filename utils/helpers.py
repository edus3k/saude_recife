# ============================================
# HELPERS GERAIS
# utils/helpers.py
# ============================================

import pandas as pd
import numpy as np
import streamlit as st

# ============================================
# VALIDAR DATAFRAME
# ============================================

def validar_dataframe(

    dados,

    mensagem="Nenhum dado encontrado."

):

    if dados is None or dados.empty:

        st.warning(mensagem)

        return False

    return True

# ============================================
# LIMPAR COLUNAS
# ============================================

def limpar_colunas(dados):

    dados = dados.copy()

    dados.columns = (

        dados.columns

        .str.strip()

        .str.lower()

        .str.replace(" ", "_")

    )

    return dados

# ============================================
# CONVERTER TIPOS
# ============================================

def converter_tipos(dados):

    dados = dados.copy()

    for col in dados.columns:

        if "ano" in col:

            dados[col] = pd.to_numeric(

                dados[col],

                errors="coerce"

            ).astype("Int64")

        elif "mes" in col:

            dados[col] = pd.to_numeric(

                dados[col],

                errors="coerce"

            ).astype("Int64")

    return dados

# ============================================
# REMOVER OUTLIERS
# ============================================

def remover_outliers(

    dados,

    coluna

):

    q1 = dados[coluna].quantile(0.25)

    q3 = dados[coluna].quantile(0.75)

    iqr = q3 - q1

    limite_inf = q1 - 1.5 * iqr

    limite_sup = q3 + 1.5 * iqr

    return dados[

        (dados[coluna] >= limite_inf)

        &

        (dados[coluna] <= limite_sup)

    ]

# ============================================
# NORMALIZAR COLUNA
# ============================================

def normalizar(dados, coluna):

    dados = dados.copy()

    min_val = dados[coluna].min()

    max_val = dados[coluna].max()

    if max_val == min_val:

        dados[coluna + "_norm"] = 0

        return dados

    dados[coluna + "_norm"] = (

        dados[coluna] - min_val

    ) / (

        max_val - min_val

    )

    return dados

# ============================================
# PIVOT RÁPIDO
# ============================================

def pivot_rapido(

    dados,

    index,

    columns,

    values,

    agg="mean"

):

    return pd.pivot_table(

        dados,

        index=index,

        columns=columns,

        values=values,

        aggfunc=agg,

        fill_value=0

    )

# ============================================
# AGRUPAMENTO SIMPLES
# ============================================

def agrupar(

    dados,

    groupby,

    agg_dict

):

    return (

        dados

        .groupby(groupby)

        .agg(agg_dict)

        .reset_index()

    )

# ============================================
# ORDENAR
# ============================================

def ordenar(

    dados,

    coluna,

    asc=False

):

    return dados.sort_values(

        coluna,

        ascending=asc

    )

# ============================================
# TOP N
# ============================================

def top_n(

    dados,

    coluna,

    n=10,

    asc=False

):

    return (

        dados

        .sort_values(

            coluna,

            ascending=asc

        )

        .head(n)

    )

# ============================================
# DETECTAR COLUNAS NUMÉRICAS
# ============================================

def colunas_numericas(dados):

    return (

        dados.select_dtypes(

            include=[np.number]

        ).columns.tolist()

    )

# ============================================
# DETECTAR COLUNAS TEXTO
# ============================================

def colunas_texto(dados):

    return (

        dados.select_dtypes(

            include=["object"]

        ).columns.tolist()

    )

# ============================================
# SUBSTITUIR VALORES NULOS
# ============================================

def tratar_nulos(

    dados,

    valor=0

):

    return dados.fillna(valor)

# ============================================
# CRIAR COLUNA PERÍODO
# ============================================

def criar_periodo(dados):

    dados = dados.copy()

    dados["periodo"] = (

        dados["ano"].astype(str)

        + "-"

        +

        dados["mes"].astype(str).str.zfill(2)

    )

    return dados

# ============================================
# RESUMO RÁPIDO
# ============================================

def resumo_rapido(dados):

    return {

        "linhas": len(dados),

        "colunas": len(dados.columns),

        "nulos": dados.isnull().sum().sum()

    }

# ============================================
# DEBUG INFO
# ============================================

def debug_info(dados):

    st.write("Shape:", dados.shape)

    st.write("Colunas:", list(dados.columns))

    st.write("Tipos:", dados.dtypes)

# ============================================
# CACHE SAFE
# ============================================

def cache_safe(func):

    def wrapper(*args, **kwargs):

        try:

            return func(*args, **kwargs)

        except Exception as e:

            st.error(f"Erro: {e}")

            return None

    return wrapper