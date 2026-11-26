
from database.db import get_connection


def criar_utilizador(username, email, password_hash, role, jogador_id=None):
    with get_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO utilizadores (
                username,
                email,
                password_hash,
                role,
                jogador_id
            )
            VALUES (?, ?, ?, ?, ?)
        """, (username, email, password_hash, role, jogador_id))

        return cursor.lastrowid


def obter_utilizador_por_email(email):
    with get_connection() as connection:
        return connection.execute("""
            SELECT *
            FROM utilizadores
            WHERE email = ?
        """, (email,)).fetchone()


def obter_utilizador_por_username(username):
    with get_connection() as connection:
        return connection.execute("""
            SELECT *
            FROM utilizadores
            WHERE username = ?
        """, (username,)).fetchone()


def obter_utilizadores_pendentes():
    with get_connection() as connection:
        return connection.execute("""
            SELECT *
            FROM utilizadores
            WHERE estado = 'pendente'
            ORDER BY data_criacao DESC
        """).fetchall()


def atualizar_estado_utilizador(utilizador_id, estado):
    with get_connection() as connection:
        cursor = connection.execute("""
            UPDATE utilizadores
            SET estado = ?
            WHERE id = ?
        """, (estado, utilizador_id))

        return cursor.rowcount > 0
