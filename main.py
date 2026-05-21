# ============================================
# MAIN - PROJETO SAÚDE RECIFE
# ============================================
# Executa automaticamente:
#
# 1. Padronização
# 2. Consolidação
# 3. Validação
# 4. Camada Analítica
# 5. Dashboard Streamlit
# ============================================

import os
import subprocess
import time

# ============================================
# FUNÇÃO EXECUÇÃO
# ============================================

def executar(script):

    print("\n===================================")
    print(f"🚀 EXECUTANDO: {script}")
    print("===================================")

    try:

        resultado = subprocess.run(
            ["python", script],
            check=True
        )

        print(f"✅ FINALIZADO: {script}")

    except subprocess.CalledProcessError as e:

        print(f"❌ ERRO EM: {script}")
        print(e)

# ============================================
# LISTA DE PROCESSOS
# ============================================

scripts = [

    # ========================================
    # PAPE
    # ========================================

    "src/03_padronizacao_integracao_pape.py",
    "src/04_consolidar_pape_parquet.py",
    "src/05_validar_pape_total.py",
    "src/06_camadas_analiticas_pape.py",

    # ========================================
    # PFPE
    # ========================================

    "src/03_padronizacao_integracao_pfpe.py",
    "src/04_consolidar_pfpe_parquet.py",
    "src/05_validar_pfpe_total.py",
    "src/06_camadas_analiticas_pfpe.py",

    # ========================================
    # STPE
    # ========================================

    "src/03_padronizacao_integracao_stpe.py",
    "src/04_consolidar_stpe_parquet.py",
    "src/05_validar_stpe_total.py",
    "src/06_camadas_analiticas_stpe.py"
]

# ============================================
# EXECUÇÃO DOS PROCESSOS
# ============================================

inicio = time.time()

for script in scripts:

    if os.path.exists(script):

        executar(script)

    else:

        print(f"⚠️ Arquivo não encontrado: {script}")

fim = time.time()

# ============================================
# TEMPO TOTAL
# ============================================

tempo_total = (fim - inicio) / 60

print("\n===================================")
print("🎯 PIPELINE FINALIZADA")
print("===================================")

print(f"\n⏱ Tempo total: {tempo_total:.2f} minutos")

# ============================================
# STREAMLIT
# ============================================

print("\n🚀 ABRINDO DASHBOARD STREAMLIT...")

subprocess.run([
    "streamlit",
    "run",
    "src/dashboard_saude_streamlit.py"
])