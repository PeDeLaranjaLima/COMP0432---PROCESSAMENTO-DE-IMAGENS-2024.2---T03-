import numpy as np
import barcode
from barcode.writer import ImageWriter
import random
from skimage import io
from skimage.transform import rotate
from skimage.io import imsave

codigo128_binarios = [
    "11011001100", "11001101111", "11001111011", "11010001111", "11010111011", 
    "11011100111", "11010100111", "11011010011", "11011011111", "11010111001", 
    "11011101001", "11010100011", "11011100101", "11010010011", "11011010111", 
    "11010111010", "11011101010", "11010101101", "11011011001", "11011011101", 
    "11010101111", "11011101101", "11010111101", "11011100110", "11010110011", 
    "11011010101", "11011101011", "11010111011", "11011010010", "11011101010", 
    "11010101011", "11011010110", "10010001100", "10010010000", "10010000100", 
    "10011000100", "10010010010", "10010000110", "10011000010", "10011010000", 
    "10010011000", "10010001110", "10011010010", "10011000011", "10010011100", 
    "10010001010", "10011001000", "10010000101", "11011001110", "11001101100", 
    "11001111000", "11010001100", "11010111000", "11011100100", "11010100100", 
    "11011010000", "11011011100", "11010111010", "11011001000", "11010100000", 
    "11010010001", "11010101001", "11010011000", "11011101111", "11010100101", 
    "11010101000", "11011110001", "11010010011", "11010011110", "11011100110", 
    "11011011000", "11010110110", "11011101000", "11011010001", "11010001001", 
    "11010110000", "11011110111", "11011110010", "11010010011", "11011000100", 
    "11010101111", "11010011011", "11010111001", "11011110101", "11011100000", 
    "11011011110", "11010110100", "11010100010", "11011101001", "11011110100", 
    "11010101101", "11011101001", "11010011110", "11011010001", "11011110101", 
    "11011100010", "11010001001", "11010100100", "11010111000", "11010100110", 
    "11010000111", "11010011000", "11011001101", "11011111000", "11011001101", 
    "11010101000", "11010110010", "11011100101", "11010110001", "11010100011", 
    "11010101110", "11011010001", "11011010000", "11011011101", "11011011001", 
    "11010011010", "11011101000", "11011101011", "11011101010", "11010010101"
]

for i, cd in enumerate(codigo128_binarios):
    random1 = random.randint(0,119)
    random2 = random.randint(0,119)
    codigo = cd + codigo128_binarios[random1] + codigo128_binarios[random2]  # O código de barras precisa ter um número válido
    code128 = barcode.get_barcode_class('code128')
    barcode_obj = code128(codigo, writer=ImageWriter())

    # Configurações do writer para manter relação 1x1
    options = {
        "module_width": 1.0,  # Cada módulo terá exatamente 1 pixel de largura
        "module_height": 40,  # Altura do código de barras
        "dpi": 300,           # Define a resolução
        "text_distance": 5,   # Espaço entre o código e o número
        "font_size": 1,      # Tamanho da fonte do número (opcional)
        "quiet_zone": 50,       # Margem ao redor do código (mínimo possível)
    }

    # Salva a imagem com as opções ajustadas
    barcode_obj.save(f"codigo_de_barras_{i}", options=options)

for i in range(119):
    img = (io.imread(f'codigo_de_barras_{i}.png', as_gray=True) * 255).astype('uint8')
    ang = random.randint(0,60)
    img_rot = rotate(img, -ang, resize=True, order=0, mode='edge', cval=1)
    imsave(f'codigo_rotacionado_{i}.png', img_rot)
