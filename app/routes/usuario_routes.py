from flask import Blueprint, jsonify, request
from app.models import Usuario
from app.config.dbconfig import db
from werkzeug.security import generate_password_hash
from app.routes import usuario_bp
import re
from flask_jwt_extended import jwt_required
from datetime import timedelta
from app.decorators import somente_admin

def email_valido(email):
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(padrao, email)

# Rota para listar usuários
@usuario_bp.route("/", methods=["GET"])
@jwt_required()
@somente_admin
def listar_usuarios():
    usuarios = Usuario.query.all()
    usuarios_json = [{"id": u.id, "nome": u.nome, "email": u.email, "perfil_id": u.perfil_id} for u in usuarios]
    return jsonify(str(usuarios_json))

# Rota para criar um novo usuário
@usuario_bp.route("/", methods=["POST"])
#@jwt_required()
#@somente_admin
def criar_usuario():
    dados = request.get_json()
    
    if not all(k in dados for k in ("nome", "email", "senha", "perfil_id")):
        return jsonify({"erro": "Campos obrigatórios: nome, email, senha, perfil_id"}), 400
    
    if not email_valido(dados["email"]):
        return jsonify({"erro": "E-mail inválido"}), 400
    
    senha_hash = generate_password_hash(dados["senha"])
    novo_usuario = Usuario(nome=dados["nome"], email=dados["email"], senha=senha_hash, perfil_id=dados["perfil_id"])
    
    db.session.add(novo_usuario)
    db.session.commit()
    
    return jsonify({"mensagem": "Usuário criado com sucesso!"}), 201

@usuario_bp.route('/usuarios', methods=['GET'])
def get_usuarios_paginados():
    """
    Endpoint para listar usuários com suporte a paginação.
    Exemplos de como chamar via frontend:
    /usuarios?page=1&per_page=10  (retorna os 10 primeiros usuários da página 1)
    /usuarios?page=2&per_page=5   (retorna os 5 usuários da página 2)
    /usuarios                     (usa os valores padrão: página 1, 10 por página)
    """
    
    # 1. Obter os parâmetros da URL, com valores padrão para o caso de não serem fornecidos.
    # O 'type=int' garante que, se o valor for fornecido, ele será convertido para inteiro.
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 2. Usar o método .paginate() na sua query do SQLAlchemy
    # É uma boa prática adicionar um .order_by() para garantir uma ordem consistente entre as páginas.
    query = Usuario.query.order_by(Usuario.nome.asc())
    
    # O método paginate faz toda a mágica: calcula offset, limit, etc.
    # 'error_out=False' evita que a aplicação quebre se o frontend pedir uma página que não existe (ex: página 99 de 10).
    pagination_object = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # 3. Extrair os itens da página atual
    usuarios_da_pagina = pagination_object.items
    
    # 4. Preparar o JSON de resposta para o frontend
    # É crucial serializar seus objetos do modelo para dicionários/JSON.
    # Uma boa prática é ter um método no seu modelo para isso. (Exemplo abaixo)
    usuarios_serializados = [usuario.to_dict() for usuario in usuarios_da_pagina]
    
    resultado_final = {
        'usuarios': usuarios_serializados,
        'pagination_metadata': {
            'page': pagination_object.page,
            'per_page': pagination_object.per_page,
            'total_pages': pagination_object.pages,
            'total_items': pagination_object.total,
            'has_next': pagination_object.has_next,
            'has_prev': pagination_object.has_prev
        }
    }
    
    return jsonify(resultado_final)

