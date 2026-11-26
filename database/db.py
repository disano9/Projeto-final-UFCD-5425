import sqlite3
from config import DATABASE_PATH

def get_connection(): 
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def init_db():
     #Tabelas de Modalidades
    with get_connection() as connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS modalidades(id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,descricao TEXT)""")
    
    #Tabelas de Equipas
        connection.execute("""CREATE TABLE IF NOT EXISTS equipas
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,descricao TEXT,
    modalidade_id INTEGER NOT NULL,
    FOREIGN KEY (modalidade_id)
    REFERENCES modalidades(id)
        )
    """)

    #Tabela de Jogadores 
        connection.execute("""
    CREATE TABLE IF NOT EXISTS jogadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        nickname TEXT NOT NULL UNIQUE,
        email TEXT UNIQUE,
        telemovel TEXT UNIQUE
         )
     """)


     #Tabela de historico de Jogadores
        connection.execute("""CREATE TABLE IF NOT EXISTS equipa_jogadores (id INTEGER PRIMARY KEY AUTOINCREMENT,
        jogador_id INTEGER NOT NULL,equipa_id INTEGER NOT NULL,
        posicao TEXT NOT NULL,
        data_entrada DATE NOT NULL,
        data_saida DATE,FOREIGN KEY (jogador_id) REFERENCES jogadores(id),
        FOREIGN KEY (equipa_id) REFERENCES equipas(id)
           ) 
        """)
    
        # Tabela de Utilizadores
        connection.execute("""
            CREATE TABLE IF NOT EXISTS utilizadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
                    CHECK (role IN ('admin', 'treinador', 'jogador')),
                jogador_id INTEGER UNIQUE,
                estado TEXT NOT NULL DEFAULT 'pendente'
                    CHECK (estado IN ('pendente', 'aprovado', 'rejeitado')),
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (jogador_id)
                    REFERENCES jogadores(id)
            )
        """)