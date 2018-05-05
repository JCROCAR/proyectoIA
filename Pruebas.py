from __future__ import division
import cv2
import numpy as np
from PIL import Image
from os import listdir
import os
import neurolab as nl
import scipy as sp


def mostrar_imagen(imagen):
    imagen = cv2.resize(imagen, (600, 400))
    cv2.imshow('tomate', imagen)
    cv2.waitKey(0)

def contornoimagen(imagen):
    imagen = imagen.copy()
    img, contornos, jerarquia =\
        cv2.findContours(imagen, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = \
        [(cv2.contourArea(contorno), contorno) for contorno in contornos]
    mayor_contorno = max(contour_sizes, key=lambda x: x[0])[1]

    mascara = np.zeros(imagen.shape, np.uint8)
    cv2.drawContours(mascara, [mayor_contorno], -1, 255, -1)
    return mayor_contorno, mascara

def definirectangulocuadrado(imagen, contorno):
    imagenConElipse = imagen.copy()
    elipse = cv2.fitEllipse(contorno)
    factor_redn = 0.5
    sx = int((elipse[1][0]*factor_redn)/2)
    sy = int((elipse[1][1]*factor_redn)/2)
    x = int(elipse[0][0]) - sy
    y = int(elipse[0][1]) - sx
    imagenConElipse = imagenConElipse[y:(y + sx*2), x:(x + sy*2)]
    return imagenConElipse

def buscarmanzana(imagen):
    im2 = imagen.copy()
    im3 = imagen.copy()
    im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2HSV)
    max_dimension = max(im2.shape)
    scale = 700/max_dimension
    im2 = cv2.resize(im2, None, fx=scale, fy=scale)
    im3 = cv2.resize(im3, None, fx=scale, fy=scale)
    filtroblue = cv2.GaussianBlur(im2, (7, 7), 0)
    rojominimo = np.array([0, 100, 80])
    rojomaximo = np.array([10, 256, 256])

    mascara1 = cv2.inRange(filtroblue, rojominimo, rojomaximo)
    rojominimo_dos = np.array([10, 100, 80])
    rojomaximo_dos = np.array([180, 256, 256])

    mascara2 = cv2.inRange(filtroblue, rojominimo_dos, rojomaximo_dos)
    mascara = mascara1 + mascara2
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    mascara_cerrada = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)
    mascara_limpia = cv2.morphologyEx(mascara_cerrada, cv2.MORPH_OPEN, kernel)

    contorno_manzana_g, mascaram = contornoimagen(mascara_limpia)

    rectangulo_manzana = definirectangulocuadrado(im3, contorno_manzana_g)
    return rectangulo_manzana

#-------------

def obtenerpixeles(imagen):
    #--Abrir imagen a utilizar
    im = Image.open(imagen)
    im = im.resize((40, 10), Image.ANTIALIAS)
    pixels = im.load()

    filas, columnas = im.size
    decimales = 4
    cadena = ""
    for columna in range (columnas):
        for fila in range(filas):
            #--Separacion de valores RGB y escritura 
            rojo = str(normalizar_entradas(pixels[fila,columna][0]))
            verde = str(normalizar_entradas(pixels[fila,columna][1]))
            azul = str(normalizar_entradas(pixels[fila,columna][2]))
            cadena = cadena + rojo[:rojo.find(".")+decimales] + " " + verde[:verde.find(".")+decimales] + " " + azul[:azul.find(".")+decimales] + " "

    return cadena


def normalizar_entradas(valor):
    salida = (valor*1.)/255.
    return salida
    
#------------------

#--Dirección de imagen a utilizar para pruebas
imagen = cv2.imread("C:\Users\juan_\Desktop\yo.jpeg")
imagen = buscarmanzana(imagen)
cv2.imwrite("manzanaprueba.jpg",imagen)

cadena =  obtenerpixeles("manzanaprueba.jpg")

if(os.path.exists("manzanainfo.csv")== True):
    os.remove("manzanainfo.csv")

archivo_entrenamiento = open("manzanainfo.csv", "a")

archivo_entrenamiento.write(cadena)
archivo_entrenamiento.close()

datos = np.matrix(sp.genfromtxt("manzanainfo.csv", delimiter=" "))



rna = nl.load("redcreada.tmt")

salida = rna.sim(datos)

podrida = salida[0][0] * 100
madura = salida[0][1] * 100
verde = salida[0][2] * 100

resultado = ""

if (podrida > 80.):
    if (madura > 40.):
        resultado = "La manzana esta sobre madura"
    else:
        resultado = "La manzana esta podrida"
elif (madura > 80.):
    if (podrida > 40.):
        resultado = "La manzana esta sobre madura"
    elif (verde > 40.):
        resultado = "La manzana casi está madura"
    else:
        resultado = "La manzana totalmente madura"
elif (verde > 80.):
    if (madura > 40.):
        resultado = "La manzana desarrola su madurez"
    else:
        resultado = "La manzana esta verde"

print resultado
