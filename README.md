Tarea programada #4

Estudiante: Jonathan Ramírez Hernández; carné: B55730.
Correo: jon231996@gmail.com
Grupo: 02.

Solución.
	Para la solución, de primero, se importaron as bibliotecas necesarias para solucionar los incisos, entre ellas: “pandas”, “numpy”, “matplotlib” y “scipy”. Posteriormente, se importó el archivo de datos usando la biblioteca pandas. En el archivo cargado, al conjunto de datos se le asignó el nombre “bits” y a la columna que contiene la información de los bits se le asignó el título “c0”. De esta forma, los elementos del archivo de datos pueden ser accesados usando “bits.c0[i]”, donde “i” representa el índice del elemento que se desea acceder.

Inciso 1: creación del esquema de modulación BPSK.
	Primeramente, se creó la forma de la señal portadora – la que está involucrada en cada periodo que le corresponde a cada bit –, para esto se definió su frecuencia de operación y el periodo. Luego, se definió la cantidad de puntos de muestreo para cada periodo. Se asigna una cantidad de puntos suficiente para poder obtener una gráfica senoidal en la que se vea bien su curvatura. La gráfica de esta señal portadora se adjunta. Una vez hecho esto, se hace la atribución a cada bit de señal portadora, en función del esquema de modulación empleado; en este caso, BPSK dice que cuando el bit es 1 se debe tener la señal senoidal como es, sin ninguna modificación, si es 0 se debe tener la señal senoidal multiplicada por -1. Luego, se crea un vector llamado “senal” que va a contener todas las formas de onda obtenidas para todos los bits. Para esta señal “completa” se crea un vector de tiempo que abarque toda la extensión de los periodos de las señales de cada bit. Luego, se hace un ciclo for para llenar el vector “senal” y, por último, se muestra la gráfica obtenida de la señal completa, pero solo en los primeros 5 bits. En la gráfica se puede ver la señal senoidal (su forma en un periodo) positiva y, también, de forma inversa, es decir, negativa, en correspondencia con los bits del archivo.

Inciso 2: potencia promedio de la señal generada.
	Para esto se calcula la potencia instantánea y, con esto, la promedio al utilizar la integración de la potencia instantánea en el tiempo dividida entre la cantidad de bits por el periodo de la señal. El valor obtenido es de 0.4900009800019598 W.

Inciso 3: simulación de un canal ruidoso de tipo AWGN.
	Para esta simulación, el ruido se simula de forma aleatoria con una distribución normal cuya varianza es la potencia del ruido. La potencia del ruido depende de la SNR (relación señal a ruido). Entonces, si se tiene SNR, se calcula la potencia del ruido que permite calcular la varianza de éste y, a su vez, la desviación estándar. Por lo que, para generar el ruido, se una distribución gaussiana con un “sigma” que se obtiene como se mencionó anteriormente. Como hay varios SNR, se obtienen varias señales ruidosas. Entre más alta sea la SNR, la señal es menos ruidosa. Por lo que se esperaría un comportamiento similar en las gráficas. En el código se usó un ciclo for para obtener las gráficas y almacenar los valores de sigma, para cada SNR, en una lista, para usarla en otro inciso. Las gráficas obtenidas se adjuntan.

Inciso 4: graficación de la densidad espectral.
	Se muestran las gráficas de la densidad espectral antes y después del canal ruidoso. Como se debe usar el método de Welch, en el código se usó el comando “signal.welch”. La densidad luego del canal ruidoso es muy similar para todos los valores de SNR involucrados.

Inciso 5: demodulación y decodificación de la señal y conteo de la tasa de error.
	Para detectar, en cada periodo, el bit respectivo, se determina un parámetro que permita identificar un tipo de onda. Este parámetro es la energía de la onda original dividido entre dos. Este parámetro representa una especie de umbral para detectar el bit respectivo en el periodo de la señal. Luego de la demodulación, se cuentan la cantidad de errores y se calcula BER. Como se tienen seis tipos de ondas ruidosas (por los SNR), se tienen seis BER.
SNR 	BER
-2	0.0017
-1 	0.0003
0 	0.0001
1 	0.0000
2 	0.0000
3	0.0000
En el inciso 6 se hace la gráfica de estos valores con SNR en X y BER, que es decreciente, por lo explicado en el inciso 3.
