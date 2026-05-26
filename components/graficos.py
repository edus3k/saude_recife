# ============================================
# GRÁFICOS PADRONIZADOS
# utils/graficos.py
# ============================================

import plotly.express as px
import streamlit as st

# ============================================
# TEMPLATE GLOBAL
# ============================================

TEMPLATE = "plotly_white"

# ============================================
# CONFIGURAÇÃO PADRÃO
# ============================================

def configurar_layout(

    fig,

    titulo="",

    altura=600,

    x_titulo="",

    y_titulo=""

):

    fig.update_layout(

        template=TEMPLATE,

        height=altura,

        title=titulo,

        title_x=0.5,

        xaxis_title=x_titulo,

        yaxis_title=y_titulo,

        legend_title="",

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )

    )

    return fig

# ============================================
# GRÁFICO BARRAS HORIZONTAL
# ============================================

def grafico_barra_horizontal(

    dados,

    x,

    y,

    titulo="",

    cor=None,

    texto=None,

    altura=700

):

    fig = px.bar(

        dados,

        x=x,

        y=y,

        orientation="h",

        color=cor,

        text=texto,

        template=TEMPLATE

    )

    fig.update_traces(

        textposition="outside"

    )

    configurar_layout(

        fig,

        titulo=titulo,

        altura=altura,

        x_titulo=x,

        y_titulo=""

    )

    return fig

# ============================================
# GRÁFICO LINHA
# ============================================

def grafico_linha(

    dados,

    x,

    y,

    titulo="",

    cor=None,

    altura=500,

    marcador=True

):

    fig = px.line(

        dados,

        x=x,

        y=y,

        color=cor,

        markers=marcador,

        template=TEMPLATE

    )

    configurar_layout(

        fig,

        titulo=titulo,

        altura=altura,

        x_titulo=x,

        y_titulo=y

    )

    return fig

# ============================================
# GRÁFICO ÁREA
# ============================================

def grafico_area(

    dados,

    x,

    y,

    titulo="",

    cor=None,

    altura=500

):

    fig = px.area(

        dados,

        x=x,

        y=y,

        color=cor,

        template=TEMPLATE

    )

    configurar_layout(

        fig,

        titulo=titulo,

        altura=altura,

        x_titulo=x,

        y_titulo=y

    )

    return fig

# ============================================
# GRÁFICO DISPERSÃO
# ============================================

def grafico_scatter(

    dados,

    x,

    y,

    titulo="",

    tamanho=None,

    cor=None,

    hover=None,

    altura=700

):

    fig = px.scatter(

        dados,

        x=x,

        y=y,

        size=tamanho,

        color=cor,

        hover_name=hover,

        template=TEMPLATE

    )

    configurar_layout(

        fig,

        titulo=titulo,

        altura=altura,

        x_titulo=x,

        y_titulo=y

    )

    return fig

# ============================================
# GRÁFICO PIZZA
# ============================================

def grafico_pizza(

    dados,

    nomes,

    valores,

    titulo="",

    altura=600

):

    fig = px.pie(

        dados,

        names=nomes,

        values=valores,

        hole=0.4,

        template=TEMPLATE

    )

    configurar_layout(

        fig,

        titulo=titulo,

        altura=altura

    )

    return fig

# ============================================
# HISTOGRAMA
# ============================================

def grafico_histograma(

    dados,

    coluna,

    titulo="",

    cor=None,

    altura=500

):

    fig = px.histogram(

        dados,

        x=coluna,

        color=cor,

        template=TEMPLATE

    )

    configurar_layout(

        fig,

        titulo=titulo,

        altura=altura,

        x_titulo=coluna,

        y_titulo="Frequência"

    )

    return fig

# ============================================
# BOXPLOT
# ============================================

def grafico_boxplot(

    dados,

    x,

    y,

    titulo="",

    cor=None,

    altura=600

):

    fig = px.box(

        dados,

        x=x,

        y=y,

        color=cor,

        template=TEMPLATE

    )

    configurar_layout(

        fig,

        titulo=titulo,

        altura=altura,

        x_titulo=x,

        y_titulo=y

    )

    return fig

# ============================================
# HEATMAP
# ============================================

def grafico_heatmap(

    dados,

    titulo="",

    altura=700

):

    fig = px.imshow(

        dados,

        text_auto=True,

        aspect="auto",

        template=TEMPLATE

    )

    configurar_layout(

        fig,

        titulo=titulo,

        altura=altura

    )

    return fig

# ============================================
# EXIBIR GRÁFICO
# ============================================

def mostrar_grafico(fig):

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ============================================
# KPIS PADRONIZADOS
# ============================================

def mostrar_kpis(lista_kpis):

    colunas = st.columns(len(lista_kpis))

    for i, item in enumerate(lista_kpis):

        colunas[i].metric(

            item["titulo"],

            item["valor"]

        )

# ============================================
# CARD EXPLICAÇÃO
# ============================================

def explicacao_grafico(

    titulo,

    descricao

):

    st.markdown(f"""

    ### {titulo}

    {descricao}

    """)

# ============================================
# DIVISOR PADRÃO
# ============================================

def divisor():

    st.markdown("---")