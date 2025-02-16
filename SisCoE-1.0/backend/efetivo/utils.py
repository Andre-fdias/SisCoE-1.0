# image_utils.py
from PIL import Image, ImageDraw, ImageFont
import os

def add_cpf_to_image(image_path, cpf, output_path):
    # Abra a imagem
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Defina a fonte e o tamanho do texto
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Caminho para a fonte
    font = ImageFont.truetype(font_path, 36)

    # Defina a posição do texto
    text_position = (10, 10)  # Posição (x, y) do texto na imagem

    # Adicione o texto na imagem
    draw.text(text_position, cpf, font=font, fill="red")

    # Salve a imagem com o CPF
    image.save(output_path)