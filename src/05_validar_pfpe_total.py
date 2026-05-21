# ============================================
# VALIDAÇÃO BIG DATA PFPE
# OTIMIZADO COM DUCKDB
# ============================================

import duckdb

# ============================================
# ARQUIVO PARQUET
# ============================================

parquet_file = "../data/dados_tratados/PFPE/PFPE_TOTAL.parquet"

print("\n===================================")
print("🚀 VALIDAÇÃO BIG DATA PFPE")
print("===================================")

# ============================================
# 1. TOTAL DE REGISTROS
# ============================================

print("\n📊 TOTAL DE REGISTROS")

total = duckdb.query(f"""
    SELECT COUNT(*) AS total_registros
    FROM '{parquet_file}'
""").fetchdf()

print(total)

# ============================================
# 2. VERIFICAÇÃO DE DUPLICADOS
# ============================================
# OBS:
# DISTINCT * em Big Data é pesado.
# Aqui usamos subquery otimizada.
# ============================================

print("\n🔁 VERIFICAÇÃO DE DUPLICADOS")

try:

    duplicados = duckdb.query(f"""
        SELECT
            (
                SELECT COUNT(*)
                FROM '{parquet_file}'
            )
            -
            (
                SELECT COUNT(*)
                FROM (
                    SELECT DISTINCT *
                    FROM '{parquet_file}'
                )
            )
            AS registros_duplicados
    """).fetchdf()

    print(duplicados)

except Exception as e:

    print("⚠️ Não foi possível validar duplicados")
    print(e)

# ============================================
# 3. ANOS DISPONÍVEIS
# ============================================

try:

    print("\n📅 ANOS DISPONÍVEIS")

    anos = duckdb.query(f"""
        SELECT
            ano,
            COUNT(*) AS quantidade
        FROM '{parquet_file}'
        GROUP BY ano
        ORDER BY ano
    """).fetchdf()

    print(anos)

except Exception as e:

    print("⚠️ Coluna 'ano' não encontrada")
    print(e)

# ============================================
# 4. MESES DISPONÍVEIS
# ============================================

try:

    print("\n📆 MESES DISPONÍVEIS")

    meses = duckdb.query(f"""
        SELECT
            mes,
            COUNT(*) AS quantidade
        FROM '{parquet_file}'
        GROUP BY mes
        ORDER BY mes
    """).fetchdf()

    print(meses)

except Exception as e:

    print("⚠️ Coluna 'mes' não encontrada")
    print(e)

# ============================================
# 5. NULOS PRINCIPAIS
# ============================================

print("\n❌ VERIFICAÇÃO DE NULOS")

try:

    nulos = duckdb.query(f"""
        SELECT
            SUM(CASE WHEN ano IS NULL THEN 1 ELSE 0 END) AS ano_nulo,
            SUM(CASE WHEN mes IS NULL THEN 1 ELSE 0 END) AS mes_nulo
        FROM '{parquet_file}'
    """).fetchdf()

    print(nulos)

except Exception as e:

    print("⚠️ Não foi possível verificar nulos")
    print(e)

# ============================================
# 6. AMOSTRA DOS DADOS
# ============================================

print("\n📋 AMOSTRA DOS DADOS")

try:

    amostra = duckdb.query(f"""
        SELECT *
        FROM '{parquet_file}'
        LIMIT 10
    """).fetchdf()

    print(amostra)

except Exception as e:

    print("⚠️ Não foi possível carregar amostra")
    print(e)

# ============================================
# FINALIZAÇÃO
# ============================================

print("\n===================================")
print("🎯 VALIDAÇÃO FINALIZADA")
print("===================================")