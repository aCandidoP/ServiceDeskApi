from flask import jsonify
from app.models import Tipos
from app.config.dbconfig import db
from app.routes import categoria_bp
from flask_jwt_extended  import jwt_required
from app.decorators import somente_admin


@categoria_bp.route('', methods=["GET"])
@jwt_required()
@somente_admin
def listar_categorias():
    tipos = Tipos.query.all()
    tipos_json = [{"id": c.id, "desc_tipo": c.desc_tipo} for c in tipos]
    return jsonify(tipos_json)