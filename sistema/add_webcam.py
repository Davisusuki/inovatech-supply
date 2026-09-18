import sys
sys.path.insert(0, r'e:\projetos\gestão project\sistema')

from app import create_app, db
from app.models.produto import Produto

app = create_app()

with app.app_context():
    # Verificar se já existe webcam Logitech
    webcam = Produto.query.filter_by(nome='Webcam Logitech HD 1080p').first()
    
    if webcam:
        # Atualizar produto existente
        webcam.imagem_url = '/static/img/produtos/logitech-webcam-hd1080p.jpg'
        print(f'📝 Atualizando: {webcam.nome}')
    else:
        # Criar novo produto
        webcam = Produto(
            nome='Webcam Logitech HD 1080p',
            descricao='Webcam profissional Full HD com foco automático e microfone integrado',
            preco=149.90,
            imagem_url='/static/img/produtos/logitech-webcam-hd1080p.jpg',
            estoque=15
        )
        print(f'✨ Criando novo produto: Webcam Logitech HD 1080p')
        db.session.add(webcam)
    
    # Salvar
    db.session.commit()
    print(f'✅ Webcam salva com sucesso!')
    print(f'   Nome: {webcam.nome}')
    print(f'   Preço: R$ {webcam.preco}')
    print(f'   Imagem: {webcam.imagem_url}')
    print(f'   Estoque: {webcam.estoque}')
