from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.config.dbconfig import DBConfig, db
from app.models import Categoria, Chamado, Organizacao, Servico, Usuario
from dotenv import load_dotenv
import os

load_dotenv()

migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=DBConfig): 
    app = Flask(__name__)
    
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "chave_padrao")
    app.debug = True
    
    app.config.from_object(config_class)  # Carrega as configurações do banco de dados

    # Inicializa as extensões Flask
    db.init_app(app)  # Passa a aplicação para a instância db
    migrate.init_app(app, db)
    
    from app.routes import usuario_bp, chamado_bp, auth_bp
    app.register_blueprint(usuario_bp)
    app.register_blueprint(chamado_bp)
    app.register_blueprint(auth_bp)
    
    
    from app.models import Servico, Chamado, Categoria, Organizacao, Usuario
    
    
    return app
