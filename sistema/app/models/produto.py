from app.extensions import db

class Produto(db.Model):
    __tablename__ = "produtos"

    id_produto = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.String(255))
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    estoque = db.Column(db.Integer, nullable=False, default=0)
    categoria = db.Column(db.String(100))
    fornecedor_id = db.Column(
        db.Integer,
        db.ForeignKey("fornecedores.id_fornecedor"),
        nullable=True,
    )
    imagem_url = db.Column(db.String(255), nullable=True)