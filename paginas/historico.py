"""Página de histórico de uso (auditoria / rastreabilidade)."""

import pandas as pd
import streamlit as st

from spacewatch.auditoria import COLUNAS_AUDITORIA, Auditoria


def exibir():
    st.title("📜 Histórico de uso")
    st.caption("Rastreabilidade do robô: quem usou o painel, o que fez e quando.")

    eventos = Auditoria().listar(limite=500)
    if not eventos:
        st.info("Ainda não há eventos registrados. Use o Painel para gerar histórico.")
        st.stop()

    hist = pd.DataFrame(eventos, columns=COLUNAS_AUDITORIA)

    usuarios = ["TODOS"] + sorted(hist["usuario"].unique().tolist())
    escolhido = st.sidebar.selectbox("Filtrar por usuário", usuarios)
    if escolhido != "TODOS":
        hist = hist[hist["usuario"] == escolhido]

    col1, col2, col3 = st.columns(3)
    col1.metric("Eventos registrados", len(hist))
    col2.metric("Execuções do robô", int((hist["acao"] == "Executou o robô").sum()))
    col3.metric("Consultas", int((hist["acao"] == "Consultou asteroides").sum()))

    st.subheader("Registros")
    st.dataframe(
        hist.rename(
            columns={
                "id": "#",
                "usuario": "Usuário",
                "acao": "Ação",
                "detalhe": "Detalhe",
                "data_hora": "Data/Hora",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )
