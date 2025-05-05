import numpy as np
from skimage.transform import hough_line
from skimage import io
from skimage.transform import resize
from skimage.draw import polygon
from skimage.color import gray2rgb
import matplotlib.pyplot as plt

img = io.imread ('codigo_de_barras.png',as_gray=True)
img[img<.5] = 0
img[img>0] = 1
img = 1-img
plt.imshow(img,cmap='gray')

tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 180, endpoint=False)
h, theta, d = hough_line(img, theta=tested_angles)
h[h>110]=0
h[h<90]=0

hplot = resize(h,(180,180))
plt.imshow(hplot,cmap='gray')

y=np.zeros(h.shape[1])
for t in range (h.shape[1]):
    for r in range (1,h.shape[0]):
        y[t] += h[r,t]

# for i in range (len(y)):
    # y[i] = np.abs(y[i]-46)
plt.plot(y,'-')
print(y[140:155])

pos_ang = np.argmax(y)
pos_ang = 148
plt.plot(h[:,pos_ang],'-')
ang = theta[pos_ang]

#Obtenção das distâncias (mínima e máxima) das retas à origem
rmin = 0
rmax = 0
j = pos_ang
i = 0
while i<h.shape[0]:
    if h[i,j] > 0:
        if rmin == 0:
            rmin = i
        if i>rmax:
            rmax = i
    i += 1
print (rmin,rmax)
print (d[rmin],d[rmax])

lmin=[]
lmax=[]
imgc = gray2rgb (np.zeros_like(img))

for x in range (img.shape[0]):
    for y in range (img.shape[1]):
        if img[x,y] > 0:
            rho = x*np.sin(ang)+y*np.cos(ang)
            # print (x,y,rho)
            if np.abs(rho-d[rmax])<5:
                lmax.append([x,y])
                imgc[x,y,0]=1
            if np.abs(rho-d[rmin])<5:
                lmin.append([x,y])
                imgc[x,y,1]=1
lmin = np.array(lmin)
lmax = np.array(lmax)
plt.imshow(imgc)

#Obtenção do retângulo envolvente
mi = np.argmin (lmin[:,1])
mx = np.argmax (lmin[:,1])
x1=lmin[mi]
x2=lmin[mx]
mi = np.argmin (lmax[:,1])
mx = np.argmax (lmax[:,1])
x3=lmax[mi]
x4=lmax[mx]

poly = np.array([x1,x2,x4,x3])
imgc = gray2rgb (img)
rr, cc = polygon(poly[:, 0], poly[:, 1], imgc.shape)
imgc[rr, cc, 0] = 1
print (imgc.shape)
plt.imshow(imgc)