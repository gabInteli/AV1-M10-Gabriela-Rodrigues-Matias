from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pedidos.db"
db = SQLAlchemy(app)

class Pedidos(db.Model):
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

@app.route("/novo", methods=["POST"])
def create_pedido():
    data = request.json
    pedido = Pedidos(nome=data["nome"], email=data["email"], descricao=data["descricao"])
    db.create_all()
    db.session.add(pedido)
    db.session.commit()
    return jsonify({"id": pedido.id})

@app.route("/pedidos", methods=["GET"])
def get_pedidos():
    pedidos = Pedidos.query.all()
    return jsonify([{"id": p.id, "nome": p.nome, "email": p.email, "descricao": p.descricao} for p in pedidos])

@app.route("/pedidos/<int:id>", methods=["GET", "PUT", "DELETE"])
def get_pedido(id):
    pedido = Pedidos.query.get(id)
    if pedido is None:
        return jsonify({"error": "Pedido não encontrado"}), 404
    if request.method == "GET":
        return jsonify({"id": pedido.id, "nome": pedido.nome, "email": pedido.email, "descricao": pedido.descricao})
    elif request.method == "PUT":
        data = request.json
        pedido.nome = data["nome"]
        pedido.email = data["email"]
        pedido.descricao = data["descricao"]
        db.session.commit()
        return jsonify({"id": pedido.id, "nome": pedido.nome, "email": pedido.email, "descricao": pedido.descricao})
    elif request.method == "DELETE":
        db.session.delete(pedido)
        db.session.commit()
        return jsonify({"message": "Pedido excluído com sucesso"})

if __name__ == "__main__":
    app.run(debug=True)