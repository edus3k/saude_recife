import matplotlib.pyplot as plt

def plotar_graficos(df):
    print("📉 Gerando gráficos...")

    # Evolução
    df.groupby("ano").size().plot()
    plt.title("Evolução dos casos de feminicídio")
    plt.xlabel("Ano")
    plt.ylabel("Casos")
    plt.show()

    # Estados
    df["estado"].value_counts().head(10).plot(kind="bar")
    plt.title("Top 10 estados")
    plt.show()