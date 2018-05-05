import neurolab as nl
import numpy as np
import scipy as sp

#--Se leen los datos de entrada generados en una matriz
datos = np.matrix(sp.genfromtxt("entrenamientodata.csv", delimiter=" "))
#--S
columnasdesalida = 3
#--Entradas para la neurona
entrada = datos[:,:-3]
#--Salidas de la neurona
objetivo = datos[:,-3:]

#-- Rango mínimo y máximo para cada entrada 
maxmin = np.matrix([[ -5, 5] for i in range(len(entrada[1,:].T))])

# --Valores de las capas de entrada
capa_entrada = entrada.shape[0]
capa_oculta1 = int(capa_entrada*0.5)
capa_oculta2 = int(capa_entrada*0.33)
capa_salida = 3

# Crear red neuronal con 4 capas 1 de entrada 2 ocultas y 1 de salida 
rna = nl.net.newff(maxmin, [ capa_entrada, capa_entrada, capa_oculta1, capa_salida])

#Cambio de algoritmo a back progation simple
rna.trainf = nl.train.train_gd

#Datos para la RNAd
error = rna.train(entrada, objetivo, epochs=7500000, show=100, goal=0.02, lr=0.01)


#rna.save("neurona.tmt")
# Simulacion RNA
rna.save("redcreada.tmt")
salida = rna.sim(entrada)

#print rna.layers[0].np['w']
#print rna.layers[1].np['w']

print salida

