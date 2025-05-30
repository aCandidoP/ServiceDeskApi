from flask import Blueprint

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')
chamado_bp = Blueprint('chamado', __name__, url_prefix='/chamados')
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


from app.routes.usuario_routes import *
from app.routes.chamado_routes import *
from app.routes.auth_routes import *