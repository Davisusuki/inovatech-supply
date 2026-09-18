from flask import Blueprint, request, jsonify
from app import db
from app.models.pedido import Pedido
from app.models.cliente import Cliente

pedido_bp = Blueprint("pedido_bp", __name__, url_prefix="/pedidos")


@pedido_bp.route("/", methods=["GET"])
def listar_pedidos():
    pedidos = Pedido.query.all()
    resultado = []
    for p in pedidos:
        resultado.append({
            "id_pedido": p.id_pedido,
            "id_cliente": p.id_cliente,
            "data_pedido": str(p.data_pedido),
            "status": p.status
        })
    return jsonify(resultado)


@pedido_bp.route("/<int:id_pedido>", methods=["GET"])
def buscar_pedido(id_pedido):
    pedido = Pedido.query.get_or_404(id_pedido)
    return jsonify({
        "id_pedido": pedido.id_pedido,
        "id_cliente": pedido.id_cliente,
        "data_pedido": str(pedido.data_pedido),
        "status": pedido.status
    })


@pedido_bp.route("/", methods=["POST"])
def criar_pedido():
    dados = request.get_json()

    cliente = Cliente.query.get(dados.get("id_cliente"))
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    novo_pedido = Pedido(
        id_cliente=dados.get("id_cliente"),
        data_pedido=dados.get("data_pedido"),
        status=dados.get("status")
    )

    db.session.add(novo_pedido)
    db.session.commit()

    return jsonify({"mensagem": "Pedido criado com sucesso", "id_pedido": novo_pedido.id_pedido}), 201


@pedido_bp.route("/<int:id_pedido>", methods=["PUT"])
def atualizar_pedido(id_pedido):
    pedido = Pedido.query.get_or_404(id_pedido)
    dados = request.get_json()

    pedido.id_cliente = dados.get("id_cliente", pedido.id_cliente)
    pedido.data_pedido = dados.get("data_pedido", pedido.data_pedido)
    pedido.status = dados.get("status", pedido.status)

    db.session.commit()

    return jsonify({"mensagem": "Pedido atualizado com sucesso"})


@pedido_bp.route("/<int:id_pedido>", methods=["DELETE"])
def deletar_pedido(id_pedido):
    pedido = Pedido.query.get_or_404(id_pedido)
    db.session.delete(pedido)
    db.session.commit()

    return jsonify({"mensagem": "Pedido deletado com sucesso"})