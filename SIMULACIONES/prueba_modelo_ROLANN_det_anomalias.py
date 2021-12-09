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
from OL_reg import nnsimul,  onelayer_reg

# Funciones del modelo

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
    SP = 50
    sp = np.array(())
    sp = np.concatenate((SP * np.ones(200), SP * np.ones(100)))
    t = np.arange(sp.size)
    noise = (np.random.rand(sp.size) / 1) 
    instante_error = 150

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

    # modelo
    # Variables a tener en cuenta

    sp_entreno = [20, 80]
    f  = 'linear'

    # Cargamos los datos

    Path = "./BBDD/lambda_0_98/pesos_f_olvido_0_98_Planta_3.csv"
    Data = pd.read_csv(Path, sep=",")

    #modelo entrenado
    w, M, U, S = modelo_red_rolann(Data, sp_entreno)

    #seleccionamos valores aleatorios
    
    b0 = random.uniform(0.1, 0.35)
    a1 = random.uniform(-0.1, 0.1)
    a0 =  w[0][0] + w[1][0] * SP + w[2][0] * b0 + w[3][0] * a1

    Num_modelo = b0
    Den_modelo = [1, a0, a1]

    numerador_ant = Num_modelo
    denominador_ant = Den_modelo
    P_ant = P
    X_ant =X


    f_olvido = 0.96

    # Bucle de simulación

    for i in t:

        #Obtenemos el error

        error.append(sp[i] - output_real[-1])

        #Ejecutamos el PID

        s_control = pid_auto.PID_dahlin(Num_modelo, Den_modelo, error, u, Tm, B=5)
        u.append(s_control)

        #Obtenemos la salida real del sistema

        output_real_aux = (u[-1] * Num_real[0] + u[-2] * Num_real[1] - output_real[-1] * Den_real[1] - output_real[-2] * Den_real[2]) + noise[i]
        
        if i == instante_error:
            output_real_aux = 30
        
        output_real.append(output_real_aux)

        


        #Hacemos la identificación
        
        

        Num_rls, Den_rls, P, X = pid_auto.RLS(u[-1], output_real_aux, Num_rls, Den_rls, P, X, f_olvido = f_olvido) # Ejecutamos RLS

        # despues de 100 iteraciones detectamos anomalias
        a0_modelo =  w[0][0] + w[1][0] * SP + w[2][0] * Num_rls + w[3][0] * Den_rls[2]
        diferencia = abs(a0_modelo - Den_rls[1])
        #print("diferencia: ", diferencia)
        if i<100:
            i=i+1
        else:
            if diferencia > 0.15:
                print("*****ANOMALIA DETECTADA EN EL INSTANTE i = {}******".format(i))
                Num_rls = numerador_ant
                Den_rls = denominador_ant
                P = P_ant
                X = X_ant

            else:
                #print("****FUNCIONAMIENTO NORMAL****")
                numerador_ant = Num_rls
                denominador_ant = Den_rls
                P_ant = P
                X_ant =X

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
