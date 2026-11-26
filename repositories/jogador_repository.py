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

def atualizar_jogador(jogador_id, nome, nickname, email, telemovel):
    connection = get_connection()

    try:
        connection.execute("""
            UPDATE jogadores
            SET nome = ?,
                nickname = ?,
                email = ?,
                telemovel = ?
            WHERE id = ?
        """, (nome, nickname, email, telemovel, jogador_id))

        connection.commit()

    finally:
        connection.close()

def remover_jogador_da_equipa(jogador_id, equipa_id, data_saida):
    connection = get_connection()

    try:
        connection.execute("""
            UPDATE equipa_jogadores
            SET data_saida = ?
            WHERE jogador_id = ?
            AND equipa_id = ?
            AND data_saida IS NULL
        """, (data_saida, jogador_id, equipa_id))

        connection.commit()

    finally:
        connection.close()


def obter_jogador_por_email(email):
    connection = get_connection()

    try:
        jogador = connection.execute(
            """
            SELECT *
            FROM jogadores
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        return jogador

    finally:
        connection.close()

def obter_area_pessoal(utilizador_id):
    connection = get_connection()

    try:
        dados = connection.execute("""
            SELECT
                j.id AS jogador_id,
                j.nome,
                j.nickname,
                j.email,
                j.telemovel,
                e.nome AS equipa,
                ej.posicao,
                ej.data_entrada,
                m.nome AS modalidade
            FROM utilizadores u
            INNER JOIN jogadores j
                ON u.jogador_id = j.id
            LEFT JOIN equipa_jogadores ej
                ON j.id = ej.jogador_id
                AND ej.data_saida IS NULL
            LEFT JOIN equipas e
                ON ej.equipa_id = e.id
            LEFT JOIN modalidades m
                ON e.modalidade_id = m.id
            WHERE u.id = ?
              AND u.role = 'jogador'
        """, (utilizador_id,)).fetchone()

        return dados

    finally:
        connection.close()
