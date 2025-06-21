from flask import jsonify
from app.models import Categoria
from app.config.dbconfig import db
from app.routes import categoria_bp
from flask_jwt_extended  import jwt_required
from app.decorators import somente_admin


@categoria_bp.route('', methods=["GET"])
@jwt_required()
@somente_admin
def listar_categorias():
    categorias = Categoria.query.all()
    categoria_json = [{"id": c.id, "nome": c.nome, "servicos": c.servicos} for c in categorias]
    return jsonify(categoria_json)