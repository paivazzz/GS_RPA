"""
DASHBOARD (Front End) — puxa o tópico da Disciplina 04 (Streamlit).

Interface visual que consome os dados que o robô coletou e salvou no
SQLite, exibindo gráficos, filtros e uma tabela — exatamente o que o
enunciado da Disciplina 04 pede: "componentes dinâmicos, gráficos
interativos e filtros que facilitem a tomada de decisão".

Como rodar:
    poetry run streamlit run dashboard.py
    (ou)  streamlit run dashboard.py
"""

import pandas as pd
import streamlit as st

from spacewatch.relatorio import COLUNAS
from spacewatch.repository import Repository
from spacewatch.rpa_bot import executar_monitoramento

# ----- Configuração da página -----
st.set_page_config(page_title="SpaceWatch RPA", page_icon="🛰️", layout="wide")
st.title("🛰️ SpaceWatch RPA — Monitor de Asteroides")
st.caption("Dados reais da NASA (NeoWs) • GS 2026.1 • AI for RPA — FIAP")


def carregar_dados() -> pd.DataFrame:
    """Lê o banco SQLite e devolve um DataFrame do pandas."""
    banco = Repository()
    linhas = banco.selecionar_asteroides()
    return pd.DataFrame(linhas, columns=COLUNAS)


# ----- Barra lateral: ações do robô -----
st.sidebar.header("⚙️ Controle do Robô")
dias = st.sidebar.slider("Dias a monitorar", min_value=1, max_value=7, value=1)

if st.sidebar.button("▶️ Executar robô agora"):
    with st.spinner("Coletando dados da NASA..."):
        resumo = executar_monitoramento(dias=dias)
    st.sidebar.success(f"{resumo['total']} asteroides coletados!")

# ----- Carrega os dados já salvos -----
df = carregar_dados()

if df.empty:
    st.warning("Nenhum dado ainda. Clique em '▶️ Executar robô agora' na lateral.")
    st.stop()

# ----- Filtro por nível de risco -----
niveis = ["TODOS"] + sorted(df["nivel_risco"].unique().tolist())
filtro = st.sidebar.selectbox("Filtrar por nível de risco", niveis)
if filtro != "TODOS":
    df = df[df["nivel_risco"] == filtro]

# ----- Indicadores (cards) -----
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de asteroides", len(df))
col2.metric("Risco CRÍTICO", int((df["nivel_risco"] == "CRITICO").sum()))
col3.metric("Risco ALTO", int((df["nivel_risco"] == "ALTO").sum()))
col4.metric("Potencialmente perigosos", int(df["potencialmente_perigoso"].sum()))

# ----- Gráfico: quantidade por nível de risco -----
st.subheader("📊 Asteroides por nível de risco")
contagem = df["nivel_risco"].value_counts()
st.bar_chart(contagem)

# ----- Gráfico: distância x tamanho -----
st.subheader("🌑 Distância (em distâncias lunares) x Tamanho (m)")
st.scatter_chart(
    df,
    x="distancia_lunar",
    y="diametro_max_m",
    color="nivel_risco",
)

# ----- Tabela detalhada -----
st.subheader("📋 Dados detalhados")
st.dataframe(df, use_container_width=True)
