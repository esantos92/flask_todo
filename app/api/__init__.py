from flask import Flask
from .auth import auth_bp
from .todos import todos_bp
from .views import views_bp

def register_blueprints(app: Flask):
    # Registra todas as blueprints da aplicação
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(todos_bp, url_prefix='/api/todos', strict_slashes=False)
    app.register_blueprint(views_bp)  # Sem prefixo para as views principais