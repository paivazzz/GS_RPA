"""
APP (front-end / output) em Streamlit — ponto de entrada multipágina.

Este arquivo faz duas coisas:
1. O "portão" de IDENTIFICAÇÃO: a pessoa precisa digitar o nome para usar
   o sistema (vale para todas as páginas). Isso dá rastreabilidade: tudo
   o que cada usuário faz fica registrado no histórico de uso.
2. A NAVEGAÇÃO entre as páginas (st.navigation), com um menu na lateral:
   - 🛰️ Painel        -> monitoramento de asteroides (paginas/painel.py)
   - 📜 Histórico de uso -> auditoria/rastreabilidade (paginas/historico.py)

Como rodar:
    poetry run streamlit run dashboard.py
    (ou)  streamlit run dashboard.py
"""

import streamlit as st

from paginas import historico, painel

# ----- Configuração da página (uma vez, antes da navegação) -----
st.set_page_config(page_title="SpaceWatch RPA", page_icon="🛰️", layout="wide")

# ----- Portão de identificação (rastreabilidade), compartilhado -----
st.sidebar.header("👤 Identificação")
nome_digitado = st.sidebar.text_input("Seu nome", key="nome_input",
                                       placeholder="Ex.: Maria Silva")
usuario = nome_digitado.strip()

if not usuario:
    st.title("🛰️ SpaceWatch RPA")
    st.info("👈 Digite seu nome na barra lateral para usar o sistema. "
            "Tudo o que você fizer fica registrado no histórico de uso.")
    st.stop()

# Disponibiliza o nome (já normalizado) para todas as páginas.
st.session_state["usuario"] = usuario
st.sidebar.success(f"Conectado como: {usuario}")

# ----- Navegação entre páginas -----
navegacao = st.navigation(
    [
        st.Page(painel.exibir, title="Painel", icon="🛰️",
                url_path="painel", default=True),
        st.Page(historico.exibir, title="Histórico de uso", icon="📜",
                url_path="historico"),
    ]
)
navegacao.run()
