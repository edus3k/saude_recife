# ============================================
# VALIDAÇÃO BIG DATA PAPE - ALTO DESEMPENHO
# USANDO DUCKDB (SEM ESTOURAR MEMÓRIA)
# ============================================

import duckdb

caminho_parquet = "../data/dados_tratados/PAPE/PAPE_TOTAL.parquet"

print("\n===================================")
print("🚀 VALIDAÇÃO PAPE - DUCKDB (OTIMIZADO)")
print("===================================")

# ============================================
# 1. INFO GERAL (SEM CARREGAR TUDO)
# ============================================

print("\n📊 CONTAGEM TOTAL DE REGISTROS")

total = duckdb.query(f"""
    SELECT COUNT(*) AS total
    FROM '{caminho_parquet}'
""").fetchdf()

print(total)

# ============================================
# 2. RESUMO POR ANO
# ============================================

print("\n📅 RESUMO POR ANO")

ano = duckdb.query(f"""
    SELECT ano, COUNT(*) AS qtd
    FROM '{caminho_parquet}'
    GROUP BY ano
    ORDER BY ano
""").fetchdf()

print(ano)

# ============================================
# 3. RESUMO POR MÊS
# ============================================

print("\n📆 RESUMO POR MÊS")

mes = duckdb.query(f"""
    SELECT mes, COUNT(*) AS qtd
    FROM '{caminho_parquet}'
    GROUP BY mes
    ORDER BY mes
""").fetchdf()

print(mes)

# ============================================
# 4. INDICADORES PRINCIPAIS (SEM RAM PESADA)
# ============================================

print("\n💰 INDICADORES FINANCEIROS")

indicadores = duckdb.query(f"""
    SELECT 
        SUM(pa_qtdpro) AS qtd_procedimentos,
        SUM(pa_qtdapr) AS qtd_aprovados,
        SUM(pa_valpro) AS valor_produzido,
        SUM(pa_valapr) AS valor_aprovado
    FROM '{caminho_parquet}'
""").fetchdf()

print(indicadores)

# ============================================
# 5. TOP ANOS/MÊS POR VALOR
# ============================================

print("\n📊 TOP PERÍODOS POR VALOR")

top = duckdb.query(f"""
    SELECT ano, mes, SUM(pa_valapr) AS total_valor
    FROM '{caminho_parquet}'
    GROUP BY ano, mes
    ORDER BY total_valor DESC
    LIMIT 10
""").fetchdf()

print(top)

print("\n===================================")
print("🎯 PROCESSAMENTO FINALIZADO COM DUCKDB")
print("===================================")