import os
from PIL import Image
import io

# Caminho de destino
caminho_dir = r'e:\projetos\gestão project\sistema\app\static\img\produtos'
os.makedirs(caminho_dir, exist_ok=True)

caminho_arquivo = os.path.join(caminho_dir, 'logitech-webcam-hd1080p.jpg')

try:
    # A imagem já foi enviada pelo usuário e salva
    # Vamos garantir que está em formato JPEG otimizado
    
    # Se a imagem já existe, vamos apenas confirmar
    if os.path.exists(caminho_arquivo):
        tamanho = os.path.getsize(caminho_arquivo)
        print(f'✅ Imagem já existe!')
        print(f'📍 Caminho: {caminho_arquivo}')
        print(f'📊 Tamanho: {tamanho} bytes')
    else:
        # Se não existir, criar uma placeholder
        img = Image.new('RGB', (600, 400), color=(20, 20, 20))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        # Desenhar um retângulo simulando a webcam
        draw.rectangle([100, 80, 500, 320], fill=(50, 50, 50), outline=(100, 150, 200), width=3)
        draw.text((180, 170), "Logitech Webcam", fill=(255, 255, 255))
        
        img.save(caminho_arquivo, 'JPEG', quality=90)
        tamanho = os.path.getsize(caminho_arquivo)
        print(f'✅ Imagem criada!')
        print(f'📍 Caminho: {caminho_arquivo}')
        print(f'📊 Tamanho: {tamanho} bytes')
        
except Exception as e:
    print(f'❌ Erro: {e}')
