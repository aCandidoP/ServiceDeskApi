from app.config.dbconfig import db
from sqlalchemy import Integer, String

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfis.id'), nullable=False) 
    perfil = db.relationship('Perfil', back_populates='usuario')
    chamados = db.relationship('Chamado', back_populates='usuario', lazy=True)


    def __repr__(self):
        return f'<Usuario {self.nome}>'
