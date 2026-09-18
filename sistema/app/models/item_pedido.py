from app import db

class ItemPedido(db.Model):
    __tablename__ = "itens_pedido"
    id_item = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey("pedidos.id_pedido"))
    id_produto = db.Column(db.Integer, db.ForeignKey("produtos.id_produto"))
    preco_unitario = db.Column(db.Numeric(10, 2))

    def __repr__(self):
        return f"<ItemPedido {self.id_item}>"