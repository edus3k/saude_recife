# Importa funções dos outros módulos
from coleta import carregar_dados
from limpeza import limpar_dados
from processamento import processar_dados
from analise import gerar_resumo

def executar_etl():
    """
    Função principal que executa todo o pipeline ETL:
    - Extract (coleta)
    - Transform (limpeza + processamento)
    - Load (salvar dados)
    """

    print("🚀 Iniciando ETL...")

    # -------------------------
    # EXTRACT (Coleta de dados)
    # -------------------------
    # Carrega o arquivo CSV tratado ou bruto
    df = carregar_dados("data/dados_tratados/dados_tratados.csv")

    # -------------------------
    # TRANSFORM (Limpeza)
    # -------------------------
    # Remove erros, valores nulos e padroniza colunas
    df = limpar_dados(df)

    # -------------------------
    # TRANSFORM (Processamento)
    # -------------------------
    # Converte tipos e prepara os dados para análise
    df = processar_dados(df)

    # -------------------------
    # ANALYSE (Resumo)
    # -------------------------
    # Agrupa dados para gerar informações úteis
    resumo = gerar_resumo(df)

    # -------------------------
    # LOAD (Salvar resultado)
    # -------------------------
    # Salva o resumo em CSV
    resumo.to_csv("data/dados_tratados/resumo.csv", index=False)

    print("✅ ETL finalizado com sucesso!")


# Executa o ETL quando rodar o arquivo
if __name__ == "__main__":
    executar_etl()