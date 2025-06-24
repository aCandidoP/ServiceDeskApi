from flask import jsonify, request
from app.models import Chamado
from app.config.dbconfig import db
from app.routes import chamado_bp
from flask_jwt_extended  import jwt_required, get_jwt_identity
from app.decorators import somente_admin
import json
from sqlalchemy import desc


@chamado_bp.route('', methods=["GET"])
@jwt_required()
@somente_admin
def listar_chamados():
    try:
        identidade_str_json = get_jwt_identity()
        identidade_dict = json.loads(identidade_str_json)
        usuario_id = identidade_dict.get("id")
        perfil_id = identidade_dict.get("perfil_id")
    except (TypeError, json.JSONDecodeError):
        return jsonify({"erro": "Formato da identidade no token é inválido."}), 401
    if str(perfil_id) == '1': # Verifica se é Admin
        chamados = Chamado.query.order_by(desc(Chamado.id))
    else:
        # Usuário comum vê apenas seus próprios chamados.
        chamados = Chamado.query.filter_by(usuario_id=usuario_id).order_by(desc(Chamado.id))
    chamados_json = [{
        "id": c.id,
        "titulo": c.titulo,
        "tipo": c.tipo.desc_tipo,
        "descricao": c.descricao,
        "categoria": c.categoria.nome,
        "data_criacao": c.data_criacao,
        "status": c.status,
        "usuario_id": c.usuario_id,
        "acompanhamentos": c.acompanhamentos}
                     for c in chamados]
    return jsonify(chamados_json)

@chamado_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def listar_chamado(id):
    chamado = Chamado.query.get_or_404(id)
    chamado_json = {
        "id": chamado.id,
        "titulo": chamado.titulo,
        "tipo": chamado.tipo.desc_tipo,
        "descricao": chamado.descricao,
        "categoria": chamado.categoria.nome,
        "data_criacao": chamado.data_criacao,
        "status": chamado.status,
        "usuario_id": chamado.usuario_id,
        "acompanhamentos": chamado.acompanhamentos
        }
        
                     
        
    return(jsonify(chamado_json))


@chamado_bp.route("/status/<string:status>", methods=["GET"])
@jwt_required()
def listar_chamado_status(status):
    status_formatado = status.upper()
    chamados = Chamado.query.filter_by(status=status_formatado).order_by(Chamado.id.desc()).all()
    chamado_json = [{
        "id": chamado.id,
        "titulo": chamado.titulo,
        "tipo": chamado.tipo.desc_tipo,
        "descricao": chamado.descricao,
        "categoria": chamado.categoria.nome,
        "data_criacao": chamado.data_criacao,
        "status": chamado.status,
        "usuario_id": chamado.usuario_id,
        "acompanhamentos": chamado.acompanhamentos
        }for chamado in chamados]
    return(jsonify(chamado_json))
    


@chamado_bp.route('', methods=["POST"])
@jwt_required()
def criar_chamado():
    dados = request.get_json()
    
    if not all(k in dados for k in ("titulo", "tipo_id", "categoria_id", "usuario_id", "organizacao_id")):
        return jsonify({"erro": "Campos obrigatórios: titulo, tipo_id, categoria_id, usuario_id, organizacao_id"}), 400
    
    
    novo_chamado = Chamado(
        titulo=dados["titulo"],
        tipo_id=dados["tipo_id"],
        categoria_id=dados["categoria_id"],
        descricao=dados["descricao"], 
        status='NOVO',
        usuario_id=dados["usuario_id"],
        organizacao_id=dados["organizacao_id"]
    )
    
    db.session.add(novo_chamado)
    db.session.commit()
    
    return jsonify({"mensagem": "Chamado criado com sucesso!",
                    "chamado_id": novo_chamado.id}), 201

@chamado_bp.route('/paginados', methods=['GET'])
@jwt_required()  
def get_chamados_paginados():
    """
    Endpoint para listar usuários com suporte a paginação.
    Exemplos de como chamar via frontend:
    /chamados?page=1&per_page=10  (retorna os 10 primeiros usuários da página 1)
    /chamados?page=2&per_page=5   (retorna os 5 usuários da página 2)
    /chamados                     (usa os valores padrão: página 1, 10 por página)
    """
    
    # 1. Obter os parâmetros da URL, com valores padrão para o caso de não serem fornecidos.
    # O 'type=int' garante que, se o valor for fornecido, ele será convertido para inteiro.
    
    try:
        identidade_str_json = get_jwt_identity()
        identidade_dict = json.loads(identidade_str_json)
        usuario_id = identidade_dict.get("id")
        perfil_id = identidade_dict.get("perfil_id")
    except (TypeError, json.JSONDecodeError):
        return jsonify({"erro": "Formato da identidade no token é inválido."}), 401
    
    
    # 2. Obter os parâmetros de paginação da URL
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 3. Criar a query condicionalmente
    query_base = None
    if str(perfil_id) == '1': # Verifica se é Admin
        query_base = Chamado.query.order_by(desc(Chamado.id))
    else:
        # Usuário comum vê apenas seus próprios chamados.
        query_base = Chamado.query.filter_by(usuario_id=usuario_id).order_by(desc(Chamado.id))

    # 4. Aplicar a paginação na query base
    pagination_object = query_base.paginate(page=page, per_page=per_page, error_out=False)
    
    # 5. Extrair e serializar os itens da página atual
    chamados_da_pagina = pagination_object.items
    chamados_serializados = [chamado.to_dict() for chamado in chamados_da_pagina]
    
    # 6. Montar a resposta final com os metadados da paginação
    resultado_final = {
        'chamados': chamados_serializados,
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

@chamado_bp.route('/paginados/<string:status>', methods=['GET'])
@jwt_required()  
def get_chamados_paginados_byStatus(status):
    """
    Endpoint para listar usuários com suporte a paginação.
    Exemplos de como chamar via frontend:
    /chamados?page=1&per_page=10  (retorna os 10 primeiros usuários da página 1)
    /chamados?page=2&per_page=5   (retorna os 5 usuários da página 2)
    /chamados                     (usa os valores padrão: página 1, 10 por página)
    """
    
    # 1. Obter os parâmetros da URL, com valores padrão para o caso de não serem fornecidos.
    # O 'type=int' garante que, se o valor for fornecido, ele será convertido para inteiro.
    
    try:
        identidade_str_json = get_jwt_identity()
        identidade_dict = json.loads(identidade_str_json)
        usuario_id = identidade_dict.get("id")
        perfil_id = identidade_dict.get("perfil_id")
    except (TypeError, json.JSONDecodeError):
        return jsonify({"erro": "Formato da identidade no token é inválido."}), 401
    
    
    # 2. Obter os parâmetros de paginação da URL
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 3. Criar a query condicionalmente
    query_base = None
    if str(perfil_id) == '1': # Verifica se é Admin
        query_base = Chamado.query.order_by(desc(Chamado.id))
    else:
        # Usuário comum vê apenas seus próprios chamados.
        query_base = Chamado.query.filter_by(usuario_id=usuario_id).order_by(desc(Chamado.id))

    # 4. Aplicar a paginação na query base
    pagination_object = query_base.paginate(page=page, per_page=per_page, error_out=False)
    
    # 5. Extrair e serializar os itens da página atual
    chamados_da_pagina = pagination_object.items
    chamados_serializados = [chamado.to_dict() for chamado in chamados_da_pagina]
    
    # 6. Montar a resposta final com os metadados da paginação
    resultado_final = {
        'chamados': chamados_serializados,
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
