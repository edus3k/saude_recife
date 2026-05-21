# ============================================
# CAMADA ANALÍTICA - INDICADORES PAPE
# ALTO DESEMPENHO (DUCKDB + PARQUET)
# ============================================

import duckdb
import os

# ============================================
# ARQUIVO BASE
# ============================================

parquet_file = "../data/dados_tratados/PAPE/PAPE_TOTAL.parquet"

print("\n===================================")
print("📊 CAMADA ANALÍTICA - INDICADORES PAPE")
print("===================================")

# ============================================
# 1. INDICADORES GERAIS
# ============================================

print("\n💰 INDICADORES GERAIS")

indicadores_gerais = duckdb.query(f"""
    SELECT 
        COUNT(*) AS total_registros,
        SUM(pa_qtdpro) AS total_procedimentos,
        SUM(pa_qtdapr) AS total_aprovados,
        SUM(pa_valpro) AS valor_total_produzido,
        SUM(pa_valapr) AS valor_total_aprovado,
        ROUND(AVG(pa_valapr), 2) AS media_valor_aprovado
    FROM '{parquet_file}'
""").to_df()

print(indicadores_gerais)

# ============================================
# 2. INDICADORES POR ANO
# ============================================

print("\n📅 INDICADORES POR ANO")

por_ano = duckdb.query(f"""
    SELECT 
        ano,
        COUNT(*) AS registros,
        SUM(pa_qtdpro) AS procedimentos,
        SUM(pa_qtdapr) AS aprovados,
        SUM(pa_valapr) AS valor_aprovado
    FROM '{parquet_file}'
    GROUP BY ano
    ORDER BY ano
""").to_df()

print(por_ano)

# ============================================
# 3. INDICADORES POR ANO/MÊS
# ============================================

print("\n📆 INDICADORES POR ANO/MÊS")

por_mes = duckdb.query(f"""
    SELECT 
        ano,
        mes,
        COUNT(*) AS registros,
        SUM(pa_qtdpro) AS procedimentos,
        SUM(pa_qtdapr) AS aprovados,
        SUM(pa_valapr) AS valor_aprovado
    FROM '{parquet_file}'
    GROUP BY ano, mes
    ORDER BY ano, mes
""").to_df()

print(por_mes)

# ============================================
# 4. TOP PERÍODOS (MAIOR PRODUÇÃO)
# ============================================

print("\n🔥 TOP 10 PERÍODOS (VALOR APROVADO)")

top_periodos = duckdb.query(f"""
    SELECT 
        ano,
        mes,
        SUM(pa_valapr) AS valor_total
    FROM '{parquet_file}'
    GROUP BY ano, mes
    ORDER BY valor_total DESC
    LIMIT 10
""").to_df()

print(top_periodos)

# ============================================
# 5. PRODUTIVIDADE MÉDIA
# ============================================

print("\n📊 PRODUTIVIDADE MÉDIA")

produtividade = duckdb.query(f"""
    SELECT 
        ano,
        ROUND(SUM(pa_qtdapr) / COUNT(*), 2) AS media_aprovados_por_registro,
        ROUND(SUM(pa_valapr) / SUM(pa_qtdapr), 2) AS valor_medio_por_procedimento
    FROM '{parquet_file}'
    GROUP BY ano
    ORDER BY ano
""").to_df()

print(produtividade)

# ============================================
# 6. SALVAR RESULTADOS ANALÍTICOS
# ============================================

output_folder = "../data/dados_tratados/PAPE/analytics"
os.makedirs(output_folder, exist_ok=True)

indicadores_gerais.to_parquet(f"{output_folder}/indicadores_gerais.parquet", index=False)
por_ano.to_parquet(f"{output_folder}/indicadores_ano.parquet", index=False)
por_mes.to_parquet(f"{output_folder}/indicadores_mes.parquet", index=False)
top_periodos.to_parquet(f"{output_folder}/top_periodos.parquet", index=False)
produtividade.to_parquet(f"{output_folder}/produtividade.parquet", index=False)

print("\n===================================")
print("🎯 CAMADA ANALÍTICA FINALIZADA")
print("===================================")
print(f"📁 Arquivos salvos em: {output_folder}")