# ============================================
# CONSOLIDAÇÃO BIG DATA STPE
# STREAMING + ALTO DESEMPENHO
# ============================================

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import glob
import os
import gc

# ============================================
# PASTAS
# ============================================

input_folder = "../data/dados_tratados/STPE"

output_file = "../data/dados_tratados/STPE/STPE_TOTAL.parquet"

os.makedirs(os.path.dirname(output_file), exist_ok=True)

# ============================================
# LISTAR PARQUETS
# ============================================

arquivos = glob.glob(
    os.path.join(input_folder, "*.parquet")
)

# remove o arquivo consolidado da lista
arquivos = [
    arq for arq in arquivos
    if "STPE_TOTAL.parquet" not in arq
]

print("\n===================================")
print("📦 CONSOLIDAÇÃO BIG DATA STPE")
print("===================================")

print(f"\n📄 Arquivos encontrados: {len(arquivos)}")

# ============================================
# CONTROLE DO PARQUET WRITER
# ============================================

writer = None

# ============================================
# LOOP DOS ARQUIVOS
# ============================================

for arq in arquivos:

    try:

        nome_arquivo = os.path.basename(arq)

        print("\n-----------------------------------")
        print(f"🔄 Processando: {nome_arquivo}")
        print("-----------------------------------")

        # ============================================
        # LEITURA DO PARQUET
        # ============================================

        df = pd.read_parquet(arq)

        print(f"📊 Registros: {len(df)}")

        # ============================================
        # REMOVE DUPLICADOS
        # ============================================

        df.drop_duplicates(inplace=True)

        # ============================================
        # REMOVE LINHAS TOTALMENTE NULAS
        # ============================================

        df.dropna(how="all", inplace=True)

        # ============================================
        # CONVERTE PARA PYARROW
        # ============================================

        tabela = pa.Table.from_pandas(
            df,
            preserve_index=False
        )

        # ============================================
        # CRIA O WRITER NA PRIMEIRA ITERAÇÃO
        # ============================================

        if writer is None:

            writer = pq.ParquetWriter(
                output_file,
                tabela.schema,
                compression="snappy"
            )

        # ============================================
        # ESCREVE NO DATASET FINAL
        # ============================================

        writer.write_table(tabela)

        print("✅ Dados adicionados ao dataset final")

        # ============================================
        # LIMPEZA DE MEMÓRIA
        # ============================================

        del df
        del tabela

        gc.collect()

    except Exception as e:

        print(f"\n❌ Erro em {nome_arquivo}")
        print(e)

# ============================================
# FECHA WRITER
# ============================================

if writer is not None:
    writer.close()

# ============================================
# FINALIZAÇÃO
# ============================================

print("\n===================================")
print("🎯 CONSOLIDAÇÃO FINALIZADA")
print("===================================")

print(f"\n✅ Arquivo gerado:")
print(output_file)