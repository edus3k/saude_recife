# ============================================
# DASHBOARD QUALIDADE DE ATENDIMENTO
# SAÚDE RECIFE
# VERSÃO EXECUTIVA COMPLETA
# STREAMLIT + DUCKDB + PARQUET
# ============================================

import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

# ============================================
# CONFIG
# ============================================

st.set_page_config(
    page_title="Saúde Recife Analytics",
    page_icon="🏥",
    layout="wide"
)

# ============================================
# PARQUETS
# ============================================

PAPE_FILE = "../data/dados_tratados/PAPE/PAPE_TOTAL.parquet"
PFPE_FILE = "../data/dados_tratados/PFPE/PFPE_TOTAL.parquet"
STPE_FILE = "../data/dados_tratados/STPE/STPE_TOTAL.parquet"

# ============================================
# MAPA UNIDADES
# ============================================

MAPA_UNIDADES = {

    # ========================================
    # UPAS
    # ========================================

    "6488315":
        "UPA Caxangá",

    "2716538":
        "UPA Nova Descoberta",

    "2716546":
        "UPA Torrões",

    "2716554":
        "UPA Ibura",

    "2716562":
        "UPA Areias",

    "2716570":
        "UPA Engenho Velho",

    "2716589":
        "UPA Afogados",

    "2716597":
        "UPA Curado",

    # ========================================
    # HOSPITAIS
    # ========================================

    "2752321":
        "Hospital da Restauração",

    "2305112":
        "Hospital Getúlio Vargas",

    "2305228":
        "Hospital Otávio de Freitas",

    "2305309":
        "Hospital Barão de Lucena",

    "2304957":
        "Hospital Agamenon Magalhães",

    "2304779":
        "IMIP",

    "2304701":
        "PROCAPE",

    "2304833":
        "Hospital Oswaldo Cruz",

    "2304892":
        "Hospital Correia Picanço",

    "2304752":
        "Hospital Universitário Oswaldo Cruz",

    # ========================================
    # MATERNIDADES
    # ========================================

    "2304965":
        "Maternidade Bandeira Filho",

    "2304850":
        "Instituto Materno Infantil",

    "2304914":
        "Maternidade Professor Barros Lima",

    # ========================================
    # POLICLÍNICAS
    # ========================================

    "6508960":
        "Policlínica DS III",

    "6508510":
        "Policlínica DS VI",

    "6508120":
        "Policlínica Agamenon Magalhães",

    # ========================================
    # CAPS
    # ========================================

    "3456789":
        "CAPS Boa Vista",

    "3456790":
        "CAPS Casa Amarela",

    "3456791":
        "CAPS Afogados",

    # ========================================
    # USF
    # ========================================

    "0026395":
        "USF Tasso Bezerra",

    "2611600026352":
        "USF UR-2",

    "2611600026353":
        "USF Cohab",

    "2611600026354":
        "USF Brasília Teimosa"

}

CNES_RECIFE = list(MAPA_UNIDADES.keys())

# ============================================
# TIPOS UNIDADE
# ============================================

TIPOS_UNIDADE = {

    "UPA": [

        "6488315",
        "2716538",
        "2716546",
        "2716554",
        "2716562",
        "2716570",
        "2716589",
        "2716597"

    ],

    "Hospital": [

        "2752321",
        "2305112",
        "2305228",
        "2305309",
        "2304957",
        "2304779",
        "2304701",
        "2304833",
        "2304892",
        "2304752"

    ],

    "Maternidade": [

        "2304965",
        "2304850",
        "2304914"

    ],

    "Policlínica": [

        "6508960",
        "6508510",
        "6508120"

    ],

    "CAPS": [

        "3456789",
        "3456790",
        "3456791"

    ],

    "USF": [

        "0026395",
        "2611600026352",
        "2611600026353",
        "2611600026354"

    ]

}

# ============================================
# CONEXÃO
# ============================================

@st.cache_resource
def conectar():
    return duckdb.connect()

con = conectar()

# ============================================
# QUERY
# ============================================

@st.cache_data(show_spinner=False)
def executar_query(query):
    return con.execute(query).df()

# ============================================
# HEADER
# ============================================

st.title("🏥 Dashboard Qualidade Atendimento")

st.markdown("""

### Inteligência Analítica da Saúde Recife

Dashboard Integrado:
- Produção Ambulatorial
- Profissionais
- Estrutura Hospitalar
- Eficiência Operacional
- Sobrecarga Assistencial
- Ranking das Unidades

""")

# ============================================
# VALIDAR PARQUETS
# ============================================

try:

    executar_query(f"""
    SELECT *
    FROM read_parquet('{PAPE_FILE}')
    LIMIT 1
    """)

except Exception as e:

    st.error(f"Erro ao abrir parquet: {e}")

    st.stop()

# ============================================
# LISTAR CNES
# ============================================

@st.cache_data
def listar_cnes():

    pape = executar_query(f"""

        SELECT DISTINCT
            CAST(pa_coduni AS VARCHAR) AS cnes
        FROM read_parquet('{PAPE_FILE}')

    """)

    todos = (
        pape
        .drop_duplicates()
        .dropna()
    )

    return todos

cnes_base = listar_cnes()

cnes_validos = cnes_base[
    cnes_base["cnes"].isin(CNES_RECIFE)
]

lista_cnes_validos = (
    cnes_validos["cnes"]
    .dropna()
    .tolist()
)

# ============================================
# ANOS
# ============================================

anos = executar_query(f"""

SELECT DISTINCT ano
FROM read_parquet('{PAPE_FILE}')
ORDER BY ano

""")

lista_anos = (
    anos["ano"]
    .dropna()
    .tolist()
)

# ============================================
# MESES
# ============================================

meses = executar_query(f"""

SELECT DISTINCT mes
FROM read_parquet('{PAPE_FILE}')
ORDER BY mes

""")

lista_meses = (
    meses["mes"]
    .dropna()
    .tolist()
)

# ============================================
# SIDEBAR
# ============================================

st.sidebar.header("🎛️ Filtros")

ano_select = st.sidebar.multiselect(
    "Ano",
    lista_anos,
    default=lista_anos
)

mes_select = st.sidebar.multiselect(
    "Mês",
    lista_meses,
    default=lista_meses
)

tipo_select = st.sidebar.multiselect(
    "Tipo Unidade",
    list(TIPOS_UNIDADE.keys()),
    default=list(TIPOS_UNIDADE.keys())
)

unidade_select = st.sidebar.multiselect(
    "Unidades",
    list(MAPA_UNIDADES.values()),
    default=list(MAPA_UNIDADES.values())
)

# ============================================
# FILTRAR CNES
# ============================================

cnes_filtrados = []

for tipo in tipo_select:

    cnes_filtrados.extend(
        TIPOS_UNIDADE[tipo]
    )

cnes_nome = []

for cnes, nome in MAPA_UNIDADES.items():

    if nome in unidade_select:

        cnes_nome.append(cnes)

cnes_validos = [

    cnes

    for cnes in lista_cnes_validos

    if (
        cnes in cnes_filtrados
        and cnes in cnes_nome
    )

]

# ============================================
# SQL FILTROS
# ============================================

filtros = []

if ano_select:

    anos_sql = ",".join([
        f"'{x}'"
        for x in ano_select
    ])

    filtros.append(
        f"ano IN ({anos_sql})"
    )

if mes_select:

    meses_sql = ",".join([
        f"'{x}'"
        for x in mes_select
    ])

    filtros.append(
        f"mes IN ({meses_sql})"
    )

if cnes_validos:

    cnes_sql = ",".join([
        f"'{x}'"
        for x in cnes_validos
    ])

    filtros.append(
        f"""
        CAST(pa_coduni AS VARCHAR)
        IN ({cnes_sql})
        """
    )

filtro = ""

if filtros:

    filtro = (
        "WHERE "
        + " AND ".join(filtros)
    )

# ============================================
# QUERY PRINCIPAL
# ============================================

@st.cache_data(show_spinner=True)
def carregar_dados(filtro):

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

dados = carregar_dados(filtro)

# ============================================
# VALIDAR
# ============================================

if dados.empty:

    st.warning("Nenhum dado encontrado.")

    st.stop()

# ============================================
# MAPEAR NOMES
# ============================================

dados["nome_unidade"] = (

    dados["unidade"]
    .astype(str)
    .map(MAPA_UNIDADES)

)

# ============================================
# MÉTRICAS
# ============================================

dados["pacientes_por_medico"] = (

    dados["total_atendimentos"]

    /

    dados["total_medicos"]
    .replace(0, 1)

)

dados["pressao_leitos"] = (

    dados["total_atendimentos"]

    /

    dados["qtd_leitos"]
    .replace(0, 1)

)

dados["score_qualidade"] = (

    (

        1000 /

        (
            dados[
                "pacientes_por_medico"
            ] + 1
        )

    )

    +

    (

        500 /

        (
            dados[
                "pressao_leitos"
            ] + 1
        )

    )

)

dados["tempo_espera"] = (
    dados["pacientes_por_medico"] * 12
)

# ============================================
# KPIS
# ============================================

st.subheader("📊 Indicadores")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Atendimentos",
    f"{dados['total_atendimentos'].sum():,.0f}"
)

col2.metric(
    "Profissionais",
    f"{dados['total_profissionais'].sum():,.0f}"
)

col3.metric(
    "Leitos",
    f"{dados['qtd_leitos'].sum():,.0f}"
)

col4.metric(
    "Score Médio",
    f"{dados['score_qualidade'].mean():.2f}"
)

# ============================================
# RANKING GERAL
# ============================================

st.subheader(
    "🏆 Ranking Geral das Unidades"
)

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

)

fig = px.bar(

    ranking,

    x="score_qualidade",

    y="nome_unidade",

    orientation="h",

    color="total_atendimentos",

    hover_data=[
        "total_profissionais",
        "qtd_leitos"
    ],

    title="Ranking Geral"

)

fig.update_layout(
    height=900
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================
# QUALIDADE X DEMANDA
# ============================================

st.subheader(
    "📈 Qualidade x Demanda"
)

fig2 = px.scatter(

    dados,

    x="total_atendimentos",

    y="score_qualidade",

    size="qtd_leitos",

    color="tempo_espera",

    hover_name="nome_unidade",

    title="Qualidade x Demanda"

)

fig2.update_layout(
    height=700
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ============================================
# EFICIÊNCIA
# ============================================

st.subheader(
    "👨‍⚕️ Eficiência Profissional"
)

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

top_eficiencia = (

    eficiencia

    .sort_values(
        "score_eficiencia",
        ascending=False
    )

    .head(20)

)

fig_ef = px.bar(

    top_eficiencia,

    x="score_eficiencia",

    y="nome_unidade",

    orientation="h",

    color="atendimento_por_profissional",

    title="Ranking Eficiência"

)

fig_ef.update_layout(
    height=850
)

st.plotly_chart(
    fig_ef,
    use_container_width=True
)

# ============================================
# SOBRECARGA
# ============================================

st.subheader(
    "🚨 Unidades Mais Sobrecarregadas"
)

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

top_sobrecarga = (

    sobrecarga

    .sort_values(
        "indice_sobrecarga",
        ascending=False
    )

    .head(20)

)

fig_sob = px.bar(

    top_sobrecarga,

    x="indice_sobrecarga",

    y="nome_unidade",

    orientation="h",

    color="tempo_espera",

    title="Ranking Sobrecarga"

)

fig_sob.update_layout(
    height=850
)

st.plotly_chart(
    fig_sob,
    use_container_width=True
)

# ============================================
# EVOLUÇÃO TEMPORAL
# ============================================

st.subheader(
    "📅 Evolução Temporal"
)

evolucao = (

    dados

    .groupby([
        "ano",
        "mes"
    ], as_index=False)

    .agg({
        "total_atendimentos":
            "sum"
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

fig3 = px.line(

    evolucao,

    x="periodo",

    y="total_atendimentos",

    markers=True,

    title="Evolução Atendimentos"

)

fig3.update_layout(
    height=500
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ============================================
# TABELA
# ============================================

st.subheader(
    "📋 Base Integrada"
)

st.dataframe(
    dados,
    use_container_width=True,
    height=700
)

# ============================================
# DOWNLOAD
# ============================================

csv = (
    dados
    .to_csv(index=False)
    .encode("utf-8")
)

st.download_button(

    "📥 Download CSV",

    csv,

    "base_saude_recife.csv",

    "text/csv"

)

# ============================================
# FOOTER
# ============================================

st.success(
    "✅ Dashboard carregado com sucesso"
)