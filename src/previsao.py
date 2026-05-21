from sklearn.linear_model import LinearRegression
import numpy as np

def prever_casos(df):
    print("🤖 Gerando previsão...")

    casos_ano = df.groupby("ano").size().reset_index()
    
    X = casos_ano["ano"].values.reshape(-1, 1)
    y = casos_ano[0].values

    modelo = LinearRegression()
    modelo.fit(X, y)

    proximo_ano = np.array([[X.max() + 1]])
    previsao = modelo.predict(proximo_ano)

    print(f"📈 Previsão para próximo ano: {int(previsao[0])} casos")

    return previsao[0]