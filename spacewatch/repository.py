"""
TÓPICO 2 do semestre: Arquivos & Database (SQLite).

Camada MODEL/Repository do MVC. Esta classe é praticamente igual à
"classe Repository" que o professor mostrou no slide de Restful APIs:
ela usa o módulo sqlite3 (que já vem no Python) para fazer o CRUD
(Create, Read, Update, Delete) num banco salvo em arquivo (.db).

Usamos placeholders (?) nas queries para evitar SQL Injection.

MELHORIA: a tabela tem uma restrição UNIQUE(neo_id, data_aproximacao)
e a inserção usa INSERT OR IGNORE. Assim o robô ACUMULA HISTÓRICO a
cada execução, sem criar registros duplicados do mesmo asteroide.
"""

import logging
import sqlite3

from .models import Asteroide

logger = logging.getLogger(__name__)


class Repository:
    """Responsável por todo o acesso ao banco de dados SQLite."""

    def __init__(self, nome_do_banco: str = "spacewatch.db"):
        self.database_name = nome_do_banco
        self.conexao = sqlite3.connect(nome_do_banco)
        self.cursor = self.conexao.cursor()
        self.criar_tabela()
        logger.info("Banco de dados iniciado (%s).", nome_do_banco)

    def criar_tabela(self):
        """Cria a tabela de asteroides caso ela ainda não exista.

        A restrição UNIQUE evita que o mesmo asteroide, na mesma data de
        aproximação, seja inserido duas vezes (permite manter histórico).
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
        self.cursor.execute(sql_create_table)
        self.conexao.commit()

    # ---------- CREATE ----------
    def inserir_asteroide(self, asteroide: Asteroide) -> bool:
        """Insere um asteroide. Devolve True se inseriu, False se já existia.

        Usa INSERT OR IGNORE: se o par (neo_id, data) já existir, o banco
        simplesmente ignora, mantendo o histórico sem duplicar.
        """
        sql_insert = """
            INSERT OR IGNORE INTO asteroides (
                neo_id, nome, data_aproximacao, diametro_min_m, diametro_max_m,
                velocidade_kmh, distancia_km, distancia_lunar,
                potencialmente_perigoso, pontuacao_risco, nivel_risco, anomalia
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.conexao = sqlite3.connect(self.database_name)
        self.cursor = self.conexao.cursor()
        self.cursor.execute(
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
        self.conexao.commit()
        # rowcount = 1 quando inseriu de fato; 0 quando ignorou (já existia).
        return self.cursor.rowcount == 1

    # ---------- READ ----------
    def selecionar_asteroides(self) -> list:
        """Retorna todos os asteroides cadastrados, do maior risco para o menor."""
        sql_select = "SELECT * FROM asteroides ORDER BY pontuacao_risco DESC"
        self.conexao = sqlite3.connect(self.database_name)
        self.cursor = self.conexao.cursor()
        self.cursor.execute(sql_select)
        return self.cursor.fetchall()

    def selecionar_por_nivel(self, nivel: str) -> list:
        """Retorna apenas os asteroides de um nível de risco específico."""
        sql_select = "SELECT * FROM asteroides WHERE nivel_risco = ?"
        self.conexao = sqlite3.connect(self.database_name)
        self.cursor = self.conexao.cursor()
        self.cursor.execute(sql_select, (nivel,))
        return self.cursor.fetchall()

    # ---------- DELETE ----------
    def limpar_tabela(self):
        """Apaga todos os registros (use só se quiser zerar o histórico)."""
        self.conexao = sqlite3.connect(self.database_name)
        self.cursor = self.conexao.cursor()
        self.cursor.execute("DELETE FROM asteroides")
        self.conexao.commit()
        logger.info("Histórico apagado (tabela zerada).")
