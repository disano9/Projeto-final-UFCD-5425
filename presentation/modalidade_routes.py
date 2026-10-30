from flask import Blueprint,render_template,request,redirect,url_for,flash

from services.modalidade_service import (adicionar_modalidade, obter_modalidades)

modalidade_bp = Blueprint("modalidade", __name__)

@modalidade_bp.route("/modalidades", methods=["GET", "POST"])

def listar():
    if request.method == "POST":
        nome = request.form.get("nome", "")
        descricao = request.form.get("descricao", "")

        sucesso, mensagem = adicionar_modalidade(nome, descricao)

        if sucesso:
            flash(mensagem, "success")
        else:
            flash(mensagem, "error")

        return redirect(url_for("modalidade.listar"))

    modalidades = obter_modalidades()

    return render_template("index.html", modalidades=modalidades)


    