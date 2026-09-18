import unittest

from app import create_app
from app.models.cliente import Cliente
from app.routes.produto_routes import produto_para_dict


class AppConfigTests(unittest.TestCase):
    def test_cliente_model_has_required_fields(self):
        self.assertTrue(hasattr(Cliente, 'nome'))
        self.assertTrue(hasattr(Cliente, 'nome_empresa'))
        self.assertTrue(hasattr(Cliente, 'pais'))
        self.assertTrue(hasattr(Cliente, 'email'))
        self.assertTrue(hasattr(Cliente, 'telefone'))

    def test_database_uri_is_valid_for_current_environment(self):
        app = create_app()
        uri = app.config['SQLALCHEMY_DATABASE_URI']
        self.assertTrue(
            uri.startswith('mysql+pymysql://') or uri.startswith('sqlite:///'),
            f'URI inválida: {uri}'
        )

    def test_produto_para_dict_converte_imagem_local_para_url_static(self):
        class ProdutoTeste:
            id_produto = 10
            nome = "Mouse Logitech G203"
            descricao = "Mouse gamer"
            preco = 299.90
            estoque = 12
            categoria = "Periféricos"
            imagem_url = "mouse-logitech-g203.png"

        produto = ProdutoTeste()
        dados = produto_para_dict(produto)

        self.assertEqual(dados["imagem_url"], "/static/img/mouse-logitech-g203.png")

    def test_produto_para_dict_converte_imagem_com_espaco_em_nome(self):
        class ProdutoTeste:
            id_produto = 11
            nome = "Produto com espaço"
            descricao = "Nome com espaço"
            preco = 199.90
            estoque = 5
            categoria = "Periféricos"
            imagem_url = "produtos/html 2.png"

        produto = ProdutoTeste()
        dados = produto_para_dict(produto)

        self.assertEqual(dados["imagem_url"], "/static/img/produtos/html%202.png")


if __name__ == '__main__':
    unittest.main()
