"""
TÓPICO 2 do semestre: Arquivos & Database (SQLite).

Camada MODEL/Repository do MVC. Esta classe é praticamente igual à
"classe Repository" que o professor mostrou no slide de Restful APIs:
ela usa o módulo sqlite3 (que já vem no Python) para fazer o CRUD
(Create, Read, Update, Delete) num banco salvo em arquivo (.db).

Usamos placeholders (?) nas queries para evitar SQL Injection, como
recomendado em aula.
"""

import sqlite3

from .models import Asteroide


class Repository:
    """Responsável por todo o acesso ao banco de dados SQLite."""

    def __init__(self, nome_do_banco: str = "spacewatch.db"):
        self.database_name = nome_do_banco
        self.conexao = sqlite3.connect(nome_do_banco)
        self.cursor = self.conexao.cursor()
        self.criar_tabela()
        print("[DB] Banco de dados iniciado!")

    def criar_tabela(self):
        """Cria a tabela de asteroides caso ela ainda não exista."""
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
                nivel_risco TEXT
            )
        """
        self.cursor.execute(sql_create_table)
        self.conexao.commit()

    # ---------- CREATE ----------
    def inserir_asteroide(self, asteroide: Asteroide):
        """Insere um asteroide no banco."""
        sql_insert = """
            INSERT INTO asteroides (
                neo_id, nome, data_aproximacao, diametro_min_m, diametro_max_m,
                velocidade_kmh, distancia_km, distancia_lunar,
                potencialmente_perigoso, pontuacao_risco, nivel_risco
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            ),
        )
        self.conexao.commit()

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
        """Apaga todos os registros (útil antes de uma nova coleta)."""
        self.conexao = sqlite3.connect(self.database_name)
        self.cursor = self.conexao.cursor()
        self.cursor.execute("DELETE FROM asteroides")
        self.conexao.commit()
