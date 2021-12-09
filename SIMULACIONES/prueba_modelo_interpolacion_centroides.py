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
import pandas as pd

# Funciones del modelo

def calculo_centroides (conjunto_datos):
    centroide = []
    for x in range(len(conjunto_datos)):
        centroide.append(conjunto_datos[x].mean())
    return centroide 

def modelo_interpolacion(bbdd, SP):

    valores_sp_bbdd = sorted(list(bbdd.keys()))

    if SP in valores_sp_bbdd:
        Numerador = bbdd[SP][2]
        Denominador = [1, bbdd[SP][0], bbdd[SP][1]]
    else:
        valores_sp_bbdd.append(SP)
        valores_sp_bbdd.sort()
        indice = valores_sp_bbdd.index(SP)
        if indice == 0:
            #el numero introducido es el más pequeño
            valor_mayor = valores_sp_bbdd[-1]
            valor_menor = valores_sp_bbdd[1]
            centroide_mayor = bbdd[valor_mayor]
            centroide_menor = bbdd[valor_menor]
            
        elif indice == len(valores_sp_bbdd) - 1:
            #el numero introducido es el más grande
            valor_mayor = valores_sp_bbdd[-2]
            valor_menor = valores_sp_bbdd[0]
            centroide_mayor = bbdd[valor_mayor]
            centroide_menor = bbdd[valor_menor]

        else:
            #el numero introducido esta entre valores de la BBDD
            valor_mayor = valores_sp_bbdd[indice+1]
            valor_menor = valores_sp_bbdd[indice-1]
            centroide_mayor = bbdd[valor_mayor]
            centroide_menor = bbdd[valor_menor]

        # Calculo del centroide
        a0 = centroide_menor[0]+((centroide_mayor[0] - centroide_menor[0])/(valor_mayor-valor_menor))*(SP-valor_menor)
        a1 = centroide_menor[1]+((centroide_mayor[1] - centroide_menor[1])/(valor_mayor-valor_menor))*(SP-valor_menor)
        b0 = centroide_menor[2]+((centroide_mayor[2] - centroide_menor[2])/(valor_mayor-valor_menor))*(SP-valor_menor)
        Numerador = b0
        Denominador = [1, a0, a1]

    return Numerador, Denominador




def main():

    # Creamos la función de transferencia del sistema
    Tm = 1
    Num_real = [0.06, 0.0]
    Den_real = [1, -0.93, -0.03]

    #Num_real = [0.06, 0.0]
    #Den_real = [1, -0.93, -0.03]

    FT_real=matlab.tf(Num_real, Den_real, Tm)
    print(FT_real)

    # Generamos los valores del SP y ruido
    SP = 60
    sp = np.array(())
    sp = np.concatenate((SP * np.ones(200), SP * np.ones(100)))
    t = np.arange(sp.size)
    noise = (np.random.rand(sp.size) / 10) 

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

    # Obtenemos el numerador y denominador del modelo

    Path =  "./BBDD/lambda_0_98/pesos_f_olvido_0_98_Planta_3.csv"
    Data = pd.read_csv(Path, sep=",")
    lista_valores_sp = [20, 40]
    diccionario_centroides= {}
    for i, valor in enumerate(lista_valores_sp):
        diccionario_centroides[valor] = calculo_centroides([Data[Data.SP == valor].a0, Data[Data.SP == valor].a1, Data[Data.SP == valor].b0])
        print("Centroide {}: ".format(valor), diccionario_centroides[valor])
    
    Num_modelo, Den_modelo = modelo_interpolacion(diccionario_centroides,SP)


    # Bucle de simulación

    for i in t:

        #Obtenemos el error

        error.append(sp[i] - output_real[-1])

        #Ejecutamos el PID

        s_control = pid_auto.PID_dahlin(Num_modelo, Den_modelo, error, u, Tm, B=1)
        u.append(s_control)

        #Obtenemos la salida real del sistema

        output_real_aux = (u[-1] * Num_real[0] + u[-2] * Num_real[1] - output_real[-1] * Den_real[1] - output_real[-2] * Den_real[2]) + noise[i]
        output_real.append(output_real_aux)

        #Hacemos la identificación
        
        f_olvido = 0.98

        Num_rls, Den_rls, P, X = pid_auto.RLS(u[-1], output_real_aux, Num_rls, Den_rls, P, X, f_olvido = f_olvido) # Ejecutamos RLS

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
    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax1 = fig.add_subplot()
    ax1.plot(sp, 'k', label="Set point")
    ax1.plot(output_real, 'b', label="Real output")
    ax1.plot(u, 'g', label="Control signal")
    ax1.plot(abs(sp-output_real[2:]), 'r', label="Error")
    ax1.set_title("Respuesta del sistema")
    ax1.set_xlabel('Tiempo (s)')
    ax1.set_ylabel('Porcentaje (%)')
    ax1.legend()
    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax2 = fig.add_subplot()
    ax2.plot(lista_numerador_b0,"g", label="b0")
    ax2.plot(lista_denominador_a0,"r", label="a0")
    ax2.plot(lista_denominador_a1,"b", label="a1")
    ax2.axhline(Num_modelo, xmin=0, xmax=len(lista_denominador_a1), color="g", linestyle="--",label="b0_modelo")
    ax2.axhline(Den_modelo[1], xmin=0, xmax=len(lista_denominador_a1), color="r", linestyle="--",label="a0_modelo")
    ax2.axhline(Den_modelo[2], xmin=0, xmax=len(lista_denominador_a1), color="b", linestyle="--", label="a1_modelo")
    ax2.set_title("Pesos de la ft")
    ax2.set_xlabel('Tiempo (s)')
    ax2.set_ylabel('Valor')
    ax2.legend()
    
    plt.show()



if __name__ == "__main__":
    main()
