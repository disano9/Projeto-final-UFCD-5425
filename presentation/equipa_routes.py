
from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for, flash

from services.equipa_services import (
    adicionar_equipa,
    obter_equipas,
    obter_jogadores_da_equipa
)

from services.modalidade_service import obter_modalidades

from services.jogador_services import (
    obter_jogadores_sem_equipa,
    adicionar_jogador_a_equipa,
    retirar_jogador_da_equipa
)

from presentation.permissions import roles_required


equipa_bp = Blueprint("equipa", __name__)


# Listar e adicionar equipas
@equipa_bp.route("/equipa", methods=["GET", "POST"])
@roles_required("admin", "treinador")
def listar():

    if request.method == "POST":
        nome = request.form.get("nome", "")
        descricao = request.form.get("descricao", "")
        modalidade_id = request.form.get("modalidade_id", "")

        if not modalidade_id.isdigit():
            flash("Selecionar uma modalidade válida.", "error")
            return redirect(url_for("equipa.listar"))

        sucesso, mensagem = adicionar_equipa(
            nome,
            descricao,
            int(modalidade_id)
        )

        flash(mensagem, "success" if sucesso else "error")

        return redirect(url_for("equipa.listar"))

    equipas = obter_equipas()
    modalidades = obter_modalidades()

    return render_template(
        "equipas.html",
        equipas=equipas,
        modalidades=modalidades
    )


# Associar jogadores a equipas
@equipa_bp.route("/associar-jogador", methods=["GET", "POST"])
@roles_required("admin", "treinador")
def associar_jogador():

    if request.method == "POST":
        jogador_id = request.form.get("jogador_id", "")
        equipa_id = request.form.get("equipa_id", "")
        posicao = request.form.get("posicao", "")
        data_entrada = request.form.get("data_entrada", "")

        if not jogador_id.isdigit() or not equipa_id.isdigit():
            flash("Seleciona um jogador e uma equipa válidos.", "error")
            return redirect(url_for("equipa.associar_jogador"))

        if not posicao or not data_entrada:
            flash("Preenche todos os campos.", "error")
            return redirect(url_for("equipa.associar_jogador"))

        sucesso, mensagem = adicionar_jogador_a_equipa(
            int(jogador_id),
            int(equipa_id),
            posicao,
            data_entrada
        )

        flash(mensagem, "success" if sucesso else "error")

        return redirect(url_for("equipa.associar_jogador"))

    jogadores = obter_jogadores_sem_equipa()
    equipas = obter_equipas()

    return render_template(
        "associar_jogador.html",
        jogadores=jogadores,
        equipas=equipas
    )


# Consultar plantel de uma equipa
@equipa_bp.route("/equipa/<int:equipa_id>/plantel")
@roles_required("admin", "treinador")
def consultar_plantel(equipa_id):

    equipas = obter_equipas()

    equipa = next(
        (e for e in equipas if e["id"] == equipa_id),
        None
    )

    if equipa is None:
        flash("Equipa não encontrada.", "error")
        return redirect(url_for("equipa.listar"))

    jogadores = obter_jogadores_da_equipa(equipa_id)

    return render_template(
        "plantel.html",
        equipa=equipa,
        jogadores=jogadores
    )


# Remover jogador de uma equipa
@equipa_bp.route(
    "/equipa/<int:equipa_id>/jogador/<int:jogador_id>/remover",
    methods=["POST"]
)
@roles_required("admin", "treinador")
def remover_jogador(equipa_id, jogador_id):

    data_saida = date.today().isoformat()

    sucesso, mensagem = retirar_jogador_da_equipa(
        jogador_id,
        equipa_id,
        data_saida
    )

    flash(mensagem, "success" if sucesso else "error")

    return redirect(url_for(
        "equipa.consultar_plantel",
        equipa_id=equipa_id
    ))
