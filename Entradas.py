from PIL import Image
from os import listdir
import os

#--Función que permite obtener y extrer datos de cada pixel que conforma la imagen
def obtenerinfopixeles(direccion, entrada):
    im = Image.open(direccion)
    #--Se utiliza el algoritmo ANTIALIAS para redimensionar
    im = im.resize((40, 10), Image.ANTIALIAS)
    #--Se carga la información de los pixeles a "pixeles_info"
    pixeles_info = im.load()
    #--Los datos de entrenamiento son guardados en "datatraining"
    datatraining = open("entrenamientodata.csv", "a")
    filas, columnas = im.size
    decimales = 4
    for columna in range (columnas):
        for fila in range(filas):
            #-- Los valores RGB se clasifican y se escriben en la variable "cadena"
            rojo = str(entradas_normalizar(pixeles_info[fila,columna][0]))
            verde = str(entradas_normalizar(pixeles_info[fila,columna][1]))
            azul = str(entradas_normalizar(pixeles_info[fila,columna][2]))
            cadena = rojo[:rojo.find(".")+decimales] + " " + verde[:verde.find(".")+decimales] + " " + azul[:azul.find(".")+decimales] + " "
            datatraining.write(cadena)

    datatraining.write(entrada)
    datatraining.write("\n")
    datatraining.close()

def recorridofichero(entradafichero, imagenes, salidas):
    for nombre_imagen in imagenes:
        print nombre_imagen
        obtenerinfopixeles(entradafichero + "/" +nombre_imagen, salidas)

def entradas_normalizar(valor):
    salidas = (valor*1.)/255.
    return salidas
    

if(os.path.exists("entrenamientodata.csv")== True):
    os.remove("entrenamientodata.csv")
recorridofichero("ManzanasRMaduras", listdir("./ManzanasRMaduras"), "0 1 0")
recorridofichero("ManzanasRPodridas",  listdir("./ManzanasRPodridas"), "1 0 0")
recorridofichero("ManzanasRVerdes", listdir("./ManzanasRVerdes"), "0 0 1" )
