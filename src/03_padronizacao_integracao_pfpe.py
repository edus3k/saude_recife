# ============================================
# PADRONIZAÇÃO PFPE - BIG DATA
# ============================================

import pandas as pd
import os


# ============================================
# PASTAS
# ============================================

input_folder = "../data/dados_limpos/PFPE"

output_folder = "../data/dados_tratados/PFPE"

os.makedirs(output_folder, exist_ok=True)


# ============================================
# LISTAR ARQUIVOS
# ============================================

arquivos = os.listdir(input_folder)

print("\n===================================")
print("📂 PROCESSAMENTO BIG DATA PFPE")
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
                .str.replace(" ", "_")
                .str.replace("-", "_")
            )


            # ============================================
            # REMOVE DUPLICADOS
            # ============================================

            df.drop_duplicates(inplace=True)


            # ============================================
            # REMOVE LINHAS VAZIAS
            # ============================================

            df.dropna(how="all", inplace=True)


            # ============================================
            # COLUNAS TEXTO
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
            # COLUNAS NUMÉRICAS
            # ============================================

            colunas_numericas = [

                "idade",
                "quantidade",
                "valor",
                "valor_total",
                "qtd_aprovada"

            ]

            for col in colunas_numericas:

                if col in df.columns:

                    df[col] = pd.to_numeric(
                        df[col],
                        errors="coerce",
                        downcast="float"
                    )


            # ============================================
            # TRATAMENTO DE COMPETÊNCIA
            # ============================================

            possiveis_competencias = [

                "competencia",
                "pa_cmp",
                "mes_ano"

            ]

            for col in possiveis_competencias:

                if col in df.columns:

                    df[col] = df[col].astype(str)

                    df["ano"] = df[col].str[:4]

                    df["mes"] = df[col].str[4:6]


            # ============================================
            # MUNICÍPIO
            # ============================================

            possiveis_municipios = [

                "municipio",
                "mun_res",
                "pa_munpcn"

            ]

            for col in possiveis_municipios:

                if col in df.columns:

                    df[col] = (
                        df[col]
                        .astype(str)
                        .str.strip()
                        .str.upper()
                    )


            # ============================================
            # CID
            # ============================================

            possiveis_cid = [

                "cid",
                "cid10",
                "pa_cidpri"

            ]

            for col in possiveis_cid:

                if col in df.columns:

                    df[col] = (
                        df[col]
                        .astype(str)
                        .str.strip()
                        .str.upper()
                    )


            # ============================================
            # SEXO
            # ============================================

            possiveis_sexo = [

                "sexo",
                "pa_sexo"

            ]

            for col in possiveis_sexo:

                if col in df.columns:

                    df[col] = (
                        df[col]
                        .astype(str)
                        .str.upper()
                    )


            # ============================================
            # FAIXA ETÁRIA
            # ============================================

            if "idade" in df.columns:

                bins = [0, 12, 18, 30, 45, 60, 200]

                labels = [
                    "CRIANCA",
                    "ADOLESCENTE",
                    "JOVEM",
                    "ADULTO",
                    "MEIA_IDADE",
                    "IDOSO"
                ]

                df["faixa_etaria"] = pd.cut(
                    df["idade"],
                    bins=bins,
                    labels=labels
                )


            # ============================================
            # COLUNA ORIGEM
            # ============================================

            df["arquivo_origem"] = file


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