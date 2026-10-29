from flask import Flask

from config import SECRET_KEY


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY

    @app.route("/")
    def home():
        return """
        <h1>Dark Team Manager</h1>
        <p>Sistema de gestão da Dark Team.</p>
        <p>Estado: aplicação iniciada com sucesso.</p>
        """

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)