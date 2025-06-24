from flask import jsonify, json
from app.models import Acompanhamento, Chamado
from app.routes import acompanhamento_bp
from flask_jwt_extended  import jwt_required, get_jwt_identity
from app.decorators import somente_admin
from flask import request
from app.config.dbconfig import db


@acompanhamento_bp.route('/:int<chamado_id>', methods=["GET"])
@jwt_required()
@somente_admin
def listar_acompanhamentos_idChamado(chamado_id):
    acompanhamentos_chamado = Acompanhamento.query.filter_by(chamado_id=chamado_id)
    acompanhamentos_json = [{
        "id": acompanhamento.id,
        "comentario": acompanhamento.nome,
        "data_criacao": acompanhamento.cidade ,
        "chamado_id": acompanhamento.estado, 
        "usuario_id": acompanhamento.segmento,
        "chamado_titulo": acompanhamento.chamado.titulo
    }for acompanhamento in acompanhamentos_chamado]
    
    return(jsonify(acompanhamentos_json))
    
@acompanhamento_bp.route('', methods=["POST"])
@jwt_required() 
def incluir_acompanhamento():
    """
    Cria um novo acompanhamento (comentário) para um chamado existente.
    Qualquer usuário autenticado pode adicionar um comentário.
    Espera um JSON com 'comentario' e 'chamado_id'.
    """
    dados = request.get_json()
    
    if not dados or not all(k in dados for k in ("comentario", "chamado_id")):
        return jsonify({"erro": "Os campos 'comentario' e 'chamado_id' são obrigatórios."}), 400

    chamado_id = dados['chamado_id']
    
    # Obtém a identidade do usuário que está fazendo o comentário, a partir do token.
    try:
        identidade_str_json = get_jwt_identity()
        identidade_dict = json.loads(identidade_str_json)
        usuario_id_logado = identidade_dict.get("id")
        if not usuario_id_logado:
            return jsonify({"erro": "ID do usuário não encontrado no token."}), 401
    except (TypeError, json.JSONDecodeError):
        return jsonify({"erro": "Formato da identidade no token é inválido."}), 401
    
    # VERIFICAÇÃO DE SEGURANÇA: Garante que o chamado realmente existe.
    Chamado.query.get_or_404(chamado_id, description=f"Não é possível adicionar acompanhamento a um chamado (ID: {chamado_id}) que não existe.")

    novo_acompanhamento = Acompanhamento(
        comentario=dados['comentario'],
        chamado_id=chamado_id,        # Pego do corpo do JSON
        usuario_id=usuario_id_logado    
        
    )
    
    db.session.add(novo_acompanhamento)
    db.session.commit()
    
    return jsonify({
        "mensagem": "Acompanhamento incluído com sucesso!",
        "acompanhamento": novo_acompanhamento.to_dict()
    }), 201