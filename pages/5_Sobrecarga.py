# ============================================
# SOBRECARGA ASSISTENCIAL
# pages/5_🚨_Sobrecarga.py
# ============================================

import streamlit as st
import pandas as pd
import plotly.express as px

from services.queries import executar_query
from services.calculos import calcular_metricas
from utils.constantes import (
    PAPE_FILE,
    PFPE_FILE,
    STPE_FILE
)

# ============================================
# CONFIG
# ============================================

st.set_page_config(
    page_title="Sobrecarga Assistencial",
    layout="wide"
)

st.title("🚨 Sobrecarga Assistencial")

st.markdown("""
Painel analítico voltado para identificação
das unidades com maior pressão operacional,
sobrecarga assistencial e risco estrutural.
""")

# ============================================
# CARREGAR DADOS
# ============================================

@st.cache_data(show_spinner=True)
def carregar_dados():

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

dados = carregar_dados()

# ============================================
# VALIDAR
# ============================================

if dados.empty:

    st.warning("Nenhum dado encontrado.")
    st.stop()

# ============================================
# NOME UNIDADE
# ============================================

dados["nome_unidade"] = (

    "CNES "

    +

    dados["unidade"]
    .astype(str)

)

# ============================================
# MÉTRICAS
# ============================================

dados = calcular_metricas(dados)

# ============================================
# ÍNDICE SOBRECARGA
# ============================================

dados["indice_sobrecarga"] = (

    dados["pacientes_por_medico"] * 0.4

    +

    dados["pressao_leitos"] * 0.3

    +

    dados["tempo_espera"] * 0.3

)

# ============================================
# SIDEBAR
# ============================================

st.sidebar.header("🎛️ Filtros")

anos = sorted(
    dados["ano"]
    .dropna()
    .unique()
)

meses = sorted(
    dados["mes"]
    .dropna()
    .unique()
)

unidades = sorted(
    dados["nome_unidade"]
    .dropna()
    .unique()
)

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
    "Unidade",
    unidades,
    default=unidades
)

top_n = st.sidebar.slider(
    "Top Sobrecarga",
    min_value=5,
    max_value=50,
    value=20
)

# ============================================
# FILTRAR
# ============================================

dados = dados[

    (dados["ano"].isin(ano_select))

    &

    (dados["mes"].isin(mes_select))

    &

    (dados["nome_unidade"].isin(unidade_select))

]

# ============================================
# KPIS
# ============================================

st.markdown("---")

st.subheader("📊 Indicadores de Sobrecarga")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Atendimentos",
    f"{dados['total_atendimentos'].sum():,.0f}"
)

col2.metric(
    "Tempo Espera",
    f"{dados['tempo_espera'].mean():.1f}"
)

col3.metric(
    "Pacientes/Médico",
    f"{dados['pacientes_por_medico'].mean():.2f}"
)

col4.metric(
    "Índice Sobrecarga",
    f"{dados['indice_sobrecarga'].mean():.2f}"
)

# ============================================
# RANKING SOBRECARGA
# ============================================

st.markdown("---")

st.subheader("🚨 Ranking de Sobrecarga")

st.markdown("""
### 📌 O que este gráfico representa?

Este gráfico apresenta as unidades com maior
nível de sobrecarga operacional.

O cálculo considera:
- pacientes por médico
- pressão sobre os leitos
- tempo médio de espera

### ✅ Conclusão Resumida

Unidades com maiores índices apresentam maior
risco operacional e possível superlotação.
Valores elevados indicam necessidade de reforço
estrutural e assistencial.
""")

ranking = (

    dados

    .groupby(
        "nome_unidade",
        as_index=False
    )

    .agg({

        "indice_sobrecarga":
            "mean",

        "tempo_espera":
            "mean",

        "pacientes_por_medico":
            "mean",

        "pressao_leitos":
            "mean"

    })

    .sort_values(
        "indice_sobrecarga",
        ascending=False
    )

    .head(top_n)

)

fig1 = px.bar(

    ranking,

    x="indice_sobrecarga",

    y="nome_unidade",

    orientation="h",

    color="tempo_espera",

    text="indice_sobrecarga",

    hover_data=[

        "pacientes_por_medico",
        "pressao_leitos"

    ],

    template="plotly_white",

    title="Ranking de Sobrecarga Assistencial"

)

fig1.update_traces(
    texttemplate='%{text:.2f}',
    textposition='outside'
)

fig1.update_layout(

    height=850,

    title_x=0.5,

    xaxis_title="Índice de Sobrecarga",

    yaxis_title=""

)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ============================================
# PRESSÃO LEITOS
# ============================================

st.markdown("---")

st.subheader("🛏️ Pressão sobre Leitos")

st.markdown("""
### 📌 O que este gráfico representa?

Mostra a pressão assistencial sobre os leitos
disponíveis nas unidades de saúde.

### ✅ Conclusão Resumida

Unidades com maiores valores apresentam maior
ocupação estrutural e maior risco de saturação
hospitalar.
""")

pressao = (

    dados

    .groupby(
        "nome_unidade",
        as_index=False
    )

    .agg({

        "pressao_leitos":
            "mean"

    })

    .sort_values(
        "pressao_leitos",
        ascending=False
    )

    .head(top_n)

)

fig2 = px.bar(

    pressao,

    x="pressao_leitos",

    y="nome_unidade",

    orientation="h",

    color="pressao_leitos",

    text="pressao_leitos",

    template="plotly_white",

    title="Pressão sobre Leitos"

)

fig2.update_traces(
    texttemplate='%{text:.2f}',
    textposition='outside'
)

fig2.update_layout(

    height=850,

    title_x=0.5,

    xaxis_title="Pressão Assistencial",

    yaxis_title=""

)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ============================================
# TEMPO ESPERA
# ============================================

st.markdown("---")

st.subheader("⏱️ Tempo Médio de Espera")

st.markdown("""
### 📌 O que este gráfico representa?

Apresenta a estimativa média do tempo
de espera nas unidades de saúde.

### ✅ Conclusão Resumida

Tempos elevados podem representar maior
sobrecarga operacional e dificuldade
na capacidade de atendimento.
""")

espera = (

    dados

    .groupby(
        "nome_unidade",
        as_index=False
    )

    .agg({

        "tempo_espera":
            "mean"

    })

    .sort_values(
        "tempo_espera",
        ascending=False
    )

    .head(top_n)

)

fig3 = px.bar(

    espera,

    x="tempo_espera",

    y="nome_unidade",

    orientation="h",

    color="tempo_espera",

    text="tempo_espera",

    template="plotly_white",

    title="Tempo Médio de Espera"

)

fig3.update_traces(
    texttemplate='%{text:.1f}',
    textposition='outside'
)

fig3.update_layout(

    height=850,

    title_x=0.5,

    xaxis_title="Tempo Médio de Espera",

    yaxis_title=""

)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ============================================
# MAPA CORRELAÇÃO
# ============================================

st.markdown("---")

st.subheader("📈 Correlação Operacional")

st.markdown("""
### 📌 O que este gráfico representa?

Relaciona:
- volume de atendimentos
- índice de sobrecarga
- tempo de espera
- pressão estrutural

Cada bolha representa uma unidade de saúde.

### ✅ Conclusão Resumida

Unidades com maior demanda tendem a apresentar
maior criticidade operacional e maior tempo
de espera assistencial.
""")

fig4 = px.scatter(

    dados,

    x="total_atendimentos",

    y="indice_sobrecarga",

    size="tempo_espera",

    color="pressao_leitos",

    hover_name="nome_unidade",

    template="plotly_white",

    title="Correlação Operacional"

)

fig4.update_layout(

    height=700,

    title_x=0.5,

    xaxis_title="Atendimentos",

    yaxis_title="Índice de Sobrecarga"

)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ============================================
# RESUMO EXECUTIVO
# ============================================

st.markdown("---")

st.subheader("📝 Resumo Executivo")

indice_medio = round(
    dados["indice_sobrecarga"].mean(),
    2
)

tempo_medio = round(
    dados["tempo_espera"].mean(),
    1
)

unidade_critica = ranking.iloc[0]["nome_unidade"]

st.info(f"""

O índice médio de sobrecarga operacional
foi de {indice_medio} pontos.

O tempo médio estimado de espera foi
de aproximadamente {tempo_medio} minutos.

A unidade com maior criticidade operacional
foi {unidade_critica}.

Os indicadores demonstram forte relação entre:
- demanda assistencial
- estrutura hospitalar
- tempo de espera
- pressão operacional

""")

# ============================================
# FOOTER
# ============================================

st.success(
    "✅ Painel de sobrecarga assistencial carregado"
)