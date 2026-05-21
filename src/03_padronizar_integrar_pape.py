# ============================================
# PADRONIZAÇÃO PAPE - BIG DATA
# ============================================

import pandas as pd
import os


# ============================================
# PASTAS
# ============================================

input_folder = "../data/dados_limpos/PAPE"

output_folder = "../data/dados_tratados/PAPE"

os.makedirs(output_folder, exist_ok=True)


# ============================================
# LISTAR ARQUIVOS
# ============================================

arquivos = os.listdir(input_folder)

print("\n===================================")
print("📂 PROCESSAMENTO BIG DATA PAPE")
print("===================================")

print(f"\n📄 Arquivos encontrados: {len(arquivos)}")


# ============================================
# LOOP DOS CSVs
# ============================================

for file in arquivos:

    if file.lower().endswith(".csv"):

        try:

            print("\n-----------------------------------")
            print(f"🔄 Processando: {file}")
            print("-----------------------------------")

            caminho_csv = os.path.join(input_folder, file)

            # ============================================
            # LEITURA CSV
            # ============================================

            df = pd.read_csv(
                caminho_csv,
                low_memory=False
            )

            print(f"📊 Registros: {len(df)}")


            # ============================================
            # PADRONIZA COLUNAS
            # ============================================

            df.columns = (
                df.columns
                .str.lower()
                .str.strip()
            )


            # ============================================
            # REMOVE DUPLICADOS
            # ============================================

            df.drop_duplicates(inplace=True)


            # ============================================
            # REMOVE NULOS
            # ============================================

            df.dropna(how="all", inplace=True)


            # ============================================
            # TEXTO
            # ============================================

            colunas_texto = df.select_dtypes(
                include=["object", "string"]
            ).columns

            for col in colunas_texto:

                df[col] = (
                    df[col]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                )


            # ============================================
            # NUMÉRICOS
            # ============================================

            colunas_numericas = [

                "pa_idade",
                "pa_qtdpro",
                "pa_qtdapr",
                "pa_valpro",
                "pa_valapr"

            ]

            for col in colunas_numericas:

                if col in df.columns:

                    df[col] = pd.to_numeric(
                        df[col],
                        errors="coerce",
                        downcast="float"
                    )


            # ============================================
            # COMPETÊNCIA
            # ============================================

            if "pa_cmp" in df.columns:

                df["pa_cmp"] = df["pa_cmp"].astype(str)

                df["ano"] = df["pa_cmp"].str[:4]

                df["mes"] = df["pa_cmp"].str[4:6]


            # ============================================
            # OTIMIZA MEMÓRIA
            # ============================================

            for col in colunas_texto:

                if col in df.columns:

                    df[col] = df[col].astype("category")


            # ============================================
            # NOME PARQUET
            # ============================================

            nome_parquet = file.replace(".csv", ".parquet")

            caminho_parquet = os.path.join(
                output_folder,
                nome_parquet
            )


            # ============================================
            # SALVAR PARQUET
            # ============================================

            df.to_parquet(
                caminho_parquet,
                index=False
            )

            print(f"✅ PARQUET salvo:")
            print(caminho_parquet)


            # ============================================
            # LIBERA MEMÓRIA
            # ============================================

            del df

        except Exception as e:

            print(f"\n❌ Erro em {file}")
            print(e)


print("\n===================================")
print("🎯 PROCESSAMENTO FINALIZADO")
print("===================================")