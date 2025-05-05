from skimage.transform import hough_line, rotate
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage.filters import sobel
from skimage.draw import polygon
from skimage.color import gray2rgb
import math

# Carregar a imagem
img = (io.imread('istockphoto-962234450-612x612.jpg', as_gray=True) * 255).astype('uint8')

# Binarizar a imagem
img_bin = img.copy()
img_bin[img_bin < 100] = 0
img_bin[img_bin > 0] = 255
img_bin = 255 - img_bin

# Detectar bordas
edges = (sobel(img_bin) * 255).astype('uint8')

# Transformada de Hough
tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 180, endpoint=False)
h, theta, d = hough_line(edges, theta=tested_angles)

# Detectar picos (linhas) na Transformada de Hough
threshold = 100  # Ajuste o limiar conforme necessário
peaks_angles = []
peaks_dists = []

# Encontrando picos significativos na Transformada de Hough
for i in range(1, h.shape[0] - 1):
    for j in range(1, h.shape[1] - 1):
        if (h[i, j] > h[i-1, j-1] and h[i, j] > h[i-1, j] and h[i, j] > h[i-1, j+1] and
            h[i, j] > h[i, j-1] and h[i, j] > h[i, j+1] and
            h[i, j] > h[i+1, j-1] and h[i, j] > h[i+1, j] and h[i, j] > h[i+1, j+1] and
            h[i, j] > threshold):
            peaks_angles.append(theta[j])
            peaks_dists.append(d[i])

# Identificando os ângulos mais próximos de 90 graus (linhas verticais)
angle_threshold = np.pi / 180  # Margem de 1 grau
lines_angles = [angle for angle in peaks_angles if np.abs(angle - np.pi / 2) \
                < angle_threshold or np.abs(angle + np.pi / 2) < angle_threshold]

# Se houver ângulos detectados
if lines_angles:
    # Calcular o ângulo de rotação
    angle = np.mean(lines_angles)
    
    # Corrigir a rotação da imagem
    img_corrigida = rotate(img, np.rad2deg(angle) - 90, mode='reflect', preserve_range=True)
    
    # Visualizar a imagem corrigida
    plt.imshow(img_corrigida, cmap='gray')
    plt.show()
else:
    print("Nenhuma linha vertical detectada.")
