from app import db
from sqlalchemy import Integer, String, ForeignKey
from app.config.dbconfig import db 

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfis.id'), nullable=False) 
    perfil = db.relationship('Perfil', back_populates='usuarios')
    
    organizacao_id = db.Column(Integer, ForeignKey('organizacoes.id'), nullable=False)
    organizacao = db.relationship('Organizacao', back_populates='usuarios')

    chamados_criados = db.relationship(
        'Chamado',
        back_populates='requerente',
        foreign_keys='Chamado.requerente_id',
        lazy='dynamic' 
    )

    
    chamados_atribuidos = db.relationship(
        'Chamado',
        back_populates='responsavel',
        foreign_keys='Chamado.responsavel_id',
        lazy='dynamic'
    )
    
   
    acompanhamentos = db.relationship('Acompanhamento', back_populates='usuario', lazy='dynamic')
    
    def to_dict(self):
        """
        Converte o objeto Usuario para um dicionário serializável.
        Nota: Serializar as listas de chamados/acompanhamentos aqui pode
        causar recursão infinita. Geralmente é melhor não incluí-los
        na serialização padrão do usuário.
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'perfil': self.perfil.to_dict() if self.perfil else None,
            'organizacao': {
                'id': self.organizacao.id,
                'nome': self.organizacao.nome
            } if self.organizacao else None
        }
    
    def __repr__(self):
        return f'<Usuario {self.nome}>'