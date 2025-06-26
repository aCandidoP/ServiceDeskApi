from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.config.dbconfig import DBConfig, db
from dotenv import load_dotenv
import os
from flask_cors import CORS
import ast
from datetime import timedelta

load_dotenv()

migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=DBConfig): 
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "*"}}, methods=["GET", "POST", "OPTIONS", "PUT"], supports_credentials=True)
    
    app.config.from_object(config_class) 
    
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    
    jwt_token_location_env = os.getenv("JWT_TOKEN_LOCATION")
    if jwt_token_location_env:
        try:
            app.config["JWT_TOKEN_LOCATION"] = ast.literal_eval(jwt_token_location_env)
        except (ValueError, SyntaxError):
            print(f"AVISO: JWT_TOKEN_LOCATION do ambiente é inválido ('{jwt_token_location_env}'). Usando padrão ['headers'].")
            app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    else:
        app.config["JWT_TOKEN_LOCATION"] = ["headers"]

    app.debug = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    
    
    db.init_app(app) 
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    from app.routes.usuario_routes import usuario_bp
    from app.routes.chamado_routes import chamado_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.categoria_routes import categoria_bp
    from app.routes.tipo_routes import tipo_bp
    from app.routes.organizacoes_routes import organizacao_bp
    from app.routes.acompanhamento_routes import acompanhamento_bp
    
    app.register_blueprint(usuario_bp)
    app.register_blueprint(chamado_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tipo_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(organizacao_bp)
    app.register_blueprint(acompanhamento_bp)
    
    return app