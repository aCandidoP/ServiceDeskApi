from app import db

class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo.id'), nullable=False)
    tipo = db.relationship('Tipo', back_populates='categorias')
    servicos = db.relationship('Servico', back_populates='categoria', lazy='dynamic')
    
    def __repr__(self):
        return f'<Categoria: {self.nome}>'