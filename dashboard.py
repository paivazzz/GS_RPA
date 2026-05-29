"""
DASHBOARD (Front End) — puxa o tópico da Disciplina 04 (Streamlit).

Interface visual que consome os dados que o robô coletou e salvou no
SQLite, exibindo gráficos, filtros e uma tabela — exatamente o que o
enunciado da Disciplina 04 pede: "componentes dinâmicos, gráficos
interativos e filtros que facilitem a tomada de decisão".

GOVERNANÇA (Disciplina 09): o usuário precisa se identificar (nome) e
toda ação relevante — executar o robô e consultar/filtrar — fica
registrada em um histórico de auditoria, visível em um clique.

Como rodar:
    poetry run streamlit run dashboard.py
    (ou)  streamlit run dashboard.py
"""

import pandas as pd
import streamlit as st

from spacewatch.auditoria import COLUNAS_AUDITORIA, Auditoria
from spacewatch.relatorio import COLUNAS
from spacewatch.repository import Repository
from spacewatch.rpa_bot import executar_monitoramento

# ----- Configuração da página -----
st.set_page_config(page_title="SpaceWatch RPA", page_icon="🛰️", layout="wide")
st.title("🛰️ SpaceWatch RPA — Monitor de Asteroides")
st.caption("Dados reais da NASA (NeoWs) • GS 2026.1 • AI for RPA — FIAP")

auditoria = Auditoria()


def carregar_dados() -> pd.DataFrame:
    """Lê o banco SQLite e devolve um DataFrame do pandas."""
    banco = Repository()
    linhas = banco.selecionar_asteroides()
    return pd.DataFrame(linhas, columns=COLUNAS)


# ----- Identificação do usuário (GOVERNANÇA) -----
st.sidebar.header("👤 Identificação")
usuario = st.sidebar.text_input("Seu nome", placeholder="Ex.: Maria Silva").strip()

if not usuario:
    st.info("👈 Digite seu nome na barra lateral para usar o painel. "
            "Tudo o que você fizer fica registrado no histórico de uso.")
    st.stop()

st.sidebar.success(f"Conectado como: {usuario}")

# ----- Barra lateral: ações do robô -----
st.sidebar.header("⚙️ Controle do Robô")
dias = st.sidebar.slider("Dias a monitorar", min_value=1, max_value=7, value=1)

if st.sidebar.button("▶️ Executar robô agora"):
    with st.spinner("Coletando dados da NASA..."):
        resumo = executar_monitoramento(dias=dias)
    auditoria.registrar(
        usuario,
        "Executou o robô",
        f"{dias} dia(s) • {resumo['total']} asteroides coletados • "
        f"{resumo['novos']} novos",
    )
    st.sidebar.success(f"{resumo['total']} asteroides coletados!")

# ----- Carrega os dados já salvos -----
df = carregar_dados()

if df.empty:
    st.warning("Nenhum dado ainda. Clique em '▶️ Executar robô agora' na lateral.")
    st.stop()

# ----- Filtro por nível de risco -----
niveis = ["TODOS"] + sorted(df["nivel_risco"].unique().tolist())
filtro = st.sidebar.selectbox("Filtrar por nível de risco", niveis)

# Registra a CONSULTA só quando o filtro realmente muda (o Streamlit
# re-executa o script a cada interação; sem esta guarda, gravaríamos
# o mesmo evento repetidas vezes).
chave_consulta = (usuario, filtro)
if st.session_state.get("ultima_consulta") != chave_consulta:
    auditoria.registrar(usuario, "Consultou asteroides", f"Filtro: {filtro}")
    st.session_state["ultima_consulta"] = chave_consulta

if filtro != "TODOS":
    df = df[df["nivel_risco"] == filtro]

# ----- Indicadores (cards) -----
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total de asteroides", len(df))
col2.metric("Risco CRÍTICO", int((df["nivel_risco"] == "CRITICO").sum()))
col3.metric("Risco ALTO", int((df["nivel_risco"] == "ALTO").sum()))
col4.metric("Potencialmente perigosos", int(df["potencialmente_perigoso"].sum()))
col5.metric("Anomalias 🚨", int(df["anomalia"].sum()))

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

# ----- Histórico de uso (GOVERNANÇA / auditoria) -----
st.divider()
st.subheader("📜 Histórico de uso (auditoria)")
st.caption("Rastreabilidade: quem usou o painel, o que fez e quando "
           "(Disciplina 09 — Governança em IA).")

if st.button("📜 Ver histórico de uso"):
    eventos = auditoria.listar(limite=100)
    if eventos:
        hist = pd.DataFrame(eventos, columns=COLUNAS_AUDITORIA)
        st.dataframe(hist, use_container_width=True, hide_index=True)
    else:
        st.info("Ainda não há eventos registrados.")
