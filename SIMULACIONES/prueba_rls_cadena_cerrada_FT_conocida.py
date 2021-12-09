# -*- coding: utf-8 -*-

"""
La primera línea es necesaria para codificar los carateres en UTF-8 ya que
Python-2 emplea la codificación ASCII
"""
"""
Script principal a ejecutar.
"""
"""
Importar las librerías necesarias
"""
import numpy as np
from time import sleep, time
import matplotlib.pyplot as plt
import random
import pid_autoajustable as pid_auto
from control import matlab


def main():

    # Creamos la función de transferencia del sistema
    Tm = 1
    Num_real = [0.005871]
    Den_real = [1, -1.896, 0.9056]
    FT_real=matlab.tf(Num_real, Den_real, Tm)
    print(FT_real)
    sp = np.array(())
    sp = np.concatenate((50 * np.ones(150), 70*np.ones(150), 30*np.ones(150), 60*np.ones(150)))
    t = np.arange(sp.size)
    noise = np.random.rand(sp.size) / 20
    print(noise)
    #variables de identificacion
    P = np.array(())
    X = np.array(())


    lista_numerador_b0 = []
    lista_denominador_a0 = []
    lista_denominador_a1 = []

    Num_rls = 0.0001
    Den_rls = [1, 0.0005, 0.0008]
    output_rls = [0, 0] 
    output_real = [0, 0]
    error = []

    for i in t:
        #Obtenemos el error

        error.append(sp[i] - output_real[-1])
        
        #Obtenemos la salida real del sistema
        output_real_aux = (error[-1] * Num_real[0] - output_real[-1] * Den_real[1] - output_real[-2] * Den_real[2]) + noise[i]
        output_real.append(output_real_aux)

        #Hacemos la identificación

        Num_rls, Den_rls, P, X = pid_auto.RLS(error[-1], output_real_aux, Num_rls, Den_rls, P, X, f_olvido = 0.8) # Ejecutamos RLS

        lista_numerador_b0.append(Num_rls)
        lista_denominador_a0.append(Den_rls[1])
        lista_denominador_a1.append(Den_rls[2])
        
        #Obtenemos la salida del sistema identificado

        output_rls_aux = error[-1] * Num_rls - output_rls[-1] * Den_rls[1] - output_rls[-2] * Den_rls[2]
        output_rls.append(output_rls_aux)

        

    # Imprimimos resultados
    FT_real=matlab.tf(Num_real, Den_real, Tm)
    print("FT_real: ")
    print(FT_real)
    FT_rls=matlab.tf(Num_rls, Den_rls, Tm)
    print("FT_rls: ")
    print(FT_rls)

    #graficamos salidas de ambos sistemas
    plt.close()
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot(sp, 'k', label="Set point")
    ax1.plot(output_real, 'b', label="Real output")
    ax1.plot(output_rls, 'r', label="RLS output")
    ax1.set_title("Respuesta del sistema")
    ax1.set_ylabel('Porcentaje (%)')
    ax1.legend()
    ax2.plot(lista_numerador_b0,"g", label="b0")
    ax2.plot(lista_denominador_a0,"r", label="a0")
    ax2.plot(lista_denominador_a1,"b", label="a1")
    ax2.set_title("Pesos de la ft")
    ax2.set_xlabel('Tiempo (s)')
    ax2.set_ylabel('Valor')
    ax2.legend()
    plt.show()




if __name__ == "__main__":
    main()