# ============================================
# CONSTANTES GLOBAIS
# utils/constantes.py
# ============================================

# ============================================
# PARQUETS
# ============================================

PAPE_FILE = (
    "data/dados_tratados/PAPE/PAPE_TOTAL.parquet"
)

PFPE_FILE = (
    "data/dados_tratados/PFPE/PFPE_TOTAL.parquet"
)

STPE_FILE = (
    "data/dados_tratados/STPE/STPE_TOTAL.parquet"
)

# ============================================
# MAPA UNIDADES RECIFE
# ============================================

MAPA_UNIDADES = {

    # ========================================
    # UPAS
    # ========================================

    "6488315":
        "UPA Caxangá",

    "2716538":
        "UPA Nova Descoberta",

    "2716546":
        "UPA Torrões",

    "2716554":
        "UPA Ibura",

    "2716562":
        "UPA Areias",

    "2716570":
        "UPA Engenho Velho",

    "2716589":
        "UPA Afogados",

    "2716597":
        "UPA Curado",

    # ========================================
    # HOSPITAIS
    # ========================================

    "2752321":
        "Hospital da Restauração",

    "2305112":
        "Hospital Getúlio Vargas",

    "2305228":
        "Hospital Otávio de Freitas",

    "2305309":
        "Hospital Barão de Lucena",

    "2304957":
        "Hospital Agamenon Magalhães",

    "2304779":
        "IMIP",

    "2304701":
        "PROCAPE",

    "2304833":
        "Hospital Oswaldo Cruz",

    "2304892":
        "Hospital Correia Picanço",

    "2304752":
        "Hospital Universitário Oswaldo Cruz",

    # ========================================
    # MATERNIDADES
    # ========================================

    "2304965":
        "Maternidade Bandeira Filho",

    "2304850":
        "Instituto Materno Infantil",

    "2304914":
        "Maternidade Professor Barros Lima",

    # ========================================
    # POLICLÍNICAS
    # ========================================

    "6508960":
        "Policlínica DS III",

    "6508510":
        "Policlínica DS VI",

    "6508120":
        "Policlínica Agamenon Magalhães",

    # ========================================
    # CAPS
    # ========================================

    "3456789":
        "CAPS Boa Vista",

    "3456790":
        "CAPS Casa Amarela",

    "3456791":
        "CAPS Afogados",

    # ========================================
    # USF
    # ========================================

    "0026395":
        "USF Tasso Bezerra",

    "2611600026352":
        "USF UR-2",

    "2611600026353":
        "USF Cohab",

    "2611600026354":
        "USF Brasília Teimosa"

}

# ============================================
# CNES RECIFE
# ============================================

CNES_RECIFE = list(
    MAPA_UNIDADES.keys()
)

# ============================================
# TIPOS UNIDADE
# ============================================

TIPOS_UNIDADE = {

    "UPA": [

        "6488315",
        "2716538",
        "2716546",
        "2716554",
        "2716562",
        "2716570",
        "2716589",
        "2716597"

    ],

    "Hospital": [

        "2752321",
        "2305112",
        "2305228",
        "2305309",
        "2304957",
        "2304779",
        "2304701",
        "2304833",
        "2304892",
        "2304752"

    ],

    "Maternidade": [

        "2304965",
        "2304850",
        "2304914"

    ],

    "Policlínica": [

        "6508960",
        "6508510",
        "6508120"

    ],

    "CAPS": [

        "3456789",
        "3456790",
        "3456791"

    ],

    "USF": [

        "0026395",
        "2611600026352",
        "2611600026353",
        "2611600026354"

    ]

}

# ============================================
# CORES DASHBOARD
# ============================================

CORES = {

    "primaria":
        "#2563eb",

    "secundaria":
        "#0f172a",

    "sucesso":
        "#16a34a",

    "alerta":
        "#f59e0b",

    "erro":
        "#dc2626",

    "info":
        "#06b6d4"

}

# ============================================
# CONFIG STREAMLIT
# ============================================

PAGE_CONFIG = {

    "page_title":
        "Saúde Recife Analytics",

    "page_icon":
        "🏥",

    "layout":
        "wide",

    "initial_sidebar_state":
        "expanded"

}

# ============================================
# ALTURAS PADRÃO
# ============================================

ALTURA_GRAFICO = 650

ALTURA_TABELA = 600

# ============================================
# TEMPLATES
# ============================================

TEMPLATE_PLOTLY = "plotly_white"

# ============================================
# TEXTOS
# ============================================

TEXTO_HOME = """

### Inteligência Analítica da Saúde Recife

Dashboard Integrado:

- Produção Ambulatorial
- Eficiência Operacional
- Ranking das Unidades
- Qualidade Assistencial
- Sobrecarga Hospitalar
- Evolução Temporal
- Indicadores Estratégicos

"""

# ============================================
# MÉTRICAS PADRÃO
# ============================================

METRICAS_PADRAO = [

    "total_atendimentos",

    "total_profissionais",

    "total_medicos",

    "qtd_leitos",

    "score_qualidade",

    "tempo_espera",

    "indice_sobrecarga",

    "score_eficiencia"

]

# ============================================
# COLUNAS EXIBIÇÃO
# ============================================

COLUNAS_EXIBICAO = [

    "nome_unidade",

    "ano",

    "mes",

    "total_atendimentos",

    "total_profissionais",

    "total_medicos",

    "qtd_leitos",

    "score_qualidade",

    "tempo_espera"

]

# ============================================
# MENSAGENS
# ============================================

MSG_SUCESSO = (
    "✅ Dashboard carregado com sucesso"
)

MSG_ERRO_DADOS = (
    "❌ Nenhum dado encontrado"
)

MSG_LOADING = (
    "⏳ Carregando dados..."
)

# ============================================
# ÍCONES
# ============================================

ICONES = {

    "ranking":
        "🏆",

    "evolucao":
        "📈",

    "sobrecarga":
        "🚨",

    "qualidade":
        "⭐",

    "hospital":
        "🏥",

    "medico":
        "👨‍⚕️",

    "tempo":
        "⏱️",

    "leito":
        "🛏️"

}

# ============================================
# MESES
# ============================================

MAPA_MESES = {

    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"

}

# ============================================
# STATUS OPERACIONAL
# ============================================

STATUS_OPERACIONAL = {

    "Excelente":
        "🟢",

    "Bom":
        "🟡",

    "Atenção":
        "🟠",

    "Crítico":
        "🔴"

}