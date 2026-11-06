from repositories.jogador_repository import (criar_jogador, listar_jogadores, obter_jogador_por_id)

from repositories.jogador_repository import (listar_jogadores_sem_equipa,associar_jogador_equipa)


def adicionar_jogador(nome, nickname, email, telemovel):
    nome = nome.strip()
    nickname = nickname.strip()
    email = email.strip()
    telemovel = telemovel.strip()

    if not nome:
        return False, "O nome do jogador é obrigatório."

    if not nickname:
        return False, "O nickname do jogador é obrigatório."

    try: 
        criar_jogador(nome, nickname, email, telemovel or None)
        return True, "Jogador adicionado com sucesso."

    except Exception as erro:
        print("Erro ao adicionar o jogador:", erro)
        return False, "Ocorreu um erro ao adicionar o jogador.Verificar se o nickname, email ou telemovel já existe no sistema."

def obter_jogadores():
    return listar_jogadores()

def consultar_jogador(jogador_id):
    return obter_jogador_por_id(jogador_id)

    
def obter_jogadores_sem_equipa():
    return listar_jogadores_sem_equipa()


def adicionar_jogador_a_equipa(jogador_id, equipa_id, posicao, data_entrada):
    try:
        associar_jogador_equipa(
            jogador_id, equipa_id, posicao, data_entrada
        )
        return True, "Jogador associado à equipa com sucesso."

    except Exception as erro:
        print("Erro ao associar jogador:", erro)
        return False, "Não foi possível associar o jogador à equipa."
        

