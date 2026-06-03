"""Testes da auditoria / histórico de uso."""

from spacewatch.auditoria import COLUNAS_AUDITORIA, Auditoria


def test_registrar_e_listar(tmp_path):
    """Registrar dois eventos e listar deve trazê-los do mais recente p/ o antigo."""
    banco = str(tmp_path / "teste.db")
    aud = Auditoria(banco)

    aud.registrar("Maria", "Executou o robô", "7 dias")
    aud.registrar("Joao", "Consultou asteroides", "Filtro: CRITICO")

    eventos = aud.listar()
    assert len(eventos) == 2

    # listar() ordena por id DESC -> o último registrado vem primeiro.
    primeiro = dict(zip(COLUNAS_AUDITORIA, eventos[0]))
    assert primeiro["usuario"] == "Joao"
    assert primeiro["acao"] == "Consultou asteroides"
    assert primeiro["data_hora"]  # carimbo de data/hora preenchido


def test_limite_de_listagem(tmp_path):
    """O parâmetro `limite` deve cortar a quantidade de eventos retornados."""
    aud = Auditoria(str(tmp_path / "teste.db"))
    for i in range(5):
        aud.registrar("Tester", "Consultou asteroides", f"evento {i}")

    assert len(aud.listar(limite=3)) == 3
    assert len(aud.listar()) == 5


def test_nome_e_normalizado(tmp_path):
    """Espaços em volta do nome devem ser removidos ao gravar."""
    aud = Auditoria(str(tmp_path / "teste.db"))
    aud.registrar("  Ana  ", "Executou o robô", "")

    evento = dict(zip(COLUNAS_AUDITORIA, aud.listar()[0]))
    assert evento["usuario"] == "Ana"
