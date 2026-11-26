
from functools import wraps

from flask import session, redirect, url_for, flash


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            flash("Tens de iniciar sessão para aceder a esta página.", "error")
            return redirect(url_for("auth.login"))

        return func(*args, **kwargs)

    return wrapper


def roles_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            if "user_id" not in session:
                flash("Tens de iniciar sessão.", "error")
                return redirect(url_for("auth.login"))

            if session.get("role") not in roles:
                flash("Não tens permissões para realizar esta ação.", "error")
                return redirect(url_for("home"))

            return func(*args, **kwargs)

        return wrapper

    return decorator
