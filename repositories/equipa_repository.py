
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

def listar_jogadores_da_equipa(equipa_id):
    connection = get_connection()

    try:
        jogadores = connection.execute("""
            SELECT
                jogadores.id,
                jogadores.nome,
                jogadores.nickname,
                jogadores.email,
                jogadores.telemovel,
                equipa_jogadores.posicao,
                equipa_jogadores.data_entrada
            FROM equipa_jogadores
            INNER JOIN jogadores
                ON equipa_jogadores.jogador_id = jogadores.id
            WHERE equipa_jogadores.equipa_id = ?
            AND equipa_jogadores.data_saida IS NULL
            ORDER BY
                CASE equipa_jogadores.posicao
                    WHEN 'Top' THEN 1
                    WHEN 'Jungle' THEN 2
                    WHEN 'Mid' THEN 3
                    WHEN 'ADC' THEN 4
                    WHEN 'Support' THEN 5
                    ELSE 6
                END
        """, (equipa_id,)).fetchall()

        return jogadores
    finally:
        connection.close()


    