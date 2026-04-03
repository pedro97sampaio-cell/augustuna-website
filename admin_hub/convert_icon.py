from PIL import Image
import os

img_path = r"c:\Users\José Cunha\Desktop\AG\Logo oficial 2.png"
ico_path = r"c:\Users\José Cunha\Desktop\AG\admin_hub\icon.ico"

print(f"Lendo imagem: {img_path}")
img = Image.open(img_path)
img.save(ico_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
print(f"Ícone guardado em: {ico_path}")
