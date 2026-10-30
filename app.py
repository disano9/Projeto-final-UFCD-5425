
from flask import Flask
from config import SECRET_KEY
from database.db import init_db
from presentation.modalidade_routes import modalidade_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY

    init_db()
    app.register_blueprint(modalidade_bp)

    @app.route("/")
    def home():
        return "<h1>Dark Team Manager</h1>"

    return app


if __name__ == "__main__":
    app = create_app()

    print("Aplicação criada com sucesso!")
    print(app.url_map)

    app.run(debug=True)
