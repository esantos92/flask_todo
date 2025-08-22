from flask import Flask
from dotenv import load_dotenv
from app.config import Dev
from app.extensions import db, jwt, migrate, bcrypt

def create_app():
    # Carrega variáveis de ambiente
    load_dotenv()

    # Cria a instância do Flask
    app = Flask(__name__)

    # Configura a aplicação
    app.config.from_object(Dev)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Registra blueprints
    from app.api import register_blueprints
    app.register_blueprint(app)

    return app