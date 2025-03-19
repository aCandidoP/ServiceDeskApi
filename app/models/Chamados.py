from app import db
from sqlalchemy import Integer, ForeignKey
import datetime
from app.models import Usuario

class Chamado(db.Model):
    __tablename__ = 'chamados'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    categoria = db.Column(db.String(15), nullable=False)
    data_criacao = db.Column(db.DateTime, default=lambda: datetime.datetime.now())
    usuario_id = db.Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    
    usuario = db.relationship('Usuario', back_populates='chamados')
    

    

    def __repr__(self):
        return f'<Usuario {self.nome}>'
