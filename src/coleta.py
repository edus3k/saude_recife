import pandas as pd

def carregar_dados(caminho):
    """
    Função responsável por carregar os dados do arquivo.

    Parâmetros:
    caminho (str): caminho do arquivo CSV

    Retorna:
    DataFrame com os dados carregados
    """

    print("📥 Carregando dados do arquivo...")

    # Lê o arquivo CSV usando pandas
    df = pd.read_csv(caminho)

    # Retorna o DataFrame
    return df