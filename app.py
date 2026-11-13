
from flask import Flask, render_template
from config import SECRET_KEY
from database.db import init_db
from presentation.modalidade_routes import modalidade_bp
from presentation.equipa_routes import equipa_bp
from presentation.jogador_routes import jogador_bp
from services.equipa_services import obter_equipas
from services.jogador_services import obter_jogadores
from services.modalidade_service import obter_modalidades





def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY

    init_db()
    app.register_blueprint(modalidade_bp)
    app.register_blueprint(equipa_bp)
    app.register_blueprint(jogador_bp)
    

    @app.route("/")
    def home():
        modalidades = obter_modalidades()
        equipas = obter_equipas()
        jogadores = obter_jogadores()
        
        return render_template(
            "dashboard.html",
            total_modalidades=len(modalidades),
            total_equipas=len(equipas),
            total_jogadores=len(jogadores)
            )
    return app

if __name__ == "__main__":
    app = create_app()
    print("Aplicação criada com sucesso!")
    print(app.url_map)
    app.run(debug=True)