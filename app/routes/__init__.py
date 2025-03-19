from flask import Blueprint

# Criação do Blueprint para usuários
usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')

# Importa as rotas de usuário
from app.routes.usuario_routes import *  # Importa todas as rotas definidas em usuario_routes.py