from app import db
from sqlalchemy import Integer, ForeignKey, func
from time import strftime
import datetime



class Chamado(db.Model):
    __tablename__ = 'chamados'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(40))
    data_criacao = db.Column(db.DateTime, default=lambda: datetime.datetime.now())
    
    requerente_id = db.Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    responsavel_id = db.Column(Integer, ForeignKey('usuarios.id'), nullable=True)

    requerente = db.relationship(
        'Usuario', 
        back_populates='chamados_criados',
        foreign_keys=[requerente_id] 
    )
    
    responsavel = db.relationship(
        'Usuario',
        back_populates='chamados_atribuidos',
        foreign_keys=[responsavel_id] 
    )

    tipo_id = db.Column(Integer, ForeignKey('tipo.id'), nullable=False)
    tipo = db.relationship('Tipo', back_populates='chamado')

    categoria_id = db.Column(Integer, ForeignKey('categorias.id'), nullable=False)
    categoria = db.relationship('Categoria', back_populates='chamados')
    
    organizacao_id = db.Column(Integer, ForeignKey('organizacoes.id'), nullable=False)
    organizacao = db.relationship('Organizacao', back_populates='chamados_organizacao')

    acompanhamentos = db.relationship(
        'Acompanhamento', 
        back_populates='chamado', 
        lazy='dynamic',
        order_by='Acompanhamento.data_criacao.asc()'
    )
    
    def to_dict(self):
        """
        Converte o objeto para um dicionário, usando as novas relações
        'criador' e 'responsavel' para garantir os dados corretos.
        """
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'status': self.status,
            'data_criacao': self.data_criacao.strftime("%d/%m/%Y %H:%M") if self.data_criacao else None,
            'tipo': {'id': self.tipo.id, 'desc_tipo': self.tipo.desc_tipo} if self.tipo else None,
            'categoria': {'id': self.categoria.id, 'nome': self.categoria.nome} if self.categoria else None,
            'organizacao': {'id': self.organizacao.id, 'nome': self.organizacao.nome} if self.organizacao else None,
            
            'requerente': {
                'id': self.requerente.id,
                'nome': self.requerente.nome
            } if self.requerente else None,
            
            'responsavel': {
                'id': self.responsavel.id,
                'nome': self.responsavel.nome
            } if self.responsavel else None,
            
            'acompanhamentos': [
                acomp.to_dict() for acomp in self.acompanhamentos.all()
            ]
        }

    def __repr__(self):
        return f'<Chamado {self.titulo}>'
