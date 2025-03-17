from app import db
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship
import datetime

class Chamado(db.Model):
    __tablename__ = 'chamados'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(15), nullable=False)
    data_criacao = db.Column(db.DateTime, default=lambda: datetime.now())
    usuario_id = db.Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    usuario = relationship('Usuarios', back_populates='chamados')
    

    

    def __repr__(self):
        return f'<Usuario {self.nome}>'
