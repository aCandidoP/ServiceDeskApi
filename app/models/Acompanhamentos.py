from app import db
from sqlalchemy import func

class Acompanhamento(db.Model):
    """
    Modelo para registrar cada interação em um chamado,
    seja um comentário do cliente ou uma nota técnica interna.
    """
    __tablename__ = 'acompanhamentos'

    id = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, server_default=func.now())
    chamado_id = db.Column(db.Integer, db.ForeignKey('chamados.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', back_populates='acompanhamentos')
    chamados = db.relationship('Chamado', back_populates='acompanhamentos')

    def to_dict(self):
        """Converte o objeto para um dicionário serializável para JSON."""
        return {
            'id': self.id,
            'comentario': self.comentario,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'usuario_id': self.usuario_id if self.usuario_id else None,
            'usuario_nome': self.usuario.nome
        }

    def __repr__(self):
        return f'<Acompanhamento id={self.id} chamado_id={self.chamado_id}>'