# ============================================
# CONEXÃO DATABASE
# services/database.py
# ============================================

import duckdb
import pandas as pd
import streamlit as st

# ============================================
# CONEXÃO GLOBAL
# ============================================

@st.cache_resource
def conectar():

    conexao = duckdb.connect()

    return conexao

# ============================================
# EXECUTAR QUERY
# ============================================

@st.cache_data(show_spinner=False)
def executar_query(query):

    con = conectar()

    return con.execute(query).df()

# ============================================
# VALIDAR PARQUET
# ============================================

def validar_parquet(arquivo):

    try:

        query = f"""

        SELECT *
        FROM read_parquet('{arquivo}')
        LIMIT 1

        """

        executar_query(query)

        return True

    except Exception as erro:

        st.error(

            f"Erro ao abrir parquet: {erro}"

        )

        return False

# ============================================
# CONTAR REGISTROS
# ============================================

def contar_registros(arquivo):

    query = f"""

    SELECT COUNT(*) AS total
    FROM read_parquet('{arquivo}')

    """

    resultado = executar_query(query)

    return int(

        resultado.iloc[0]["total"]

    )

# ============================================
# LISTAR COLUNAS
# ============================================

def listar_colunas(arquivo):

    query = f"""

    SELECT *
    FROM read_parquet('{arquivo}')
    LIMIT 1

    """

    dados = executar_query(query)

    return list(dados.columns)

# ============================================
# PREVIEW DADOS
# ============================================

def preview_dados(

    arquivo,

    limite=10

):

    query = f"""

    SELECT *
    FROM read_parquet('{arquivo}')
    LIMIT {limite}

    """

    return executar_query(query)

# ============================================
# CARREGAR PAPE
# ============================================

@st.cache_data(show_spinner=True)
def carregar_pape(arquivo):

    query = f"""

    SELECT *

    FROM read_parquet('{arquivo}')

    """

    return executar_query(query)

# ============================================
# CARREGAR PFPE
# ============================================

@st.cache_data(show_spinner=True)
def carregar_pfpe(arquivo):

    query = f"""

    SELECT *

    FROM read_parquet('{arquivo}')

    """

    return executar_query(query)

# ============================================
# CARREGAR STPE
# ============================================

@st.cache_data(show_spinner=True)
def carregar_stpe(arquivo):

    query = f"""

    SELECT *

    FROM read_parquet('{arquivo}')

    """

    return executar_query(query)

# ============================================
# QUERY PERSONALIZADA
# ============================================

def query_personalizada(query):

    return executar_query(query)

# ============================================
# LISTAR ANOS
# ============================================

def listar_anos(arquivo):

    query = f"""

    SELECT DISTINCT ano

    FROM read_parquet('{arquivo}')

    ORDER BY ano

    """

    dados = executar_query(query)

    return (

        dados["ano"]

        .dropna()

        .tolist()

    )

# ============================================
# LISTAR MESES
# ============================================

def listar_meses(arquivo):

    query = f"""

    SELECT DISTINCT mes

    FROM read_parquet('{arquivo}')

    ORDER BY mes

    """

    dados = executar_query(query)

    return (

        dados["mes"]

        .dropna()

        .tolist()

    )

# ============================================
# LISTAR CNES
# ============================================

def listar_cnes(

    arquivo,

    coluna="pa_coduni"

):

    query = f"""

    SELECT DISTINCT

        CAST({coluna} AS VARCHAR)
            AS cnes

    FROM read_parquet('{arquivo}')

    """

    dados = executar_query(query)

    return (

        dados["cnes"]

        .dropna()

        .tolist()

    )

# ============================================
# FILTRO SQL
# ============================================

def montar_filtro_sql(

    anos=None,

    meses=None,

    unidades=None,

    coluna_unidade="pa_coduni"

):

    filtros = []

    # ========================================
    # ANOS
    # ========================================

    if anos:

        anos_sql = ",".join([

            f"'{x}'"

            for x in anos

        ])

        filtros.append(

            f"ano IN ({anos_sql})"

        )

    # ========================================
    # MESES
    # ========================================

    if meses:

        meses_sql = ",".join([

            f"'{x}'"

            for x in meses

        ])

        filtros.append(

            f"mes IN ({meses_sql})"

        )

    # ========================================
    # UNIDADES
    # ========================================

    if unidades:

        unidades_sql = ",".join([

            f"'{x}'"

            for x in unidades

        ])

        filtros.append(

            f"""

            CAST({coluna_unidade} AS VARCHAR)

            IN ({unidades_sql})

            """

        )

    # ========================================
    # RETORNO
    # ========================================

    if filtros:

        return (

            "WHERE "

            + " AND ".join(filtros)

        )

    return ""

# ============================================
# QUERY INTEGRADA
# ============================================

@st.cache_data(show_spinner=True)
def carregar_base_integrada(

    pape_file,

    pfpe_file,

    stpe_file,

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

        FROM read_parquet('{pape_file}')

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

        FROM read_parquet('{pfpe_file}')

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

        FROM read_parquet('{stpe_file}')

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
# FECHAR CONEXÃO
# ============================================

def fechar_conexao():

    try:

        con = conectar()

        con.close()

    except:

        pass