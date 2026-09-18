from flask import Blueprint, request, jsonify
from app import db
from app.models.item_pedido import ItemPedido
from app.models.pedido import Pedido
from app.models.produto import Produto

item_pedido_bp = Blueprint("item_pedido_bp", __name__, url_prefix="/itens_pedido")


@item_pedido_bp.route("/", methods=["GET"])
def listar_itens_pedido():
    itens = ItemPedido.query.all()
    resultado = []
    for i in itens:
        resultado.append({
            "id_item": i.id_item,
            "id_pedido": i.id_pedido,
            "id_produto": i.id_produto,
            "preco_unitario": "{0}".format(i.preco_unitario)
        })
    return jsonify(resultado)


@item_pedido_bp.route("/<int:id_item>", methods=["GET"])
def buscar_item_pedido(id_item):
    item = ItemPedido.query.get_or_404(id_item)
    return jsonify({
        "id_item": item.id_item,
        "id_pedido": item.id_pedido,
        "id_produto": item.id_produto,
        "preco_unitario": "{0}".format(item.preco_unitario)
    })


@item_pedido_bp.route("/", methods=["POST"])
def criar_item_pedido():
    dados = request.get_json()

    # Aqui são DUAS verificações, uma para cada FK
    pedido = Pedido.query.get(dados.get("id_pedido"))
    if not pedido:
        return jsonify({"erro": "Pedido não encontrado"}), 404

    produto = Produto.query.get(dados.get("id_produto"))
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    novo_item = ItemPedido(
        id_pedido=dados.get("id_pedido"),
        id_produto=dados.get("id_produto"),
        preco_unitario=dados.get("preco_unitario")
    )

    db.session.add(novo_item)
    db.session.commit()

    return jsonify({"mensagem": "Item de pedido criado com sucesso", "id_item": novo_item.id_item}), 201


@item_pedido_bp.route("/<int:id_item>", methods=["PUT"])
def atualizar_item_pedido(id_item):
    item = ItemPedido.query.get_or_404(id_item)
    dados = request.get_json()

    item.id_pedido = dados.get("id_pedido", item.id_pedido)
    item.id_produto = dados.get("id_produto", item.id_produto)
    item.preco_unitario = dados.get("preco_unitario", item.preco_unitario)

    db.session.commit()

    return jsonify({"mensagem": "Item de pedido atualizado com sucesso"})


@item_pedido_bp.route("/<int:id_item>", methods=["DELETE"])
def deletar_item_pedido(id_item):
    item = ItemPedido.query.get_or_404(id_item)
    db.session.delete(item)
    db.session.commit()

    return jsonify({"mensagem": "Item de pedido deletado com sucesso"})