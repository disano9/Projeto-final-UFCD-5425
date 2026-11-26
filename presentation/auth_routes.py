
from functools import wraps

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from services.auth_service import (
    registar_jogador,
    autenticar_utilizador
)

from repositories.utilizador_repository import (
    obter_utilizadores_pendentes,
    atualizar_estado_utilizador
)


auth_bp = Blueprint("auth", __name__)


# Verificar se o utilizador é administrador
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            flash("Tens de iniciar sessão.", "error")
            return redirect(url_for("auth.login"))

        if session.get("role") != "admin":
            flash("Não tens permissões para aceder a esta área.", "error")
            return redirect(url_for("home"))

        return func(*args, **kwargs)

    return wrapper


# Registo de jogadores
@auth_bp.route("/registo", methods=["GET", "POST"])
def registar():
    if request.method == "POST":
        username = request.form.get("username", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        sucesso, mensagem = registar_jogador(
            username,
            email,
            password
        )

        flash(mensagem, "success" if sucesso else "error")

        if sucesso:
            return redirect(url_for("auth.login"))

    return render_template("auth/registo.html")


# Login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        sucesso, mensagem, utilizador = autenticar_utilizador(
            email,
            password
        )

        if sucesso:
            session.clear()
            session["user_id"] = utilizador["id"]
            session["username"] = utilizador["username"]
            session["role"] = utilizador["role"]

            flash("Sessão iniciada com sucesso.", "success")
            return redirect(url_for("home"))

        flash(mensagem, "error")

    return render_template("auth/login.html")


# Logout
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sessão terminada.", "success")
    return redirect(url_for("auth.login"))


# Consultar pedidos pendentes
@auth_bp.route("/admin/pedidos")
@admin_required
def pedidos():
    utilizadores = obter_utilizadores_pendentes()

    return render_template(
        "auth/pedidos.html",
        utilizadores=utilizadores
    )


# Aprovar jogador
@auth_bp.route(
    "/admin/utilizador/<int:utilizador_id>/aprovar",
    methods=["POST"]
)
@admin_required
def aprovar(utilizador_id):
    sucesso = atualizar_estado_utilizador(
        utilizador_id,
        "aprovado"
    )

    if sucesso:
        flash("Conta aprovada com sucesso.", "success")
    else:
        flash("Não foi possível aprovar a conta.", "error")

    return redirect(url_for("auth.pedidos"))


# Rejeitar jogador
@auth_bp.route(
    "/admin/utilizador/<int:utilizador_id>/rejeitar",
    methods=["POST"]
)
@admin_required
def rejeitar(utilizador_id):
    sucesso = atualizar_estado_utilizador(
        utilizador_id,
        "rejeitado"
    )

    if sucesso:
        flash("Pedido rejeitado com sucesso.", "success")
    else:
        flash("Não foi possível rejeitar o pedido.", "error")

    return redirect(url_for("auth.pedidos"))
