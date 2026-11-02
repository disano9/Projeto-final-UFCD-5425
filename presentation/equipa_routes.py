from flask import Blueprint, render_template, request, redirect, url_for, flash

from services.equipa_services import adicionar_equipa, obter_equipas
from services.modalidade_service import obter_modalidades

equipa_bp = Blueprint("equipa", __name__)

@equipa_bp.route("/equipa", methods=["GET", "POST"])
def listar():
    if request.method == "POST":
        nome = request.form.get("nome", "")
        descricao = request.form.get("descricao", "")
        modalidade_id = request.form.get("modalidade_id", "")

        if not modalidade_id.isdigit():
          flash("Selecionar uma modalidade válida.", "error")
          return redirect(url_for("equipa.listar"))

        sucesso, mensagem = adicionar_equipa(nome, descricao, int(modalidade_id))

        if sucesso:
           flash(mensagem, "success")
        else:
           flash(mensagem, "error")

        return redirect(url_for("equipa.listar"))

    equipas = obter_equipas()
    modalidades = obter_modalidades()

    return render_template("equipas.html", equipas=equipas, modalidades=modalidades)