# 🏥 Projeto Big Data — Qualidade de Atendimento nas UPAs

## 📌 Sobre o Projeto

Este projeto tem como objetivo realizar uma análise da qualidade de atendimento nas Unidades de Pronto Atendimento (UPAs) do Recife, utilizando técnicas de Big Data, análise de dados e visualização interativa.

A aplicação permite identificar:

- Eficiência das unidades
- Volume de atendimentos
- Tempo médio de espera
- Relação entre demanda e qualidade
- Evolução temporal dos atendimentos
- Profissionais mais eficientes
- Unidades mais sobrecarregadas

O sistema foi desenvolvido como projeto acadêmico da disciplina **TÓPICOS DE BIG DATA EM PYTHON**.

---

# 🎯 Objetivo

Analisar indicadores de desempenho das UPAs do Recife através de dashboards interativos e processamento de grandes volumes de dados, auxiliando na interpretação e tomada de decisão na área da saúde pública.

---

# 🗂️ Bases de Dados Utilizadas

## Portal Brasileiro de Dados Abertos

Dados públicos governamentais utilizados para complementar as análises.

https://dados.gov.br

---

## DataSUS — Ministério da Saúde

Base oficial contendo informações de saúde pública e atendimentos.

https://datasus.saude.gov.br

---

# 🚀 Tecnologias Utilizadas

- Python
- Pandas
- Streamlit
- DuckDB
- Plotly
- NumPy
- PyArrow

---

# 📁 Estrutura do Projeto

```bash
projeto_bigdata_saude/
│
├── data/
│   ├── pape.parquet
│   ├── pfpe.parquet
│   └── stpe.parquet
│
├── src/
│   ├── dashboard_saude_streamlit.py
│   │
│   ├── pages/
│   │   ├── 1_Indicadores.py
│   │   ├── 2_Ranking_Unidades.py
│   │   ├── 3_Qualidade_Demanda.py
│   │   ├── 4_Profissionais.py
│   │   └── 5_Evolucao_Temporal.py
│   │
│   ├── services/
│   │   ├── calculos.py
│   │   └── queries.py
│   │
│   └── utils/
│       └── constantes.py
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Instalação

## 1️⃣ Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd projeto_bigdata_saude
```

---

## 2️⃣ Criar Ambiente Virtual (Opcional)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / MacOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

---

# ▶️ Como Executar

## Executar o Dashboard

```bash
streamlit run .\app.py
```

ou

```bash
python -m streamlit run .\app.py
```

---

# 📊 Funcionalidades

## 📈 Indicadores Gerais

- Total de atendimentos
- Tempo médio de espera
- Índice de qualidade
- Taxa de eficiência

---

## 🏥 Ranking das Unidades

- Comparação entre unidades
- Unidades mais eficientes
- Unidades mais sobrecarregadas

---

## 📉 Qualidade x Demanda

- Relação entre demanda e qualidade
- Impacto da superlotação

---

## 👨‍⚕️ Análise dos Profissionais

- Profissionais com maior eficiência
- Volume de atendimentos
- Comparativos mensais

---

## 📅 Evolução Temporal

- Evolução mensal
- Evolução anual
- Tendências históricas

---

# 📦 Dependências Principais

## requirements.txt

```txt
streamlit
pandas
duckdb
plotly
numpy
pyarrow
```

---

# 🧠 Exemplo de Inicialização do Projeto

## dashboard_saude_streamlit.py

```python
import streamlit as st

st.set_page_config(
    page_title="Dashboard Saúde Recife",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Dashboard de Qualidade de Atendimento")
st.subheader("UPAs do Recife")

st.markdown("""
Este dashboard realiza análises de qualidade de atendimento,
demanda e eficiência das unidades de saúde.
""")
```

---

# 📌 Exemplo de Leitura dos Dados

```python
import pandas as pd

df = pd.read_parquet("data/pape.parquet")

print(df.head())
```

---

# 📈 Exemplo de Gráfico

```python
import plotly.express as px

fig = px.bar(
    df,
    x="unidade",
    y="atendimentos",
    title="Atendimentos por Unidade"
)

fig.show()
```

---

# 👨‍💻 Desenvolvedor

**Eduardo Santos**

Disciplina: **TÓPICOS DE BIG DATA EM PYTHON**

Orientador: **Davi Câmara**

Instituição: **Unidade Estácio Abdias de Carvalho - Recife/PE**

---

# 📌 Observações

- O projeto utiliza arquivos `.parquet` para otimizar o processamento de grandes volumes de dados.
- O dashboard foi desenvolvido para fins acadêmicos e analíticos.
- Todos os dados utilizados possuem origem pública.

---

# 📄 Licença

Projeto desenvolvido exclusivamente para fins educacionais e acadêmicos.