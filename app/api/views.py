from flask import Blueprint, render_template

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def home():
    """Rota para a página inicial"""
    return render_template('home.html')

@views_bp.route('/home')
def home_alt():
    """Rota alternativa para a página inicial"""
    return render_template('home.html')
