# Programa de comparativa del modelo ROLANN y planos

# Cargamos librerías

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from OL_reg import nnsimul,  onelayer_reg
from sklearn.metrics import mean_squared_error, r2_score



#########################################################################################################################
                                    ### MODELO PLANOS ###
#########################################################################################################################
def interpolacion(sp, diccionario_planos):
    valores_sp_bbdd = sorted(list(diccionario_planos.keys()))

    if sp in valores_sp_bbdd:
        coef_0 = diccionario_planos[sp][0]
        coef_1 = diccionario_planos[sp][1]
        indep  = diccionario_planos[sp][2]
    else:
        valores_sp_bbdd.append(sp)
        valores_sp_bbdd.sort()
        indice = valores_sp_bbdd.index(sp)

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
        
        
        plano_mayor = diccionario_planos[valor_mayor]
        plano_menor = diccionario_planos[valor_menor]
        #interpolacion_lineal
        # calculo del plano interpolado
        coef_0 = plano_menor[0]+((plano_mayor[0] - plano_menor[0])/(valor_mayor-valor_menor))*(sp-valor_menor)
        coef_1 = plano_menor[1]+((plano_mayor[1] - plano_menor[1])/(valor_mayor-valor_menor))*(sp-valor_menor)
        indep = plano_menor[2]+((plano_mayor[2] - plano_menor[2])/(valor_mayor-valor_menor))*(sp-valor_menor)

    return coef_0, coef_1, indep


def modelo_planos(Data, sp_entreno, sp_test):
    diccionario_planos = {}
    for valor in sp_entreno:
        #obtenemos hiperplanos
        modelo_LR = LinearRegression()
        X = Data[Data.SP == valor][['a0','a1']].values
        y = Data[Data.SP == valor]['b0'].values
        modelo_LR.fit(X,y)
        #diccionario a0, b0, termino indep
        diccionario_planos[valor] = [modelo_LR.coef_[0], modelo_LR.coef_[1], modelo_LR.intercept_]
    #obtenemos el plano interpolado
    coef_0, coef_1, indep = interpolacion(sp_test, diccionario_planos)
    plano = np.array([[indep], [coef_0], [coef_1]])

    return plano

#########################################################################################################################
                                    ### MODELO ROLANN ###
#########################################################################################################################


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

    # Variables a tener en cuenta

    sp_entreno = [20, 55, 60]
    sp_test = 40
    f  = 'linear'

    # Cargamos los datos

    Path = "./BBDD/lambda_0_98/pesos_f_olvido_0_98_Planta_3.csv"
    Data = pd.read_csv(Path, sep=",")

    # Modelo planos

    modelo_plano = modelo_planos(Data, sp_entreno, sp_test)
    print(modelo_plano)
    # Modelo ROLANN

    modelo_rolann, M, U, S = modelo_red_rolann(Data, sp_entreno)
    print(modelo_rolann)

    # Obtenemos los datos de entrenamiento para el modelo del plano
    Data_test = Data[Data.SP == sp_test]
    X_test = Data_test.loc[:, ['a0', 'a1']].values
    t_test = Data_test.loc[:, 'b0'].values
    X_test = X_test.T
    #Obtenemos los valores predichos
    t_predicho_plano = nnsimul(modelo_plano,X_test,f).transpose()
    # The coefficient of determination: 1 is perfect prediction
    #print("RESULTADOS CON MODELO DE PLANOS")
    #print("Mean squared error: ", mean_squared_error(t_test, t_predicho_plano))
    #print("Coefficient of determination: ", r2_score(t_test, t_predicho_plano))

    # Obtenemos los datos de entrenamiento para el modelo del rolann
    Data_test = Data[Data.SP == sp_test]
    X_test = Data_test.loc[:, ['SP', 'b0', 'a1']].values
    t_test = Data_test.loc[:, 'a0'].values
    X_test = X_test.T
    #Obtenemos los valores predichos
    t_predicho_rolann = nnsimul(modelo_rolann,X_test,f).transpose()
    # The coefficient of determination: 1 is perfect prediction
    print("RESULTADOS CON MODELO ROLANN")
    print('Modelo entrenado con valores del {} y {}%'.format(sp_entreno[0], sp_entreno[1]))
    print('Modelo testeado con valores del {}%'.format(sp_test))
    print("Mean squared error: ", mean_squared_error(t_test, t_predicho_rolann))
    print("Coefficient of determination: ", r2_score(t_test, t_predicho_rolann))
    #print("w: ", modelo_rolann)







if __name__ == "__main__":
    main()
