from app import db

class Servico(db.Model):
    __tablename__ = 'servicos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False, unique=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)

    categoria = db.relationship('Categoria', back_populates='servicos')

    def __repr__(self):
        return f'<Servico {self.nome} - Categoria: {self.categoria.nome}>'
