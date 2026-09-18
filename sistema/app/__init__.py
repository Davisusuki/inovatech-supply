import os
import re
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_cors import CORS
from flask import render_template
from sqlalchemy import inspect, text
from app.extensions import db
from flask import Flask, render_template, request


def sincronizar_colunas_produtos():
    inspector = inspect(db.engine)
    colunas = {coluna["name"] for coluna in inspector.get_columns("produtos")}
    alteracoes = {
        "fornecedor_id": "ALTER TABLE produtos ADD COLUMN fornecedor_id INTEGER NULL",
        "imagem_url": "ALTER TABLE produtos ADD COLUMN imagem_url VARCHAR(255) NULL",
    }

    with db.engine.begin() as connection:
        for nome, comando in alteracoes.items():
            if nome not in colunas:
                connection.execute(text(comando))


def normalizar_nome_produto(nome_arquivo):
    nome = os.path.splitext(os.path.basename(nome_arquivo))[0]
    nome = nome.replace("_", " ").replace("-", " ")
    nomes = []
    for parte in nome.split():
        if parte.lower() in {"png", "jpg", "jpeg", "webp", "gif"}:
            continue
        if parte.isdigit():
            nomes.append(parte)
            continue
        if parte.lower() in {"msi", "ryzen", "rtx", "hdd", "ssd", "rgb", "cpu", "gpu", "monitor", "water", "cooler", "fan", "amd", "intel", "lg", "corsair", "gigabyte", "aorus", "kingston", "seagate", "logitech", "hyperx", "redragon"}:
            nomes.append(parte.capitalize() if parte.isalpha() else parte)
            continue
        if parte.lower() in {"ax", "cv550", "5700x", "b550m", "24mp400", "240mm", "2tb", "500gb", "32gb", "16gb"}:
            nomes.append(parte.upper() if parte.isalpha() else parte)
            continue
        nomes.append(parte.capitalize())
    nome_final = " ".join(nomes)
    if not nome_final:
        return "Produto"
    return nome_final


def popular_produtos_padrao():
    from app.models.produto import Produto

    if Produto.query.first():
        return

    pasta_base = Path(__file__).resolve().parent / "static"
    caminhos = [
        pasta_base / "img" / "produtos",
        pasta_base / "img",
    ]

    arquivos = []
    for pasta in caminhos:
        if not pasta.exists():
            continue
        for arquivo in sorted(pasta.iterdir()):
            if arquivo.is_file() and arquivo.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
                arquivos.append(arquivo)

    for arquivo in arquivos:
        nome = normalizar_nome_produto(arquivo.name)
        produto = Produto(
            nome=nome,
            descricao="Produto de tecnologia com imagem oficial do catálogo.",
            preco=0,
            estoque=1,
            categoria="Geral",
            imagem_url=f"/static/{arquivo.relative_to(pasta_base).as_posix()}",
        )
        db.session.add(produto)

    db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)


    db.init_app(app)

    with app.app_context():
        from app.models import cliente, fornecedor, produto, pedido, item_pedido, pagamento
        db.create_all()
        sincronizar_colunas_produtos()
        popular_produtos_padrao()

    from app.routes.fornecedor_routes import fornecedor_bp
    app.register_blueprint(fornecedor_bp)

    from app.routes.produto_routes import produto_bp
    app.register_blueprint(produto_bp)

    from app.routes.cliente_routes import cliente_bp
    app.register_blueprint(cliente_bp)

    from app.routes.pedido_routes import pedido_bp
    app.register_blueprint(pedido_bp)

    from app.routes.item_pedido_routes import item_pedido_bp
    app.register_blueprint(item_pedido_bp)

    from app.routes.pagamento_routes import pagamento_bp
    app.register_blueprint(pagamento_bp)

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/clientes/cadastrar")
    def cadastro_clientes():
        return render_template("cliente_cadastro.html")

    @app.route("/produto/<int:id_produto>")
    def produto_detalhe(id_produto):
     return render_template("produto.html", id_produto=id_produto)

    @app.route("/Finalizar Pedido",methods=["GET", "POST"])
    def finalizar_pedido():
        if request.method == "POST":
            nome = request.form.get("nome")
            endereco = request.form.get("endereco")
            pagamento = request.form.get("pagamento")

            print(nome, endereco, pagamento)

        return render_template("finalizar_pedido.html") 
    return app