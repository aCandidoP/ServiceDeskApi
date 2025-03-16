import os
from flask_sqlalchemy import SQLAlchemy

# Instancia o objeto SQLAlchemy
db = SQLAlchemy()

class DBConfig:
    # Conexão com o banco de dados MySQL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://flask_user:J2425#!lda*@localhost/servicedesk')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desabilita o rastreamento de modificações para economizar memória
