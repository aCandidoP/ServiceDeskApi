from app import db
from sqlalchemy import Integer, ForeignKey
import datetime



class Chamado(db.Model):
    __tablename__ = 'chamados'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    tipo_id = db.Column(Integer, ForeignKey('tipo.id'), nullable=False)
    tipo = db.relationship('Tipo', back_populates='chamado')
    categoria_id = db.Column(Integer, ForeignKey('categorias.id'), nullable=False)
    categoria = db.relationship('Categoria', back_populates='chamados')
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(40))
    data_criacao = db.Column(db.DateTime, default=lambda: datetime.datetime.now())
    usuario_id = db.Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', back_populates='chamados')
    organizacao_id = db.Column(Integer, ForeignKey('organizacoes.id'))
    organizacao = db.relationship('Organizacao', back_populates='chamados_organizacao')
    acompanhamentos = db.relationship(
        'Acompanhamento', 
        back_populates='chamado', 
        lazy='dynamic',
        order_by='Acompanhamento.data_criacao.asc()'
    )
    
    
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'tipo_id': self.categoria.tipo_id,
            'desc_tipo': self.categoria.tipo.desc_tipo,
            'categoria_id': self.categoria_id,
            'categoria_nome': self.categoria.nome,
            'descricao': self.descricao,
            'status': self.status,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'usuario_id': self.usuario.id,
            'usuario_nome': self.usuario.nome if self.usuario else None,
            'organizacao_id': self.organizacao_id if self.organizacao_id else None,
            'organizacao_nome': self.organizacao.nome if self.organizacao.nome else None,
            
            'acompanhamentos': [
                acompanhamento.to_dict() for acompanhamento in self.acompanhamentos
            ]
        }

        

    def __repr__(self):
        return f'<Chamado {self.titulo}>'
