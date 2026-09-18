import urllib.request
import json

try:
    response = urllib.request.urlopen('http://127.0.0.1:5000/produtos')
    data = json.loads(response.read())
    
    print(f"Total de produtos: {len(data)}\n")
    
    # Procurar pela webcam Logitech
    logitech = [p for p in data if 'logitech' in p['nome'].lower()]
    
    if logitech:
        for p in logitech:
            print(f"✅ Produto encontrado!")
            print(f"   Nome: {p['nome']}")
            print(f"   Preço: R$ {p['preco']}")
            print(f"   Imagem: {p['imagem_url']}")
            print(f"   Estoque: {p['estoque']}")
    else:
        print("❌ Webcam Logitech não encontrada!")
        print("\nProdutos disponíveis:")
        for p in data:
            print(f"  - {p['nome']}")
            
except Exception as e:
    print(f"Erro: {e}")
