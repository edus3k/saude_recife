# ============================================
# RANKING DAS UNIDADES
# pages/2_🏆_Ranking.py
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
    page_title="Ranking das Unidades",
    layout="wide"
)

st.title("🏆 Ranking das Unidades")

st.markdown("""
Painel analítico para comparação de desempenho
entre as unidades de saúde do Recife.

O objetivo desta página é identificar:
- unidades mais eficientes
- unidades mais demandadas
- capacidade estrutural
- distribuição de profissionais
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
# SIDEBAR
# ============================================

st.sidebar.header("🎛️ Filtros Ranking")

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
    "Top Ranking",
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

st.subheader("📊 Indicadores Gerais")

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
    "Médicos",
    f"{dados['total_medicos'].sum():,.0f}"
)

col4.metric(
    "Leitos",
    f"{dados['qtd_leitos'].sum():,.0f}"
)

# ============================================
# RANKING QUALIDADE
# ============================================

st.markdown("---")

st.subheader("🏥 Ranking de Qualidade")

st.info("""
📌 O gráfico apresenta as unidades com melhor desempenho operacional.

A análise considera:
- score de qualidade
- estrutura hospitalar
- pressão assistencial
- relação entre demanda e profissionais

Conclusão resumida:
Unidades com scores maiores apresentam melhor equilíbrio operacional
e menor risco de sobrecarga assistencial.
""")

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

fig1 = px.bar(

    ranking,

    x="score_qualidade",

    y="nome_unidade",

    orientation="h",

    color="score_qualidade",

    text="score_qualidade",

    hover_data=[

        "total_atendimentos",
        "total_profissionais",
        "qtd_leitos"

    ],

    template="plotly_white",

    title="Ranking Geral de Qualidade"

)

fig1.update_traces(
    texttemplate='%{text:.2f}',
    textposition='outside'
)

fig1.update_layout(

    height=850,

    title_x=0.5,

    xaxis_title="Score Qualidade",

    yaxis_title=""

)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown("""
### 📖 Detalhamento do Gráfico

#### ✅ Indicador analisado
Score médio de qualidade operacional das unidades de saúde.

#### ✅ Cálculo utilizado
- Métrica principal: `score_qualidade`
- Função aplicada: `MEAN()` → Calcula a média dos valores.

Exemplo:
- Unidade A → 70
- Unidade B → 80
- Unidade C → 90

Resultado:
(70 + 80 + 90) ÷ 3 = 80

#### ✅ Como interpretar
- Barras maiores representam melhor desempenho.
- Scores elevados indicam maior eficiência operacional.
- Scores baixos podem indicar sobrecarga.

#### ✅ Ferramentas utilizadas
- Pandas
- Plotly Express
- Streamlit
- DuckDB
""")

# ============================================
# RANKING DEMANDA
# ============================================

st.markdown("---")

st.subheader("📈 Ranking por Demanda")

st.info("""
📌 O gráfico apresenta as unidades com maior volume de atendimentos.

Conclusão resumida:
Unidades mais demandadas podem apresentar maior pressão operacional,
necessitando maior suporte estrutural e profissional.
""")

ranking_demanda = (

    dados

    .groupby(
        "nome_unidade",
        as_index=False
    )

    .agg({

        "total_atendimentos":
            "sum"

    })

    .sort_values(
        "total_atendimentos",
        ascending=False
    )

    .head(top_n)

)

fig2 = px.bar(

    ranking_demanda,

    x="total_atendimentos",

    y="nome_unidade",

    orientation="h",

    color="total_atendimentos",

    text="total_atendimentos",

    template="plotly_white",

    title="Ranking de Atendimentos"

)

fig2.update_traces(
    texttemplate='%{text:.0f}',
    textposition='outside'
)

fig2.update_layout(

    height=850,

    title_x=0.5,

    xaxis_title="Atendimentos",

    yaxis_title=""

)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("""
### 📖 Detalhamento do Gráfico

#### ✅ Indicador analisado
Quantidade total de atendimentos realizados.

#### ✅ Cálculo utilizado
- Métrica principal: `total_atendimentos`
- Função aplicada: `SUM()` → Realiza a soma total dos valores.

Exemplo:
- Janeiro → 100
- Fevereiro → 150
- Março → 200

Resultado:
100 + 150 + 200 = 450

#### ✅ Como interpretar
- Barras maiores representam maior demanda assistencial.
- Valores elevados indicam maior utilização da unidade.
- Altos volumes podem indicar pressão operacional.

#### ✅ Ferramentas utilizadas
- Pandas
- Plotly Express
- Streamlit
- DuckDB
""")

# ============================================
# RANKING LEITOS
# ============================================

st.markdown("---")

st.subheader("🛏️ Ranking Estrutural")

st.info("""
📌 O gráfico apresenta a capacidade estrutural das unidades.

Conclusão resumida:
Unidades com maior quantidade de leitos possuem maior suporte
hospitalar e capacidade operacional.
""")

ranking_leitos = (

    dados

    .groupby(
        "nome_unidade",
        as_index=False
    )

    .agg({

        "qtd_leitos":
            "mean"

    })

    .sort_values(
        "qtd_leitos",
        ascending=False
    )

    .head(top_n)

)

fig3 = px.bar(

    ranking_leitos,

    x="qtd_leitos",

    y="nome_unidade",

    orientation="h",

    color="qtd_leitos",

    text="qtd_leitos",

    template="plotly_white",

    title="Ranking de Leitos"

)

fig3.update_traces(
    texttemplate='%{text:.0f}',
    textposition='outside'
)

fig3.update_layout(

    height=850,

    title_x=0.5,

    xaxis_title="Quantidade de Leitos",

    yaxis_title=""

)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.markdown("""
### 📖 Detalhamento do Gráfico

#### ✅ Indicador analisado
Capacidade estrutural baseada em leitos.

#### ✅ Cálculo utilizado
- Métrica principal: `qtd_leitos`
- Função aplicada: `MEAN()` → Calcula a média dos valores.

Exemplo:
(50 + 60 + 70) ÷ 3 = 60

#### ✅ Como interpretar
- Barras maiores indicam maior capacidade hospitalar.
- Menor quantidade pode indicar limitação estrutural.
- Unidades maiores tendem a suportar maior demanda.

#### ✅ Ferramentas utilizadas
- Pandas
- Plotly Express
- Streamlit
- DuckDB
""")

# ============================================
# RANKING MÉDICOS
# ============================================

st.markdown("---")

st.subheader("👨‍⚕️ Ranking Profissional")

st.info("""
📌 O gráfico apresenta a distribuição médica nas unidades.

Conclusão resumida:
Unidades com maior quantidade de médicos tendem a apresentar
melhor capacidade assistencial e menor risco de sobrecarga.
""")

ranking_medicos = (

    dados

    .groupby(
        "nome_unidade",
        as_index=False
    )

    .agg({

        "total_medicos":
            "mean"

    })

    .sort_values(
        "total_medicos",
        ascending=False
    )

    .head(top_n)

)

fig4 = px.bar(

    ranking_medicos,

    x="total_medicos",

    y="nome_unidade",

    orientation="h",

    color="total_medicos",

    text="total_medicos",

    template="plotly_white",

    title="Ranking de Médicos"

)

fig4.update_traces(
    texttemplate='%{text:.0f}',
    textposition='outside'
)

fig4.update_layout(

    height=850,

    title_x=0.5,

    xaxis_title="Quantidade de Médicos",

    yaxis_title=""

)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.markdown("""
### 📖 Detalhamento do Gráfico

#### ✅ Indicador analisado
Quantidade média de médicos registrados.

#### ✅ Cálculo utilizado
- Métrica principal: `total_medicos`
- Função aplicada: `COUNT()` → Conta quantos registros existem.

Exemplo:
- 10 médicos cadastrados
- Resultado → COUNT() = 10

#### ✅ Como interpretar
- Barras maiores representam maior disponibilidade médica.
- Quantidades menores podem indicar sobrecarga.
- Baixo número de médicos pode impactar o tempo de espera.

#### ✅ Ferramentas utilizadas
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

melhor_unidade = ranking.iloc[0]["nome_unidade"]

melhor_score = round(
    ranking.iloc[0]["score_qualidade"],
    2
)

maior_demanda = ranking_demanda.iloc[0]["nome_unidade"]

total_atend = int(
    dados["total_atendimentos"].sum()
)

st.info(f"""

A unidade com maior score operacional foi
{melhor_unidade},
com score médio de {melhor_score} pontos.

A unidade com maior demanda assistencial foi
{maior_demanda}.

O período analisado registrou
aproximadamente {total_atend:,} atendimentos.

A análise permite identificar possíveis
situações de sobrecarga, eficiência operacional
e capacidade estrutural das unidades.

""")

# ============================================
# FOOTER
# ============================================

st.success(
    "✅ Ranking carregado com sucesso"
)