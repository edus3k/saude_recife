# ============================================
# PAGE INICIAL - SAÚDE RECIFE ANALYTICS
# ============================================

import streamlit as st
from pathlib import Path

# ============================================
# CONFIG
# ============================================

st.set_page_config(
    page_title="Saúde Recife Analytics",
    page_icon="🏥",
    layout="wide"
)

# ============================================
# PATH BASE
# ============================================

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# SIDEBAR
# ============================================

st.sidebar.success("✅ Sistema Online")

st.sidebar.info("""

🏥 Saúde Recife Analytics

Versão 1.0

Projeto Big Data em Saúde Pública

""")

# ============================================
# HEADER
# ============================================

st.markdown("""

# 🏥 DASHBOARD QUALIDADE DE ATENDIMENTO

## Saúde Recife Analytics

Sistema analítico para monitoramento da qualidade
dos atendimentos da rede pública de saúde do Recife.

---

""")

# ============================================
# LAYOUT PRINCIPAL
# ============================================

col1, col2 = st.columns([2,1])

# ============================================
# OBJETIVO
# ============================================

with col1:

    st.markdown("""

    ## 📌 Objetivo do Projeto

    Este projeto foi desenvolvido com o objetivo de integrar,
    tratar e analisar grandes volumes de dados da saúde pública
    do Recife utilizando técnicas de Big Data e Analytics.

    O sistema realiza correlação entre:

    - Produção Ambulatorial
    - Profissionais de Saúde
    - Estrutura Hospitalar

    permitindo análises avançadas sobre:

    ✅ Qualidade do atendimento  
    ✅ Eficiência operacional  
    ✅ Unidades sobrecarregadas  
    ✅ Pressão hospitalar  
    ✅ Tempo estimado de espera  
    ✅ Ranking inteligente das unidades  
    ✅ Evolução temporal da demanda  
    ✅ Correlação entre estrutura e atendimento  

    Além disso, o dashboard auxilia gestores públicos
    na tomada de decisão baseada em dados.

    """)

# ============================================
# AUTOR
# ============================================

with col2:

    st.info("""

    👨‍💻 Desenvolvido por

    ### Eduardo Santos

    ---

    📊 Projeto Big Data em Python

    🏥 Saúde Pública

    📍 Recife - Pernambuco

    ---

    🚀 Tecnologias Utilizadas:

    - Python
    - Streamlit
    - DuckDB
    - Plotly
    - Pandas
    - Parquet

    """)

# ============================================
# TECNOLOGIAS
# ============================================

st.markdown("---")

st.markdown("## 🛠️ Ferramentas Utilizadas")

tec1, tec2, tec3, tec4 = st.columns(4)

# ============================================
# PYTHON
# ============================================

with tec1:

    st.success("""

    ### 🐍 Python

    Linguagem principal do projeto.

    Responsável por:

    - Tratamento de dados
    - Limpeza dos arquivos
    - Integração das bases
    - Criação dos indicadores
    - Desenvolvimento do dashboard

    """)

# ============================================
# DUCKDB
# ============================================

with tec2:

    st.success("""

    ### ⚡ DuckDB

    Banco analítico em memória.

    Utilizado para:

    - Consultas SQL rápidas
    - Processamento de milhões de registros
    - Alta performance analítica
    - Integração com arquivos Parquet

    """)

# ============================================
# STREAMLIT
# ============================================

with tec3:

    st.success("""

    ### 📊 Streamlit

    Framework web utilizado
    para construção do dashboard.

    Permite:

    - Gráficos interativos
    - Filtros dinâmicos
    - Visualização em tempo real
    - Interface moderna e intuitiva

    """)

# ============================================
# PARQUET
# ============================================

with tec4:

    st.success("""

    ### 📁 Parquet

    Formato otimizado para Big Data.

    Benefícios:

    - Alta compressão
    - Leitura extremamente rápida
    - Melhor performance analítica
    - Redução do uso de memória

    """)

# ============================================
# BASES UTILIZADAS
# ============================================

st.markdown("---")

st.markdown("## 🗂️ Bases Integradas")

base1, base2, base3 = st.columns(3)

# ============================================
# PAPE
# ============================================

with base1:

    st.warning("""

    ### 📄 PAPE

    Produção Ambulatorial

    Dados relacionados a:

    - Procedimentos
    - Atendimentos
    - Produção SUS
    - Demanda ambulatorial
    - Quantidade de serviços

    """)

# ============================================
# PFPE
# ============================================

with base2:

    st.warning("""

    ### 👨‍⚕️ PFPE

    Profissionais de Saúde

    Informações sobre:

    - Médicos
    - Equipes
    - Recursos Humanos
    - Especialidades
    - CBO
    - Profissionais ativos

    """)

# ============================================
# STPE
# ============================================

with base3:

    st.warning("""

    ### 🏥 STPE

    Estrutura Hospitalar

    Informações sobre:

    - Leitos
    - Equipamentos
    - Salas
    - Estrutura física
    - Capacidade hospitalar

    """)

# ============================================
# PROCESSAMENTO DOS DADOS
# ============================================

st.markdown("---")

st.markdown("## 🔄 Pipeline de Tratamento dos Dados")

st.info("""

Os dados disponibilizados pelo DATASUS apresentam
grandes desafios de processamento e conversão.

Os arquivos originais são disponibilizados no formato:

### 📦 DBC (Data Base Compressed)

Esse formato é compactado e não possui suporte
direto em bibliotecas Python modernas.

Por esse motivo, foi necessário utilizar
o programa oficial do DATASUS:

## 🖥️ TabWin

Ferramenta responsável pela conversão dos arquivos:

DBC → DBF

Após isso, os dados passaram pelas etapas:

DBF → CSV → Limpeza → Padronização → Parquet → Analytics

""")

# ============================================
# FLUXO ANALÍTICO
# ============================================

st.markdown("## ⚙️ Fluxo Analítico do Projeto")

st.code("""

        DADOS DATASUS

              │

              ▼

        Arquivos .DBC
              │
              ▼

      Conversão no TabWin
          DBC → DBF
              │
              ▼

         Conversão CSV
              │
              ▼

       Limpeza dos Dados
    - Valores nulos
    - Colunas inválidas
    - Padronização
    - Tipagem
              │
              ▼

      Conversão para Parquet
              │
              ▼

       Integração no DuckDB
              │
              ▼

      Analytics + Dashboard
              │
              ▼

       Visualização Streamlit

""")

# ============================================
# DIFICULDADES
# ============================================

st.markdown("---")

st.markdown("## ⚠️ Dificuldades Encontradas")

dif1, dif2 = st.columns(2)

with dif1:

    st.error("""

    ### 📌 Desafios Técnicos

    - Ausência de bibliotecas Python
      para leitura de arquivos DBC

    - Grande volume de dados

    - Estruturas inconsistentes

    - Padronização de colunas

    - Dados incompletos

    - Necessidade de otimização
      de memória e processamento

    """)

with dif2:

    st.error("""

    ### 🛠️ Soluções Aplicadas

    - Utilização do TabWin DATASUS

    - Conversão para Parquet

    - Processamento com DuckDB

    - Limpeza automatizada em Python

    - Queries analíticas otimizadas

    - Integração entre múltiplas bases

    """)

# ============================================
# FUNCIONALIDADES
# ============================================

st.markdown("---")

st.markdown("## 🚀 Funcionalidades do Dashboard")

f1, f2, f3, f4 = st.columns(4)

with f1:

    st.metric(
        "📊 Analytics",
        "100%"
    )

    st.caption("Indicadores inteligentes")

with f2:

    st.metric(
        "🏥 Unidades",
        "Ranking"
    )

    st.caption("Comparação operacional")

with f3:

    st.metric(
        "⚡ Performance",
        "Alta"
    )

    st.caption("DuckDB + Parquet")

with f4:

    st.metric(
        "📈 Monitoramento",
        "Tempo Real"
    )

    st.caption("Análise dinâmica")

# ============================================
# OBJETIVOS ANALÍTICOS
# ============================================

st.markdown("---")

st.markdown("## 🎯 Objetivos Estratégicos")

st.success("""

✔️ Identificar gargalos operacionais

✔️ Avaliar qualidade da rede de saúde

✔️ Detectar unidades sobrecarregadas

✔️ Medir eficiência hospitalar

✔️ Avaliar demanda ambulatorial

✔️ Auxiliar tomada de decisão

✔️ Melhorar gestão da saúde pública

✔️ Aplicar Big Data na saúde

✔️ Gerar indicadores inteligentes

""")

# ============================================
# RODAPÉ
# ============================================

st.markdown("---")

st.caption("""

Projeto acadêmico desenvolvido utilizando
Big Data, Engenharia de Dados e Analytics
aplicados à Saúde Pública do Recife.

""")