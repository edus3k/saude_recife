# ============================================
# EFICIÊNCIA OPERACIONAL
# pages/4_👨‍⚕️_Eficiencia.py
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
    page_title="Eficiência Operacional",
    layout="wide"
)

st.title("👨‍⚕️ Eficiência Operacional")

st.markdown("""
Painel analítico voltado para avaliação da eficiência
operacional das unidades de saúde do Recife.

A análise considera:
- produtividade assistencial
- estrutura profissional
- qualidade operacional
- volume de atendimentos
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
# CALCULAR MÉTRICAS
# ============================================

dados = calcular_metricas(dados)

# ============================================
# SCORE EFICIÊNCIA
# ============================================

dados["atendimento_por_profissional"] = (

    dados["total_atendimentos"]

    /

    dados["total_profissionais"]
    .replace(0, 1)

)

dados["score_eficiencia"] = (

    dados["atendimento_por_profissional"]
    * 0.7

    +

    dados["score_qualidade"]
    * 0.3

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
    "Top Eficiência",
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

st.subheader("📊 Indicadores de Eficiência")

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
    "Atend./Profissional",
    f"{dados['atendimento_por_profissional'].mean():.2f}"
)

col4.metric(
    "Score Eficiência",
    f"{dados['score_eficiencia'].mean():.2f}"
)

# ============================================
# RANKING EFICIÊNCIA
# ============================================

st.markdown("---")

st.subheader("🏆 Ranking de Eficiência")

st.info("""
📌 Este gráfico apresenta as unidades com melhor eficiência operacional.

A análise considera:
- produtividade assistencial
- qualidade operacional
- volume de atendimentos
- desempenho das equipes

Conclusão resumida:
Unidades com maiores scores apresentam melhor equilíbrio
entre produtividade e qualidade assistencial.
""")

ranking = (

    dados

    .groupby(
        "nome_unidade",
        as_index=False
    )

    .agg({

        "score_eficiencia":
            "mean",

        "atendimento_por_profissional":
            "mean",

        "score_qualidade":
            "mean",

        "total_atendimentos":
            "sum"

    })

    .sort_values(
        "score_eficiencia",
        ascending=False
    )

    .head(top_n)

)

fig1 = px.bar(

    ranking,

    x="score_eficiencia",

    y="nome_unidade",

    orientation="h",

    color="atendimento_por_profissional",

    text="score_eficiencia",

    hover_data=[

        "score_qualidade",
        "total_atendimentos"

    ],

    template="plotly_white",

    title="Ranking de Eficiência Operacional"

)

fig1.update_traces(
    texttemplate='%{text:.2f}',
    textposition='outside'
)

fig1.update_layout(

    height=850,

    title_x=0.5,

    xaxis_title="Score Eficiência",

    yaxis_title=""

)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown("""
### 📖 Detalhamento do Gráfico

#### ✅ Indicador analisado
Score médio de eficiência operacional das unidades.

#### ✅ Cálculo utilizado
- Métrica principal: `score_eficiencia`
- Função aplicada: `MEAN()`

#### ✅ O que significa MEAN()
A função `MEAN()` calcula a média dos valores.

Exemplo:
- Unidade A → 70
- Unidade B → 80
- Unidade C → 90

Resultado:
(70 + 80 + 90) ÷ 3 = 80

#### ✅ Como interpretar
- Barras maiores representam melhor eficiência.
- Scores elevados indicam maior produtividade operacional.
- Valores baixos podem indicar sobrecarga.

#### ✅ Ferramentas Python utilizadas
- Pandas
- Plotly Express
- Streamlit
- DuckDB
""")

# ============================================
# PRODUTIVIDADE
# ============================================

st.markdown("---")

st.subheader("👨‍⚕️ Atendimento por Profissional")

st.info("""
📌 O gráfico apresenta a média de atendimentos
realizados por profissional em cada unidade.

Conclusão resumida:
Valores elevados representam maior produtividade,
porém níveis excessivos podem indicar sobrecarga.
""")

produtividade = (

    dados

    .groupby(
        "nome_unidade",
        as_index=False
    )

    .agg({

        "atendimento_por_profissional":
            "mean"

    })

    .sort_values(
        "atendimento_por_profissional",
        ascending=False
    )

    .head(top_n)

)

fig2 = px.bar(

    produtividade,

    x="atendimento_por_profissional",

    y="nome_unidade",

    orientation="h",

    color="atendimento_por_profissional",

    text="atendimento_por_profissional",

    template="plotly_white",

    title="Atendimento por Profissional"

)

fig2.update_traces(
    texttemplate='%{text:.2f}',
    textposition='outside'
)

fig2.update_layout(

    height=850,

    title_x=0.5,

    xaxis_title="Atendimentos por Profissional",

    yaxis_title=""

)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("""
### 📖 Detalhamento do Gráfico

#### ✅ Indicador analisado
Produtividade média assistencial por profissional.

#### ✅ Cálculo utilizado
- Métrica principal: `atendimento_por_profissional`
- Fórmula:
`total_atendimentos / total_profissionais`

#### ✅ Como interpretar
- Barras maiores indicam maior produtividade.
- Valores elevados podem indicar sobrecarga.
- Auxilia na análise da distribuição operacional.

#### ✅ Ferramentas Python utilizadas
- Pandas
- Plotly Express
- Streamlit
- DuckDB
""")

# ============================================
# CORRELAÇÃO
# ============================================

st.markdown("---")

st.subheader("📈 Correlação Operacional")

st.info("""
📌 O gráfico relaciona:
- profissionais
- eficiência operacional
- qualidade assistencial
- volume de atendimentos

Cada bolha representa uma unidade de saúde.
""")

fig3 = px.scatter(

    dados,

    x="total_profissionais",

    y="score_eficiencia",

    size="total_atendimentos",

    color="score_qualidade",

    hover_name="nome_unidade",

    template="plotly_white",

    title="Correlação de Eficiência"

)

fig3.update_layout(

    height=700,

    title_x=0.5,

    xaxis_title="Quantidade de Profissionais",

    yaxis_title="Score Eficiência"

)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.markdown("""
### 📖 Detalhamento do Gráfico

#### ✅ Indicador analisado
Relação entre profissionais e eficiência operacional.

#### ✅ Cálculo utilizado
- Eixo X → `total_profissionais`
- Eixo Y → `score_eficiencia`
- Tamanho → `total_atendimentos`
- Cor → `score_qualidade`

#### ✅ Como interpretar
- Bolhas maiores representam maior demanda.
- Pontos mais altos indicam maior eficiência.
- Cores mais intensas indicam maior score de qualidade.

#### ✅ Ferramentas Python utilizadas
- Pandas
- Plotly Express
- Streamlit
- DuckDB
""")

# ============================================
# EVOLUÇÃO TEMPORAL
# ============================================

st.markdown("---")

st.subheader("📅 Evolução da Eficiência")

st.info("""
📌 O gráfico apresenta a evolução temporal
da eficiência operacional média.

Conclusão resumida:
Permite identificar crescimento ou redução
da eficiência ao longo do tempo.
""")

evolucao = (

    dados

    .groupby([
        "ano",
        "mes"
    ], as_index=False)

    .agg({

        "score_eficiencia":
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

fig4 = px.line(

    evolucao,

    x="periodo",

    y="score_eficiencia",

    markers=True,

    template="plotly_white",

    title="Evolução Temporal da Eficiência"

)

fig4.update_layout(

    height=500,

    title_x=0.5,

    xaxis_title="Período",

    yaxis_title="Score Eficiência"

)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.markdown("""
### 📖 Detalhamento do Gráfico

#### ✅ Indicador analisado
Evolução média da eficiência operacional.

#### ✅ Cálculo utilizado
- Métrica principal: `score_eficiencia`
- Função aplicada: `MEAN()`
- Agrupamento: Ano e Mês

#### ✅ Como interpretar
- Crescimento da linha indica melhora operacional.
- Queda da linha pode indicar aumento de pressão assistencial.
- Auxilia no acompanhamento temporal dos indicadores.

#### ✅ Ferramentas Python utilizadas
- Pandas
- Plotly Express
- Streamlit
- DuckDB
""")

# ============================================
# GLOSSÁRIO SQL E PANDAS
# ============================================

st.markdown("---")

# ============================================
# RESUMO EXECUTIVO
# ============================================

st.markdown("---")

st.subheader("📝 Resumo Executivo")

score_medio = round(
    dados["score_eficiencia"].mean(),
    2
)

prod_media = round(
    dados["atendimento_por_profissional"].mean(),
    2
)

melhor_unidade = ranking.iloc[0]["nome_unidade"]

st.info(f"""

O score médio de eficiência operacional
foi de {score_medio} pontos.

A produtividade média registrada foi de
{prod_media} atendimentos por profissional.

A unidade com melhor desempenho operacional
foi {melhor_unidade}.

Os resultados demonstram a relação entre:
- capacidade operacional
- produtividade
- qualidade assistencial
- eficiência das equipes

""")

# ============================================
# FOOTER
# ============================================

st.success(
    "✅ Painel de eficiência operacional carregado"
)