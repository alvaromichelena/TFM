# -*- coding: utf-8 -*-
"""
La primera línea es necesaria para codificar los carateres en UTF-8 ya que
Python-2 emplea la codificación ASCII
"""

"""
En este archivo se incluyen todas las funciones necesarias para ejecutar 
tanto la identificación del sistema por RLS como la ejecución y ajuste de
los parámetros del PID autoajustable.
"""


import numpy as np


def PID_dahlin(numerador, denominador, e, u, Tm, B=1):

    """
    Función para ejecutar el PID de Dahlin (autoajustable).

    Se obtienen los valores de las constantes a partir de los valores de los coeficientes
    de la función de transferencia (b0, a0 y a1)

    Argumentos:
        - numerador: coeficientes del numerador de la función de transferencia (float).
        - denominador: coeficientes del denominador de la función de transferencia (list).
        - e: valores de error (sp-pv) (list).
        - u: valores de la señal de control (list).
        - Tm: tiempo de muestreo (int).
        - B: factor de ajuste. Cuanto menor valor de B la respuesta del sistema es más rápida (int/float).

    Returns:
        - u: señal de control (float).

    """

    b1 = numerador
    a1 = denominador[1]
    a2 = denominador[2]

    Q = 1 - np.exp(-Tm / B) 
    Kp = - (( a1 + 2*a2 ) * Q) / b1
    Td = ( Tm * a2 * Q ) / ( Kp * b1 )
    Ti = - Tm / ( 1 / ( a1 + 2*a2 ) + 1 + (Td / Tm) )



    u = Kp*(e[-1]-e[-2]+ (Tm / Ti) * e[-1] + (Td/Tm)*(e[-1] - 2*e[-2] + e[-3])) + u[-1]

    # Control del valor de la salida

    if u > 100:
        u = 100
    elif u < 0:
        u = 0


    return u


def calculo_constantes_ap(numerador, denominador, a=10):


    """
    Función para calcular las constantes del PID (Kp, Ti, Td)

    El método de autoajuste empleado es el de asignación por polos.

    Se obtienen los valores de p0, p1, p2 a partir de los valores de los coeficientes
    de la función de transferencia (b0, a0 y a1)

    Argumentos:
        - numerador: coeficientes del numerador de la función de transferencia (float).
        - denominador: coeficientes del denominador de la función de transferencia (list).
        - Tm: tiempo de muestreo (int).
        - k: valor del retardo que se le añade al sistema (cero) (int).

    Returns:
        - p0: constante de trabajo del PID (float).
        - p1: constante de trabajo del PID (float).
        - p2: constante de trabajo del PID (float).

    """

    b0 = numerador
    a0 = denominador[1]
    a1 = denominador[2]


    p0 = (1 / b0) * (1 + a0 - (3 / a))
    p1 = (1 / b0) * (a1 - a0 + (3 / a**2))
    p2 = -(1 / b0) * (a1 + (1 / a**3))


    return p0, p1, p2 



def calculo_constantes_mf(numerador, denominador, Tm, k=0):


    """
    Función para calcular las constantes del PID (Kp, Ti, Td)

    El método de autoajuste empleado es el de margen de fase prefijado.

    Se obtienen los valores de p0, p1, p2 a partir de los valores de los coeficientes
    de la función de transferencia (b0, a0 y a1)

    Argumentos:
        - numerador: coeficientes del numerador de la función de transferencia (float).
        - denominador: coeficientes del denominador de la función de transferencia (list).
        - Tm: tiempo de muestreo (int).
        - k: valor del retardo que se le añade al sistema (cero) (int).

    Returns:
        - p0: constante de trabajo del PID (float).
        - p1: constante de trabajo del PID (float).
        - p2: constante de trabajo del PID (float).

    """

    b0 = numerador
    a0 = denominador[1]
    a1 = denominador[2]


    p0 = 1 / (b0 * Tm**2 * (2*k + 1))
    p1 = - (a0 * p0)
    p2 = - (a1 * p0)


    return p0, p1, p2 



def PID_autoajustable(p0, p1, p2, error, u, Km=1):



    """
    Función para calcular la salida de control del PID autoajustable

    Ley de control basada en el regulador:

                           -1         -2
        -1      p0 + p1 * z   + p2 * z
    Gr(z  ) = ___________________________
                              -1
                         1 - z 

    Se obtienen los valor de salida a partir de los valores de error medidos
    y de las constantes p0, p1 y p2 calculadas a partir de los parámetros de
    la función de transferencia identificada (b0, a0, a1).

    Puesto que el algoritmo puede producir valores inferiores a 0 y mayores 
    de 100 (el sistema funciona en valores porcentuales) se limita la señal
    de salida entre estos dos valores.

    Argumentos:
        - p0: constante de trabajo del PID (float).
        - p1: constante de trabajo del PID (float).
        - p2: constante de trabajo del PID (float).
        - error: lista de valores de los errores medidos ().
        - u: lista de valores de control generados ().

    Returns:
        - s_control: señal de control (float).

    """
    
    s_control = u[-1] + (p0 * error[-1] + p1 * error[-2] + p2 * error[-3]) * Km

    # Control del valor de la salida

    if s_control > 100:
        s_control = 100
    elif s_control < 0:
        s_control = 0

    

    return s_control



def RLS(entrada_sistema,salida_sistema,n,d,P,X,f_olvido=0.9): 
   
    """
    Función para la ejecución del algoritmo RLS

    Argumentos:
        - entrada_sistema: entrada actual al sistema (float).
        - salida_sistema: salida actual del sistema (float).
        - n: numerador de la función de transferencia (float).
        - d: denominador de la función de transferencia (lista).
        - P: matriz de covarianzas (numpy matrix).
        - X: vector regresor de entrada y salidas (numpy array).
        - f_olvido: factor de olvido (por defecto 0.9) (float).
    
    Returns:
        - num: numerador de la función de transferencia actualizado (float).
        - den: denominador de la función de transferencia actualizado (lista).
        - P: matriz de covarianzas actualizada (numpy matrix).
        - X: vector regresor de entradas y salidas actualizado (numpy array).
    
    """

    #creamos un par de variables internas
    #la función RLS implementada corresponde con un sistema de 2 orden

    #por defecto factor de olvido de 0.9

    if X.size == 0 or P.size == 0:

        #comprobamos si se crearon las matrices X y P

        X = np.random.rand(3,1)/1000
        P = np.identity(3)*1000 #valor grande inicial

    #obtenemos el vector Theta

    Theta = np.array([[n], [-d[1]], [-d[2]]])
    #print("Theta", Theta)

    #actualizacion del vector X

    X[0,0]=entrada_sistema
    #print("X", X)

    #calculamos la matriz K del sistema para el instante actual

    K = (P @ X)/(f_olvido + X.T @ P @ X)
    #print("K", K)

    #calculo del error

    Error = salida_sistema - X.T @ Theta
    #print("Error", Error)

    #nuevos coeficientes

    Theta = Theta + K * Error
    #print("Theta", Theta)

    #calculo matriz p para la siguiente iteracióon

    P = (1/f_olvido) * (P - (K @ X.T @ P))
    #print("P", P)

    #actualizamos el vector x con los nuevos valores de entrada y salida
    
    X[2,0] = X[1,0] 
    X[1,0] = salida_sistema
    #print("X", X)

    #obtenemos el valor del numerador y denominador a partir del vector theta

    num = Theta[0, 0]
    den = [1, -Theta[1,0], -Theta[2,0]]

    #la función devuelve el valor del numerador, denominador, P y X

    return num, den, P, X

