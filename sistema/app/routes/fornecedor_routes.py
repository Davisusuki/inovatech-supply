from flask import Blueprint, request, jsonify
from app import db
from app.models.fornecedor import Fornecedor

fornecedor_bp = Blueprint("fornecedor_bp", __name__, url_prefix="/fornecedores")


@fornecedor_bp.route("/", methods=["GET"])
def listar_fornecedores():
    fornecedores = Fornecedor.query.all()
    resultado = []
    for f in fornecedores:
        resultado.append({
            "id_fornecedor": f.id_fornecedor,
            "nome": f.nome,
            "pais": f.pais,
            "contato": f.contato
        })
    return jsonify(resultado)


@fornecedor_bp.route("/<int:id_fornecedor>", methods=["GET"])
def buscar_fornecedor(id_fornecedor):
    fornecedor = Fornecedor.query.get_or_404(id_fornecedor)
    return jsonify({
        "id_fornecedor": fornecedor.id_fornecedor,
        "nome": fornecedor.nome,
        "pais": fornecedor.pais,
        "contato": fornecedor.contato
    })


@fornecedor_bp.route("/", methods=["POST"])
def criar_fornecedor():
    dados = request.get_json()

    novo_fornecedor = Fornecedor(
        nome=dados.get("nome"),
        pais=dados.get("pais"),
        contato=dados.get("contato")
    )

    db.session.add(novo_fornecedor)
    db.session.commit()

    return jsonify({"mensagem": "Fornecedor criado com sucesso", "id_fornecedor": novo_fornecedor.id_fornecedor}), 201


@fornecedor_bp.route("/<int:id_fornecedor>", methods=["PUT"])
def atualizar_fornecedor(id_fornecedor):
    fornecedor = Fornecedor.query.get_or_404(id_fornecedor)
    dados = request.get_json()

    fornecedor.nome = dados.get("nome", fornecedor.nome)
    fornecedor.pais = dados.get("pais", fornecedor.pais)
    fornecedor.contato = dados.get("contato", fornecedor.contato)

    db.session.commit()

    return jsonify({"mensagem": "Fornecedor atualizado com sucesso"})


@fornecedor_bp.route("/<int:id_fornecedor>", methods=["DELETE"])
def deletar_fornecedor(id_fornecedor):
    fornecedor = Fornecedor.query.get_or_404(id_fornecedor)
    db.session.delete(fornecedor)
    db.session.commit()

    return jsonify({"mensagem": "Fornecedor deletado com sucesso"})