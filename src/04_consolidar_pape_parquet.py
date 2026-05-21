# ============================================
# CONSOLIDAÇÃO BIG DATA PAPE (OTIMIZADA)
# STREAMING - SEM ESTOURAR MEMÓRIA
# ============================================

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import glob
import os

# ============================================
# CONFIGURAÇÃO DE PASTAS
# ============================================

input_folder = "../data/dados_tratados/PAPE"
output_file = "../data/dados_tratados/PAPE/PAPE_TOTAL.parquet"

os.makedirs(os.path.dirname(output_file), exist_ok=True)

# ============================================
# LISTA DE ARQUIVOS PARQUET
# ============================================

arquivos = glob.glob(os.path.join(input_folder, "*.parquet"))

print("\n===================================")
print("📦 CONSOLIDAÇÃO PAPE - STREAMING OTIMIZADO")
print("===================================")

print(f"\n📄 Arquivos encontrados: {len(arquivos)}")

# ============================================
# PREPARAÇÃO DO ESCRITOR PARQUET (PYARROW)
# ============================================

writer = None  # controla o arquivo final

# ============================================
# LOOP STREAMING (SEM CONCATENAR NA MEMÓRIA)
# ============================================

for arq in arquivos:

    try:
        print(f"\n🔄 Lendo: {os.path.basename(arq)}")

        # ============================================
        # LEITURA DO PARQUET
        # ============================================

        df = pd.read_parquet(arq)

        print(f"📊 Registros: {len(df)}")

        # ============================================
        # CONVERSÃO PARA PYARROW TABLE
        # ============================================

        table = pa.Table.from_pandas(df)

        # ============================================
        # ESCRITA INCREMENTAL
        # ============================================

        if writer is None:
            # cria o arquivo na primeira vez
            writer = pq.ParquetWriter(
                output_file,
                table.schema,
                compression="snappy"
            )

        writer.write_table(table)

        # libera memória imediatamente
        del df
        del table

    except Exception as e:
        print(f"❌ Erro em {arq}: {e}")

# ============================================
# FECHAR ESCRITOR
# ============================================

if writer is not None:
    writer.close()

print("\n===================================")
print("🎯 PROCESSAMENTO FINALIZADO")
print("===================================")
print(f"✅ BASE FINAL GERADA:")
print(output_file)