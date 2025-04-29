from flask import request, jsonify
from werkzeug.security import check_password_hash
from app.models import Usuario
from flask_jwt_extended import create_access_token
from app.routes import auth_bp

@auth_bp.route('', methods=['POST'])
def auth():
    dados = request.get_json()

    if not dados or not dados.get("email") or not dados.get("senha"):
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    usuario = Usuario.query.filter_by(email=dados["email"]).first()

    if not usuario or not check_password_hash(usuario.senha, dados["senha"]):
        return jsonify({"erro": "Credenciais inválidas"}), 401

    access_token = create_access_token(identity={"id": usuario.id, "perfil": usuario.perfil.perfil})

    return jsonify({"token": access_token, "mensagem": "Login realizado com sucesso!"})
