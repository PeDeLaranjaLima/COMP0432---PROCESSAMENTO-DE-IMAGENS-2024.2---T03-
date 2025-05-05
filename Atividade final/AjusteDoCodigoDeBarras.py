# import numpy as np
# import matplotlib.pyplot as plt
# from skimage.transform import hough_line
# from skimage import io
# from skimage.filters import sobel
# from skimage.transform import hough_line
# from numpy import cos,sin,deg2rad
# import math
# import skimage.draw
# import skimage.color
# from skimage.transform import rescale
# import os
# import pandas as pd

# # Funções para operações geométricas passadas na aula

# def translacao (tx, ty):

#     return np.array ([[1,0,tx], \
#                       [0,1,ty], \
#                       [0,0,1]]).astype('float')

# def escalonamento (sx, sy):
#     return np.array ([[sx,0,0], \
#                       [0,sy,0], \
#                       [0,0,1]]).astype('float')

# def rotacao (theta):
#     theta = deg2rad (theta)
#     c = cos (theta)
#     s = sin (theta)
#     return np.array ([[c,-s,0], \
#                       [s,c,0], \
#                       [0,0,1]]).astype('float')

# # Leitura dos códigos de barras, converção de escala para tons de cinza e converção inteiro
# img = (io.imread ('codigo_de_barras.png',as_gray=True)*255).astype('uint8') 

# # Exibe uma única imagem
# plt.figure(figsize=(5, 5))  # Ajustar o tamanho da figura
# plt.imshow(img, cmap='gray',vmin=0,vmax=255)  # Mostrar a imagem em escala de cinza
# plt.title('Imagem de entrada')  # Definir o título
# plt.show()
# print(f"Imagem.shape[0] = {img.shape[0]}, Imagem.shape[1] = {img.shape[1]}") # Apresentando o tamanho da imagem

# # Exibe o histograma da imagem
# plt.figure(figsize=(5, 5))  # Ajustar o tamanho da figura
# h = np.histogram (img,bins=256) # Calcula o histograma
# plt.plot (h[0],'-k')
# plt.title('Histograma')  # Definir o título
# plt.show()

# # Binarização da imagem, continua em tons de cinza, porém com limites bem estabelecidos
# img_bin = img.copy()
# img_bin[img_bin<100] = 0 # Define limitre inferior
# img_bin[img_bin>0] = 255 # Define limite superior
# img_bin = 255-img_bin 
# plt.imshow (img_bin,cmap='gray')

# # Aplica o filtro derivativo de sobel com a função da biblioteca skimage
# edges = (sobel (img_bin)*255).astype('uint8')

# # Exibe uma única imagem
# plt.figure(figsize=(5, 5))  # Ajustar o tamanho da figura
# plt.imshow(edges, cmap='gray',vmin=0,vmax=255)  # Mostrar a imagem resultante do Sobel em escala de cinza
# plt.title('Sobel')  # Definir o título
# plt.show()

# h = np.histogram (edges,bins=256) # Calcula o histograma da imagem de Sobel

# # Exibe uma única imagem
# plt.figure(figsize=(5, 5))  # Ajustar o tamanho da figura
# plt.plot(h[0],'-k')
# plt.title('Histograma do Sobel')  # Definir o título
# plt.show()

# tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 180, endpoint=False) # Cria o espaço de parâmetros
# h, theta, d = hough_line(edges, theta=tested_angles) # Alimenta as variáveis h, theta e d com as retas, os ângulos e as distências,
#                                                      # respectivamente

# h.max() # Pega o valor máximo de reta, ou seja, a reta mais votada
# # Exibe uma única imagem
# plt.figure(figsize=(5, 5))  # Ajustar o tamanho da figura
# plt.imshow (h,cmap='gray',aspect=1/10) # Ajusta a escala do plot
# plt.title('Espaço de parâmetros')  # Definir o título
# plt.show()

# h_aux = h.copy() # Faz uma cópia de h
# h_aux[h_aux<120] = 0 # Pega somente os h's com mais votos, dentro desse limite (que ainda permite muitas retas)

# # Exibe uma única imagem
# plt.figure(figsize=(5, 5))  # Ajusta o tamanho da figura
# plt.imshow (h_aux,cmap='gray',aspect=1/10) # Exibe o espaço de parâmetros com as retas mais votadas
# plt.title('Espaço de parâmetros')  # Define o título
# plt.show()

# # Detectando picos nas linhas
# # O threshold (limiar para filtrar os picos com valores baixos) pode ser ajustado para garantir que apenas
# # linhas significativas sejam detectadas, o que garante melhores valores para os ângulos, porém isso ainda
# # é ponto de dificuldade da equipe
# threshold = 50

# # Matriz de Hough (h_max) e ângulos (theta) e distâncias (d)
# # Inicializando listas para armazenar os picos detectados
# picos_de_angulos = []
# picos_de_distancias = []

# # Percorre a matriz de Hough para encontrar os picos
# for i in range(1, h_aux.shape[0] - 1):  # Evita as bordas da imagem
#     for j in range(1, h_aux.shape[1] - 1):
#         # Verifica se o valor na posição (i, j) é maior que os vizinhos
#         if (h_aux[i, j] > h_aux[i-1, j-1] and h_aux[i, j] > h_aux[i-1, j] and h_aux[i, j] > h_aux[i-1, j+1] and
#             h_aux[i, j] > h_aux[i, j-1] and h_aux[i, j] > h_aux[i, j+1] and
#             h_aux[i, j] > h_aux[i+1, j-1] and h_aux[i, j] > h_aux[i+1, j] and h_aux[i, j] > h_aux[i+1, j+1]):
            
#             # Se o valor for maior que o limiar, é um pico
#             if h[i, j] > threshold:
#                 # Armazena o ângulo e a distância correspondentes aos picos
#                 picos_de_angulos.append(theta[j])  # ângulo correspondente à coluna j
#                 picos_de_distancias.append(d[i])    # distância correspondente à linha i

# # Filtra as linhas verticais (ângulos próximos de 90° ou -90°)
# # A margem de 10° pode ser aumentada para incluir mais linhas
# angle_threshold = np.pi / 180 * 10
# lines = [
#     (picos_de_distancias[i], picos_de_angulos[i])
#     for i in range(len(picos_de_angulos))
#     if (abs(picos_de_angulos[i] - np.pi / 2) < angle_threshold) or (abs(picos_de_angulos[i] + np.pi / 2) < angle_threshold)
# ]

# angulos = list() # Cria uma lista
# cdst = skimage.color.gray2rgb(edges) # Converte, usando os skimage, a imagem de cinza para rgb

# if lines is not None: # Verifica se a lista de retas não está vazia
#     for i in range(0, len(lines)):
#         rho = lines[i][0] # Pega cada distância
#         theta = lines[i][1] # Pega cada ângulo
#         deg = np.rad2deg (theta)
#         # Pega retas horizontais e verticais
#         if not (deg < 5 or \
#         np.abs (deg - 90) < 5 or \
#         np.abs (deg - 180) < 5):
#             continue
#         angulos.append(theta) # Adiciona na lista de ângulos
#         # Calcula os a's e b's da equação
#         a = math.cos(theta)
#         b = math.sin(theta)
#         # Calcula os x0's e y0's da equação
#         x0 = a * rho
#         y0 = b * rho
#         # Define os pontos
#         pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
#         pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))

#         # Cria a linha usando skimage
#         rr, cc = skimage.draw.line(pt1[1], pt1[0], pt2[1], pt2[0])
        
#         # Garante que os índices estejam dentro dos limites da imagem
#         rr = np.clip(rr, 0, cdst.shape[0] - 1)
#         cc = np.clip(cc, 0, cdst.shape[1] - 1)

#         # Desenha a linha na imagem para cada reta detectada
#         cdst[rr, cc] = [255, 0, 0]  # Cria uma reta vermelha na imagem

# # Exibe uma única imagem
# plt.figure(figsize=(5, 5))  # Ajusta o tamanho da figura
# plt.imshow (cdst) # Mostra a imagem com as retas
# plt.title('Retas')  # Defini o título
# plt.show()

# angulos_graus = [np.rad2deg(x) for x in angulos] # Convertendo os ângulos para graus

# # Encontra o ângulo mais votado, ou seja, o mais significativo dos ângulos
# hist, bin_edges = np.histogram(angulos_graus, bins=180, range=(-20, 20)) # Calcula o histograma, pois se o ângulo que mais se
#                                                                          # repetir é mais significativo, pois mais retas tem 
#                                                                          # a mesma inclinação/ângulo
# angulo_mais_votado = bin_edges[np.argmax(hist)]  # Pega o ângulo com maior contagem


# # Usando as funções da transformações geométricas passas em sala para realizar a operação de rotação
# IM = translacao(img.shape[0]//2,\
#                 img.shape[1]//2).dot(rotacao(-angulo_mais_votado)).dot(translacao(-img.shape[0]//2,\
#                                                                             -img.shape[0]//2))
# print (IM)

# # Faz a rotação no ângulo mais votado
# result = np.zeros_like (img)
# for x in range (img.shape[0]):
#     for y in range (img.shape[1]):
#         p1 = np.array([x,y,1]).reshape(3,1)
#         p2 = IM.dot (p1)
#         if p2[0] >= 0 and p2[0]<img.shape[0]-.5 and p2[1] >= 0 and p2[1] <img.shape[1]-.5:
#             result[x,y] = img [int (p2[0]+0.5), int(p2[1]+0.5)]

# # Visualiza o antes e o depois
# fig, ax = plt.subplots(1, 2, figsize=(10, 5))  # Ajusta o tamanho da figura
# ax[0].set_title('Imagem original')  # Define o título
# ax[0].imshow(img, cmap='gray')
# ax[1].set_title('Imagem rotacionada')  # Define o título
# ax[1].imshow(result, cmap='gray')
# plt.tight_layout()  # Exibe as duas imagens
# plt.show()

# # As transformações e rotações aplicada geram distorções de escala, sendo necessária essa operação se 
# scale = 1/4
# img= rescale(img, scale, anti_aliasing=True)

# # Binariza novamente a imagem
# img[img <= 0.5] = 0
# img[img > 0.5] = 1

# # Encontrar o índice da linha central
# linha_central = img.shape[0] // 2  # Divide por 2 para pegar o meio

# # Pegar apenas a linha central e todas as suas colunas
# codigo = img[linha_central, :]
# print(codigo)
# print(len(codigo))

# # Exibe a linha como uma imagem
# plt.plot(codigo, '-k')  # Plota a intensidade da linha
# plt.show()

# codigo = 1 - codigo # Calcula o negativo, pois código de barras é em nagetivo, todos os valores comaçam com uma barra de zeros
#                     # que são lidos como uns

# cont = 0
# for uns in range(len(codigo)):
#     if codigo[uns] == 1:  # Verifica se encontrou o primeiro "zero"
#         break             # se encontrou, para
#     cont += 1  # Conta o número de posições antes do primeiro "zero"

# codigo = codigo[cont:len(codigo) - cont] # Consta o começo e o final da linha central, restando apenas o código de barras


# # Concatena o array, tornando-o uma string, o que retira as vírgulas
# str_codigo = "".join((codigo.astype(int)).astype(str))

# print(str_codigo) # Printa o código

# # Teste de leitura do código, e até o momento funcionou bem, compara corretamente
# tabela = pd.read_excel('tabela_code128_completa.xlsx', engine='openpyxl') # A tabeçla é só de uma caractere,
#                                                                           # assim temos cercad e 128 opções

# # Separar as colunas em variáveis separadas
# referencia = tabela['Padrão Code 128'].to_numpy()  # Substitua 'nome_da_coluna_numerica' pelo nome correto da coluna
# mensagem = tabela['Caractere'].to_numpy()    # Substitua 'nome_da_coluna_strings' pelo nome correto da coluna

# palavras = [] # Cria uma lista para as palavras, os conjuntos de 11 dígitos que formam o código de barras
# grupo = 0 # Contado para separar as palavras
# for e in range(len(str_codigo)):
#     palavras.append(str_codigo[grupo:grupo+11]) # Juntas os conjuntos na lista
#     grupo = grupo + 11 # Pula a cada 11 dígitos

# palavras = [item for item in palavras if item != ""] # Retira os elementos vazios da lista, se houver

# print(palavras) # Printa a lista com as palavras

# # Ao encontrar o código correspondente, é impresso o caractere associado.
# # O enumerate() acessa tanto o valor de referencia quanto o índice,
# # e permite imprimir o caractere correspondente a mensagem[i].
# for p in palavras:  # Compara a lista com a tabela
#     for i, confere in enumerate(referencia): 
#         if confere == int(p): # Passa novamente para int, a fim de comparar com a tabela
#             print(f"Encontrado: {mensagem[i]}") # Apresenta o resultado das comparações realizadas