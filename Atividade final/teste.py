import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import hough_line
from skimage import io
from skimage.filters import sobel
from skimage.transform import hough_line
from skimage import io
from skimage.transform import resize
from skimage.draw import polygon
from skimage.color import gray2rgb
import matplotlib.pyplot as plt

img = (io.imread ('codigo_de_barras.png',as_gray=True)*255).astype('uint8') 
plt.imshow (img,cmap='gray',vmin=0,vmax=255)

h = np.histogram (img,bins=256)
plt.plot (h[0],'-k')

img_bin = img.copy()
img_bin[img_bin<100] = 0
img_bin[img_bin>0] = 255
img_bin = 255-img_bin
plt.imshow (img_bin,cmap='gray')


edges = (sobel (img_bin)*255).astype('uint8')
plt.imshow (edges,cmap='gray')

h = np.histogram (edges,bins=256)

plt.plot(h[0],'-k')

tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 180, endpoint=False)
h, theta, d = hough_line(edges, theta=tested_angles)

h.max()

plt.imshow (h,cmap='gray',aspect=1/10)

h_aux = h.copy()
h_aux[h_aux<120] = 0
plt.imshow (h_aux,cmap='gray',aspect=1/10)

import cv2 as cv # Tudo bem usar a cv2?
# R = não
import math
import skimage.draw
import skimage.color
#lines = cv.HoughLines(edges, 1, np.pi / 180, 20) # Restringindo apenas para linhas verticais

# Aplicando a Transformada de Hough com skimage
hspace, angles, dists = skimage.transform.hough_line(edges)

# Detectando picos nas linhas
# O threshold pode ser ajustado para garantir que apenas linhas significativas sejam detectadas
import numpy as np

# Limiar para filtrar os picos com valores baixos
threshold = 10

# Matriz de Hough (hspace) e ângulos (angles) e distâncias (dists)
# hspace, angles, dists já foram definidos em seu código

# Inicializando listas para armazenar os picos detectados
peaks_angles = []
peaks_dists = []

# Percorrendo a matriz de Hough para encontrar os picos
for i in range(1, hspace.shape[0] - 1):  # Evitar as bordas
    for j in range(1, hspace.shape[1] - 1):
        # Verificar se o valor na posição (i, j) é maior que os vizinhos
        if (hspace[i, j] > hspace[i-1, j-1] and hspace[i, j] > hspace[i-1, j] and hspace[i, j] > hspace[i-1, j+1] and
            hspace[i, j] > hspace[i, j-1] and hspace[i, j] > hspace[i, j+1] and
            hspace[i, j] > hspace[i+1, j-1] and hspace[i, j] > hspace[i+1, j] and hspace[i, j] > hspace[i+1, j+1]):
            
            # Se o valor for maior que o limiar, é um pico
            if hspace[i, j] > threshold:
                # Armazenar o ângulo e a distância correspondentes aos picos
                peaks_angles.append(angles[j])  # ângulo correspondente à coluna j
                peaks_dists.append(dists[i])    # distância correspondente à linha i

# Agora você tem os ângulos e distâncias dos picos detectados
print("Picos detectados em ângulos:", peaks_angles)
print("Picos detectados em distâncias:", peaks_dists)

# Pegando os ângulos e distâncias das linhas detectadas
angles_detected = peaks_angles
dists_detected = peaks_dists

# Filtrando apenas as linhas verticais (ângulos próximos de 90° ou -90°)
angle_threshold = np.pi / 180  # Pequena margem para considerar variações

# Filtrando as linhas verticais (ângulos próximos de 90° ou -90°)
# A margem de 10° pode ser aumentada para incluir mais linhas
angle_threshold = np.pi / 180  # Ajustando para uma margem maior (10 graus)
lines = [
    (dists_detected[i], angles_detected[i])
    for i in range(len(angles_detected))
    if (abs(angles_detected[i] - np.pi / 2) > angle_threshold) or (abs(angles_detected[i] + np.pi / 2) > angle_threshold)
]

angulos = list()

# Convertendo a imagem para RGB (semelhante ao cv.COLOR_GRAY2BGR)
cdst = skimage.color.gray2rgb(edges)

if lines is not None:
    for i in range(0, len(lines)):
        rho = lines[i][0]
        theta = lines[i][1]
        deg = np.rad2deg (theta)
        # if not (np.abs (deg - 90) < 4 or np.abs (deg - 180) < 4):
        if not (deg < 1 or \
        np.abs (deg - 90) < 1 or \
        np.abs (deg - 180) < 1):
            continue
        angulos.append(theta)
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
        pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
        # cv.line(cdst, pt1, pt2, (255,0,0), 3, cv.LINE_AA)

          # Criando a linha usando skimage
        rr, cc = skimage.draw.line(pt1[1], pt1[0], pt2[1], pt2[0])
        
        # Garantindo que os índices estejam dentro dos limites da imagem
        rr = np.clip(rr, 0, cdst.shape[0] - 1)
        cc = np.clip(cc, 0, cdst.shape[1] - 1)

        # Desenhando a linha na imagem (assumindo que cdst seja uma imagem RGB)
        cdst[rr, cc] = [255, 0, 0]  # Cor vermelha

plt.imshow(cdst)

[np.rad2deg(x) for x in angulos]

from skimage.transform import rotate

# Corrigindo a rotação baseada na média dos ângulos detectados
angulo_medio = np.mean([np.rad2deg(l[1]) for l in lines if np.abs(np.rad2deg(l[1]) - 90) < 4])
img_corrigida = rotate(img, (angulo_medio - 90)) # Talvez usar outra função de rotação

img_corrigida[img_corrigida<0.5] = 0
img_corrigida[img_corrigida>0] = 1

_,ax = plt.subplots(1,2)
ax[0].imshow(img,cmap='gray')
ax[1].imshow(img_corrigida,cmap='gray')
plt.show()

# Verificar o que pode estar causando o erro, se for nos eixos do for ou algo assim
codigo = 0
for x in range(img_corrigida.shape[0]):
    for y in range(img_corrigida.shape[1]):
        if img_corrigida[x, y] == 0:
            codigo = img_corrigida[x+1, y:y+11]
            break 
    if codigo.all():
        break  # Sai do loop externo após encontrar a linha

print(codigo) 

import os
str_codigo = "".join((codigo.astype(int)).astype(str)) # Convertendo o array de float 1.0 ou 0.0 em int e depois em string
print(str_codigo)                                      # para concatenar e remover as vírgulas

_,ax = plt.subplots(1,2)
ax[0].imshow(img,cmap='gray')
ax[1].imshow(img_corrigida,cmap='gray')
plt.show()

# Teste de leitura do código, e até o momento funcionou bem compara corretamente

import pandas as pd

tabela = pd.read_excel('tabela_code128_completa.xlsx', engine='openpyxl') # A tabeçla é só de uma caractere,
                                                                          # assim temos cercad e 128 opções
# Separar as colunas em variáveis separadas
referencia = tabela['Padrão Code 128'].to_numpy()  # Substitua 'nome_da_coluna_numerica' pelo nome correto da coluna
mensagem = tabela['Caractere'].to_numpy()    # Substitua 'nome_da_coluna_strings' pelo nome correto da coluna

#Ao encontrar o código correspondente, ele imprime o caractere associado.
#O enumerate() para acessar tanto o valor de referencia quanto o índice,
#dessa forma, evia o erro de achar várias referências (que foi um doa probleemas)
#e permite imprimir o caractere correspondente de mensagem[i].

# while tiver entrada concatene com o for
for i, confere in enumerate(referencia): # While enumerate para ver quantos for?
    if confere == int(str_codigo): # Passando novamente para int, a fim de comparar com a tabela
        print(f"Encontrado: {mensagem[i]}")
        break  # Se encontrar o código, já pode parar a busca