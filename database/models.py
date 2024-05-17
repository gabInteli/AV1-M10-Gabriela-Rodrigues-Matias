from sqlalchemy import Column, Integer, String, DateTime
from database.database import db

class Pedido(db.Model):
    __tablename__ = 'Pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f'<Pedido:[id:{self.id}, nome:{self.npme}, email:{self.email}, descricao:{self.descricao}]>'

    def serialize(self):
        return {
        "id": self.id,
        "nome": self.nome,
        "email": self.email,
        "descricao": self.descricao
        }
