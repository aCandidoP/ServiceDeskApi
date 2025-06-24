from flask import Blueprint

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')
chamado_bp = Blueprint('chamado', __name__, url_prefix='/chamados')
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
categoria_bp = Blueprint('categoria', __name__, url_prefix='/categorias')
tipo_bp = Blueprint('tipo', __name__, url_prefix='/tipos')
organizacao_bp = Blueprint('organizacao', __name__, url_prefix='/organizacoes')
acompanhamento_bp = Blueprint('acompanhamento', __name__, url_prefix='/acompanhamentos')

from app.routes.usuario_routes import *
from app.routes.chamado_routes import *
from app.routes.auth_routes import *
from app.routes.categoria_routes import *
from app.routes.tipo_routes import *
from app.routes.organizacoes_routes import *
from app.routes.acompanhamento_routes import *