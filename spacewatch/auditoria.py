"""
RASTREABILIDADE / HISTÓRICO DE USO do robô.

Um robô de RPA bem-feito é AUDITÁVEL: precisa registrar quem o acionou e
o que cada pessoa consultou. Toda ação relevante feita no dashboard fica
registrada aqui: QUEM fez, O QUE fez, DETALHE e QUANDO. Em um cenário real
(monitoramento de risco de asteroides) isso é essencial para saber quem
disparou cada análise. Reforça o critério "Arquitetura de Fluxo e
Engenharia de Software" da avaliação de AI for RPA.

Segue o mesmo padrão Repository do resto do projeto (sqlite3 + context
manager que abre/commita/fecha a conexão), gravando na mesma base
`spacewatch.db`, em uma tabela separada `auditoria`.
"""

import logging
import sqlite3
from contextlib import contextmanager
from datetime import datetime

logger = logging.getLogger(__name__)

# Colunas da tabela de auditoria, na ordem em que o banco devolve as linhas.
COLUNAS_AUDITORIA = ["id", "usuario", "acao", "detalhe", "data_hora"]


class Auditoria:
    """Registra e consulta o histórico de uso do sistema (quem fez o quê)."""

    def __init__(self, nome_do_banco: str = "spacewatch.db"):
        self.database_name = nome_do_banco
        self.criar_tabela()

    @contextmanager
    def _conectar(self):
        """Abre a conexão, commita ao fim do bloco e SEMPRE fecha."""
        conexao = sqlite3.connect(self.database_name)
        try:
            yield conexao
            conexao.commit()
        finally:
            conexao.close()

    def criar_tabela(self):
        """Cria a tabela de auditoria caso ainda não exista."""
        sql = """
            CREATE TABLE IF NOT EXISTS auditoria (
                id INTEGER PRIMARY KEY,
                usuario TEXT NOT NULL,
                acao TEXT NOT NULL,
                detalhe TEXT,
                data_hora TEXT NOT NULL
            )
        """
        with self._conectar() as conexao:
            conexao.execute(sql)

    def registrar(self, usuario: str, acao: str, detalhe: str = "") -> None:
        """Grava um evento de uso (quem, o quê, detalhe, quando)."""
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = (
            "INSERT INTO auditoria (usuario, acao, detalhe, data_hora) "
            "VALUES (?, ?, ?, ?)"
        )
        with self._conectar() as conexao:
            conexao.execute(sql, (usuario.strip(), acao, detalhe, agora))
        logger.info("Auditoria: %s -> %s (%s)", usuario, acao, detalhe)

    def listar(self, limite: int = 100) -> list:
        """Retorna os eventos mais recentes primeiro (até `limite` linhas)."""
        sql = "SELECT * FROM auditoria ORDER BY id DESC LIMIT ?"
        with self._conectar() as conexao:
            return conexao.execute(sql, (limite,)).fetchall()
