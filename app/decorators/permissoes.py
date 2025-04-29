from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify

def somente_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        identidade = get_jwt_identity() 
        if identidade.get("perfil") != "Administrador":
            return jsonify({"erro": "Acesso negado. Apenas administradores."}), 403
        return f(*args, **kwargs)
    return wrapper
