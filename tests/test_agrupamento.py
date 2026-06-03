"""Testes do agrupamento por perfil (K-Means)."""

import pytest

from spacewatch.repository import COLUNAS

pytest.importorskip("sklearn")

from spacewatch.agrupamento import agrupar_por_perfil


def _linha(neo, pontuacao, diametro, dist, vel):
    valores = {
        "id": 0, "neo_id": neo, "nome": f"({neo})", "data_aproximacao": "2026-06-01",
        "diametro_min_m": diametro / 2, "diametro_max_m": diametro,
        "velocidade_kmh": vel, "distancia_km": dist * 384400,
        "distancia_lunar": dist, "potencialmente_perigoso": 0,
        "pontuacao_risco": pontuacao, "nivel_risco": "BAIXO", "anomalia": 0,
    }
    return tuple(valores[c] for c in COLUNAS)


def test_agrupa_em_perfis_distintos():
    # Dois blocos bem separados: baixo risco x alto risco.
    linhas = [
        _linha("1", 10, 50, 50, 20000),
        _linha("2", 12, 60, 45, 22000),
        _linha("3", 90, 900, 1, 110000),
        _linha("4", 88, 950, 2, 105000),
    ]
    df = agrupar_por_perfil(linhas, n_clusters=2)

    assert "cluster" in df.columns
    assert "perfil" in df.columns
    assert df["cluster"].nunique() == 2
    # Os dois de baixo risco no mesmo grupo; os dois de alto risco no outro.
    assert df.iloc[0]["cluster"] == df.iloc[1]["cluster"]
    assert df.iloc[2]["cluster"] == df.iloc[3]["cluster"]
    assert df.iloc[0]["cluster"] != df.iloc[2]["cluster"]


def test_poucos_dados_viram_grupo_unico():
    df = agrupar_por_perfil([_linha("1", 10, 50, 50, 20000)], n_clusters=3)
    assert df["perfil"].tolist() == ["Grupo único"]
