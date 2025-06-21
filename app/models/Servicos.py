from app import db

class Servico(db.Model):
    __tablename__ = 'servicos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    categoria = db.relationship('Categoria', back_populates='servicos')
    
    def to_dict(self):
        """
        Converte o objeto Perfil para um dicionário,
        facilitando a conversão para JSON.
        """
        return {
            'id': self.id,
            'perfil': self.perfil,
            'categoria_id': self.categoria_id
 
        }

    def __repr__(self):
        return f'<Servico {self.nome}>'
