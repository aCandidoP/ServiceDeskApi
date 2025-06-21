from app.config.dbconfig import db

class Tipo(db.Model):
    __tablename__ = 'tipo'
    
    id = db.Column(db.Integer, primary_key=True)
    desc_tipo = db.Column(db.String(30), unique=True, nullable=False)
    categorias = db.relationship('Categoria', back_populates='tipo', lazy='dynamic')
    # Relação com Chamado (verificar necessidade)
    chamado = db.relationship('Chamado', back_populates='tipo')
    