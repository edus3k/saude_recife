# ============================================
# VISÃO GERAL
# pages/1_📊_Visao_Geral.py
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
    page_title="Visão Geral",
    layout="wide"
)

st.title("📊 Visão Geral da Saúde Recife")

st.markdown("""
Painel executivo com visão consolidada dos indicadores
assistenciais das unidades de saúde.

O objetivo desta análise é:
- acompanhar a demanda assistencial
- analisar a estrutura operacional
- avaliar eficiência das unidades
- identificar possíveis sobrecargas
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
# SIDEBAR FILTROS
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

st.subheader("📌 Indicadores Gerais")

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
# ATENDIMENTOS POR MÊS
# ============================================

st.markdown("---")

st.subheader("📅 Evolução dos Atendimentos")

st.info("""
📌 Este gráfico representa a evolução mensal do volume de atendimentos realizados.

Conclusão resumida:
O crescimento da linha representa aumento da demanda assistencial,
permitindo identificar períodos de maior pressão operacional nas unidades.
""")

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

    +

    "-"

    +

    evolucao["mes"]
    .astype(str)
    .str.zfill(2)

)

fig1 = px.line(

    evolucao,

    x="periodo",

    y="total_atendimentos",

    markers=True,

    template="plotly_white",

    title="Evolução Temporal"

)

fig1.update_layout(
    height=500,
    title_x=0.5,
    xaxis_title="Período",
    yaxis_title="Atendimentos"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown("""
### 📖 Detalhamento do Gráfico

#### ✅ Indicador analisado
Volume total de atendimentos realizados pelas unidades de saúde ao longo do tempo.

#### ✅ Cálculo utilizado
- Métrica principal: `total_atendimentos`
- Função aplicada: `SUM()` → Realiza a soma total dos valores.

Exemplo:
- Janeiro → 100 atendimentos
- Fevereiro → 150 atendimentos
- Março → 200 atendimentos

Resultado:
100 + 150 + 200 = 450 atendimentos

#### ✅ Como interpretar
- Crescimento da linha → aumento da demanda assistencial.
- Queda da linha → redução de atendimentos.
- Picos podem indicar sazonalidade ou maior procura.

#### ✅ Ferramentas Python utilizadas
- Pandas
- Plotly Express
- Streamlit
- DuckDB
""")

# ============================================
# DISTRIBUIÇÃO DE PROFISSIONAIS
# ============================================

st.markdown("---")

st.subheader("👨‍⚕️ Distribuição de Profissionais")

st.info("""
📌 O gráfico representa a quantidade média de profissionais por unidade.

Conclusão resumida:
Unidades com maior número de profissionais possuem maior capacidade
operacional para atender a demanda assistencial.
""")

profissionais = (

    dados

    .groupby(
        "nome_unidade",
        as_index=False
    )

    .agg({

        "total_profissionais":
            "mean"

    })

    .sort_values(
        "total_profissionais",
        ascending=False
    )

)

fig2 = px.bar(

    profissionais,

    x="total_profissionais",

    y="nome_unidade",

    orientation="h",

    color="total_profissionais",

    template="plotly_white",

    title="Profissionais por Unidade"

)

fig2.update_layout(
    height=900,
    title_x=0.5,
    xaxis_title="Profissionais",
    yaxis_title=""
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("""
### 📖 Detalhamento do Gráfico

#### ✅ Indicador analisado
Quantidade média de profissionais disponíveis por unidade.

#### ✅ Cálculo utilizado
- Métrica principal: `total_profissionais`
- Função aplicada: `MEAN()` → Calcula a média dos valores.

Exemplo:
(20 + 30 + 40) ÷ 3 = 30 profissionais

#### ✅ Como interpretar
- Barras maiores indicam maior capacidade operacional.
- Barras menores podem indicar maior risco de sobrecarga.

#### ✅ Ferramentas Python utilizadas
- Pandas
- Plotly Express
- Streamlit
- DuckDB
""")

# ============================================
# QUALIDADE X DEMANDA
# ============================================

st.markdown("---")

st.subheader("📈 Qualidade x Demanda")

st.info("""
📌 O gráfico representa a relação entre demanda assistencial
e qualidade operacional das unidades.

Conclusão resumida:
Unidades com alta demanda e baixo score podem apresentar
maior risco de sobrecarga operacional.
""")

fig3 = px.scatter(

    dados,

    x="total_atendimentos",

    y="score_qualidade",

    size="qtd_leitos",

    color="tempo_espera",

    hover_name="nome_unidade",

    template="plotly_white",

    title="Qualidade x Demanda"

)

fig3.update_layout(
    height=700,
    title_x=0.5,
    xaxis_title="Atendimentos",
    yaxis_title="Score Qualidade"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.markdown("""
### 📖 Detalhamento do Gráfico

#### ✅ Indicador analisado
Relação entre demanda assistencial e desempenho operacional.

#### ✅ Cálculo utilizado
- Eixo X → `total_atendimentos`
- Eixo Y → `score_qualidade`
- Tamanho do ponto → `qtd_leitos`
- Cor → `tempo_espera`

#### ✅ Como interpretar
- Pontos mais altos → melhor qualidade operacional.
- Pontos à direita → maior demanda.
- Pontos maiores → maior estrutura hospitalar.
- Cores intensas → maior tempo de espera.

#### ✅ Ferramentas Python utilizadas
- Pandas
- Plotly Express
- Streamlit
- DuckDB
""")

# ============================================
# RESUMO EXECUTIVO
# ============================================

st.markdown("---")

st.subheader("📝 Resumo Executivo")

media_score = round(
    dados["score_qualidade"].mean(),
    2
)

total_atend = int(
    dados["total_atendimentos"].sum()
)

total_prof = int(
    dados["total_profissionais"].sum()
)

st.info(f"""

O sistema registrou aproximadamente
{total_atend:,} atendimentos.

Foram contabilizados
{total_prof:,} profissionais
nas unidades avaliadas.

O score médio operacional
foi de {media_score} pontos.

A análise demonstra a importância do monitoramento
dos indicadores assistenciais para apoio à gestão
e tomada de decisão estratégica.

""")

# ============================================
# GLOSSÁRIO SQL E PANDAS
# ============================================

st.markdown("---")

# ============================================
# FOOTER
# ============================================

st.success(
    "✅ Visão geral carregada com sucesso"
)