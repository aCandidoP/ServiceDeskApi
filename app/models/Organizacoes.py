from app.config.dbconfig import db
from sqlalchemy import Integer, String

class Organizacao(db.Model):
    __tablename__ = 'organizacoes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(15), nullable=False)
    segmento = db.Column(db.String(100), nullable=False)
    

    

    def __repr__(self):
        return f'<Usuario {self.nome}>'