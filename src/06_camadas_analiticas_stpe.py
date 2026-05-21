# ============================================
# CAMADA ANALÍTICA STPE
# ALTO DESEMPENHO COM DUCKDB
# ============================================

import duckdb
import os

# ============================================
# ARQUIVO PARQUET
# ============================================

parquet_file = "../data/dados_tratados/STPE/STPE_TOTAL.parquet"

# ============================================
# PASTA DE SAÍDA
# ============================================

output_folder = "../data/dados_tratados/STPE/analytics"

os.makedirs(output_folder, exist_ok=True)

print("\n===================================")
print("📊 CAMADA ANALÍTICA STPE")
print("===================================")

# ============================================
# 1. INDICADORES GERAIS
# ============================================

print("\n💰 INDICADORES GERAIS")

indicadores_gerais = duckdb.query(f"""
    SELECT
        COUNT(*) AS total_registros
    FROM '{parquet_file}'
""").to_df()

print(indicadores_gerais)

# salva parquet
indicadores_gerais.to_parquet(
    f"{output_folder}/indicadores_gerais.parquet",
    index=False
)

# ============================================
# 2. INDICADORES POR ANO
# ============================================

try:

    print("\n📅 INDICADORES POR ANO")

    indicadores_ano = duckdb.query(f"""
        SELECT
            ano,
            COUNT(*) AS quantidade
        FROM '{parquet_file}'
        GROUP BY ano
        ORDER BY ano
    """).to_df()

    print(indicadores_ano)

    indicadores_ano.to_parquet(
        f"{output_folder}/indicadores_ano.parquet",
        index=False
    )

except Exception as e:

    print("⚠️ Não foi possível gerar indicadores por ano")
    print(e)

# ============================================
# 3. INDICADORES POR MÊS
# ============================================

try:

    print("\n📆 INDICADORES POR MÊS")

    indicadores_mes = duckdb.query(f"""
        SELECT
            ano,
            mes,
            COUNT(*) AS quantidade
        FROM '{parquet_file}'
        GROUP BY ano, mes
        ORDER BY ano, mes
    """).to_df()

    print(indicadores_mes)

    indicadores_mes.to_parquet(
        f"{output_folder}/indicadores_mes.parquet",
        index=False
    )

except Exception as e:

    print("⚠️ Não foi possível gerar indicadores por mês")
    print(e)

# ============================================
# 4. TOP 10 PERÍODOS
# ============================================

try:

    print("\n🔥 TOP 10 PERÍODOS")

    top_periodos = duckdb.query(f"""
        SELECT
            ano,
            mes,
            COUNT(*) AS quantidade
        FROM '{parquet_file}'
        GROUP BY ano, mes
        ORDER BY quantidade DESC
        LIMIT 10
    """).to_df()

    print(top_periodos)

    top_periodos.to_parquet(
        f"{output_folder}/top_periodos.parquet",
        index=False
    )

except Exception as e:

    print("⚠️ Não foi possível gerar top períodos")
    print(e)

# ============================================
# 5. AMOSTRA ANALÍTICA
# ============================================

try:

    print("\n📋 AMOSTRA ANALÍTICA")

    amostra = duckdb.query(f"""
        SELECT *
        FROM '{parquet_file}'
        LIMIT 100
    """).to_df()

    amostra.to_parquet(
        f"{output_folder}/amostra_analitica.parquet",
        index=False
    )

    print(amostra.head())

except Exception as e:

    print("⚠️ Não foi possível gerar amostra")
    print(e)

# ============================================
# FINALIZAÇÃO
# ============================================

print("\n===================================")
print("🎯 CAMADA ANALÍTICA FINALIZADA")
print("===================================")

print(f"\n📁 Arquivos salvos em:")
print(output_folder)