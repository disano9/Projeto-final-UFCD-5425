from flask import Blueprint, render_template, request, redirect, url_for, flash

from services.jogador_services import adicionar_jogador, obter_jogadores

jogador_bp = Blueprint("jogador", __name__)

@jogador_bp.route("/jogadores", methods=["GET", "POST"])

def jogadores():

    if request.method == "POST":
        nome = request.form.get("nome", "")
        nickname = request.form.get("nickname", "")
        email = request.form.get("email", "")
        telemovel = request.form.get("telemovel", "")

        sucesso, mensagem = adicionar_jogador(nome, nickname, email, telemovel)

        if sucesso:
            flash(mensagem, "success")
        else:
            flash(mensagem, "error")
        return redirect(url_for("jogador.jogadores"))

    jogadores = obter_jogadores()
    
    return render_template("jogadores.html", jogadores=jogadores)
    


