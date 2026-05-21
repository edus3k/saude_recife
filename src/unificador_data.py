import pandas as pd
import os

pasta = "data/dados_tratados/"
dfs = []

for file in os.listdir(pasta):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(pasta, file))
        dfs.append(df)

df_final = pd.concat(dfs, ignore_index=True)

df_final.to_csv("data/dados_tratados/dados_unificados.csv", index=False)

print("✅ Dados unificados!")