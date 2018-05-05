#--Recortes de imagenes a analizar
from __future__ import division
import cv2
import numpy as np
from os import listdir

#--Permite mostrar la imagen actual
def mostrarimagen(imagen):
    imagen = cv2.resize(imagen, (600, 400))
    cv2.imshow('tomate', imagen)
    cv2.waitKey(0)

#--Permite recorrer el fichero con las direcciones de las imagenes
def recorridofichero(carpeta_entrada, carpeta_salida, lista_imagenes):
    for nombre_imagen in lista_imagenes:
        print nombre_imagen
        imagen = cv2.imread(carpeta_entrada + "/" +nombre_imagen)
        encontrar = encontrarmanzana(imagen)
        cv2.imwrite(carpeta_salida + "/" + nombre_imagen, encontrar)

#--Permite encontrar todo el contorno de la imagen tratada
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


#--Define un rectangulo para hacer los recortes de las imagenes
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

#--Analiza la imagen y busca los recuadros creados
def encontrarmanzana(imagen):
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

recorridofichero("ManzanasMaduras", "ManzanasRMaduras", listdir("./ManzanasMaduras"))
recorridofichero("ManzanasPodridas", "ManzanasRPodridas", listdir("./ManzanasPodridas"))
recorridofichero("ManzanasVerdes", "ManzanasRVerdes", listdir("./ManzanasVerdes"))
