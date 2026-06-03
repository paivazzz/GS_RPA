"""Testes do Repository (CRUD em SQLite)."""

from spacewatch.models import Asteroide
from spacewatch.repository import COLUNAS, Repository


def _asteroide(neo="1", data="2026-06-01", nivel="BAIXO", pontuacao=10):
    """Cria um Asteroide já classificado para os testes."""
    return Asteroide(
        neo_id=neo, nome="(x)", data_aproximacao=data,
        diametro_min_m=1.0, diametro_max_m=2.0, velocidade_kmh=1000.0,
        distancia_km=1000.0, distancia_lunar=5.0, potencialmente_perigoso=False,
        pontuacao_risco=pontuacao, nivel_risco=nivel, anomalia=False,
    )


def test_inserir_e_deduplicar(tmp_path):
    """O mesmo (neo_id, data) não pode ser inserido duas vezes."""
    repo = Repository(str(tmp_path / "t.db"))
    assert repo.inserir_asteroide(_asteroide()) is True
    assert repo.inserir_asteroide(_asteroide()) is False
    assert len(repo.selecionar_asteroides()) == 1


def test_selecao_ordena_por_risco(tmp_path):
    """selecionar_asteroides deve vir do maior risco para o menor."""
    repo = Repository(str(tmp_path / "t.db"))
    repo.inserir_asteroide(_asteroide(neo="1", pontuacao=10))
    repo.inserir_asteroide(_asteroide(neo="2", pontuacao=90, nivel="CRITICO"))

    linhas = repo.selecionar_asteroides()
    idx = COLUNAS.index("pontuacao_risco")
    assert linhas[0][idx] == 90  # o de maior risco vem primeiro


def test_filtro_por_nivel(tmp_path):
    repo = Repository(str(tmp_path / "t.db"))
    repo.inserir_asteroide(_asteroide(neo="1", nivel="BAIXO"))
    repo.inserir_asteroide(_asteroide(neo="2", nivel="CRITICO", pontuacao=90))

    assert len(repo.selecionar_por_nivel("CRITICO")) == 1
    assert len(repo.selecionar_por_nivel("BAIXO")) == 1


def test_limpar_tabela(tmp_path):
    repo = Repository(str(tmp_path / "t.db"))
    repo.inserir_asteroide(_asteroide())
    repo.limpar_tabela()
    assert repo.selecionar_asteroides() == []
