# ============================================
# QUALIDADE X DEMANDA
# pages/3_📈_Qualidade_Demanda.py
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
    page_title="Qualidade x Demanda",
    layout="wide"
)

st.title("📈 Qualidade x Demanda")

st.markdown("""
Análise da relação entre:
- volume de atendimentos
- qualidade operacional
- pressão assistencial
- tempo estimado de espera
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
# KPIS
# ============================================

st.markdown("---")

st.subheader("📊 Indicadores Analíticos")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Atendimentos",
    f"{dados['total_atendimentos'].sum():,.0f}"
)

col2.metric(
    "Tempo Médio Espera",
    f"{dados['tempo_espera'].mean():.1f}"
)

col3.metric(
    "Pacientes/Médico",
    f"{dados['pacientes_por_medico'].mean():.2f}"
)

col4.metric(
    "Score Médio",
    f"{dados['score_qualidade'].mean():.2f}"
)

# ============================================
# QUALIDADE X DEMANDA
# ============================================

st.markdown("---")

st.subheader("📈 Correlação Qualidade x Demanda")

st.caption("""
Cada bolha representa uma unidade de saúde.

- Eixo X:
Quantidade total de atendimentos

- Eixo Y:
Score de qualidade operacional

- Tamanho:
Quantidade de leitos

- Cor:
Tempo médio estimado de espera
""")

fig1 = px.scatter(

    dados,

    x="total_atendimentos",

    y="score_qualidade",

    size="qtd_leitos",

    color="tempo_espera",

    hover_name="nome_unidade",

    hover_data=[

        "total_profissionais",
        "total_medicos",
        "pacientes_por_medico"

    ],

    template="plotly_white",

    title="Qualidade x Demanda"

)

fig1.update_layout(

    height=750,

    title_x=0.5,

    xaxis_title="Total de Atendimentos",

    yaxis_title="Score Qualidade"

)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown("""
### 📖 Detalhamento do Gráfico

#### ✅ Indicador analisado
Relação entre demanda assistencial e qualidade operacional das unidades de saúde.

#### ✅ Cálculo utilizado
- Eixo X: `total_atendimentos`
- Eixo Y: `score_qualidade`
- Tamanho da bolha: `qtd_leitos`
- Cor da bolha: `tempo_espera`

#### ✅ Como interpretar
- Bolhas mais altas representam melhor qualidade operacional.
- Bolhas mais à direita indicam maior volume de atendimentos.
- Bolhas maiores possuem maior capacidade estrutural.
- Cores mais intensas representam maior tempo médio de espera.

#### ✅ Conclusão resumida
O gráfico demonstra a relação entre o volume de atendimentos e a qualidade operacional das unidades.

Foi possível identificar unidades com alta demanda e bom desempenho operacional, enquanto outras apresentaram maior pressão assistencial e aumento no tempo estimado de espera.

A análise auxilia na identificação de possíveis gargalos operacionais e na necessidade de redistribuição de recursos.

#### ✅ Ferramentas Python utilizadas
- `Pandas`
- `Plotly Express`
- `Streamlit`
- `DuckDB`
""")

# ============================================
# TEMPO ESPERA
# ============================================

st.markdown("---")

st.subheader("⏱️ Tempo Médio de Espera")

st.caption("""
Estimativa do tempo médio de espera
baseada na pressão assistencial.
""")

tempo_espera = (

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

)

fig2 = px.bar(

    tempo_espera,

    x="tempo_espera",

    y="nome_unidade",

    orientation="h",

    color="tempo_espera",

    text="tempo_espera",

    template="plotly_white",

    title="Tempo Médio de Espera"

)

fig2.update_traces(
    texttemplate='%{text:.1f}',
    textposition='outside'
)

fig2.update_layout(

    height=900,

    title_x=0.5,

    xaxis_title="Tempo Espera",

    yaxis_title=""

)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("""
### 📖 Detalhamento do Gráfico

#### ✅ Indicador analisado
Tempo médio estimado de espera nas unidades de saúde.

#### ✅ Cálculo utilizado
- Métrica principal: `tempo_espera`
- Função aplicada: `MEAN()`
- Agrupamento: Unidade de Saúde

#### ✅ Como interpretar
- Barras maiores indicam maior tempo de espera.
- Valores elevados podem indicar sobrecarga operacional.
- Auxilia na análise de eficiência do atendimento.

#### ✅ Conclusão resumida
As unidades com maiores tempos de espera tendem a apresentar maior sobrecarga assistencial e pressão operacional.

O indicador evidencia possíveis dificuldades relacionadas à capacidade de atendimento e disponibilidade profissional.

#### ✅ Ferramentas Python utilizadas
- `Pandas`
- `Plotly Express`
- `Streamlit`
- `DuckDB`
""")

# ============================================
# PRESSÃO LEITOS
# ============================================

st.markdown("---")

st.subheader("🛏️ Pressão sobre Leitos")

st.caption("""
Mede a pressão operacional sobre
a estrutura hospitalar disponível.
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

)

fig3 = px.bar(

    pressao,

    x="pressao_leitos",

    y="nome_unidade",

    orientation="h",

    color="pressao_leitos",

    text="pressao_leitos",

    template="plotly_white",

    title="Pressão Assistencial"

)

fig3.update_traces(
    texttemplate='%{text:.2f}',
    textposition='outside'
)

fig3.update_layout(

    height=900,

    title_x=0.5,

    xaxis_title="Pressão Leitos",

    yaxis_title=""

)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.markdown("""
### 📖 Detalhamento do Gráfico

#### ✅ Indicador analisado
Nível de pressão operacional sobre os leitos disponíveis.

#### ✅ Cálculo utilizado
- Métrica principal: `pressao_leitos`
- Função aplicada: `MEAN()`
- Agrupamento: Unidade de Saúde

#### ✅ Como interpretar
- Barras maiores indicam maior ocupação e pressão assistencial.
- Valores elevados podem representar risco de superlotação.
- Auxilia no planejamento estrutural hospitalar.

#### ✅ Conclusão resumida
O gráfico evidencia quais unidades apresentam maior utilização da estrutura hospitalar disponível.

Valores elevados podem indicar risco de superlotação e necessidade de ampliação da capacidade assistencial.

#### ✅ Ferramentas Python utilizadas
- `Pandas`
- `Plotly Express`
- `Streamlit`
- `DuckDB`
""")

# ============================================
# PACIENTES POR MÉDICO
# ============================================

st.markdown("---")

st.subheader("👨‍⚕️ Pacientes por Médico")

st.caption("""
Indicador de carga assistencial médica.
""")

ppm = (

    dados

    .groupby(
        "nome_unidade",
        as_index=False
    )

    .agg({

        "pacientes_por_medico":
            "mean"

    })

    .sort_values(
        "pacientes_por_medico",
        ascending=False
    )

)

fig4 = px.bar(

    ppm,

    x="pacientes_por_medico",

    y="nome_unidade",

    orientation="h",

    color="pacientes_por_medico",

    text="pacientes_por_medico",

    template="plotly_white",

    title="Pacientes por Médico"

)

fig4.update_traces(
    texttemplate='%{text:.2f}',
    textposition='outside'
)

fig4.update_layout(

    height=900,

    title_x=0.5,

    xaxis_title="Pacientes/Médico",

    yaxis_title=""

)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.markdown("""
### 📖 Detalhamento do Gráfico

#### ✅ Indicador analisado
Carga média de pacientes atendidos por médico.

#### ✅ Cálculo utilizado
- Métrica principal: `pacientes_por_medico`
- Função aplicada: `MEAN()`
- Agrupamento: Unidade de Saúde

#### ✅ Como interpretar
- Barras maiores indicam maior carga assistencial médica.
- Valores elevados podem indicar sobrecarga profissional.
- Auxilia na análise de distribuição médica.

#### ✅ Conclusão resumida
A análise permite identificar unidades com maior carga assistencial médica.

Valores elevados podem representar sobrecarga profissional e impacto na qualidade do atendimento prestado.

#### ✅ Ferramentas Python utilizadas
- `Pandas`
- `Plotly Express`
- `Streamlit`
- `DuckDB`
""")

# ============================================
# RESUMO EXECUTIVO
# ============================================

st.markdown("---")

st.subheader("📝 Resumo Executivo")

score_medio = round(
    dados["score_qualidade"].mean(),
    2
)

tempo_medio = round(
    dados["tempo_espera"].mean(),
    1
)

pacientes_medico = round(
    dados["pacientes_por_medico"].mean(),
    2
)

st.info(f"""

O período analisado apresentou
score médio operacional de
{score_medio} pontos.

O tempo médio estimado de espera foi
de aproximadamente {tempo_medio} minutos.

A média assistencial registrada foi de
{pacientes_medico} pacientes por médico.

""")

# ============================================
# FOOTER
# ============================================

st.success(
    "✅ Análise Qualidade x Demanda carregada"
)