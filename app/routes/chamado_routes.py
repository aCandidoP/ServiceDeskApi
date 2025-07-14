# app/routes/chamado_routes.py

from flask import jsonify, request
from app.models import Chamado, Usuario, Organizacao # Importar Usuario para a rota de criação
from app.config.dbconfig import db
from app.routes import chamado_bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.decorators import somente_admin
import json
from sqlalchemy import desc, func
import datetime


# Rota para listar todos os chamados (não paginada)
@chamado_bp.route('', methods=["GET"])
@jwt_required()
def listar_chamados():
    try:
        identidade_str_json = get_jwt_identity()
        identidade_dict = json.loads(identidade_str_json)
        usuario_id_token = identidade_dict.get("id")
        perfil_id = identidade_dict.get("perfil_id")
    except (TypeError, json.JSONDecodeError):
        return jsonify({"erro": "Formato da identidade no token é inválido."}), 401

    if str(perfil_id) == '1': # Verifica se é Admin
        chamados_query = Chamado.query.order_by(desc(Chamado.id))
    elif str(perfil_id) == '3': # 2. SENÃO, SE for Gerente de Organização...
        usuario_gerente = Usuario.query.get_or_404(usuario_id_token)
        chamados_query = Chamado.query.filter_by(organizacao_id=usuario_gerente.organizacao_id).order_by(desc(Chamado.id))
    else:
        # Filtra pelo campo 'requerente_id'
        chamados_query = Chamado.query.filter_by(requerente_id=usuario_id_token).order_by(desc(Chamado.id))
    
    chamados = chamados_query.all()
    
    # Usa o método .to_dict() para garantir uma serialização consistente e correta
    chamados_json = [c.to_dict() for c in chamados]
    
    return jsonify({"chamados": chamados_json})

# Rota para listar um chamado específico por ID
@chamado_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def listar_chamado_byId(id):
    chamado = Chamado.query.get_or_404(id)
    
    # Simplificado para usar o método .to_dict() do modelo, que já tem toda a lógica
    return jsonify(chamado.to_dict())


# Rota para listar chamados por status
@chamado_bp.route("/status/<string:status>", methods=["GET"])
@jwt_required()
def listar_chamado_byStatus(status):
    try:
        identidade_str_json = get_jwt_identity()
        identidade_dict = json.loads(identidade_str_json)
        usuario_id_token = identidade_dict.get("id")
        perfil_id = identidade_dict.get("perfil_id")
    except (TypeError, json.JSONDecodeError):
        return jsonify({"erro": "Formato da identidade no token é inválido."}), 401
        
    status_formatado = status.upper()

    if str(perfil_id) == '1': # Se for Admin, busca em todos os chamados
        chamados = Chamado.query.filter_by(status=status_formatado).order_by(Chamado.id.desc()).all()
    elif str(perfil_id) == '3': # 2. SENÃO, SE for Gerente de Organização...
        usuario_gerente = Usuario.query.filter_by(usuario_id_token)
        organizacao_do_gerente_id = usuario_gerente.to_dict()['organizacao_id']
        chamados = Chamado.query.filter_by(
            organizacao_id=organizacao_do_gerente_id
        ).order_by(desc(Chamado.id))
    else: # Se não, busca apenas nos chamados do próprio usuário
        chamados = Chamado.query.filter_by(status=status_formatado, requerente_id=usuario_id_token).order_by(Chamado.id.desc()).all()
    
    chamados_json = [chamado.to_dict() for chamado in chamados]
    
    return jsonify({"chamados": chamados_json})

# Rota para criar um novo chamado
@chamado_bp.route('/', methods=["POST"])
@jwt_required()
def criar_chamado():
    dados = request.get_json()
    
    # VALIDAÇÃO: Garante que todos os campos que o usuário deve enviar estão presentes
    if not all(k in dados for k in ("titulo", "tipo_id", "categoria_id", "descricao")):
        return jsonify({"erro": "Campos obrigatórios: titulo, tipo_id, categoria_id, descricao"}), 400
    
    # Pega o criador e a organização do token, não do JSON, para segurança
    try:
        identidade_str_json = get_jwt_identity()
        identidade_dict = json.loads(identidade_str_json)
        usuario_id_logado = identidade_dict.get("id")
        if not usuario_id_logado:
            return jsonify({"erro": "ID do usuário não encontrado no token."}), 401
    except (TypeError, json.JSONDecodeError):
        return jsonify({"erro": "Formato da identidade no token é inválido."}), 401

    usuario_logado = Usuario.query.get_or_404(usuario_id_logado)
    
    novo_chamado = Chamado(
        titulo=dados["titulo"],
        tipo_id=dados["tipo_id"],
        categoria_id=dados["categoria_id"],
        descricao=dados["descricao"], 
        status='NOVO',
        # ALTERAÇÃO: 'requerente_id' é definido pelo usuário do token
        requerente_id=usuario_logado.id,
        organizacao_id=usuario_logado.organizacao_id,
        # 'responsavel_id' é opcional e pode ser passado no JSON
        responsavel_id=dados.get("responsavel_id", None)
    )
    
    db.session.add(novo_chamado)
    db.session.commit()
    
    return jsonify({
        "mensagem": "Chamado criado com sucesso!",
        "chamado": novo_chamado.to_dict()
    }), 201


@chamado_bp.route('/paginados', methods=['GET'])
@jwt_required()
def get_chamados_paginados():
    try:
        identidade_str_json = get_jwt_identity()
        identidade_dict = json.loads(identidade_str_json)
        usuario_id_token = identidade_dict.get("id")
        perfil_id = identidade_dict.get("perfil_id")
    except (TypeError, json.JSONDecodeError):
        return jsonify({"erro": "Formato da identidade no token é inválido."}), 401
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query_base = None
    if str(perfil_id) == '1':
        query_base = Chamado.query.order_by(desc(Chamado.id))
    elif str(perfil_id) == '3': # 2. SENÃO, SE for Gerente de Organização...
        usuario_gerente = Usuario.query.get_or_404(usuario_id_token)
        query_base = Chamado.query.filter_by(organizacao_id=usuario_gerente.organizacao_id).order_by(desc(Chamado.id))
    else:
        query_base = Chamado.query.filter_by(requerente_id=usuario_id_token).order_by(desc(Chamado.id))

    pagination_object = query_base.paginate(page=page, per_page=per_page, error_out=False)
    
    chamados_da_pagina = pagination_object.items
    chamados_serializados = [chamado.to_dict() for chamado in chamados_da_pagina]
    
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

# Rota para listar chamados paginados por status
@chamado_bp.route('/paginados/<string:status>', methods=['GET'])
@jwt_required()
def get_chamados_paginados_byStatus(status):
    try:
        identidade_str_json = get_jwt_identity()
        identidade_dict = json.loads(identidade_str_json)
        usuario_id_token = identidade_dict.get("id")
        perfil_id = identidade_dict.get("perfil_id")
    except (TypeError, json.JSONDecodeError):
        return jsonify({"erro": "Formato da identidade no token é inválido."}), 401
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status_formatado = status.upper()
    
    query_base = None
    if str(perfil_id) == '1':
        query_base = Chamado.query.filter_by(status=status_formatado).order_by(desc(Chamado.id))
    elif str(perfil_id) == '3':
        usuario_gerente = Usuario.query.get_or_404(usuario_id_token)
        query_base = Chamado.query.filter_by(organizacao_id=usuario_gerente.organizacao_id, status=status_formatado).order_by(desc(Chamado.id))
    else:
        query_base = Chamado.query.filter_by(requerente_id=usuario_id_token, status=status_formatado).order_by(desc(Chamado.id))

    pagination_object = query_base.paginate(page=page, per_page=per_page, error_out=False)
    
    chamados_da_pagina = pagination_object.items
    chamados_serializados = [chamado.to_dict() for chamado in chamados_da_pagina]
    
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

@chamado_bp.route('/contagem_por_status', methods=['GET'])
@jwt_required()
def get_contagem_por_status():
    try:
        identidade_str_json = get_jwt_identity()
        identidade_dict = json.loads(identidade_str_json)
        usuario_id_token = identidade_dict.get("id")
        perfil_id = identidade_dict.get("perfil_id")

        query = db.session.query(
            Chamado.status, 
            func.count(Chamado.id).label('quantidade')
        )
        
        if str(perfil_id) == '3':
            usuario_gerente = Usuario.query.get_or_404(usuario_id_token)
            query = query.filter(Chamado.organizacao_id == usuario_gerente.organizacao_id)
        elif str(perfil_id) != '1': # Se não for admin nem gerente
            query = query.filter(Chamado.requerente_id == usuario_id_token)

        contagens = query.group_by(Chamado.status).all()
        resultado_formatado = {status: quantidade for status, quantidade in contagens}
        
        return jsonify(resultado_formatado)

    except Exception as e:
        print(f"Erro ao gerar estatísticas de chamados: {e}")
        return jsonify({"erro": "Não foi possível processar as estatísticas"}), 500

@chamado_bp.route('/<int:chamado_id>/status', methods=['PUT'])
@jwt_required()
def atualizar_status_chamado(chamado_id):
    """
    Atualiza o status de um chamado.
    Espera um JSON com o novo status, ex: {"status": "EM_ATENDIMENTO"}
    """
    dados = request.get_json()
    novo_status = dados.get('status')
    if not novo_status:
        return jsonify({"erro": "O campo 'status' é obrigatório."}), 400
    
    chamado_a_atualizar = Chamado.query.get_or_404(
        chamado_id, 
        description=f"Chamado com ID {chamado_id} não encontrado."
    )

    try:
        identidade_str_json = get_jwt_identity()
        identidade_dict = json.loads(identidade_str_json)
        usuario_id_logado = identidade_dict.get("id")
        perfil_id_logado = identidade_dict.get("perfil_id")
        
    except (TypeError, json.JSONDecodeError):
        return jsonify({"erro": "Formato da identidade no token é inválido."}), 401
        
    if str(perfil_id_logado) != '1' and chamado_a_atualizar.responsavel_id != usuario_id_logado:
        return jsonify({"erro": "Apenas o responsável ou um administrador podem alterar o status deste chamado."}), 403
    
    chamado_a_atualizar.status = novo_status.upper()
    if(chamado_a_atualizar.responsavel_id):
        pass
    else:
        chamado_a_atualizar.responsavel_id = usuario_id_logado
    chamado_a_atualizar.ultima_atualizacao = datetime.datetime.now()

    db.session.add(chamado_a_atualizar)
    db.session.commit()

    return jsonify({
        "mensagem": "Status do chamado atualizado com sucesso!",
        "chamado": chamado_a_atualizar.to_dict()
    })
