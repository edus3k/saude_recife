from dbfread import DBF
import pandas as pd
import os


# ---------------------------------------
# PASTAS
# ---------------------------------------

input_folder = "../data/dados_intermediarios/PAPE"

output_folder = "../data/dados_convertidos/PAPE"

os.makedirs(output_folder, exist_ok=True)


# ---------------------------------------
# LISTA ARQUIVOS
# ---------------------------------------

print(f"\n📂 Verificando pasta:")
print(input_folder)

arquivos = os.listdir(input_folder)

print(f"\n📄 Arquivos encontrados: {len(arquivos)}")


# ---------------------------------------
# LOOP DOS DBF
# ---------------------------------------

for file in arquivos:

    if file.lower().endswith(".dbf"):

        print("\n====================================")
        print(f"🔄 Convertendo: {file}")
        print("====================================")

        try:

            # Caminho DBF
            caminho_dbf = os.path.join(input_folder, file)

            print(f"📍 Caminho DBF:")
            print(caminho_dbf)


            # ---------------------------------------
            # LEITURA DBF
            # ---------------------------------------

            table = DBF(
                caminho_dbf,
                encoding="latin1",
                ignore_missing_memofile=True
            )

            print("✅ DBF lido")


            # ---------------------------------------
            # DATAFRAME
            # ---------------------------------------

            df = pd.DataFrame(iter(table))

            print(f"✅ DataFrame criado")
            print(f"📊 Total registros: {len(df)}")


            # ---------------------------------------
            # COLUNAS
            # ---------------------------------------

            df.columns = [col.lower() for col in df.columns]


            # ---------------------------------------
            # CSV
            # ---------------------------------------

            nome_csv = os.path.splitext(file)[0] + ".csv"

            caminho_csv = os.path.join(output_folder, nome_csv)

            print(f"📍 Salvando CSV:")
            print(caminho_csv)


            # ---------------------------------------
            # SALVAR
            # ---------------------------------------

            df.to_csv(
                caminho_csv,
                index=False,
                encoding="utf-8-sig"
            )

            print(f"✅ CSV salvo com sucesso!")

        except Exception as e:

            print("\n❌ ERRO DETALHADO:")
            print(type(e).__name__)
            print(e)


print("\n🎯 PROCESSAMENTO FINALIZADO")