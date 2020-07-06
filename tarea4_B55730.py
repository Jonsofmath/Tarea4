#!/usr/bin/env python
# coding: utf-8

# In[20]:


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm
import math
from scipy import stats
from scipy import signal
from scipy import integrate


# In[21]:


#Lectura del archivo de datos.
address = 'bits10k.csv'
names = ['c0']
bits = pd.read_csv(address, names = names)
bits


# In[22]:


#Inciso 1: Esquema de modulación BPSK.
#Los bits por utilizar ya están importados del archivo.

#Frecuencia de operación y período de cada símbolo.
f = 5000   #En Hertz.
T = 1/f

#Debido a que no existe tiempo continuo, se debe definir una
#cantidad de "puntos" que va a tener la onda. Estos son como una 
#"resolución" de la señal. Entre más tenga, la señal se ve de forma 
#más parecida a una senoidal continua, entre menos tenga, tendrá una 
#forma más "pixelada".

#Cantidad de puntos de muestreo por periodo.
p = 50

#Puntos de muestreo para cada periodo.
tp = np.linspace(0,T,p)   #La cantidad de punto es "p" debido a lo anterior.

#Creación de la forma de onda portadora.
sinus = np.sin(2*np.pi*f*tp)

#Graficación.
plt.plot(tp, sinus)
plt.title("Gráfica de la onda portadora.")
plt.xlabel('Tiempo (s)')
plt.ylabel("Amplitud")


#Con la forma de onda se hace la atribución a cada bit en función
#del esquema de modulación que dice que a 1 se le asigna sinus y 
# a 0 se le asigna -sinus.

#Frecuencia de muestreo (Número de muestras por segundo).
fs = p/T

#Para la simulación, lo que se hace es crear un gran vector
#donde están depositadas todas las formas de onda asociadas
#con los bits involucrados.

#Creación de una línea temporal para toda la señal Tx
#que abarca todos los periodos de todos los bits.
n = len(bits)
t = np.linspace(0,n*T,n*p)

#Inicializar el vector de la señal.
#Se inicializa con ceros.
senal = np.zeros(t.shape) 

#Creación de la señal modulada.
#Recorrer cada bit y generar una forma de onda en funcion de cada bit.

for k in range(0,len(bits)):
    if bits.c0[k] == 0:
        senal[k*p:(k+1)*p] = -sinus
    else:
        senal[k*p:(k+1)*p] = sinus
    
#Visualizacion de los primeros bits modulados.
#Si funciona solo con algunos bits, el resto también sirve; también,
#es un poco complicado graficar la información de los 10000 bits.
pb = 5
plt.figure()
plt.plot(senal[0:pb*p])
plt.title("Gráfica de la señal completa en los primeros 5 bits.")


# In[23]:


#Inciso 2: potencia promedio de la señal modulada general
#Potencia instantánea.
Pinst = senal**2
#Potencia promedio.
Ps = integrate.trapz(Pinst, t)/(len(bits)*T)
print("La potencia promedio de la señal es: "+str(Ps)+" W")


# In[24]:


#Inciso 3: simulación de un canal ruidoso de tipo AWGN.

#Relación señal-ruido deseada
SNR = list(range(-2,4))
print(SNR)
sigma_arr = np.zeros(6)    #Lista para almacenar los valores de sigma. Sera necesaria para calcular el BER para cada SNR
for i in range(0,6):
    #Potencia del ruido para SNR y potencia de la señal dadas.
    Pn=Ps/(10**(SNR[i]/10))

    #Desviación estándar del ruido.
    sigma = np.sqrt(Pn)
    sigma_arr[i] = sigma
    
    #Creación del ruido (Pn = sigma^2)
    #El ruido por crear es aditivo blanco gaussiano, por lo que
    #se utiliza una distribución normal.
    ruido = np.random.normal(0, sigma, senal.shape)

    #Simular el canal: señal recibida.
    RX = senal + ruido   #Señal ruidosa.

    #Visualización de los primeros bits recibidos de la señal ruidosa.
    pb = 5
    plt.figure()
    plt.plot(RX[0:pb*p])
    plt.title("Canal ruidoso con SNR de "+str(SNR[i]))
    plt.xlabel('Tiempo (s)')
    plt.ylabel("Amplitud")

print(sigma_arr)


# In[36]:


#Inciso 4: graficacion de la densidad espectral de potencia de la señal
#con el método de Welch antes y después del canal ruidoso.

# Antes del canal ruidoso
fw, PSD = signal.welch(senal, fs, nperseg=1024)
plt.figure()
plt.semilogy(fw, PSD)
plt.title("Densidad espectral de potencia de la señal antes del canal ruidoso")
plt.xlabel('Frecuencia / Hz')
plt.ylabel('Densidad espectral de potencia / V**2/Hz')
plt.show()

# Después del canal ruidoso
fw, PSD = signal.welch(RX, fs, nperseg=1024)
plt.figure()
plt.semilogy(fw, PSD)
plt.title("Densidad espectral de potencia de la señal luego del canal ruidoso")
plt.xlabel('Frecuencia / Hz')
plt.ylabel('Densidad espectral de potencia / V**2/Hz')
plt.show()


# In[130]:


#Inciso 5 (Demodulación).
#Demodular y decodificar la señal.
#Demodulación por detección de energía
#Para cada período se calcula un parámetro que permita identificar un tipo de onda.

#Pseudoenergía de la onda original.
Es =  np.sum(sinus**2)
print(Es)

#Inicialización del vector de bits recibidos.
bitsRX = np.zeros(len(bits))

#Inicialización de una lista que almacene los valores de BER.
BER_arr = []

#Decodificación de la señal por detección de energía.
for s in sigma_arr:
    #Se vuelve a hacer la función RX para el sigma respectivo.
    ruido = np.random.normal(0, s, senal.shape)
    RX = senal + ruido
    umbral = Es/2
    
    for k in range(0,len(bits)):
        #Producto interno de dos funciones.
        Ep = np.sum(RX[k*p:(k+1)*p]*sinus) #Energida contenida en RX.
        if Ep > umbral:
            bitsRX[k] = 1
        else:
            bitsRX[k] = 0
        
    #Se analiza cada periodo para ver si hay una forma de onda
    #print(bits)
    #print(bitsRX)
    err = np.sum(np.abs(bits.c0 - bitsRX))
    BER = err/len(bits)
    BER_arr.append(BER)
    print(BER)
print(BER_arr)


# In[131]:


#Inciso 6: graficación de BER vs SNR.
#La información de ambas listas (BER y SNR) ya está disponible a partir de los resultados de los incisos anteriores.

plt.plot(SNR, BER_arr)
plt.title("Gráfica BER vs SNR")
plt.xlabel("SNR")
plt.ylabel("BER")


# In[ ]:





# In[ ]:




