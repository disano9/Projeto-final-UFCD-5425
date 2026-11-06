from database.db import get_connection

def criar_jogador(nome, nickname, email, telemovel):
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO jogadores (nome, nickname, email, telemovel)
            VALUES (?, ?, ?, ?)
            """,
            (nome, nickname, email, telemovel)
        )
        connection.commit()
    finally:
        connection.close()

def listar_jogadores():
    connection = get_connection()

    try:
        jogadores = connection.execute("" \
        "SELECT * FROM jogadores ORDER BY nickname"
        ).fetchall()

        return jogadores
    finally:
       connection.close()

def obter_jogador_por_id(jogador_id):
    connection = get_connection()

    try:
        jogador = connection.execute(
            "SELECT * FROM jogadores WHERE id = ?",
            (jogador_id,)
        ).fetchone()

        return jogador
    finally:
       connection.close()

def listar_jogadores_sem_equipa():
    connection = get_connection()
    try:
        jogadores = connection.execute("""
            SELECT * FROM jogadores
            WHERE id NOT IN (
                SELECT jogador_id
                FROM equipa_jogadores
                WHERE data_saida IS NULL
            )
            ORDER BY nickname
        """).fetchall()

        return jogadores
    finally:
        connection.close()


def associar_jogador_equipa(jogador_id, equipa_id, posicao, data_entrada):
    connection = get_connection()
    try:
        connection.execute("""
            INSERT INTO equipa_jogadores
            (jogador_id, equipa_id, posicao, data_entrada)
            VALUES (?, ?, ?, ?)
        """, (jogador_id, equipa_id, posicao, data_entrada))

        connection.commit()
    finally:
        connection.close()