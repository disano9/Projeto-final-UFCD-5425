from database.db import get_connection

def criar_modalidade(nome, descricao):
    connection = get_connection()

    try: 
        connection.execute(
            "INSERT INTO modalidades (nome, descricao) VALUES (?, ?)",
            (nome, descricao)
        )
        connection.commit()
    finally:
        connection.close()

def listar_modalidades():
    connection = get_connection()

    try:
        resultado = connection.execute(
            "SELECT * FROM modalidades ORDER BY nome"
        ).fetchall()

        return resultado
    finally:
        connection.close()