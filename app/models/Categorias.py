from app import db
from sqlalchemy.orm import backref

class Categoria(db.Model):
    """
    Modelo para as categorias de chamados, com suporte
    para uma estrutura hierárquica (pai-filho).
    """
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    
    parent_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=True)

    # Relação que busca as categorias "filhas".
    # 'backref' cria a relação de volta '.parent' automaticamente.
    children = db.relationship('Categoria',
                               backref=backref('parent', remote_side=[id]),
                               lazy='dynamic')

    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo.id'), nullable=False)
    tipo = db.relationship('Tipo', back_populates='categorias')
    
    chamados = db.relationship('Chamado', back_populates='categoria')
    
    def to_dict(self):
        """
        Converte o objeto para um dicionário, incluindo a estrutura
        de sub-categorias para o frontend.
        """
        permite_abertura = self.children.count() == 0

        return {
            'id': self.id,
            'nome': self.nome,
            'parent_id': self.parent_id,
            'permite_abertura': permite_abertura,
            # Chama o to_dict() para cada filho, criando a árvore aninhada.
            'sub_categorias': [child.to_dict() for child in self.children]
        }
    
    def __repr__(self):
        return f'<Categoria: {self.nome}>'