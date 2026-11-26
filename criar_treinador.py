
from getpass import getpass
import sqlite3

from werkzeug.security import generate_password_hash

from repositories.utilizador_repository import (
    criar_utilizador,
    obter_utilizador_por_email,
    atualizar_estado_utilizador
)


def criar_treinador():
    print("\n=== DARK TEAM MANAGER ===")
    print("Criação de conta de treinador\n")

    username = input("Username: ").strip()
    email = input("Email: ").strip().lower()

    password = getpass("Palavra-passe: ")
    confirmar_password = getpass("Confirmar palavra-passe: ")

    if not username or not email or not password:
        print("\nErro: todos os campos são obrigatórios.")
        return

    if len(password) < 8:
        print("\nErro: a palavra-passe deve ter pelo menos 8 caracteres.")
        return

    if password != confirmar_password:
        print("\nErro: as palavras-passe não coincidem.")
        return

    password_hash = generate_password_hash(password)

    try:
        criar_utilizador(
            username=username,
            email=email,
            password_hash=password_hash,
            role="treinador"
        )

        utilizador = obter_utilizador_por_email(email)

        atualizar_estado_utilizador(
            utilizador["id"],
            "aprovado"
        )

        print("\nConta de treinador criada com sucesso!")

    except sqlite3.IntegrityError:
        print("\nErro: esse username ou email já está registado.")


if __name__ == "__main__":
    criar_treinador()
