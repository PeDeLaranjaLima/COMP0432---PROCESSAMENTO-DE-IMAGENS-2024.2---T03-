import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
import scipy
from skimage.color import rgb2gray

from skimage.transform import rescale

############## Código rescale.ipynb ##############

scale = 1/4
image = imread ('placa04.png',as_gray=True)
image_rescaled = rescale(image, scale, anti_aliasing=True)
image_restored = rescale(image_rescaled, 1/scale, anti_aliasing=True)

_,ax = plt.subplots (1,3)
ax[0].imshow(image,cmap='gray')
ax[1].imshow(image_rescaled,cmap='gray')
ax[2].imshow(image_restored,cmap='gray')

# Adição para ver o gráfico:
plt.show()  # Exibe o gráfico

############## Aplicação do filtro highboost ##############

from scipy.ndimage import uniform_filter

# Filtro passa baixas:

filt_md = uniform_filter(image_restored, size=7) # Cria o filtro da média para uma janela de 7x7

# Criação da máscara:
# A imagem é a soma das altas e baixas frequÊncias, como explicado em aula. Logo, para se obter as altas frequÊncias, basta apenas
# Subtrair as baixas frequências da imagem

altas_frequencias = image_restored - filt_md

# Criação do fator peso da máscara do filtro Highboost

peso = 9 # Para essa imagem, foi encontrado a base de testes

# Multiplicação das altas frequências pelo peso da imagem

boost = peso * altas_frequencias # boost é a intensificação das altas frequências

# Soma da imagem com as altas frequências

image_highboost = image_restored + boost

# Exibição dos resultados
_, ax = plt.subplots(1, 3, figsize=(12, 4))
ax[0].imshow(image_restored, cmap='gray')
ax[0].set_title('Restaurada')
ax[1].imshow(filt_md, cmap='gray')
ax[1].set_title('Passa-Baixa (Filtro da Média)')
ax[2].imshow(image_highboost, cmap='gray')
ax[2].set_title('Highboost (Filtro da Média)')
plt.show()