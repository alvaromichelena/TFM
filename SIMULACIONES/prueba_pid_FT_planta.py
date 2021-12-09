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
import matplotlib.pyplot as plt
import random
import pid_autoajustable as pid_auto
from control import matlab


def main():

    # Creamos la función de transferencia del sistema
    Tm = 1
    #Num_real = [0.06, 0.0]
    #Den_real = [1, -0.93, -0.03]
    Num_real = [0.06, 0.0]
    Den_real = [1, -0.93, -0.03]
    FT_real=matlab.tf(Num_real, Den_real, Tm)
    print(FT_real)

    # Generamos los valores del SP y ruido

    sp = np.array(())
    sp = np.concatenate((50 * np.ones(200), 50*np.ones(100)))
    t = np.arange(sp.size)
    noise = (np.random.rand(sp.size) / 2) 

    # Variables de identificación

    P = np.array(())
    X = np.array(())
    lista_numerador_b0 = []
    lista_denominador_a0 = []
    lista_denominador_a1 = []
    Num_rls = random.random()
    Den_rls = [1, random.random(), random.random()]
    output_rls = [0, 0] 
    output_real = [0, 0]
    error = [0, 0]
    u = [0]

    # Bucle de simulación

    for i in t:

        #Obtenemos el error

        error.append(sp[i] - output_real[-1])

        #Ejecutamos el PID
        
        p0, p1, p2 = pid_auto.calculo_constantes_ap(Num_real[0], Den_real, a=10)
        #p0, p1, p2 = pid_auto.calculo_constantes_mf(Num_rls, Den_rls, k=1, Tm=1)

        #s_control = pid_auto.PID_dahlin(Num_real[0], Den_real, error, u, Tm, B=5)
        s_control = pid_auto.PID_autoajustable(p0, p1, p2, error, u, Km=0.02)
        u.append(s_control)

        #Obtenemos la salida real del sistema

        output_real_aux = (u[-1] * Num_real[0] + u[-2] * Num_real[1] - output_real[-1] * Den_real[1] - output_real[-2] * Den_real[2]) + noise[i]
        output_real.append(output_real_aux)

        #Hacemos la identificación

        Num_rls, Den_rls, P, X = pid_auto.RLS(u[-1], output_real_aux, Num_rls, Den_rls, P, X, f_olvido = 0.98) # Ejecutamos RLS

        lista_numerador_b0.append(Num_rls)
        lista_denominador_a0.append(Den_rls[1])
        lista_denominador_a1.append(Den_rls[2])
        
        #Obtenemos la salida del sistema identificado

        output_rls_aux = u[-1] * Num_rls - output_rls[-1] * Den_rls[1] - output_rls[-2] * Den_rls[2]
        output_rls.append(output_rls_aux)

        

    # Imprimimos resultados
    FT_real=matlab.tf(Num_real, Den_real, Tm)
    print(FT_real)
    FT_rls=matlab.tf(Num_rls, Den_rls, Tm)
    print(FT_rls)

    #graficamos salidas de ambos sistemas
    plt.close()
    plt.plot(sp, 'k', label="Set point")
    plt.plot(output_real, 'b', label="Real output")
    plt.plot(u, 'g', label="Control signal")
    plt.plot(abs(sp-output_real[2:]), 'r', label="Error")
    plt.title("Respuesta del sistema")
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Porcentaje (%)')
    plt.legend()
    plt.show()




if __name__ == "__main__":
    main()
