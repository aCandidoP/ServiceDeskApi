from flask import jsonify, request
from app.models import Chamado
from app.config.dbconfig import db
from app.routes import chamado_bp


@chamado_bp.route('', methods=["GET"])
def listar_chamados():
    chamados = Chamado.query.all()
    chamados_json = [{"id": c.id, "titulo": c.titulo, "tipo": c.tipo , "categoria": c.categoria, "data_criacao": c.data_criacao,
                      "status": c.status, "usuario_id": c.usuario_id} for c in chamados]
    return jsonify(chamados_json)

@chamado_bp.route('', methods=["POST"])
def criar_usuario():
    dados = request.get_json()
    
    if not all(k in dados for k in ("titulo", "tipo", "categoria", "usuario_id")):
        return jsonify({"erro": "Campos obrigatórios: titulo, tipo, categoria, usuario_id"}), 400
    
    
    novo_chamado = Chamado(titulo=dados["titulo"], tipo=dados["tipo"], categoria=dados["categoria"], status='Novo', usuario_id=dados["usuario_id"])
    
    db.session.add(novo_chamado)
    db.session.commit()
    
    return jsonify({"mensagem": "Chamado criado com sucesso!"}), 201
