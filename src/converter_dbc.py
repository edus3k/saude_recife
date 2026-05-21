# ---------------------------------------
# IMPORTAÇÃO DE BIBLIOTECAS
# ---------------------------------------

# Biblioteca para ler arquivos DBF (formato do DATASUS após conversão)
from dbfread import DBF

# Biblioteca para manipulação de dados
import pandas as pd

# Biblioteca para trabalhar com caminhos de arquivos
import os


# ---------------------------------------
# DEFINIÇÃO DE PASTAS
# ---------------------------------------

# Pasta onde estão os arquivos convertidos (.dbf)
input_folder = "data/dados_bruto/convertidos_dbf"

# Pasta onde serão salvos os arquivos finais (.csv)
output_folder = "data/dados_intermediarios"

# Cria a pasta de saída caso não exista
os.makedirs(output_folder, exist_ok=True)


# ---------------------------------------
# LOOP PARA LER TODOS OS ARQUIVOS DBF
# ---------------------------------------

# Percorre todos os arquivos da pasta de entrada
for file in os.listdir(input_folder):

    # Verifica se o arquivo é do tipo .dbf
    if file.endswith(".dbf"):

        # Exibe mensagem informando qual arquivo está sendo processado
        print(f"🔄 Lendo arquivo: {file}")

        # Cria o caminho completo do arquivo
        caminho_dbf = os.path.join(input_folder, file)

        # ---------------------------------------
        # LEITURA DO ARQUIVO DBF
        # ---------------------------------------

        # Lê o arquivo DBF usando codificação latin1 (padrão DATASUS)
        table = DBF(caminho_dbf, encoding="latin1")

        # Converte os dados para DataFrame (estrutura de tabela do pandas)
        df = pd.DataFrame(iter(table))


        # ---------------------------------------
        # TRATAMENTO BÁSICO (OPCIONAL)
        # ---------------------------------------

        # Padroniza nomes das colunas para minúsculo
        df.columns = [col.lower() for col in df.columns]


        # ---------------------------------------
        # SALVAR COMO CSV
        # ---------------------------------------

        # Cria nome do arquivo CSV baseado no original
        nome_csv = file.replace(".dbf", ".csv")

        # Define o caminho de saída
        caminho_csv = os.path.join(output_folder, nome_csv)

        # Salva o DataFrame em formato CSV
        df.to_csv(caminho_csv, index=False)


        # ---------------------------------------
        # FINALIZAÇÃO
        # ---------------------------------------

        print(f"✅ Arquivo convertido: {nome_csv}")