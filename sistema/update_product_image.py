import sys
sys.path.insert(0, r'e:\projetos\gestão project\sistema')

from app import create_app, db
from app.models.produto import Produto

# Criar aplicação Flask
app = create_app()

with app.app_context():
    # Atualizar o produto com a imagem
    produto = Produto.query.filter_by(nome='Headset HyperX Cloud Stinger 2').first()
    
    if produto:
        produto.imagem_url = '/static/img/produtos/hyperx-cloud-stinger-2.jpg'
        db.session.commit()
        print(f'✅ Produto atualizado!')
        print(f'   Nome: {produto.nome}')
        print(f'   Imagem: {produto.imagem_url}')
    else:
        print('❌ Produto não encontrado no banco de dados')
        print('\nProdutos disponíveis:')
        for p in Produto.query.all():
            print(f'  - {p.nome}')
