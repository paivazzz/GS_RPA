"""App Streamlit (front-end): identificação do usuário e navegação entre páginas."""

import streamlit as st

from paginas import agrupamento, historico, painel

st.set_page_config(page_title="SpaceWatch RPA", page_icon="🛰️", layout="wide")

st.sidebar.header("👤 Identificação")
nome_digitado = st.sidebar.text_input("Seu nome", key="nome_input",
                                       placeholder="Ex.: Maria Silva")
usuario = nome_digitado.strip()

if not usuario:
    st.title("🛰️ SpaceWatch RPA")
    st.info("👈 Digite seu nome na barra lateral para usar o sistema. "
            "Tudo o que você fizer fica registrado no histórico de uso.")
    st.stop()

st.session_state["usuario"] = usuario
st.sidebar.success(f"Conectado como: {usuario}")

navegacao = st.navigation(
    [
        st.Page(painel.exibir, title="Painel", icon="🛰️",
                url_path="painel", default=True),
        st.Page(agrupamento.exibir, title="Agrupamento (IA)", icon="🧩",
                url_path="agrupamento"),
        st.Page(historico.exibir, title="Histórico de uso", icon="📜",
                url_path="historico"),
    ]
)
navegacao.run()
