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
        connection.execute("""CREATE TABLE IF NOT EXISTS modalidades(id INTEGER PRIMARY KEY AUTOINCREMENT,nome TEXT NOT NULL UNIQUE,descricao TEXT)""")
    
    #Tabelas de Equipas
    connection.execute("""CREATE TABLE IF NOT EXISTS equipas
    (id INTEGER PRIMARY KEY AUTOINCREMENT,nome TEXT NOT NULL,descricao TEXT,modalidade_id INTEGER NOT NULL,FOREIGN KEY (modalidade_id)REFERENCES modalidades(id))
    """)