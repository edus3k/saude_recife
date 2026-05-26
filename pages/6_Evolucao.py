# ============================================
# EVOLUÇÃO TEMPORAL
# pages/6_📅_Evolucao.py
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
    page_title="Evolução Temporal",
    layout="wide"
)

st.title("📅 Evolução Temporal")

st.markdown("""
Análise temporal dos indicadores assistenciais
das unidades de saúde do Recife.
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

    "CNES " +

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
# CRIAR PERÍODO
# ============================================

dados["periodo"] = (

    dados["ano"]
    .astype(str)

    + "-"

    +

    dados["mes"]
    .astype(str)
    .str.zfill(2)

)

# ============================================
# KPIS
# ============================================

st.markdown("---")

st.subheader("📊 Indicadores Temporais")

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
    "Score Médio",
    f"{dados['score_qualidade'].mean():.2f}"
)

col4.metric(
    "Tempo Espera",
    f"{dados['tempo_espera'].mean():.1f}"
)

# ============================================
# EVOLUÇÃO ATENDIMENTOS
# ============================================

st.markdown("---")

st.subheader("📈 Evolução dos Atendimentos")

st.info("""
Este gráfico apresenta a evolução mensal da quantidade
de atendimentos realizados pelas unidades de saúde.

A análise permite identificar:
- crescimento da demanda assistencial;
- períodos de maior pressão operacional;
- sazonalidade dos atendimentos;
- comportamento histórico da rede de saúde.
""")

evolucao_atendimentos = (

    dados

    .groupby(
        "periodo",
        as_index=False
    )

    .agg({

        "total_atendimentos":
            "sum"

    })

)

fig1 = px.line(

    evolucao_atendimentos,

    x="periodo",

    y="total_atendimentos",

    markers=True,

    template="plotly_white",

    title="Evolução Atendimentos"

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

st.success(f"""
Conclusão resumida:

O período analisado apresentou aproximadamente
{int(evolucao_atendimentos['total_atendimentos'].sum()):,} atendimentos.

A tendência observada permite avaliar o crescimento
da demanda assistencial ao longo do tempo.
""")

# ============================================
# EVOLUÇÃO QUALIDADE
# ============================================

st.markdown("---")

st.subheader("🏥 Evolução Qualidade")

st.info("""
Este gráfico demonstra a evolução do score médio
de qualidade operacional das unidades de saúde.

O indicador auxilia na avaliação:
- da eficiência operacional;
- da estabilidade dos atendimentos;
- do impacto da demanda na qualidade assistencial.
""")

evolucao_qualidade = (

    dados

    .groupby(
        "periodo",
        as_index=False
    )

    .agg({

        "score_qualidade":
            "mean"

    })

)

fig2 = px.line(

    evolucao_qualidade,

    x="periodo",

    y="score_qualidade",

    markers=True,

    template="plotly_white",

    title="Evolução Qualidade"

)

fig2.update_layout(

    height=500,

    title_x=0.5,

    xaxis_title="Período",

    yaxis_title="Score Qualidade"

)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.success(f"""
Conclusão resumida:

O score médio operacional registrado foi de
{round(evolucao_qualidade['score_qualidade'].mean(), 2)} pontos.

Os resultados demonstram o comportamento da qualidade
operacional ao longo do período analisado.
""")

# ============================================
# EVOLUÇÃO ESPERA
# ============================================

st.markdown("---")

st.subheader("⏱️ Evolução Tempo Espera")

st.info("""
Este gráfico apresenta a evolução estimada
do tempo médio de espera assistencial.

A análise permite identificar:
- períodos de maior sobrecarga;
- gargalos operacionais;
- impacto da demanda no atendimento.
""")

evolucao_espera = (

    dados

    .groupby(
        "periodo",
        as_index=False
    )

    .agg({

        "tempo_espera":
            "mean"

    })

)

fig3 = px.line(

    evolucao_espera,

    x="periodo",

    y="tempo_espera",

    markers=True,

    template="plotly_white",

    title="Evolução Tempo Espera"

)

fig3.update_layout(

    height=500,

    title_x=0.5,

    xaxis_title="Período",

    yaxis_title="Tempo Espera"

)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.success(f"""
Conclusão resumida:

O tempo médio estimado de espera foi de
{round(evolucao_espera['tempo_espera'].mean(), 1)} minutos.

O comportamento temporal do indicador auxilia
na identificação de períodos críticos da operação.
""")

# ============================================
# EVOLUÇÃO PROFISSIONAIS
# ============================================

st.markdown("---")

st.subheader("👨‍⚕️ Evolução Profissionais")

st.info("""
Este gráfico apresenta a evolução da quantidade
média de profissionais registrados nas unidades.

O indicador auxilia na análise:
- da capacidade operacional;
- do crescimento das equipes;
- do suporte assistencial disponível.
""")

evolucao_profissionais = (

    dados

    .groupby(
        "periodo",
        as_index=False
    )

    .agg({

        "total_profissionais":
            "mean"

    })

)

fig4 = px.area(

    evolucao_profissionais,

    x="periodo",

    y="total_profissionais",

    template="plotly_white",

    title="Evolução Profissionais"

)

fig4.update_layout(

    height=500,

    title_x=0.5,

    xaxis_title="Período",

    yaxis_title="Profissionais"

)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.success(f"""
Conclusão resumida:

A média registrada foi de
{round(evolucao_profissionais['total_profissionais'].mean(), 2)} profissionais.

A evolução da equipe operacional demonstra
a capacidade assistencial disponível ao longo do período.
""")

# ============================================
# COMPARAÇÃO UNIDADES
# ============================================

st.markdown("---")

st.subheader("📊 Comparação entre Unidades")

st.info("""
Este gráfico compara o comportamento temporal
dos atendimentos entre as unidades de saúde.

A análise permite:
- identificar unidades mais demandadas;
- comparar evolução operacional;
- avaliar pressão assistencial entre unidades.
""")

comparativo = (

    dados

    .groupby([
        "periodo",
        "nome_unidade"
    ], as_index=False)

    .agg({

        "total_atendimentos":
            "sum"

    })

)

fig5 = px.line(

    comparativo,

    x="periodo",

    y="total_atendimentos",

    color="nome_unidade",

    template="plotly_white",

    title="Comparativo Unidades"

)

fig5.update_layout(

    height=700,

    title_x=0.5,

    xaxis_title="Período",

    yaxis_title="Atendimentos"

)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.success("""
Conclusão resumida:

A comparação entre unidades demonstra diferenças
no volume de demanda assistencial ao longo do tempo.

As unidades com linhas mais elevadas apresentam
maior pressão operacional e maior fluxo de atendimentos.
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

media_espera = round(
    dados["tempo_espera"].mean(),
    1
)

total_atend = int(
    dados["total_atendimentos"].sum()
)

st.info(f"""

O período analisado registrou
aproximadamente {total_atend:,} atendimentos.

O score médio operacional foi de
{media_score} pontos.

O tempo médio estimado de espera
foi de {media_espera} minutos.

Os resultados demonstram a evolução
dos indicadores assistenciais da rede
de saúde do Recife ao longo do período analisado.

""")

# ============================================
# FOOTER
# ============================================

st.success(
    "✅ Painel de evolução temporal carregado"
)