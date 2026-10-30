from repositories.modalidade_repository import (criar_modalidade, listar_modalidades)

def adicionar_modalidade(nome, descricao):
    nome = nome.strip()
    descricao = descricao.strip()

    if not nome:
        return False, " O nome da Modalidade é obrigatório."

    try: 
        criar_modalidade(nome, descricao)
        return True, "Modalidade adicionada com sucesso."

    except Exception:
        return False, "Nao foi possível adicionar a modalidade. Verifque se já existe"

def obter_modalidades():
    return listar_modalidades()
