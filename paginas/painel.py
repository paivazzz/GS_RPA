"""
Página PAINEL — monitoramento de asteroides.

Cards de indicadores, gráficos interativos, filtro por nível de risco e o
botão que dispara o robô. É a "carga de dados estruturados para o front-end"
(critério de Entrega de Artefatos de AI for RPA).
"""

import pandas as pd
import streamlit as st

from spacewatch.auditoria import Auditoria
from spacewatch.relatorio import COLUNAS
from spacewatch.repository import Repository
from spacewatch.rpa_bot import executar_monitoramento


def _carregar_dados() -> pd.DataFrame:
    """Lê o banco SQLite e devolve um DataFrame do pandas."""
    banco = Repository()
    return pd.DataFrame(banco.selecionar_asteroides(), columns=COLUNAS)


def exibir():
    usuario = st.session_state["usuario"]
    auditoria = Auditoria()

    st.title("🛰️ Painel de Monitoramento")
    st.caption("Dados reais da NASA (NeoWs) • GS 2026.1 • AI for RPA — FIAP")

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
        if resumo["total"] == 0:
            st.sidebar.warning(
                "A NASA não retornou dados agora (pode ser o limite da "
                "DEMO_KEY). Tente de novo em instantes."
            )
        else:
            st.sidebar.success(f"{resumo['total']} asteroides coletados!")

    # ----- Carrega os dados já salvos -----
    df = _carregar_dados()
    if df.empty:
        st.warning("Nenhum dado ainda. Clique em '▶️ Executar robô agora' na lateral.")
        st.stop()

    # ----- Filtro por nível de risco -----
    niveis = ["TODOS"] + sorted(df["nivel_risco"].unique().tolist())
    filtro = st.sidebar.selectbox("Filtrar por nível de risco", niveis)

    # Registra a CONSULTA só quando o filtro realmente muda (o Streamlit
    # re-executa o script a cada interação; sem esta guarda gravaríamos
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
    st.bar_chart(df["nivel_risco"].value_counts())

    # ----- Gráfico: distância x tamanho -----
    st.subheader("🌑 Distância (em distâncias lunares) x Tamanho (m)")
    st.scatter_chart(df, x="distancia_lunar", y="diametro_max_m", color="nivel_risco")

    # ----- Tabela detalhada -----
    st.subheader("📋 Dados detalhados")
    st.dataframe(df, use_container_width=True, hide_index=True)
