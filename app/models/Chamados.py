from app import db
from sqlalchemy import Integer, ForeignKey
import datetime

class Chamado(db.Model):
    __tablename__ = 'chamados'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    tipo_id = db.Column(Integer, ForeignKey('tipo.id'), nullable=False)
    tipo = db.relationship('Tipo', back_populates='chamado')
    categoria = db.Column(db.String(15), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(40))
    data_criacao = db.Column(db.DateTime, default=lambda: datetime.datetime.now())
    usuario_id = db.Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', back_populates='chamados')
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'tipo': self.tipo_id,
            'categoria': self.categoria,
            'descricao': self.descricao,
            'status': self.status,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'usuario_id': self.usuario.id,
            'usuario_nome': self.usuario.nome if self.usuario else None
        }

        

    def __repr__(self):
        return f'<Usuario {self.titulo}>'
