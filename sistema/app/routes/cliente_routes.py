from flask import Blueprint, request, jsonify
from app import db
from app.models.cliente import Cliente

cliente_bp = Blueprint("cliente_bp", __name__, url_prefix="/clientes")


@cliente_bp.route("/", methods=["GET"])
def listar_clientes():
    clientes = Cliente.query.all()
    resultado = []
    for c in clientes:
        resultado.append({
            "id_cliente": c.id_cliente,
            "nome": c.nome,
            "nome_empresa": c.nome_empresa,
            "pais": c.pais,
            "email": c.email,
            "telefone": c.telefone
        })
    return jsonify(resultado)


@cliente_bp.route("/<int:id_cliente>", methods=["GET"])
def buscar_cliente(id_cliente):
    cliente = Cliente.query.get_or_404(id_cliente)
    return jsonify({
        "id_cliente": cliente.id_cliente,
        "nome": cliente.nome,
        "nome_empresa": cliente.nome_empresa,
        "pais": cliente.pais,
        "email": cliente.email,
        "telefone": cliente.telefone
    })


@cliente_bp.route("/", methods=["POST"])
def criar_cliente():
    dados = request.get_json()

    novo_cliente = Cliente(
        nome=dados.get("nome"),
        nome_empresa=dados.get("nome_empresa"),
        pais=dados.get("pais"),
        email=dados.get("email"),
        telefone=dados.get("telefone")
    )

    db.session.add(novo_cliente)
    db.session.commit()

    return jsonify({"mensagem": "Cliente criado com sucesso", "id_cliente": novo_cliente.id_cliente}), 201


@cliente_bp.route("/<int:id_cliente>", methods=["PUT"])
def atualizar_cliente(id_cliente):
    cliente = Cliente.query.get_or_404(id_cliente)
    dados = request.get_json()

    cliente.nome = dados.get("nome", cliente.nome)
    cliente.nome_empresa = dados.get("nome_empresa", cliente.nome_empresa)
    cliente.pais = dados.get("pais", cliente.pais)
    cliente.email = dados.get("email", cliente.email)
    cliente.telefone = dados.get("telefone", cliente.telefone)

    db.session.commit()

    return jsonify({"mensagem": "Cliente atualizado com sucesso"})


@cliente_bp.route("/<int:id_cliente>", methods=["DELETE"])
def deletar_cliente(id_cliente):
    cliente = Cliente.query.get_or_404(id_cliente)
    db.session.delete(cliente)
    db.session.commit()

    return jsonify({"mensagem": "Cliente deletado com sucesso"})