import os
import re
from pathlib import Path
from urllib.parse import quote

from flask import Blueprint, jsonify, request
from app import db
from app.models.produto import Produto


produto_bp = Blueprint("produto_bp", __name__, url_prefix="/produtos")


def slugify(valor):
    if not valor:
        return ""
    return re.sub(r"[^a-z0-9]+", "-", valor.lower()).strip("-")


def normalizar_imagem_url(imagem_url):
    if not imagem_url:
        return None
    valor = str(imagem_url).strip()
    if valor.startswith(("http://", "https://")):
        return valor

    caminho = valor.replace('\\', '/')
    caminho = caminho.replace(" ", "%20")

    if caminho.startswith("/static/") or caminho.startswith("/img/"):
        return "/" + quote(caminho.lstrip("/"), safe="/")
    if caminho.startswith("static/") or caminho.startswith("img/"):
        return "/" + quote(caminho, safe="/")
    if caminho.startswith("produtos/"):
        return "/static/img/" + quote(caminho.replace("produtos/", ""), safe="/")
    if caminho.endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
        return "/static/img/" + quote(caminho.lstrip("/"), safe="/")
    return valor


def nome_a_partir_do_arquivo(imagem_url):
    if not imagem_url:
        return ""
    nome_arquivo = os.path.basename(str(imagem_url))
    nome_base = os.path.splitext(nome_arquivo)[0]
    nome = nome_base.replace("_", " ").replace("-", " ")
    return " ".join(part.capitalize() for part in nome.split() if part)


def nome_produto_padronizado(produto):
    nome = (getattr(produto, "nome", "") or "").strip()
    if nome and nome.lower() not in {"produto", "produto sem nome", "sem nome"}:
        return nome
    imagem_url = normalizar_imagem_url(getattr(produto, "imagem_url", ""))
    if imagem_url:
        nome_arquivo = nome_a_partir_do_arquivo(imagem_url)
        if nome_arquivo:
            return nome_arquivo
    categoria = (getattr(produto, "categoria", "") or "").strip()
    if categoria:
        return categoria
    return "Produto"


def imagem_padrao(produto):
    return f"https://picsum.photos/seed/{produto.id_produto}/600/400"


def resolver_imagem_produto(produto):
    imagem_url = normalizar_imagem_url(getattr(produto, "imagem_url", ""))
    if imagem_url:
        return imagem_url

    pasta_base = Path(__file__).resolve().parents[1] / "static"
    caminhos = [
        pasta_base / "img" / "produtos",
        pasta_base / "img",
    ]
    nome_alvo = slugify(nome_produto_padronizado(produto))
    categoria_alvo = slugify(getattr(produto, "categoria", "") or "")

    candidatos = []
    for pasta in caminhos:
        if not pasta.exists():
            continue
        for arquivo in pasta.iterdir():
            if arquivo.is_file() and arquivo.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
                slug = slugify(arquivo.stem)
                score = 0
                if nome_alvo and nome_alvo in slug:
                    score += 5
                if categoria_alvo and categoria_alvo in slug:
                    score += 3
                if "seagate-barracuda-2tb" in slug and "hdd" in slug:
                    score += 1
                candidatos.append((score, arquivo.name))

    if candidatos:
        candidatos.sort(key=lambda item: item[0], reverse=True)
        melhor_arquivo = candidatos[0][1]
        melhor_path = Path(melhor_arquivo)
        if melhor_path.parent.name == "produtos":
            return f"/static/img/produtos/{melhor_arquivo}"
        return f"/static/img/{melhor_arquivo}"

    return imagem_padrao(produto)


def produto_para_dict(produto):
    nome = nome_produto_padronizado(produto)
    imagem_url = resolver_imagem_produto(produto)
    return {
        "id_produto": produto.id_produto,
        "nome": nome,
        "descricao": produto.descricao,
        "preco": "{0}".format(produto.preco),
        "estoque": produto.estoque,
        "categoria": produto.categoria,
        "imagem_url": imagem_url,
    }


@produto_bp.route("/", methods=["GET"])
def listar_produtos():
    return jsonify([produto_para_dict(produto) for produto in Produto.query.all()])


@produto_bp.route("/<int:id_produto>", methods=["GET"])
def buscar_produto(id_produto):
    return jsonify(produto_para_dict(Produto.query.get_or_404(id_produto)))


@produto_bp.route("/", methods=["POST"])
def criar_produto():
    dados = request.get_json(silent=True)
    if not dados:
        return jsonify({"erro": "Corpo da requisição precisa ser um JSON válido"}), 400

    novo_produto = Produto(
        nome=dados.get("nome"),
        descricao=dados.get("descricao"),
        preco=dados.get("preco"),
        estoque=dados.get("estoque"),
        categoria=dados.get("categoria"),
        imagem_url=dados.get("imagem_url"),
    )
    db.session.add(novo_produto)
    db.session.commit()

    return jsonify({
        "mensagem": "Produto criado com sucesso",
        "id_produto": novo_produto.id_produto,
    }), 201


@produto_bp.route("/<int:id_produto>", methods=["PUT"])
def atualizar_produto(id_produto):
    produto = Produto.query.get_or_404(id_produto)
    dados = request.get_json(silent=True)
    if not dados:
        return jsonify({"erro": "Corpo da requisição precisa ser um JSON válido"}), 400

    produto.nome = dados.get("nome", produto.nome)
    produto.descricao = dados.get("descricao", produto.descricao)
    produto.preco = dados.get("preco", produto.preco)
    produto.estoque = dados.get("estoque", produto.estoque)
    produto.categoria = dados.get("categoria", produto.categoria)
    produto.imagem_url = dados.get("imagem_url", produto.imagem_url)
    db.session.commit()

    return jsonify({"mensagem": "Produto atualizado com sucesso"})


@produto_bp.route("/<int:id_produto>", methods=["DELETE"])
def deletar_produto(id_produto):
    produto = Produto.query.get_or_404(id_produto)
    db.session.delete(produto)
    db.session.commit()

    return jsonify({"mensagem": "Produto deletado com sucesso"})
