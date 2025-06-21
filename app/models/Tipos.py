from app.config.dbconfig import db
from sqlalchemy import Integer, String

class Tipo(db.Model):
    __tablename__ = 'tipo'
    
    id = db.Column(db.Integer, primary_key=True)
    desc_tipo = db.Column(db.String(30))
    chamado = db.relationship('Chamado', back_populates='tipo')
    