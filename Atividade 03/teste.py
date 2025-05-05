# import numpy as np
# import matplotlib.pyplot as plt
# from skimage import io
# from skimage.morphology import binary_erosion, binary_dilation

# def erosao(a, b):
#     # Convertendo as entradas para binário (0 e 1)
#     a = a.astype('uint8')
#     b = b.astype('uint8')

#     al, ac = a.shape
#     bl, bc = b.shape

#     # Adicionando padding para evitar erros de borda
#     a_ = (np.zeros((al+2, ac+2))).astype('uint8')
#     a_[1:1+al, 1:1+ac] = a  # Posiciona a matriz `a` no centro de `a_`
#     ae = np.zeros_like(a, dtype='uint8')  # Matriz de saída com o mesmo tamanho de `a`

#     # Aplicando a erosão
#     for i in range(al):
#         for j in range(ac):
#             # Extraindo a região correspondente
#             # Verificando se a região corresponde ao elemento estruturante
#             if np.all((a_[i:i + bl, j:j + bc] & b) == b):
#                 ae[i, j] = 1

#     return ae

# def hit_or_miss (a,x,w): # Função passada na aula
#     d1 = erosao(a,x)
#     d2 = erosao((1-a),w)
#     return d1*d2

# # Implementação da poda

# p1 = np.array([[0, 0, 0], 
#                [1, 1, 0], 
#                [0, 0, 0]])


# p1c = np.array([[0, 1, 1], 
#                 [0, 0, 1], 
#                 [0, 1, 1]])

# p2 = np.array([[0, 1, 0], 
#                [0, 1, 0], 
#                [0, 0, 0]])

# p2c = np.array([[0, 0, 0], 
#                 [1, 0, 1], 
#                 [1, 1, 1]])

# p3 = np.array([[0, 0, 0], 
#                [0, 1, 1], 
#                [0, 0, 0]])

# p3c = np.array([[1, 1, 0], 
#                 [1, 0, 0],
#                 [1, 1, 0]])

# p4 = np.array([[0, 0, 0], 
#                [0, 1, 0], 
#                [0, 1, 0]])

# p4c = np.array([[1, 1, 1], 
#                 [1, 0, 1],
#                 [0, 0, 0]])

# p5 = np.array([[1, 0, 0], 
#                [0, 1, 0], 
#                [0, 0, 0]])

# p5c = 1 - p5

# p6 = np.array([[0, 0, 1], 
#                [0, 1, 0], 
#                [0, 0, 0]])

# p6c = 1 - p6           

# p7 = np.array([[0, 0, 0], 
#                [0, 1, 0], 
#                [0, 0, 1]])

# p7c = 1 - p6         

# p8 = np.array([[0, 0, 0], 
#                [0, 1, 0], 
#                [1, 0, 0]])

# p8c = 1 - p8    

# # Conjunto de EE's
# p = [[p1, p1c], [p2, p2c], [p3, p3c], [p4, p4c],
#      [p5, p5c], [p6, p6c], [p7, p7c], [p8, p8c]]

# aux = np.array([
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
#     [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#     [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# ])

# aux1 = (np.zeros((aux.shape[0]+2, aux.shape[1]+2))).astype('uint8')
# aux1[1:1+aux.shape[0], 1:1+aux.shape[1]] = aux
# aux_ = aux1.copy()
# for i in range (50):
#     for ee in p:
#         aux = aux ^ hit_or_miss (aux,ee[0],ee[1])
# print(aux1)

import numpy as np
import matplotlib.pyplot as plt

n = np.ones((1,1), dtype=np.uint8)  # Começa com 1x1

for i in range(5):  # Expande 5 vezes
    n_ = np.zeros((n.shape[0]+2, n.shape[1]+2), dtype=np.uint8)  # Cria uma matriz maior
    n_[1:-1, 1:-1] = n  # Mantém a estrutura anterior no centro
    n = n_  # Atualiza 'n'

    plt.figure()
    plt.imshow(n, cmap='gray')
    plt.title(f'Iteração {i+1}')
    plt.show()
