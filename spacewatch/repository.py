"""Camada de banco de dados (SQLite) com o padrão Repository."""

import logging
import sqlite3
from contextlib import contextmanager

from .models import Asteroide

logger = logging.getLogger(__name__)

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


class Repository:
    """Responsável por todo o acesso ao banco de dados SQLite."""

    def __init__(self, nome_do_banco: str = "spacewatch.db"):
        self.database_name = nome_do_banco
        self.criar_tabela()
        logger.info("Banco de dados iniciado (%s).", nome_do_banco)

    @contextmanager
    def _conectar(self):

        conexao = sqlite3.connect(self.database_name)
        try:
            yield conexao
            conexao.commit()
        finally:
            conexao.close()

    def criar_tabela(self):
        """Cria a tabela de asteroides caso ela ainda não exista.
        """
        sql_create_table = """
            CREATE TABLE IF NOT EXISTS asteroides (
                id INTEGER PRIMARY KEY,
                neo_id TEXT,
                nome TEXT NOT NULL,
                data_aproximacao TEXT,
                diametro_min_m REAL,
                diametro_max_m REAL,
                velocidade_kmh REAL,
                distancia_km REAL,
                distancia_lunar REAL,
                potencialmente_perigoso INTEGER,
                pontuacao_risco INTEGER,
                nivel_risco TEXT,
                anomalia INTEGER,
                UNIQUE(neo_id, data_aproximacao)
            )
        """
        with self._conectar() as conexao:
            conexao.execute(sql_create_table)

    def inserir_asteroide(self, asteroide: Asteroide) -> bool:
        """Insere um asteroide. Devolve True se inseriu, False se já existia.
        """
        sql_insert = """
            INSERT OR IGNORE INTO asteroides (
                neo_id, nome, data_aproximacao, diametro_min_m, diametro_max_m,
                velocidade_kmh, distancia_km, distancia_lunar,
                potencialmente_perigoso, pontuacao_risco, nivel_risco, anomalia
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self._conectar() as conexao:
            cursor = conexao.execute(
                sql_insert,
                (
                    asteroide.neo_id,
                    asteroide.nome,
                    asteroide.data_aproximacao,
                    asteroide.diametro_min_m,
                    asteroide.diametro_max_m,
                    asteroide.velocidade_kmh,
                    asteroide.distancia_km,
                    asteroide.distancia_lunar,
                    int(asteroide.potencialmente_perigoso),
                    asteroide.pontuacao_risco,
                    asteroide.nivel_risco,
                    int(bool(asteroide.anomalia)),
                ),
            )
            # rowcount = 1 quando inseriu de fato; 0 quando ignorou (já existia).
            return cursor.rowcount == 1

    def selecionar_asteroides(self) -> list:
        """Retorna todos os asteroides cadastrados, do maior risco para o menor."""
        sql_select = "SELECT * FROM asteroides ORDER BY pontuacao_risco DESC"
        with self._conectar() as conexao:
            return conexao.execute(sql_select).fetchall()

    def selecionar_por_nivel(self, nivel: str) -> list:
        """Retorna apenas os asteroides de um nível de risco específico."""
        sql_select = (
            "SELECT * FROM asteroides WHERE nivel_risco = ? "
            "ORDER BY pontuacao_risco DESC"
        )
        with self._conectar() as conexao:
            return conexao.execute(sql_select, (nivel,)).fetchall()

    def limpar_tabela(self):
        """Apaga todos os registros (use só se quiser zerar o histórico)."""
        with self._conectar() as conexao:
            conexao.execute("DELETE FROM asteroides")
        logger.info("Histórico apagado (tabela zerada).")
