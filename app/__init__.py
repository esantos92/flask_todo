from flask import Flask, jsonify
from dotenv import load_dotenv

def create_app():
    # Carrega variáveis de ambiente PRIMEIRO
    load_dotenv()
    
    from app.config import Dev
    from app.extensions import db, jwt, migrate, bcrypt

    # Cria a instância do Flask
    app = Flask(__name__)

    # Configura a aplicação
    app.config.from_object(Dev)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Adicionar handlers de erro JWT
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'msg': 'Token expirado'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"=== JWT Invalid Token Error: {error} ===")
        return jsonify({'msg': 'Token inválido', 'error': str(error)}), 422

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        print(f"=== JWT Missing Token Error: {error} ===")
        return jsonify({'msg': 'Token não fornecido', 'error': str(error)}), 401

    # Handler de erro geral para 422
    @app.errorhandler(422)
    def handle_422(error):
        print(f"=== 422 Error: {error} ===")
        return jsonify({'msg': 'Erro de validação', 'error': str(error)}), 422

    # Registra blueprints
    from app.api import register_blueprints
    register_blueprints(app)

    return app