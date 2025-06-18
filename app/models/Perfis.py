from app import db

class Perfil(db.Model):
    __tablename__ = 'perfis'
    
    id = db.Column(db.Integer, primary_key=True)
    perfil = db.Column(db.String(100), nullable=False)
    
    usuario = db.relationship('Usuario', back_populates='perfil')
    
    def to_dict(self):
        """
        Converte o objeto Perfil para um dicionário,
        facilitando a conversão para JSON.
        """
        return {
            'id': self.id,
            'perfil': self.perfil
 
        }
    
    def __repr__(self):
        return f'Perfil: {self.perfil}'