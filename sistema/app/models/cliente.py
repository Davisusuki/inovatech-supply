from app import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id_cliente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    nome_empresa = db.Column(db.String(150))
    pais = db.Column(db.String(100))
    email = db.Column(db.String(150), unique=True)
    telefone = db.Column(db.String(50))

    def __repr__(self):
        return f"<Cliente {self.nome}>"