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

    Tm = 1

    Num_real = [0.005871]
    Den_real = [1, -1.896, 0.9056]
    
    FT_real=matlab.tf(Num_real, Den_real, Tm)
    print(FT_real)

    input_data = np.array(())
    input_data = np.concatenate((50 * np.ones(150), 70*np.ones(150), 30*np.ones(150), 60*np.ones(150)))
    
    t = np.arange(input_data.size)
    
    output_data, t, _ = matlab.lsim(FT_real,input_data,t)

    # Ejecución inicial
    # Creamos todas las variables que se van a utilizar
    P = np.array(())
    X = np.array(())

    Num_rls = 0.0001
    Den_rls = [1, 0.0005, 0.0008]
    

    lista_numerador_b0 = []
    lista_denominador_a0 = []
    lista_denominador_a1 = []

    lista_numerador_b0_mean_5 = []
    lista_denominador_a0_mean_5 = []
    lista_denominador_a1_mean_5 = []

    lista_numerador_b0_mean_10 = []
    lista_denominador_a0_mean_10 = []
    lista_denominador_a1_mean_10 = []
    
    
    #valopres iniciales de la señal de error y la señal de entrada u
    error = [0, 0]  # ya que en el pid intervienen 2 valores anteriores
    u = [0, 0] 
    y = [0, 0] 
    output_rls = [0, 0] 
    output_rls_mean_5 = [0, 0]
    output_rls_mean_10 = [0, 0]

    # Ejecución del PID autoajustable

    for i in t:
        # Ejecutamos la identificación de la planta
        Num_rls, Den_rls, P, X = pid_auto.RLS(input_data[i], output_data[i], Num_rls, Den_rls, P, X, f_olvido = 0.9) # Ejecutamos RLS
        lista_numerador_b0.append(Num_rls)
        lista_denominador_a0.append(Den_rls[1])
        lista_denominador_a1.append(Den_rls[2])
        array_b0 = np.array(lista_numerador_b0)
        array_a0 = np.array(lista_denominador_a0)
        array_a1 = np.array(lista_denominador_a1)
        #mean de 5 valores
        lista_numerador_b0_mean_5.append(np.mean(array_b0[-5:]))
        lista_denominador_a0_mean_5.append(np.mean(array_a0[-5:]))
        lista_denominador_a1_mean_5.append(np.mean(array_a1[-5:]))
        output_rls_aux = input_data[i] * Num_rls - output_rls[-1] * Den_rls[1] - output_rls[-2] * Den_rls[2]
        output_rls_mean_5_aux = input_data[i] * lista_numerador_b0_mean_5[-1] - output_rls_mean_5[-1] * lista_denominador_a0_mean_5[-1] - output_rls_mean_5[-2] * lista_denominador_a1_mean_5[-1]
        output_rls.append(output_rls_aux)
        output_rls_mean_5.append(output_rls_mean_5_aux)
        #mean de 10 valores
        lista_numerador_b0_mean_10.append(np.mean(array_b0[-10:]))
        lista_denominador_a0_mean_10.append(np.mean(array_a0[-10:]))
        lista_denominador_a1_mean_10.append(np.mean(array_a1[-10:]))
        output_rls_mean_10_aux = input_data[i] * lista_numerador_b0_mean_10[-1] - output_rls_mean_10[-1] * lista_denominador_a0_mean_10[-1] - output_rls_mean_10[-2] * lista_denominador_a1_mean_10[-1]
        output_rls_mean_10.append(output_rls_mean_10_aux)

    # Imprimimos resultados
    FT_real=matlab.tf(Num_real, Den_real, Tm)
    print(FT_real)
    FT_rls=matlab.tf(Num_rls, Den_rls, Tm)
    print(FT_rls)

    print("Programa finalizado.")
    plt.close()
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    ax1.plot(input_data,"g", label="input_data")
    ax1.plot(output_data,"r", label="real_output_data")
    ax1.plot(output_rls,"b", label="rls_output_data")
    ax1.plot(output_rls_mean_5,"y", label="rls_mean_5_output_data")
    ax1.plot(output_rls_mean_10,"m", label="rls_mean_10_output_data")
    ax1.set_title("Respuesta del sistema e identificaciones")
    ax1.legend(loc="upper right")
    ax2.plot(lista_numerador_b0,"g", label="b0")
    ax2.plot(lista_denominador_a0,"r", label="a0")
    ax2.plot(lista_denominador_a1,"b", label="a1")
    ax2.set_title("Valores de la ft")
    ax2.legend(loc="upper right")
    ax3.plot(lista_numerador_b0_mean_5,"g", label="b0_5_mean")
    ax3.plot(lista_denominador_a0_mean_5,"r", label="a0_5_mean")
    ax3.plot(lista_denominador_a1_mean_5,"b", label="a1_5_mean")
    ax3.plot(lista_numerador_b0_mean_10,"k", linestyle="--", label="b0_10_mean")
    ax3.plot(lista_denominador_a0_mean_10,"k", linestyle="--", label="a0_10_mean")
    ax3.plot(lista_denominador_a1_mean_10,"k", linestyle="--", label="a1_10_mean")
    ax3.set_title("Valores de la ft mean")
    ax3.legend(loc="upper right")
    plt.show()





if __name__ == "__main__":
    main()












