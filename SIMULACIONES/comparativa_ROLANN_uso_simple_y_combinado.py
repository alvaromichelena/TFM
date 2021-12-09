# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
#from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import StandardScaler
from OL_reg import nnsimul,  onelayer_reg

from sklearn.metrics import mean_squared_error, r2_score

# Hyperparameter (regularization)
lamb = 1

# Activation functions: 'logs' o 'rel' (Logistic or ReLu)
afun = 'lin'

if (afun == 'logs'):     # Logistic sctivation functions
    f      = 'logsig' 
    finv   = 'ilogsig'
    fderiv = 'dlogsig'
elif (afun == 'rel' ):  # ReLu sctivation functions
    f      = 'relu' 
    finv   = 'irelu'  
    fderiv = 'drelu'
elif (afun == 'lin' ):  # Linear activation functions
    f      = 'linear' 
    finv   = 'ilinear'  
    fderiv = 'dlinear'


#CARGA DE DATOS


##################################################################################################
############################OBTENCION DEL MODELO CON 1 DATASET####################################
##################################################################################################

Path = "./BBDD/lambda_0_98/pesos_f_olvido_0_98_Planta_3.csv"
        
Data = pd.read_csv(Path, sep=",")

Data_train = Data.drop(Data.loc[Data.SP == 55].index)

Data_test = Data.drop(Data.loc[Data.SP != 55].index)

lista_sp = sorted(Data_train['SP'].unique())
print(lista_sp)
lista_sp = sorted(Data_test['SP'].unique())
print(lista_sp)

"""
#NORMALIZACIÓN DE DATOS

normalizador = StandardScaler().fit(Data_train)
Data_train_nor= normalizador.transform(Data_train)
X_train = Data_train_nor[:,:-1]
t_train = Data_train_nor[:,-1]
Data_test_nor= normalizador.transform(Data_test)
X_test = Data_test_nor[:,:-1]
t_test = Data_test_nor[:,-1]
"""

#DATOS SIN NORMALIZAR

Data_train = Data_train.values

Data_test = Data_test.values

X_train = Data_train[:,:-1]

t_train = Data_train[:,-1]

X_test = Data_test[:,:-1]

t_test = Data_test[:,-1]

#ADAPTAMOS LOS DATOS PARA INTRODUCIRLO AL ALGORITMO ROLLAN

X_train = X_train.T
X_test = X_test.T

#EJECUTAMOS EL MODELO

w, M, U, S = onelayer_reg(X_train,t_train,finv,fderiv,lamb)

#OBTENEMOS RESULTADOS

t_predicho = nnsimul(w,X_test,f).transpose()

print("*********************************************************************************")
print("RESULTADOS AL EJECUTAR TODO EL DATASET")
print("w:", w)
# The mean squared error

# The coefficient of determination: 1 is perfect prediction
print("Mean squared error: ", mean_squared_error(t_test, t_predicho))
print("Coefficient of determination: ", r2_score(t_test, t_predicho))
print("*********************************************************************************")

##################################################################################################
############################OBTENCION DEL MODELO CON 2 DATASETS###################################
##################################################################################################

#CARGA DE NUEVOS DATOS

Data_train_1 = Data.drop(Data.loc[Data.SP > 54].index)

Data_train_2 = Data.drop(Data.loc[Data.SP < 56].index)

lista_sp = sorted(Data_train_1['SP'].unique())
print(lista_sp)
lista_sp = sorted(Data_train_2['SP'].unique())
print(lista_sp)


"""
#NORMALIZACIÓN DE DATOS

normalizador = StandardScaler().fit(Data_train)
Data_train_nor= normalizador.transform(Data_train)
X_train = Data_train_nor[:,:-1]
t_train = Data_train_nor[:,-1]
Data_test_nor= normalizador.transform(Data_test)
X_test = Data_test_nor[:,:-1]
t_test = Data_test_nor[:,-1]
"""

#DATOS SIN NORMALIZAR

Data_train_1 = Data_train_1.values

Data_train_2 = Data_train_2.values

X_train_1 = Data_train_1[:,:-1]

t_train_1 = Data_train_1[:,-1]

X_train_2 = Data_train_2[:,:-1]

t_train_2 = Data_train_2[:,-1]

#ADAPTAMOS LOS DATOS PARA INTRODUCIRLO AL ALGORITMO ROLLAN

X_train_1 = X_train_1.T
X_train_2 = X_train_2.T

#EJECUTAMOS EL PRIMER MODELO

w, M, U, S = onelayer_reg(X_train_1,t_train_1,finv,fderiv,lamb)

t_predicho = nnsimul(w,X_train_2,f).transpose()

print("*********************************************************************************")
print("RESULTADOS AL EJECUTAR EL DATASET POR PARTES")
print("w:", w)
# The mean squared error

# The coefficient of determination: 1 is perfect prediction
print("Mean squared error: ", mean_squared_error(t_train_2, t_predicho))
print("Coefficient of determination: ", r2_score(t_train_2, t_predicho))
print("*********************************************************************************")

#EJECUTAMOS EL SEGUNDO MODELO

w, M, U, S = onelayer_reg(X_train_2,t_train_2,finv,fderiv,lamb, M, U, S)

#OBTENEMOS RESULTADOS

t_predicho = nnsimul(w,X_test,f).transpose()

print("*********************************************************************************")
print("RESULTADOS AL EJECUTAR EL DATASET POR PARTES")
print("w:", w)
# The mean squared error

# The coefficient of determination: 1 is perfect prediction
print("Mean squared error: ", mean_squared_error(t_test, t_predicho))
print("Coefficient of determination: ", r2_score(t_test, t_predicho))
print("*********************************************************************************")





