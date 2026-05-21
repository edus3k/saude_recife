def gerar_resumo(df):
    """
    Função que realiza análise dos dados.

    Parâmetros:
    df (DataFrame): dados processados

    Retorna:
    DataFrame com resumo das análises
    """

    print("📊 Gerando análise...")

    # Agrupa por especialidade e soma os atendimentos
    resumo = df.groupby("especialidade")["atendimentos"].sum().reset_index()

    # Ordena do maior para o menor
    resumo = resumo.sort_values(by="atendimentos", ascending=False)

    return resumo