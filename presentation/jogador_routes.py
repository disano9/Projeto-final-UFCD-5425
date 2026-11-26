
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from services.jogador_services import (
    adicionar_jogador,
    obter_jogadores,
    consultar_jogador,
    editar_jogador,
    consultar_area_pessoal
)

from presentation.permissions import roles_required


jogador_bp = Blueprint("jogador", __name__)


# Consultar e adicionar jogadores
@jogador_bp.route("/jogadores", methods=["GET", "POST"])
@roles_required("admin", "treinador")
def jogadores():

    if request.method == "POST":
        nome = request.form.get("nome", "")
        nickname = request.form.get("nickname", "")
        email = request.form.get("email", "")
        telemovel = request.form.get("telemovel", "")

        sucesso, mensagem = adicionar_jogador(
            nome,
            nickname,
            email,
            telemovel
        )

        flash(mensagem, "success" if sucesso else "error")

        return redirect(url_for("jogador.jogadores"))

    jogadores = obter_jogadores()

    return render_template(
        "jogadores.html",
        jogadores=jogadores
    )


# Editar jogadores
@jogador_bp.route(
    "/jogadores/editar/<int:jogador_id>",
    methods=["GET", "POST"]
)
@roles_required("admin", "treinador")
def editar(jogador_id):

    jogador = consultar_jogador(jogador_id)

    if jogador is None:
        flash("Jogador não encontrado.", "error")
        return redirect(url_for("jogador.jogadores"))

    if request.method == "POST":
        nome = request.form.get("nome", "")
        nickname = request.form.get("nickname", "")
        email = request.form.get("email", "")
        telemovel = request.form.get("telemovel", "")

        sucesso, mensagem = editar_jogador(
            jogador_id,
            nome,
            nickname,
            email,
            telemovel
        )

        flash(mensagem, "success" if sucesso else "error")

        if sucesso:
            return redirect(url_for("jogador.jogadores"))

    return render_template(
        "editar_jogador.html",
        jogador=jogador
    )


# Área pessoal do jogador
@jogador_bp.route("/minha-area")
@roles_required("jogador")
def minha_area():

    dados = consultar_area_pessoal(
        session["user_id"]
    )

    if dados is None:
        flash("Não foi possível encontrar o teu perfil de jogador.", "error")
        return redirect(url_for("home"))

    return render_template(
        "auth/minha_area.html",
        jogador=dados
    )
