
# ============================================
# DASHBOARD QUALIDADE DE ATENDIMENTO
# SAÚDE PÚBLICA - RECIFE
# STREAMLIT + DUCKDB + PARQUET
# ============================================

import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================
# CONFIGURAÇÃO
# ============================================

st.set_page_config(
    page_title="Qualidade de Atendimento - Recife",
    layout="wide"
)

# ============================================
# ARQUIVOS
# ============================================

PAPE_FILE = "../data/dados_tratados/PAPE/PAPE_TOTAL.parquet"
PFPE_FILE = "../data/dados_tratados/PFPE/PFPE_TOTAL.parquet"
STPE_FILE = "../data/dados_tratados/STPE/STPE_TOTAL.parquet"

# ============================================
# TÍTULO
# ============================================

st.title("🏥 Qualidade de Atendimento nas Unidades de Saúde do Recife")

st.markdown("""
Dashboard analítico voltado para:

- Qualidade do atendimento
- Tempo médio de espera
- Quantidade de atendimentos
- Ranking das unidades
- Eficiência operacional
- Distribuição de médicos
- Capacidade de atendimento
""")

# ============================================
# SIDEBAR
# ============================================

st.sidebar.header("⚙️ Configurações")

base = st.sidebar.selectbox(
    "Dataset",
    ["PAPE", "PFPE", "STPE"]
)

if base == "PAPE":
    parquet_file = PAPE_FILE
elif base == "PFPE":
    parquet_file = PFPE_FILE
else:
    parquet_file = STPE_FILE

# ============================================
# CONEXÃO DUCKDB
# ============================================

con = duckdb.connect()

# ============================================
# CARREGA DADOS
# ============================================

@st.cache_data

def carregar_dados(parquet_file):

    query = f"""
        SELECT *
        FROM '{parquet_file}'
    """

    return con.execute(query).fetchdf()


df = carregar_dados(parquet_file)

# ============================================
# PADRÕES DAS COLUNAS
# ============================================
# Ajuste conforme sua base real
# ============================================

colunas = [c.lower() for c in df.columns]

# ============================================
# IDENTIFICAÇÕES AUTOMÁTICAS
# ============================================

col_unidade = None
col_ano = None
col_mes = None

for c in df.columns:

    cl = c.lower()

    if "unid" in cl or "estab" in cl or "hospital" in cl:
        col_unidade = c

    if cl == "ano":
        col_ano = c

    if cl == "mes":
        col_mes = c

# ============================================
# FILTROS
# ============================================

if col_ano:

    anos = sorted(df[col_ano].dropna().astype(str).unique())

    anos_sel = st.sidebar.multiselect(
        "Ano",
        anos,
        default=anos
    )

    df = df[df[col_ano].astype(str).isin(anos_sel)]

# ============================================
# CRIA MÉTRICAS ANALÍTICAS
# ============================================
# OBS:
# Como os datasets não possuem algumas métricas
# reais de qualidade, estamos criando indicadores
# estimados para análise gerencial.
# ============================================

# quantidade de atendimentos

df["atendimentos"] = 1

# ============================================
# TEMPO ESTIMADO DE ESPERA
# ============================================
# Simulação baseada em volume
# ============================================

if col_unidade:

    volume_unidade = (
        df.groupby(col_unidade)
        .size()
        .reset_index(name="volume")
    )

    # cria tempo estimado
    volume_unidade["tempo_espera_min"] = (
        volume_unidade["volume"] / 50
    ).round(0)

    # médicos estimados
    volume_unidade["medicos"] = (
        volume_unidade["volume"] / 300
    ).round(0)

    volume_unidade["medicos"] = volume_unidade["medicos"].replace(0, 1)

    # pacientes por médico
    volume_unidade["pacientes_por_medico"] = (
        volume_unidade["volume"] /
        volume_unidade["medicos"]
    ).round(0)

    # score de qualidade
    volume_unidade["score_qualidade"] = (
        100
        - volume_unidade["tempo_espera_min"] * 0.4
        - volume_unidade["pacientes_por_medico"] * 0.1
    )

    volume_unidade["score_qualidade"] = (
        volume_unidade["score_qualidade"]
        .clip(lower=0)
        .round(2)
    )

else:

    st.error("Não foi possível identificar a coluna da unidade de saúde")
    st.stop()

# ============================================
# KPIS PRINCIPAIS
# ============================================

st.subheader("📊 Indicadores Gerais")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🏥 Total de Unidades",
    f"{volume_unidade[col_unidade].nunique():,}"
)

col2.metric(
    "👥 Total Atendimentos",
    f"{volume_unidade['volume'].sum():,}"
)

col3.metric(
    "⏱ Tempo Médio Espera",
    f"{volume_unidade['tempo_espera_min'].mean():.0f} min"
)

col4.metric(
    "⭐ Score Médio",
    f"{volume_unidade['score_qualidade'].mean():.1f}"
)

# ============================================
# MELHOR E PIOR UNIDADE
# ============================================

st.subheader("🏆 Ranking de Qualidade")

melhor = volume_unidade.sort_values(
    "score_qualidade",
    ascending=False
).head(1)

pior = volume_unidade.sort_values(
    "score_qualidade",
    ascending=True
).head(1)

colA, colB = st.columns(2)

with colA:

    st.success("🥇 Melhor Unidade")

    st.metric(
        melhor[col_unidade].values[0],
        f"Score: {melhor['score_qualidade'].values[0]:.1f}"
    )

    st.write(f"⏱ Espera média: {melhor['tempo_espera_min'].values[0]:.0f} min")
    st.write(f"👨‍⚕️ Médicos estimados: {melhor['medicos'].values[0]:.0f}")

with colB:

    st.error("🚨 Pior Unidade")

    st.metric(
        pior[col_unidade].values[0],
        f"Score: {pior['score_qualidade'].values[0]:.1f}"
    )

    st.write(f"⏱ Espera média: {pior['tempo_espera_min'].values[0]:.0f} min")
    st.write(f"👨‍⚕️ Médicos estimados: {pior['medicos'].values[0]:.0f}")

# ============================================
# TOP 10 MELHORES UNIDADES
# ============================================

st.subheader("🥇 Top 10 Melhores Unidades")

ranking = volume_unidade.sort_values(
    "score_qualidade",
    ascending=False
).head(10)

fig_rank = px.bar(
    ranking,
    x="score_qualidade",
    y=col_unidade,
    orientation="h",
    title="Melhores Unidades por Score de Qualidade"
)

st.plotly_chart(fig_rank, use_container_width=True)

# ============================================
# PIORES UNIDADES
# ============================================

st.subheader("🚨 Unidades com Pior Atendimento")

piores = volume_unidade.sort_values(
    "score_qualidade"
).head(10)

fig_piores = px.bar(
    piores,
    x="score_qualidade",
    y=col_unidade,
    orientation="h",
    title="Piores Unidades"
)

st.plotly_chart(fig_piores, use_container_width=True)

# ============================================
# TEMPO DE ESPERA
# ============================================

st.subheader("⏱ Tempo Médio de Espera")

fig_espera = px.scatter(
    volume_unidade,
    x="volume",
    y="tempo_espera_min",
    size="medicos",
    hover_data=[col_unidade],
    title="Volume x Tempo de Espera"
)

st.plotly_chart(fig_espera, use_container_width=True)

# ============================================
# PACIENTES POR MÉDICO
# ============================================

st.subheader("👨‍⚕️ Relação Pacientes por Médico")

fig_medico = px.bar(
    volume_unidade.sort_values(
        "pacientes_por_medico",
        ascending=False
    ).head(15),
    x=col_unidade,
    y="pacientes_por_medico",
    title="Pacientes por Médico"
)

st.plotly_chart(fig_medico, use_container_width=True)

# ============================================
# TABELA ANALÍTICA
# ============================================

st.subheader("📋 Tabela Analítica")

st.dataframe(
    volume_unidade.sort_values(
        "score_qualidade",
        ascending=False
    ),
    use_container_width=True
)

# ============================================
# DOWNLOAD CSV
# ============================================

csv = volume_unidade.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Baixar Ranking CSV",
    data=csv,
    file_name="ranking_unidades.csv",
    mime="text/csv"
)

# ============================================
# RODAPÉ
# ============================================

st.markdown("---")

st.markdown("""
### 📌 Observação Técnica

Algumas métricas como:

- tempo de espera
- quantidade de médicos
- pacientes por médico

foram estimadas analiticamente com base no volume de produção,
pois os datasets PAPE/PFPE/STPE normalmente não possuem essas
informações explicitamente.

Para análises reais de qualidade assistencial,
o ideal é integrar:

- CNES
- SISREG
- e-SUS
- tempo real de triagem
- escala médica
""")