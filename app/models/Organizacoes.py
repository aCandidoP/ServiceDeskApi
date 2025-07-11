from app.config.dbconfig import db

class Organizacao(db.Model):
    __tablename__ = 'organizacoes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    segmento = db.Column(db.String(100), nullable=False)
    chamados_organizacao = db.relationship('Chamado', back_populates='organizacao')
    usuarios = db.relationship('Usuario', back_populates='organizacao')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cidade': self.cidade,
            'estado': self.estado,
            'segmento': self.segmento
        }
    
    
    def __repr__(self):
        return f'<Organizacao {self.nome}>'