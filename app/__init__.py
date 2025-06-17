from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.config.dbconfig import DBConfig, db
from app.models import Categoria, Chamado, Organizacao, Servico, Usuario, Tipo
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()

migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=DBConfig): 
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "*"}}, methods=["GET", "POST", "OPTIONS"])
    
    jwt.init_app(app)
    
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_TOKEN_LOCATION"] = os.getenv("JWT_TOKEN_LOCATION", ["headers"])
    app.debug = True
    
    app.config.from_object(config_class)  # Carrega as configurações do banco de dados

    db.init_app(app) 
    migrate.init_app(app, db)
    
    from app.routes import usuario_bp, chamado_bp, auth_bp
    app.register_blueprint(usuario_bp)
    app.register_blueprint(chamado_bp)
    app.register_blueprint(auth_bp)
    
    
    from app.models import Servico, Chamado, Categoria, Organizacao, Usuario
    
    
    return app
