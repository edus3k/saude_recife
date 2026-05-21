import pandas as pd

def processar_dados(df):
    """
    Função responsável por transformar os dados em formato adequado.

    Parâmetros:
    df (DataFrame): dados limpos

    Retorna:
    DataFrame processado
    """

    print("⚙️ Processando dados...")

    # Converte a coluna de atendimentos para número
    df["atendimentos"] = pd.to_numeric(df["atendimentos"], errors="coerce")

    # Converte a coluna hora para formato datetime e extrai apenas a hora (0–23)
    df["hora"] = pd.to_datetime(df["hora"], errors="coerce").dt.hour

    # Remove possíveis valores inválidos gerados na conversão
    df = df.dropna()

    return df