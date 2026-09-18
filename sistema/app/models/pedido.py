from app import db

class Pedido(db.Model):
    __tablename__ = "pedidos"
    id_pedido = db.Column(db.Integer, primary_key=True )
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id_cliente"))
    data_pedido = db.Column(db.Date)
    status = db.Column(db.String(50))
   

    def __repr__(self):
        return f"<Pedidos {self.id_pedido}>"
    
