from flask import jsonify
from app.models import Organizacao
from app.routes import organizacao_bp
from flask_jwt_extended  import jwt_required
from app.decorators import somente_admin
from flask import request
from app.config.dbconfig import db


@organizacao_bp.route('', methods=["GET"])
@jwt_required()
@somente_admin
def listar_organizacoes():
    organizacoes = Organizacao.query.all()
    organizacoes_json = [{
        "id": o.id,
        "nome": o.nome,
        "cidade": o.cidade ,
        "estado": o.estado, 
        "segmento": o.segmento 
        
    }for o in organizacoes]
    
    return(jsonify(organizacoes_json))
    
@organizacao_bp.route('/', methods=["POST"])
@jwt_required()
@somente_admin
def cadastrar_organizacao():
    dados = request.get_json()
    
    if not all(k in dados for k in ("nome", "cidade", "estado", "segmento")):
        return jsonify({"erro": "Campos obrigatórios não preenchidos"}), 400
    
    nova_organizacao = Organizacao(nome=dados['nome'], cidade=dados['cidade'], estado=dados['estado'],
                                   segmento=dados['segmento'])
    
    
    db.session.add(nova_organizacao)
    db.session.commit()
    
    return jsonify({"mensagem": "Organização Criada com Sucessp!"}), 201