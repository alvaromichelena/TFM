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
from sklearn.linear_model import LinearRegression
import pandas as pd
from OL_reg import nnsimul,  onelayer_reg


#funcion para visualizar la interpolazion de los planos

def visualizacion_planos(bbdd_planos, coef_1, coef_2, indep, SP, a0, a1, b0, w):
    colores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    fig = plt.figure(figsize=plt.figaspect(0.5))
    fig.suptitle('cOMPARATIVAS RESULTADOS', fontsize=18, fontweight='bold')
    ax1 = fig.add_subplot(projection='3d')
    lista_valores_sp = sorted(list(bbdd_planos.keys()))
    for n, valor in enumerate(lista_valores_sp):
        # graficamos el plano
        # Creamos una malla, sobre la cual graficaremos el plano
        xx, yy = np.meshgrid(np.linspace(-1.2, -0.4, num=10), np.linspace(-0.4, 0.4, num=10))
        # calculamos los valores del plano para los puntos x e y
        nuevoX = (bbdd_planos[valor][0] * xx)
        nuevoY = (bbdd_planos[valor][1] * yy) 
        # calculamos los correspondientes valores para z. Debemos sumar el punto de intercepción
        z = (nuevoX + nuevoY + bbdd_planos[valor][2])
        # Graficamos el plano
        ax1.plot_surface(xx, yy, z, alpha=0.3)
        ax1.scatter(Data[Data.SP == valor].a0, Data[Data.SP == valor].a1, Data[Data.SP == valor].b0, c = colores[n], label = "SP {}".format(valor), s=4)
    # calculamos los valores del plano para los puntos x e y
    nuevoX = (coef_1 * xx)
    nuevoY = (coef_2 * yy) 
    # calculamos los correspondientes valores para z. Debemos sumar el punto de intercepción
    z = (nuevoX + nuevoY + indep)
    # Graficamos el plano
    limites_b0 = [0, 0.8]
    limites_a0 = [-1.2, -0.4]
    limites_a1 = [-0.4, 0.4]
    ax1.scatter(Data[Data.SP == SP].a0, Data[Data.SP == SP].a1, Data[Data.SP == SP].b0, c = colores[n+1], label = "SP {}".format(SP), s=4)
    ax1.scatter(a0, a1, b0, c = 'k', label = "FT con modelo centroide", s=10)
    #a0 = -0.9
    #a1 = -0.2
    b0_planos = a0 * coef_1 + a1 * coef_2 + indep
    ax1.scatter(a0, a1, b0_planos, c = 'r', label = "Ft CON MODELO PLANOS", s=10)
    a0_rolann =  w[0][0] + w[1][0] * SP + w[2][0] * b0 + w[3][0] * a1
    ax1.scatter(a0_rolann, a1, b0_planos, c = 'orange', label = "Ft CON MODELO ROLANN", s=10)
    ax1.plot_surface(xx, yy, z, alpha=0.3)
    ax1.set_xlim(limites_a0)
    ax1.set_ylim(limites_a1)
    ax1.set_zlim(limites_b0)
    ax1.set_xlabel('a0')
    ax1.set_ylabel('a1')
    ax1.set_zlabel('b0')
    ax1.legend()
    ax1.view_init(elev=0, azim=-45)
    plt.show()
        

# Funciones del modelo

def calculo_centroides (conjunto_datos):
    centroide = []
    for x in range(len(conjunto_datos)):
        centroide.append(conjunto_datos[x].mean())
    return centroide 

def modelo_interpolacion(bbdd_centroides, bbdd_planos, SP, w):

    valores_sp_bbdd = sorted(list(bbdd_centroides.keys()))

    if SP in valores_sp_bbdd:
        b0 = bbdd_centroides[SP][2]
        a0 = bbdd_centroides[SP][0]
        a1 = bbdd_centroides[SP][1]
        coef_1 = bbdd_planos[SP][0]
        coef_2 = bbdd_planos[SP][1]
        indep = bbdd_planos[SP][2]
    else:
        valores_sp_bbdd.append(SP)
        valores_sp_bbdd.sort()
        indice = valores_sp_bbdd.index(SP)

        if indice == 0:
            #el numero introducido es el más pequeño
            valor_mayor = valores_sp_bbdd[-1]
            valor_menor = valores_sp_bbdd[1]
            
        elif indice == len(valores_sp_bbdd) - 1:
            #el numero introducido es el más grande
            valor_mayor = valores_sp_bbdd[-2]
            valor_menor = valores_sp_bbdd[0]

        else:
            #el numero introducido esta entre valores de la BBDD
            valor_mayor = valores_sp_bbdd[indice+1]
            valor_menor = valores_sp_bbdd[indice-1]
        
        
        centroide_mayor = bbdd_centroides[valor_mayor]
        centroide_menor = bbdd_centroides[valor_menor]
        plano_mayor = bbdd_planos[valor_mayor]
        plano_menor = bbdd_planos[valor_menor]
        #interpolacion_lineal
        # Calculo del centroide
        a0 = centroide_menor[0]+((centroide_mayor[0] - centroide_menor[0])/(valor_mayor-valor_menor))*(SP-valor_menor)
        a1 = centroide_menor[1]+((centroide_mayor[1] - centroide_menor[1])/(valor_mayor-valor_menor))*(SP-valor_menor)
        b0 = centroide_menor[2]+((centroide_mayor[2] - centroide_menor[2])/(valor_mayor-valor_menor))*(SP-valor_menor)
        # calculo del plano interpolado
        coef_1 = plano_menor[0]+((plano_mayor[0] - plano_menor[0])/(valor_mayor-valor_menor))*(SP-valor_menor)
        coef_2 = plano_menor[1]+((plano_mayor[1] - plano_menor[1])/(valor_mayor-valor_menor))*(SP-valor_menor)
        indep = plano_menor[2]+((plano_mayor[2] - plano_menor[2])/(valor_mayor-valor_menor))*(SP-valor_menor)
        

    visualizacion_planos(bbdd_planos, coef_1, coef_2, indep, SP, a0, a1, b0, w)
        
    #obtenemos el valor de a1 
    #b0 = a0 * coef_1 + a1 * coef_2 + indep

    Numerador = b0
    Denominador = [1, a0, a1]

        

    return Numerador, Denominador

def modelo_red_rolann(Data, sp_entreno):

    # Datos de funcionamiento
    lamb = 1 
    finv   = 'ilinear'  
    fderiv = 'dlinear'
    var_entradas = ['SP', 'b0', 'a1']
    var_salidas = ['a0']
    # Separamos los datos
    Data_train = Data[Data.SP.isin(sp_entreno)]
    X_train = Data_train.loc[:, var_entradas].values
    t_train = Data_train.loc[:, var_salidas].values
    X_train = X_train.T
    # Ejecutamos el modelo 
    w, M, U, S= onelayer_reg(X_train,t_train,finv,fderiv,lamb)

    return w, M, U, S


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
    global Data
    Path =  "./BBDD/lambda_0_98/pesos_f_olvido_0_98_Planta_3.csv"
    Data = pd.read_csv(Path, sep=",")
    lista_valores_sp = [20, 40]
    diccionario_centroides= {}
    diccionario_planos = {}
    for i, valor in enumerate(lista_valores_sp):
        #obtenemos centroides
        diccionario_centroides[valor] = calculo_centroides([Data[Data.SP == valor].a0, Data[Data.SP == valor].a1, Data[Data.SP == valor].b0])
        print("Centroide {}: ".format(valor), diccionario_centroides[valor])
        #obtenemos hiperplanos
        modelo_LR = LinearRegression()
        X = Data[Data.SP == valor][['a0','a1']].values
        y = Data[Data.SP == valor]['b0'].values
        modelo_LR.fit(X,y)
        #diccionario a0, b0, termino indep
        diccionario_planos[valor] = [modelo_LR.coef_[0], modelo_LR.coef_[1], modelo_LR.intercept_]
        print("Plano {}: ".format(valor), diccionario_planos[valor])
    
    #modelo entrenado
    w, M, U, S = modelo_red_rolann(Data, lista_valores_sp)

    Num_modelo, Den_modelo = modelo_interpolacion(diccionario_centroides, diccionario_planos, SP, w)


    # Bucle de simulación

    for i in t:

        #Obtenemos el error

        error.append(sp[i] - output_real[-1])

        #Ejecutamos el PID

        s_control = pid_auto.PID_dahlin(Num_modelo, Den_modelo, error, u, Tm, B=5)
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

    """
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
    """
    
    plt.show()



if __name__ == "__main__":
    main()
