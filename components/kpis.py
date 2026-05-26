# ============================================
# KPIs PADRONIZADOS
# utils/kpis.py
# ============================================

import streamlit as st
import pandas as pd

# ============================================
# KPI SIMPLES
# ============================================

def kpi(

    titulo,

    valor,

    delta=None,

    ajuda=None

):

    st.metric(

        label=titulo,

        value=valor,

        delta=delta,

        help=ajuda

    )

# ============================================
# EXIBIR VÁRIOS KPIs
# ============================================

def exibir_kpis(lista_kpis):

    """

    lista_kpis = [

        {
            "titulo": "Atendimentos",
            "valor": "120.000"
        },

        {
            "titulo": "Profissionais",
            "valor": "5.000"
        }

    ]

    """

    colunas = st.columns(len(lista_kpis))

    for i, item in enumerate(lista_kpis):

        colunas[i].metric(

            label=item["titulo"],

            value=item["valor"],

            delta=item.get("delta", None),

            help=item.get("help", None)

        )

# ============================================
# KPI ATENDIMENTOS
# ============================================

def kpi_atendimentos(dados):

    total = int(

        dados["total_atendimentos"]
        .sum()

    )

    return {

        "titulo": "🏥 Atendimentos",

        "valor": f"{total:,.0f}"

    }

# ============================================
# KPI PROFISSIONAIS
# ============================================

def kpi_profissionais(dados):

    total = int(

        dados["total_profissionais"]
        .sum()

    )

    return {

        "titulo": "👨‍⚕️ Profissionais",

        "valor": f"{total:,.0f}"

    }

# ============================================
# KPI MÉDICOS
# ============================================

def kpi_medicos(dados):

    total = int(

        dados["total_medicos"]
        .sum()

    )

    return {

        "titulo": "🩺 Médicos",

        "valor": f"{total:,.0f}"

    }

# ============================================
# KPI LEITOS
# ============================================

def kpi_leitos(dados):

    total = int(

        dados["qtd_leitos"]
        .sum()

    )

    return {

        "titulo": "🛏️ Leitos",

        "valor": f"{total:,.0f}"

    }

# ============================================
# KPI SCORE
# ============================================

def kpi_score(dados):

    media = round(

        dados["score_qualidade"]
        .mean(),

        2

    )

    return {

        "titulo": "⭐ Score Médio",

        "valor": f"{media}"

    }

# ============================================
# KPI ESPERA
# ============================================

def kpi_espera(dados):

    media = round(

        dados["tempo_espera"]
        .mean(),

        1

    )

    return {

        "titulo": "⏱️ Tempo Espera",

        "valor": f"{media}"

    }

# ============================================
# KPI SOBRECARGA
# ============================================

def kpi_sobrecarga(dados):

    media = round(

        dados["indice_sobrecarga"]
        .mean(),

        2

    )

    return {

        "titulo": "🚨 Sobrecarga",

        "valor": f"{media}"

    }

# ============================================
# KPI EFICIÊNCIA
# ============================================

def kpi_eficiencia(dados):

    media = round(

        dados["score_eficiencia"]
        .mean(),

        2

    )

    return {

        "titulo": "📈 Eficiência",

        "valor": f"{media}"

    }

# ============================================
# KPI PACIENTES/MÉDICO
# ============================================

def kpi_pacientes_medico(dados):

    media = round(

        dados["pacientes_por_medico"]
        .mean(),

        2

    )

    return {

        "titulo": "👨‍⚕️ Pacientes/Médico",

        "valor": f"{media}"

    }

# ============================================
# KPI PRESSÃO LEITOS
# ============================================

def kpi_pressao_leitos(dados):

    media = round(

        dados["pressao_leitos"]
        .mean(),

        2

    )

    return {

        "titulo": "🛏️ Pressão Leitos",

        "valor": f"{media}"

    }

# ============================================
# KPI PERSONALIZADO
# ============================================

def criar_kpi(

    titulo,

    valor,

    delta=None,

    help_text=None

):

    return {

        "titulo": titulo,

        "valor": valor,

        "delta": delta,

        "help": help_text

    }

# ============================================
# RESUMO EXECUTIVO
# ============================================

def resumo_executivo(

    titulo,

    descricao

):

    st.markdown("---")

    st.subheader("📝 " + titulo)

    st.info(descricao)

# ============================================
# ALERTA OPERACIONAL
# ============================================

def alerta_operacional(

    mensagem,

    tipo="warning"

):

    if tipo == "success":

        st.success(mensagem)

    elif tipo == "error":

        st.error(mensagem)

    elif tipo == "info":

        st.info(mensagem)

    else:

        st.warning(mensagem)

# ============================================
# BADGE STATUS
# ============================================

def status_operacional(valor):

    """

    Retorna status baseado no score.

    """

    if valor >= 80:

        return "🟢 Excelente"

    elif valor >= 60:

        return "🟡 Bom"

    elif valor >= 40:

        return "🟠 Atenção"

    else:

        return "🔴 Crítico"

# ============================================
# KPI COM STATUS
# ============================================

def kpi_com_status(

    titulo,

    valor

):

    status = status_operacional(valor)

    st.metric(

        titulo,

        valor,

        delta=status

    )