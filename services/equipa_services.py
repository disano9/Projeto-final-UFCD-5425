
from repositories.equipa_repository import (
    criar_equipa,
    listar_equipas
)


def adicionar_equipa(nome, descricao, modalidade_id):
    nome = nome.strip()
    descricao = descricao.strip()

    if not nome:
        return False, "O nome da equipa é obrigatório."

    if not modalidade_id:
        return False, "Tens de selecionar uma modalidade."

    try:
        criar_equipa(nome, descricao, modalidade_id)
        return True, "Equipa adicionada com sucesso!"

    except Exception as erro:
        print("Erro ao adicionar equipa:", erro)
        return False, "Não foi possível adicionar a equipa."


def obter_equipas():
    return listar_equipas()

    