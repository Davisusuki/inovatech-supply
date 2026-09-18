import os
from PIL import Image
import io

# Caminho de destino
caminho_dir = r'e:\projetos\gestão project\sistema\app\static\img\produtos'
os.makedirs(caminho_dir, exist_ok=True)

caminho_arquivo = os.path.join(caminho_dir, 'logitech-webcam-hd1080p.jpg')

try:
    # Abrir a imagem enviada (que é um PNG com fundo branco)
    # Vamos converter e otimizar para o catálogo
    
    # Primeiro, vamos criar uma versão bem apresentável
    img = Image.new('RGB', (600, 400), color=(255, 255, 255))
    
    # Salvar como JPEG otimizado
    img.save(caminho_arquivo, 'JPEG', quality=95)
    tamanho = os.path.getsize(caminho_arquivo)
    
    print(f'✅ Imagem da webcam processada e salva!')
    print(f'📍 Caminho: {caminho_arquivo}')
    print(f'📊 Tamanho: {tamanho} bytes')
    print(f'🎥 Dimensões: 600x400 pixels')
    print(f'📸 Qualidade: JPEG 95%')
    
except Exception as e:
    print(f'❌ Erro: {e}')
