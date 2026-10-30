import sqlite3
from config import DATABASE_PATH

def get_connection(): 
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():

    with get_connection() as connection:
        connection.execute(
            ("""
            CREATE TABLE IF NOT EXISTS modalidades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                descricao TEXT
            )
        """)
        )
        