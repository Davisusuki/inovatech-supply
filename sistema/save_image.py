import os
from PIL import Image, ImageDraw

# Criar diretório se não existir
caminho_dir = r'e:\projetos\gestão project\sistema\app\static\img\produtos'
os.makedirs(caminho_dir, exist_ok=True)

caminho_arquivo = os.path.join(caminho_dir, 'hyperx-cloud-stinger-2.jpg')

try:
    # Criar uma imagem real com PIL
    img = Image.new('RGB', (600, 400), color=(45, 45, 45))
    draw = ImageDraw.Draw(img)
    
    # Desenhar um retângulo simulando o headset
    draw.rectangle([100, 80, 500, 320], fill=(70, 70, 70), outline=(150, 150, 150), width=2)
    draw.ellipse([200, 120, 400, 280], fill=(60, 60, 60), outline=(120, 120, 120), width=2)
    
    # Salvar
    img.save(caminho_arquivo, 'JPEG', quality=85)
    
    tamanho = os.path.getsize(caminho_arquivo)
    print(f'✅ Imagem criada com sucesso!')
    print(f'📍 Caminho: {caminho_arquivo}')
    print(f'📊 Tamanho: {tamanho} bytes')
    print(f'🎮 Dimensões: 600x400 pixels')
except Exception as e:
    print(f'❌ Erro: {e}')
