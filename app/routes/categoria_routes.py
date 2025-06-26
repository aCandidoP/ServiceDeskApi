from flask import jsonify
from app.models import Categoria
from app.config.dbconfig import db
from app.routes import categoria_bp
from flask_jwt_extended  import jwt_required
from app.decorators import somente_admin


@categoria_bp.route('', methods=["GET"])
@jwt_required()
def listar_categorias():
    categorias = Categoria.query.all()
    categorias_dict = [categoria.to_dict() for categoria in categorias]
    return jsonify(categorias_dict)