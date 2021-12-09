import pandas as pd


#Cargamos fichero

Data = pd.read_csv("./BBDD/lambda_1/pesos_f_olvido_1.csv", sep=",")

#hacemos un split

lista_id = sorted(Data['ID_planta'].unique())
print(lista_id)



for x in lista_id:
    #almacenamos los valores de cada planta en un dataframe
    #cada uno de estos dataframes se almacenan en un diccionario
    Data[Data.ID_planta == x][['SP', 'b0', 'a0', 'a1']].to_csv('./BBDD/lambda_1/pesos_f_olvido_1_Planta_{}.csv'.format(x),sep=',',index=False)










