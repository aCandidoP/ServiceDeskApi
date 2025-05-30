from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify
import json # << IMPORTAR JSON AQUI

def somente_admin(f): # Novo nome para clareza
    @wraps(f)
    def wrapper(*args, **kwargs):
        identidade_str_json = get_jwt_identity()
        if not isinstance(identidade_str_json, str):
            print("ERRO no Decorator: A identidade não é uma string, como esperado para decodificação JSON.")
            return jsonify({"erro": "Formato da identidade no token inesperado (não é string para JSON)."}), 401

        try:
            identidade_dict = json.loads(identidade_str_json)
        except json.JSONDecodeError:
            print(f"ERRO no Decorator: Falha ao decodificar a string JSON da identidade: '{identidade_str_json}'")
            return jsonify({"erro": "Formato da identidade (string JSON) inválido no token."}), 401
        
        print(f"DEBUG no Decorator: Dicionário decodificado da identidade: {identidade_dict}")

        perfil_id = identidade_dict.get("perfil_id")

        if perfil_id is None:
            print(f"AVISO no Decorator: Chave 'perfil_id' não encontrada no dicionário da identidade. Conteúdo: {identidade_dict}")
            return jsonify({"erro": "Chave 'perfil_id' não encontrada nos dados da identidade."}), 403
        
        print(f"DEBUG no Decorator: 'perfil_id' encontrado: {perfil_id}, tipo: {type(perfil_id)}")

        if str(perfil_id) == '1': 
            return f(*args, **kwargs)
        else:
            return jsonify({"erro": "Acesso negado. Somente administradores."}), 403
    return wrapper