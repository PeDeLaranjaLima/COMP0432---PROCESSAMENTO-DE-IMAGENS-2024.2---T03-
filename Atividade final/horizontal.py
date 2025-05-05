import numpy as np
import matplotlib.pyplot as plt
from skimage import io, transform, color, draw
from skimage.filters import sobel

# Carregar imagem
img = (io.imread('istockphoto-962234450-612x612.jpg', as_gray=True) * 255).astype('uint8')

# Binzarizando a imagem
img_bin = img.copy()
img_bin[img_bin < 100] = 0
img_bin[img_bin > 0] = 255
img_bin = 255 - img_bin

# Detectando bordas
edges = (sobel(img_bin) * 255).astype('uint8')

# Realizando a Transformada de Hough
tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 180, endpoint=False)
h, theta, d = transform.hough_line(edges, theta=tested_angles)

# Encontrar o ângulo mais próximo da vertical (90° ou -90°)
vertical_lines = [i for i, angle in enumerate(theta) if np.abs(np.rad2deg(angle) - 90) < 10 or np.abs(np.rad2deg(angle) + 90) < 10]

# Escolher o ângulo da linha mais vertical
if vertical_lines:
    angle_to_rotate = np.rad2deg(theta[vertical_lines[0]])  # Pega o primeiro ângulo encontrado
else:
    # Caso não encontre uma linha vertical, vamos usar um ângulo padrão (0 graus, sem rotação)
    angle_to_rotate = 0

# Ajuste a rotação de acordo com o ângulo da linha vertical
img_corrigida = transform.rotate(img, angle_to_rotate, mode='reflect', preserve_range=True)

# Clipping para garantir valores válidos
img_corrigida = np.clip(img_corrigida, 0, 255).astype('uint8')

# Visualizando antes e depois
_, ax = plt.subplots(1, 2)
ax[0].imshow(img, cmap='gray')
ax[1].imshow(img_corrigida, cmap='gray')
plt.show()
