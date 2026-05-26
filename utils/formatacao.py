# ============================================
# FORMATAÇÃO GLOBAL
# utils/formatacao.py
# ============================================

import pandas as pd
import numpy as np

# ============================================
# FORMATAR NÚMERO
# ============================================

def formatar_numero(valor):

    try:

        return f"{valor:,.0f}"

    except:

        return valor

# ============================================
# FORMATAR DECIMAL
# ============================================

def formatar_decimal(

    valor,

    casas=2

):

    try:

        return f"{valor:,.{casas}f}"

    except:

        return valor

# ============================================
# FORMATAR PERCENTUAL
# ============================================

def formatar_percentual(

    valor,

    casas=2

):

    try:

        return f"{valor:.{casas}f}%"

    except:

        return valor

# ============================================
# FORMATAR MOEDA
# ============================================

def formatar_moeda(

    valor,

    moeda="R$"

):

    try:

        return (

            f"{moeda} "

            f"{valor:,.2f}"

        )

    except:

        return valor

# ============================================
# FORMATAR TEMPO
# ============================================

def formatar_tempo(

    minutos

):

    try:

        horas = int(minutos // 60)

        mins = int(minutos % 60)

        if horas > 0:

            return f"{horas}h {mins}min"

        return f"{mins}min"

    except:

        return minutos

# ============================================
# FORMATAR DATA
# ============================================

def formatar_data(

    ano,

    mes

):

    try:

        return (

            f"{str(mes).zfill(2)}"

            f"/{ano}"

        )

    except:

        return f"{mes}/{ano}"

# ============================================
# FORMATAR PERÍODO
# ============================================

def criar_periodo(dados):

    dados["periodo"] = (

        dados["ano"]
        .astype(str)

        + "-"

        +

        dados["mes"]
        .astype(str)
        .str.zfill(2)

    )

    return dados

# ============================================
# FORMATAR COLUNAS NUMÉRICAS
# ============================================

def formatar_dataframe(

    dados

):

    dados = dados.copy()

    colunas_float = (

        dados

        .select_dtypes(

            include=["float64", "float"]

        )

        .columns

    )

    for coluna in colunas_float:

        dados[coluna] = (

            dados[coluna]

            .round(2)

        )

    return dados

# ============================================
# FORMATAR STATUS
# ============================================

def formatar_status(

    status

):

    mapa = {

        "Excelente":
            "🟢 Excelente",

        "Bom":
            "🟡 Bom",

        "Atenção":
            "🟠 Atenção",

        "Crítico":
            "🔴 Crítico"

    }

    return mapa.get(status, status)

# ============================================
# FORMATAR SCORE
# ============================================

def formatar_score(

    valor

):

    try:

        valor = round(valor, 2)

        if valor >= 80:

            return f"🟢 {valor}"

        elif valor >= 60:

            return f"🟡 {valor}"

        elif valor >= 40:

            return f"🟠 {valor}"

        return f"🔴 {valor}"

    except:

        return valor

# ============================================
# FORMATAR LISTA
# ============================================

def formatar_lista(

    lista

):

    try:

        return ", ".join(

            [str(x) for x in lista]

        )

    except:

        return lista

# ============================================
# FORMATAR TEXTO
# ============================================

def capitalizar(

    texto

):

    try:

        return texto.title()

    except:

        return texto

# ============================================
# FORMATAR CNES
# ============================================

def formatar_cnes(

    cnes

):

    try:

        return str(cnes).zfill(7)

    except:

        return cnes

# ============================================
# FORMATAR MILHÕES
# ============================================

def formatar_milhoes(

    valor

):

    try:

        if valor >= 1_000_000:

            return (

                f"{valor / 1_000_000:.1f}M"

            )

        elif valor >= 1_000:

            return (

                f"{valor / 1_000:.1f}K"

            )

        return str(valor)

    except:

        return valor

# ============================================
# FORMATAR VARIAÇÃO
# ============================================

def formatar_variacao(

    valor

):

    try:

        if valor > 0:

            return f"📈 +{valor:.2f}%"

        elif valor < 0:

            return f"📉 {valor:.2f}%"

        return f"➖ {valor:.2f}%"

    except:

        return valor

# ============================================
# FORMATAR NOME COLUNAS
# ============================================

def formatar_nome_colunas(

    dados

):

    dados.columns = [

        coluna

        .replace("_", " ")

        .title()

        for coluna in dados.columns

    ]

    return dados

# ============================================
# FORMATAR BOOLEANO
# ============================================

def formatar_booleano(

    valor

):

    if valor:

        return "✅ Sim"

    return "❌ Não"

# ============================================
# FORMATAR COR
# ============================================

def cor_score(

    valor

):

    try:

        if valor >= 80:

            return "green"

        elif valor >= 60:

            return "orange"

        return "red"

    except:

        return "gray"

# ============================================
# FORMATAR SÉRIE TEMPORAL
# ============================================

def ordenar_periodo(

    dados,

    coluna="periodo"

):

    dados = dados.copy()

    dados = dados.sort_values(

        coluna

    )

    return dados

# ============================================
# FORMATAÇÃO FINAL DASHBOARD
# ============================================

def preparar_visualizacao(

    dados

):

    dados = formatar_dataframe(dados)

    dados = formatar_nome_colunas(dados)

    return dados