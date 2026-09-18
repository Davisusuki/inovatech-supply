from app import db

class Fornecedor(db.Model):
    __tablename__ = "fornecedores"

    id_fornecedor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    pais = db.Column(db.String(50))
    contato = db.Column(db.String(100))

    def __repr__(self):
        return f"<Fornecedor {self.nome}>"