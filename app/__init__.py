from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.config.dbconfig import DBConfig, db

migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=DBConfig):
    app = Flask(__name__)  # Inicializa a aplicação Flask
    app.config.from_object(config_class)  # Carrega as configurações do banco de dados

    # Inicializa as extensões Flask
    db.init_app(app)  # Passa a aplicação para a instância db
    migrate.init_app(app, db)
    
    from app.models import chamado, usuario, organizacao

    return app
