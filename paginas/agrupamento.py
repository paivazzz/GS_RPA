"""Página de agrupamento de asteroides por perfil (K-Means)."""

import streamlit as st

from spacewatch.agrupamento import FEATURES, agrupar_por_perfil
from spacewatch.repository import Repository


def exibir():
    st.title("🧩 Agrupamento por perfil (K-Means)")
    st.caption(
        "Aprendizado não supervisionado: agrupa asteroides com características "
        "semelhantes (risco, tamanho, distância e velocidade)."
    )

    linhas = Repository().selecionar_asteroides()
    if not linhas:
        st.info("Ainda não há dados. Gere a coleta no Painel primeiro.")
        st.stop()

    n = st.sidebar.slider("Número de grupos (k)", min_value=2, max_value=5, value=3)

    try:
        df = agrupar_por_perfil(linhas, n_clusters=n)
    except ImportError as erro:
        st.error(str(erro))
        st.stop()

    st.subheader("🌑 Distribuição dos grupos")
    st.scatter_chart(df, x="distancia_lunar", y="diametro_max_m", color="perfil")

    st.subheader("📊 Média de cada perfil")
    resumo = df.groupby("perfil")[FEATURES].mean().round(1).reset_index()
    st.dataframe(resumo, use_container_width=True, hide_index=True)

    st.subheader("📋 Asteroides por grupo")
    colunas = ["nome", "perfil", "pontuacao_risco", "nivel_risco"] + FEATURES[1:]
    st.dataframe(df[colunas], use_container_width=True, hide_index=True)
