from flask import Blueprint, jsonify, request
from app.models import Usuario
from app.config.dbconfig import db
from werkzeug.security import generate_password_hash
from app.routes import usuario_bp
import re
from flask_jwt_extended import jwt_required
from datetime import timedelta

def email_valido(email):
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(padrao, email)

# Rota para listar usuários
@usuario_bp.route("/", methods=["GET"])
@jwt_required()
def listar_usuarios():
    usuarios = Usuario.query.all()
    usuarios_json = [{"id": u.id, "nome": u.nome, "email": u.email, "perfil": u.perfil} for u in usuarios]
    return jsonify(usuarios_json)

# Rota para criar um novo usuário
@usuario_bp.route("/", methods=["POST"])
@jwt_required
def criar_usuario():
    dados = request.get_json()
    
    if not all(k in dados for k in ("nome", "email", "senha", "perfil")):
        return jsonify({"erro": "Campos obrigatórios: nome, email, senha, perfil"}), 400
    
    if not email_valido(dados["email"]):
        return jsonify({"erro": "E-mail inválido"}), 400
    
    senha_hash = generate_password_hash(dados["senha"])
    novo_usuario = Usuario(nome=dados["nome"], email=dados["email"], senha=senha_hash, perfil=dados["perfil"])
    
    db.session.add(novo_usuario)
    db.session.commit()
    
    return jsonify({"mensagem": "Usuário criado com sucesso!"}), 201

