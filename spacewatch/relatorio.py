"""
Geração de relatório em Excel/CSV usando pandas.

Complementa o TÓPICO de Arquivos: além do banco de dados (SQLite),
o robô gera uma PLANILHA (.xlsx) que qualquer pessoa abre no Excel,
exatamente como o slide "Manipulando Arquivos Excel com Pandas".

Isso é o "entregável" visual do RPA: um relatório pronto para a
tomada de decisão.
"""

import logging

import pandas as pd

logger = logging.getLogger(__name__)

# Nomes das colunas, na mesma ordem em que o Repository devolve as linhas.
COLUNAS = [
    "id",
    "neo_id",
    "nome",
    "data_aproximacao",
    "diametro_min_m",
    "diametro_max_m",
    "velocidade_kmh",
    "distancia_km",
    "distancia_lunar",
    "potencialmente_perigoso",
    "pontuacao_risco",
    "nivel_risco",
    "anomalia",
]


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
