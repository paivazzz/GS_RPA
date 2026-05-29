"""
Testes da geração de arquivos (Excel/CSV) com pandas, em pasta temporária.
"""

import pandas as pd

from spacewatch.relatorio import COLUNAS, gerar_csv, gerar_excel


def _linha():
    """Uma linha no formato que o Repository devolve (uma posição por coluna)."""
    return tuple(range(len(COLUNAS)))


def test_gerar_excel(tmp_path):
    caminho = str(tmp_path / "r.xlsx")
    retorno = gerar_excel([_linha()], caminho)

    assert retorno == caminho
    df = pd.read_excel(caminho)
    assert list(df.columns) == COLUNAS
    assert len(df) == 1


def test_gerar_csv(tmp_path):
    caminho = str(tmp_path / "r.csv")
    gerar_csv([_linha()], caminho)

    df = pd.read_csv(caminho)
    assert list(df.columns) == COLUNAS
    assert len(df) == 1
