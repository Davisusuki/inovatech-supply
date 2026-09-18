from app import db

class Pagamento(db.Model):
    __tablename__ = "pagamentos"
    id_pagamento = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey("pedidos.id_pedido") )
    valor = db.Column(db.Numeric(10, 2))
    metodo = db.Column(db.String(50))
    data_pagamento = db.Column(db.Date)

    def __repr__(self):
        return f"<pagamento {self.id_pagamento}>"