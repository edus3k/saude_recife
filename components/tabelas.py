# ============================================
# TABELAS PADRONIZADAS
# utils/tabelas.py
# ============================================

import streamlit as st
import pandas as pd

# ============================================
# CONFIGURAÇÃO PADRÃO
# ============================================

ALTURA_PADRAO = 600

# ============================================
# EXIBIR DATAFRAME
# ============================================

def mostrar_tabela(

    dados,

    titulo=None,

    altura=ALTURA_PADRAO,

    use_container_width=True

):

    if titulo:

        st.subheader(titulo)

    st.dataframe(

        dados,

        height=altura,

        use_container_width=use_container_width

    )

# ============================================
# TABELA COM ESTILO
# ============================================

def mostrar_tabela_estilizada(

    dados,

    titulo=None,

    altura=ALTURA_PADRAO

):

    if titulo:

        st.subheader(titulo)

    st.dataframe(

        dados.style.format({

            col: "{:,.2f}"

            for col in dados.select_dtypes(
                include=["float", "float64"]
            ).columns

        }),

        height=altura,

        use_container_width=True

    )

# ============================================
# TABELA TOP N
# ============================================

def mostrar_top_n(

    dados,

    coluna,

    top_n=10,

    titulo=None,

    ascendente=False

):

    top = (

        dados

        .sort_values(
            coluna,
            ascending=ascendente
        )

        .head(top_n)

    )

    mostrar_tabela(

        top,

        titulo=titulo

    )

# ============================================
# TABELA RESUMO
# ============================================

def tabela_resumo(

    dados,

    groupby,

    metricas

):

    resumo = (

        dados

        .groupby(
            groupby,
            as_index=False
        )

        .agg(metricas)

    )

    return resumo

# ============================================
# TABELA RANKING
# ============================================

def tabela_ranking(

    dados,

    coluna_ranking,

    top_n=20

):

    ranking = (

        dados

        .sort_values(
            coluna_ranking,
            ascending=False
        )

        .head(top_n)

        .reset_index(drop=True)

    )

    ranking.index = ranking.index + 1

    ranking = ranking.reset_index()

    ranking.rename(

        columns={

            "index": "Posição"

        },

        inplace=True

    )

    return ranking

# ============================================
# TABELA TEMPORAL
# ============================================

def tabela_temporal(

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
# FILTRAR COLUNAS
# ============================================

def selecionar_colunas(

    dados,

    colunas

):

    return dados[colunas]

# ============================================
# RENOMEAR COLUNAS
# ============================================

def renomear_colunas(

    dados,

    mapa_colunas

):

    return dados.rename(
        columns=mapa_colunas
    )

# ============================================
# ORDENAR TABELA
# ============================================

def ordenar_tabela(

    dados,

    coluna,

    ascendente=False

):

    return dados.sort_values(

        coluna,

        ascending=ascendente

    )

# ============================================
# EXPORTAR CSV
# ============================================

def gerar_csv(dados):

    return (

        dados

        .to_csv(index=False)

        .encode("utf-8")

    )

# ============================================
# BOTÃO DOWNLOAD
# ============================================

def botao_download(

    dados,

    nome_arquivo="dados.csv",

    texto="📥 Download CSV"

):

    csv = gerar_csv(dados)

    st.download_button(

        label=texto,

        data=csv,

        file_name=nome_arquivo,

        mime="text/csv"

    )

# ============================================
# TABELA PAGINADA
# ============================================

def tabela_paginada(

    dados,

    page_size=20,

    titulo=None

):

    if titulo:

        st.subheader(titulo)

    total_paginas = (

        len(dados) // page_size

    ) + 1

    pagina = st.number_input(

        "Página",

        min_value=1,

        max_value=total_paginas,

        step=1

    )

    inicio = (

        (pagina - 1)

        * page_size

    )

    fim = inicio + page_size

    st.dataframe(

        dados.iloc[inicio:fim],

        use_container_width=True

    )

# ============================================
# TABELA COM PESQUISA
# ============================================

def tabela_com_pesquisa(

    dados,

    coluna_busca,

    titulo=None

):

    if titulo:

        st.subheader(titulo)

    busca = st.text_input(
        "Pesquisar"
    )

    if busca:

        dados = dados[

            dados[coluna_busca]

            .astype(str)

            .str.contains(

                busca,

                case=False,

                na=False

            )

        ]

    st.dataframe(

        dados,

        use_container_width=True

    )

# ============================================
# TABELA ESTATÍSTICA
# ============================================

def tabela_estatistica(

    dados,

    titulo="Resumo Estatístico"

):

    st.subheader(titulo)

    resumo = dados.describe()

    st.dataframe(

        resumo,

        use_container_width=True

    )

# ============================================
# TABELA DUPLA
# ============================================

def tabela_dupla(

    tabela1,

    tabela2,

    titulo1="Tabela 1",

    titulo2="Tabela 2"

):

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(titulo1)

        st.dataframe(

            tabela1,

            use_container_width=True

        )

    with col2:

        st.subheader(titulo2)

        st.dataframe(

            tabela2,

            use_container_width=True

        )

# ============================================
# ALERTA TABELA VAZIA
# ============================================

def validar_tabela(

    dados,

    mensagem="Nenhum dado encontrado."

):

    if dados.empty:

        st.warning(mensagem)

        return False

    return True