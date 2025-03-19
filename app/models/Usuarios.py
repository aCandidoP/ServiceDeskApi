from app.config.dbconfig import db
from sqlalchemy import Integer, String

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    perfil = db.Column(db.String(50), nullable=False)
    
    chamados = db.relationship('Chamado', backref='usuario_rel', lazy=True)


    def __repr__(self):
        return f'<Usuario {self.nome}>'
