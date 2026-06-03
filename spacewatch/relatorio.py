"""Gera o relatório dos asteroides em Excel/CSV com pandas."""

import logging

import pandas as pd

# Fonte única dos nomes das colunas (definidos no Repository, na mesma
# ordem em que o banco devolve as linhas). Reexportado aqui por
# compatibilidade com quem já importava de relatorio.
from .repository import COLUNAS

logger = logging.getLogger(__name__)


def gerar_excel(linhas: list, caminho: str = "relatorio_asteroides.xlsx") -> str:
    """Recebe as linhas do banco e escreve uma planilha Excel.

    Retorna o caminho do arquivo gerado.
    """
    # Monta um DataFrame (tabela) do pandas a partir das linhas do SQLite.
    df = pd.DataFrame(linhas, columns=COLUNAS)

    # Escreve no Excel sem a coluna de índice automática do pandas.
    df.to_excel(caminho, index=False, sheet_name="Asteroides")

    logger.info("Planilha gerada: %s (%d asteroides)", caminho, len(df))
    return caminho


def gerar_csv(linhas: list, caminho: str = "relatorio_asteroides.csv") -> str:
    """Versão alternativa em CSV (também vista em aula com pandas)."""
    df = pd.DataFrame(linhas, columns=COLUNAS)
    df.to_csv(caminho, index=False, encoding="utf-8")
    logger.info("CSV gerado: %s", caminho)
    return caminho
