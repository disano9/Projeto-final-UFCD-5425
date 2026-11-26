
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash

from repositories.utilizador_repository import (
    criar_utilizador,
    obter_utilizador_por_email
)

from repositories.jogador_repository import (
    obter_jogador_por_email
)


def registar_jogador(username, email, password):
    username = username.strip()
    email = email.strip().lower()

    if not username or not email or not password:
        return False, "Todos os campos são obrigatórios."

    if len(password) < 8:
        return False, "A palavra-passe deve ter pelo menos 8 caracteres."

    jogador = obter_jogador_por_email(email)

    if jogador is None:
        return False, "Não existe nenhum jogador registado com esse email. Contacta a administração."

    password_hash = generate_password_hash(password)

    try:
        criar_utilizador(
            username=username,
            email=email,
            password_hash=password_hash,
            role="jogador",
            jogador_id=jogador["id"]
        )

        return True, "Registo efetuado. Aguarda aprovação da administração."

    except sqlite3.IntegrityError:
        return False, "Esse username ou email já está registado, ou o jogador já tem uma conta."


def autenticar_utilizador(email, password):
    email = email.strip().lower()

    utilizador = obter_utilizador_por_email(email)

    if utilizador is None:
        return False, "Email ou palavra-passe incorretos.", None

    if not check_password_hash(utilizador["password_hash"], password):
        return False, "Email ou palavra-passe incorretos.", None

    if utilizador["estado"] != "aprovado":
        return False, "A tua conta ainda não foi aprovada.", None

    return True, "Autenticação efetuada com sucesso.", utilizador
