import streamlit as st
import pandas as pd

# -----------------------------
# CARREGAMENTO DOS DADOS
# -----------------------------

# Lê os dados tratados
df = pd.read_csv("data/dados_tratados/dados_tratados.csv")

# -----------------------------
# TÍTULO DO DASHBOARD
# -----------------------------
st.title("📊 Qualidade do Atendimento - Recife")

# -----------------------------
# MÉTRICAS
# -----------------------------

# Mostra total de registros
st.metric("Total de Atendimentos", len(df))

# -----------------------------
# GRÁFICO DE ESPECIALIDADES
# -----------------------------
st.subheader("Atendimentos por Especialidade")

# Conta quantas vezes cada especialidade aparece
st.bar_chart(df["especialidade"].value_counts())

# -----------------------------
# GRÁFICO DE HORÁRIOS
# -----------------------------
st.subheader("Atendimentos por Horário")

# Converte coluna hora
df["hora"] = pd.to_datetime(df["hora"]).dt.hour

# Agrupa por hora
horario = df.groupby("hora").size()

# Mostra gráfico de linha
st.line_chart(horario)