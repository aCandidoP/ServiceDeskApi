from flask import jsonify
from app.models import Tipo
from app.routes import tipo_bp
from flask_jwt_extended  import jwt_required


@tipo_bp.route('', methods=["GET"])
@jwt_required()
def listar_tipos():
    tipos = Tipo.query.all()
    tipos_json = [{"id": c.id, "desc_tipo": c.desc_tipo} for c in tipos]
    return jsonify(tipos_json)