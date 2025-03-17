# app/configs/__init__.py
from app.config.dbconfig import DBConfig, db  # Importa as configurações do banco de dados

def init_app(app):
    """Configura o banco de dados e inicializa o SQLAlchemy no Flask."""
    app.config.from_object(DBConfig)  # Aplica as configurações do banco ao app
    db.init_app(app)  # Inicializa o SQLAlchemy com o Flask
