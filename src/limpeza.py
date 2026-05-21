# ---------------------------------------
# IMPORTAÇÃO DE BIBLIOTECAS
# ---------------------------------------

import pandas as pd
import os


# ---------------------------------------
# PASTAS
# ---------------------------------------

input_folder = "../data/dados_convertidos/PAPE"

output_folder = "../data/dados_limpos/PAPE"

os.makedirs(output_folder, exist_ok=True)


# ---------------------------------------
# LISTA ARQUIVOS CSV
# ---------------------------------------

arquivos = os.listdir(input_folder)

print(f"\n📄 Arquivos encontrados: {len(arquivos)}")


# ---------------------------------------
# LOOP DOS CSV
# ---------------------------------------

for file in arquivos:

    if file.lower().endswith(".csv"):

        try:

            print("\n===================================")
            print(f"🧹 Limpando arquivo: {file}")
            print("===================================")

            # Caminho CSV
            caminho_csv = os.path.join(input_folder, file)

            # Leitura CSV
            df = pd.read_csv(
                caminho_csv,
                low_memory=False
            )

            print(f"📊 Registros originais: {len(df)}")


            # ---------------------------------------
            # PADRONIZA COLUNAS
            # ---------------------------------------

            df.columns = (
                df.columns
                .str.lower()
                .str.strip()
                .str.replace(" ", "_")
            )


            # ---------------------------------------
            # REMOVE LINHAS TOTALMENTE VAZIAS
            # ---------------------------------------

            df.dropna(how="all", inplace=True)


            # ---------------------------------------
            # REMOVE COLUNAS TOTALMENTE VAZIAS
            # ---------------------------------------

            df.dropna(axis=1, how="all", inplace=True)


            # ---------------------------------------
            # REMOVE DUPLICADOS
            # ---------------------------------------

            df.drop_duplicates(inplace=True)


            # ---------------------------------------
            # REMOVE ESPAÇOS EXTRAS
            # ---------------------------------------

            for col in df.select_dtypes(include="object").columns:

                df[col] = (
                    df[col]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                )


            print(f"✅ Registros após limpeza: {len(df)}")


            # ---------------------------------------
            # SALVAR CSV LIMPO
            # ---------------------------------------

            caminho_saida = os.path.join(output_folder, file)

            df.to_csv(
                caminho_saida,
                index=False,
                encoding="utf-8-sig"
            )

            print(f"💾 Arquivo salvo:")
            print(caminho_saida)

        except Exception as e:

            print(f"\n❌ Erro no arquivo: {file}")
            print(e)


print("\n🎯 LIMPEZA FINALIZADA")