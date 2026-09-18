from flask import Blueprint, request, jsonify
from app import db
from app.models.pagamento import Pagamento
from app.models.pedido import Pedido

pagamento_bp = Blueprint("pagamento_bp", __name__, url_prefix="/pagamentos")


@pagamento_bp.route("/", methods=["GET"])
def listar_pagamentos():
    pagamentos = Pagamento.query.all()
    resultado = []
    for p in pagamentos:
        resultado.append({
            "id_pagamento": p.id_pagamento,
            "id_pedido": p.id_pedido,
            "valor": str(p.valor),
            "metodo": p.metodo,
            "data_pagamento": str(p.data_pagamento)
        })
    return jsonify(resultado)


@pagamento_bp.route("/<int:id_pagamento>", methods=["GET"])
def buscar_pagamento(id_pagamento):
    pagamento = Pagamento.query.get_or_404(id_pagamento)
    return jsonify({
        "id_pagamento": pagamento.id_pagamento,
        "id_pedido": pagamento.id_pedido,
        "valor": str(pagamento.valor),
        "metodo": pagamento.metodo,
        "data_pagamento": str(pagamento.data_pagamento)
    })


@pagamento_bp.route("/", methods=["POST"])
def criar_pagamento():
    dados = request.get_json()

    pedido = Pedido.query.get(dados.get("id_pedido"))
    if not pedido:
        return jsonify({"erro": "Pedido não encontrado"}), 404

    novo_pagamento = Pagamento(
        id_pedido=dados.get("id_pedido"),
        valor=dados.get("valor"),
        metodo=dados.get("metodo"),
        data_pagamento=dados.get("data_pagamento")
    )

    db.session.add(novo_pagamento)
    db.session.commit()

    return jsonify({"mensagem": "Pagamento criado com sucesso", "id_pagamento": novo_pagamento.id_pagamento}), 201


@pagamento_bp.route("/<int:id_pagamento>", methods=["PUT"])
def atualizar_pagamento(id_pagamento):
    pagamento = Pagamento.query.get_or_404(id_pagamento)
    dados = request.get_json()

    pagamento.id_pedido = dados.get("id_pedido", pagamento.id_pedido)
    pagamento.valor = dados.get("valor", pagamento.valor)
    pagamento.metodo = dados.get("metodo", pagamento.metodo)
    pagamento.data_pagamento = dados.get("data_pagamento", pagamento.data_pagamento)

    db.session.commit()

    return jsonify({"mensagem": "Pagamento atualizado com sucesso"})


@pagamento_bp.route("/<int:id_pagamento>", methods=["DELETE"])
def deletar_pagamento(id_pagamento):
    pagamento = Pagamento.query.get_or_404(id_pagamento)
    db.session.delete(pagamento)
    db.session.commit()

    return jsonify({"mensagem": "Pagamento deletado com sucesso"})