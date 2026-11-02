
from database.db import get_connection


def criar_equipa(nome, descricao, modalidade_id):
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO equipas (nome, descricao, modalidade_id)
            VALUES (?, ?, ?)
            """,
            (nome, descricao, modalidade_id)
        )
        connection.commit()
    finally:
        connection.close()


def listar_equipas():
    connection = get_connection()

    try:
        equipas = connection.execute(
            """
            SELECT
                equipas.id,
                equipas.nome,
                equipas.descricao,
                modalidades.nome AS modalidade
            FROM equipas
            INNER JOIN modalidades
                ON equipas.modalidade_id = modalidades.id
            ORDER BY equipas.nome
            """
        ).fetchall()

        return equipas
    finally:
        connection.close()

    