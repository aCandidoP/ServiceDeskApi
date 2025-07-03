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
    
    def to_dict(self, include_children=True):
        """
        Converte o objeto para um dicionário.
        O parâmetro 'include_children' controla se as sub-categorias devem ser incluídas.
        """
        permite_abertura = self.children.count() == 0

        data = {
            'id': self.id,
            'nome': self.nome,
            'parent_id': self.parent_id,
            'permite_abertura': permite_abertura
        }
        
        if include_children:
            data['sub_categorias'] = [child.to_dict(include_children=False) for child in self.children]
        
        return data
    
    def __repr__(self):
        return f'<Categoria: {self.nome}>'
    
    