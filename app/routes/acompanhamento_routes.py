from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
import datetime

from app.models import Acompanhamento, Chamado
from app import db
from . import acompanhamento_bp

@acompanhamento_bp.route('', methods=["POST"])
@jwt_required() 
def incluir_acompanhamento():
    """
    Cria um novo acompanhamento e atualiza a data de 'ultima_atualizacao'
    do chamado correspondente.
    """
    dados = request.get_json()
    
    if not dados or not all(k in dados for k in ("comentario", "chamado_id")):
        return jsonify({"erro": "Os campos 'comentario' e 'chamado_id' são obrigatórios."}), 400

    chamado_id = dados['chamado_id']
    
    try:
        identidade_str_json = get_jwt_identity()
        identidade_dict = json.loads(identidade_str_json)
        usuario_id_logado = identidade_dict.get("id")
        if not usuario_id_logado:
            return jsonify({"erro": "ID do usuário não encontrado no token."}), 401
    except (TypeError, json.JSONDecodeError):
        return jsonify({"erro": "Formato da identidade no token é inválido."}), 401
    
    # --- LÓGICA DE ATUALIZAÇÃO ---

    chamado_a_atualizar = Chamado.query.get_or_404(
        chamado_id, 
        description=f"Não é possível adicionar acompanhamento a um chamado (ID: {chamado_id}) que não existe."
    )

    chamado_a_atualizar.ultima_atualizacao = datetime.datetime.now()

    novo_acompanhamento = Acompanhamento(
        comentario=dados['comentario'],
        chamado_id=chamado_id,
        usuario_id=usuario_id_logado
    )
    
    db.session.add(novo_acompanhamento)
    db.session.add(chamado_a_atualizar)
    
    db.session.commit()
    
    return jsonify({
        "mensagem": "Acompanhamento incluído e chamado atualizado com sucesso!",
        "acompanhamento": novo_acompanhamento.to_dict()
    }), 201