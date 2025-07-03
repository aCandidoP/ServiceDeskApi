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

# Exemplo de como a sua rota de API deve ser

@categoria_bp.route('/arvore', methods=['GET']) # Uma rota específica para a árvore
@jwt_required()
def get_arvore_de_categorias():

    categorias_mae = Categoria.query.filter_by(parent_id=None).all()
    arvore_json = [categoria.to_dict() for categoria in categorias_mae]
    
    return jsonify({"categorias": arvore_json})