import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns
import numpy as np
import os

# Creamos la carpeta donde se almacenarán las gráficas

carpeta = "ANALISIS DE DATOS/Graficas"

if not os.path.exists(carpeta):
    os.makedirs(carpeta)

# Cargamos el dataset

Path =  "./BBDD/lambda_0_98/pesos_f_olvido_0_98_Planta_3.csv"

Data = pd.read_csv(Path, sep=",")
print("El conjunto de datos cargados contiene un total de {} muestras.".format(Data.shape[0]))


# Comprobación de datos nulos

if Data.isnull().sum().any():
    print("Hay valores nulos en el conjunto de datos.")
else:
    print("No hay valores nulos en el conjunto de datos.")


# Representamos la distribución de las variables 

lista_variables = ["b0", "a0", "a1"]

fig = plt.figure(figsize=plt.figaspect(0.5))
fig.suptitle("Distrbución de los pesos (con anomalías)", fontsize=18, fontweight='bold')
axs = fig.subplots(1, 3)
for i, var in enumerate(lista_variables):
    sns.boxplot(ax=axs[i], x=Data[var], orient="H")
    axs[i].set_title(f"{var} data")

plt.savefig(os.path.join(carpeta, "Distrbución de los pesos (con anomalías).pdf"))

# Eliminación de anomalías

casos_antes = Data.shape[0]
Data = Data[Data.b0 < 2.5]
Data = Data[Data.a0 < 0.4]
Data = Data[Data.a1 < 2]
print(f"Se han eliminado: {casos_antes - Data.shape[0]} anomalías.")


# Representamos la distribución de las variables una vez eliminadas las anomalías

fig = plt.figure(figsize=plt.figaspect(0.5))
fig.suptitle("Distrbución de los pesos (sin anomalías)", fontsize=18, fontweight='bold')
axs = fig.subplots(1, 3)
for i, var in enumerate(lista_variables):
    sns.boxplot(ax=axs[i], x=Data[var], orient="H")
    axs[i].set_title(f"{var} data")

plt.savefig(os.path.join(carpeta, "Distrbución de los pesos (sin anomalías).pdf"))

# Graficamos la nube de puntos en 3D sin fijar la posición

lista_valores_sp = sorted(Data['SP'].unique())
colores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
limites_b0 = [0, 0.8]
limites_a0 = [-1.2, -0.4]
limites_a1 = [-0.4, 0.4]

 
fig = plt.figure(figsize=plt.figaspect(0.5))
ax1 = fig.add_subplot(projection='3d')
for i, sp in enumerate(lista_valores_sp):
    ax1.scatter(Data[Data.SP == sp].a0, Data[Data.SP == sp].a1, Data[Data.SP == sp].b0, c = colores[i], label = "SP {}".format(sp), s=4)
ax1.legend()
ax1.set_title("Dataset obtenido", fontsize=18, fontweight='bold')
ax1.set_xlim(limites_a0)
ax1.set_ylim(limites_a1)
ax1.set_zlim(limites_b0)
ax1.set_xlabel('a0')
ax1.set_ylabel('a1')
ax1.set_zlabel('b0')

plt.savefig(os.path.join(carpeta, "Nube de puntos inicial.pdf"))

# Graficamos las proyecciones de la nube de puntos

fig = plt.figure(figsize=plt.figaspect(0.5))
fig.suptitle("Proyecciones de la nube de puntos", fontsize=18, fontweight='bold')
ax1 = fig.add_subplot(1, 3, 1)
ax1.set_title("Relación b0 - a0")
ax1.set_xlabel("b0")
ax1.set_ylabel("a0")
ax2 = fig.add_subplot(1, 3, 2)
ax2.set_title("Relación b0 - a1")
ax2.set_xlabel("b0")
ax2.set_ylabel("a1")
ax3 = fig.add_subplot(1, 3, 3)
ax3.set_title("Relación a0 - a1")
ax3.set_xlabel("a0")
ax3.set_ylabel("a1")

for n, sp in enumerate(lista_valores_sp):
    ax1.scatter(Data[Data.SP == sp].b0, Data[Data.SP == sp].a0, c = colores[n], label = "SP {}".format(sp), s=4)
    ax2.scatter(Data[Data.SP == sp].b0, Data[Data.SP == sp].a1, c = colores[n], label = "SP {}".format(sp), s=4)
    ax3.scatter(Data[Data.SP == sp].a0, Data[Data.SP == sp].a1, c = colores[n], label = "SP {}".format(sp), s=4)

ax1.legend()
ax2.legend()
ax3.legend()

fig.tight_layout()

plt.savefig(os.path.join(carpeta, "Proyecciones de la nube de puntos.pdf"))

# Graficamos la matriz de correlación

#sns.set(font_scale=2)
X = Data.SP
etiquetas = ['SP']
t = Data.drop(['SP'], axis=1)
etiquetas.extend(list(t.columns.values))
plt.figure(figsize=(10, 10))
plt.suptitle("Matriz de correlación", fontsize=18, fontweight='bold')
corr_mat = np.corrcoef(np.c_[X,t].T)
sns.heatmap(corr_mat, vmin=-1, vmax=1, annot=True, linewidths=1, cmap='BrBG',xticklabels=etiquetas, yticklabels=etiquetas)

plt.savefig(os.path.join(carpeta, "Matriz de correlación.pdf"))


# Graficamos la nube de puntos en 3D fijando la posición

fig = plt.figure(figsize=plt.figaspect(0.5))
ax1 = fig.add_subplot(projection='3d')
for i, sp in enumerate(lista_valores_sp):
    ax1.scatter(Data[Data.SP == sp].a0, Data[Data.SP == sp].a1, Data[Data.SP == sp].b0, c = colores[i], label = "SP {}".format(sp), s=4)
ax1.view_init(elev=0, azim=-45)
ax1.legend()
ax1.set_title("Dataset obtenido", fontsize=18, fontweight='bold')
ax1.set_xlim(limites_a0)
ax1.set_ylim(limites_a1)
ax1.set_zlim(limites_b0)
ax1.set_xlabel('a0')
ax1.set_ylabel('a1')
ax1.set_zlabel('b0')

plt.savefig(os.path.join(carpeta, "Nube de puntos con posición fijada.pdf"))


# Graficamos la nube de puntos en 3D fijando la posición y añadiendo los centroides

# Función del cálculo de centroides
def calculo_centroides (conjunto_datos):
    centroide = []
    for x in range(len(conjunto_datos)):
        centroide.append(conjunto_datos[x].mean())
    return centroide


diccionario_centroides = {}
fig = plt.figure(figsize=plt.figaspect(0.5))
ax1 = fig.add_subplot(projection='3d')
for i, sp in enumerate(lista_valores_sp):
    ax1.scatter(Data[Data.SP == sp].a0, Data[Data.SP == sp].a1, Data[Data.SP == sp].b0, c = colores[i], label = "SP {}".format(sp), s=4, alpha = 0.02)
    centroides = calculo_centroides([Data[Data.SP == sp].a0, Data[Data.SP == sp].a1, Data[Data.SP == sp].b0])
    diccionario_centroides[sp] = centroides
    print("Centroide {} (a0,a1,b0): ".format(sp),centroides[0], centroides[1], centroides[2])
    ax1.scatter(centroides[0], centroides[1], centroides[2],  c = colores[i], label = "Centroide {}".format(sp), s=10, alpha=1)
ax1.view_init(elev=0, azim=-45)
ax1.legend()
ax1.set_title("Centroides calculados" , fontsize=18, fontweight='bold')
ax1.set_xlim(limites_a0)
ax1.set_ylim(limites_a1)
ax1.set_zlim(limites_b0)
ax1.set_xlabel('a0')
ax1.set_ylabel('a1')
ax1.set_zlabel('b0')

plt.savefig(os.path.join(carpeta, "Nube de puntos con posición fijada y centroide.pdf"))

#graficamos los centroides en sus proyecciones en busqueda de obtener una relación de los mismos

fig = plt.figure(figsize=plt.figaspect(0.5))
fig.suptitle("Proyecciones de los centroides", fontsize=18, fontweight='bold')
ax1 = fig.add_subplot(1, 3, 1)
ax1.set_title("Relación SP - b0")
ax1.set_xlabel("b0")
ax1.set_ylabel("SP")
ax2 = fig.add_subplot(1, 3, 2)
ax2.set_title("Relación SP - a0")
ax2.set_xlabel("b0")
ax2.set_ylabel("SP")
ax3 = fig.add_subplot(1, 3, 3)
ax3.set_title("Relación SP - a1")
ax3.set_xlabel("a0")
ax3.set_ylabel("SP")

for n, sp in enumerate(lista_valores_sp):
    ax1.scatter(diccionario_centroides[sp][2], sp, c = colores[n], label = "SP {}".format(sp), s=10)
    ax2.scatter(diccionario_centroides[sp][0], sp, c = colores[n], label = "SP {}".format(sp), s=10)
    ax3.scatter(diccionario_centroides[sp][1], sp, c = colores[n], label = "SP {}".format(sp), s=10)

ax1.legend()
ax2.legend()
ax3.legend()

fig.tight_layout()

plt.savefig(os.path.join(carpeta, "Proyecciones de los centroides.pdf"))

#########################################################################################3
#INTERPOLACION
#########################################################################################3
centroide_20 = [-0.7801481260302818, 0.03722973066491977, 0.15888479602049999]
centroide_40 = [-0.7303542921439213, -0.07231343083663493, 0.19946571764034232]
centroide_80 = [-0.7620268404780519, -0.06922334234856307, 0.2632394954535744]

a0 = centroide_20[0]+((centroide_80[0] - centroide_20[0])/(80-20))*(50-20)
a1 = centroide_20[1]+((centroide_80[1] - centroide_20[1])/(80-20))*(50-20)
b0 = centroide_20[2]+((centroide_80[2] - centroide_20[2])/(80-20))*(50-20)

print("Centroide 50 (a0,a1,b0): ",a0, a1, b0)

a0 = centroide_20[0]+((centroide_40[0] - centroide_20[0])/(40-20))*(60-20)
a1 = centroide_20[1]+((centroide_40[1] - centroide_20[1])/(40-20))*(60-20)
b0 = centroide_20[2]+((centroide_40[2] - centroide_20[2])/(40-20))*(60-20)

print("Centroide 60 (a0,a1,b0): ",a0, a1, b0)

# Graficamos los hiperplanos


diccionario_planos = {}
fig = plt.figure(figsize=plt.figaspect(0.5))
fig.suptitle('Planos descritos por la nube de puntos', fontsize=18, fontweight='bold')
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
lista_valores_sp = sorted(Data['SP'].unique())
for n, sp in enumerate(lista_valores_sp):
    # creacion del modelo de regresion lineal
    modelo_LR = LinearRegression()
    # calcaulamos ese hiperplano
    X = Data[Data.SP == sp][['a0','a1']].values
    t = Data[Data.SP == sp]['b0'].values
    # entrenamos el modelo
    modelo_LR.fit(X,t)
    diccionario_planos[sp] = [modelo_LR.coef_[0], modelo_LR.coef_[1], modelo_LR.intercept_]
    print("Plano {} (coef0,coef1,indep): ".format(sp),diccionario_planos[sp][0], diccionario_planos[sp][1], diccionario_planos[sp][2])
    # graficamos el plano
    # Creamos una malla, sobre la cual graficaremos el plano
    xx, yy = np.meshgrid(np.linspace(-1.2, -0.4, num=10), np.linspace(-0.4, 0.4, num=10))
    # calculamos los valores del plano para los puntos x e y
    nuevoX = (modelo_LR.coef_[0] * xx)
    nuevoY = (modelo_LR.coef_[1] * yy) 
    # calculamos los correspondientes valores para z. Debemos sumar el punto de intercepción
    z = (nuevoX + nuevoY + modelo_LR.intercept_)
    # Graficamos el plano
    ax1.plot_surface(xx, yy, z, alpha=0.3)
    ax2.plot_surface(xx, yy, z, alpha=0.3)
    #graficamos los puntos
    ax1.scatter(Data[Data.SP == sp].a0, Data[Data.SP == sp].a1, Data[Data.SP == sp].b0, c = colores[n], label = "SP {}".format(sp), s=4)
    ax2.scatter(Data[Data.SP == sp].a0, Data[Data.SP == sp].a1, Data[Data.SP == sp].b0, c = colores[n], label = "SP {}".format(sp), s=4)


ax1.set_xlabel('a0')
ax1.set_ylabel('a1')
ax1.set_zlabel('b0')
ax1.set_xlim(limites_a0)
ax1.set_ylim(limites_a1)
ax1.set_zlim(limites_b0)
ax1.legend()
ax1.view_init(elev=0, azim=-45)
ax2.set_xlabel('a0')
ax2.set_ylabel('a1')
ax2.set_zlabel('b0')
ax2.set_xlim(limites_a0)
ax2.set_ylim(limites_a1)
ax2.set_zlim(limites_b0)
ax2.legend()
ax2.view_init(elev=14, azim=-54)

plt.savefig(os.path.join(carpeta, "Nube de puntos con planos.pdf"))

#graficamos las proyecciones de los valores de los planos para tratar de encontarr relaciones

fig = plt.figure(figsize=plt.figaspect(0.5))
fig.suptitle("Proyecciones de los coeficientes de los planos", fontsize=18, fontweight='bold')
ax1 = fig.add_subplot(1, 3, 1)
ax1.set_title("Relación SP - coef0")
ax1.set_xlabel("coef0")
ax1.set_ylabel("SP")
ax2 = fig.add_subplot(1, 3, 2)
ax2.set_title("Relación SP - coef1")
ax2.set_xlabel("coef1")
ax2.set_ylabel("SP")
ax3 = fig.add_subplot(1, 3, 3)
ax3.set_title("Relación SP - indep")
ax3.set_xlabel("indep")
ax3.set_ylabel("SP")

for n, sp in enumerate(lista_valores_sp):
    ax1.scatter(diccionario_planos[sp][0], sp, c = colores[n], label = "SP {}".format(sp), s=10)
    ax2.scatter(diccionario_planos[sp][1], sp, c = colores[n], label = "SP {}".format(sp), s=10)
    ax3.scatter(diccionario_planos[sp][2], sp, c = colores[n], label = "SP {}".format(sp), s=10)

ax1.legend()
ax2.legend()
ax3.legend()

fig.tight_layout()

plt.savefig(os.path.join(carpeta, "Proyecciones de los coeficientes de los planos.pdf"))


# Graficamos anomalías

#cargamos los datos anómalos

Path =  "./BBDD/lambda_0_97/pesos_f_olvido_0_97_Planta_1.csv"

Anomalias = pd.read_csv(Path, sep=",")

# creacion del modelo de regresion lineal
modelo_LR = LinearRegression()
# calcaulamos ese hiperplano
X = Data[Data.SP == 40][['a0','a1']].values
t = Data[Data.SP == 40]['b0'].values
# entrenamos el modelo
modelo_LR.fit(X,t)
#graficamos
fig = plt.figure(figsize=plt.figaspect(0.5))
fig.suptitle('Detección de anomalías', fontsize=18, fontweight='bold')
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
# Creamos una malla, sobre la cual graficaremos el plano
xx, yy = np.meshgrid(np.linspace(-1.2, -0.4, num=10), np.linspace(-0.4, 0.4, num=10))
# calculamos los valores del plano para los puntos x e y
nuevoX = (modelo_LR.coef_[0] * xx)
nuevoY = (modelo_LR.coef_[1] * yy) 
# calculamos los correspondientes valores para z. Debemos sumar el punto de intercepción
z = (nuevoX + nuevoY + modelo_LR.intercept_)
ax1.plot_surface(xx, yy, z, alpha=0.3)
ax1.scatter(Data[Data.SP == 40].a0, Data[Data.SP == 40].a1, Data[Data.SP == 40].b0, c = colores[0], label = "Datos normales", s=4)
ax1.scatter(Anomalias.a0,Anomalias.a1, Anomalias.b0, c = colores[3], label = "Datos anómalos", s=4)
ax2.plot_surface(xx, yy, z, alpha=0.3)
ax2.scatter(Data[Data.SP == 40].a0, Data[Data.SP == 40].a1, Data[Data.SP == 40].b0, c = colores[0], label = "Datos normales", s=4)
ax2.scatter(Anomalias.a0,Anomalias.a1, Anomalias.b0, c = colores[3], label = "Datos anómalos", s=4)
ax1.set_xlabel('a0')
ax1.set_ylabel('a1')
ax1.set_zlabel('b0')
ax1.set_xlim(limites_a0)
ax1.set_ylim(limites_a1)
ax1.set_zlim(limites_b0)
ax1.legend()
ax1.view_init(elev=0, azim=-45)
ax2.set_xlabel('a0')
ax2.set_ylabel('a1')
ax2.set_zlabel('b0')
ax2.set_xlim(limites_a0)
ax2.set_ylim(limites_a1)
ax2.set_zlim(limites_b0)
ax2.legend()
ax2.view_init(elev=11, azim=-57)

plt.savefig(os.path.join(carpeta, "Detección de anomalías.pdf"))

# Grafica nube de puntos de las plantas distintas (3 y 4)

# Cargamos el dataset

Path =  "./BBDD/lambda_0_97/pesos_f_olvido_0_97_Planta_4.csv"

Data_2 = pd.read_csv(Path, sep=",")
lista_valores_sp_planta_3 = lista_valores_sp
lista_valores_sp_planta_4 = sorted(Data_2['SP'].unique())
lista_valores_sp.extend(lista_valores_sp_planta_4)
lista_valores_sp.sort()


fig = plt.figure(figsize=plt.figaspect(0.5))
ax1 = fig.add_subplot(projection='3d')
for i, sp in enumerate(lista_valores_sp):
    if sp in lista_valores_sp_planta_3:
        ax1.scatter(Data[Data.SP == sp].a0, Data[Data.SP == sp].a1, Data[Data.SP == sp].b0, c = colores[i], label = "SP {}, planta 3".format(sp), s=4)
    if sp in lista_valores_sp_planta_4:
        ax1.scatter(Data_2[Data_2.SP == sp].a0, Data_2[Data_2.SP == sp].a1, Data_2[Data_2.SP == sp].b0, c = colores[i], label = "SP {}, planta 4".format(sp), s=4)
ax1.view_init(elev=0, azim=-45)
ax1.legend()
ax1.set_title("Dataset obtenido", fontsize=18, fontweight='bold')
ax1.set_xlim(limites_a0)
ax1.set_ylim(limites_a1)
ax1.set_zlim(limites_b0)
ax1.set_xlabel('a0')
ax1.set_ylabel('a1')
ax1.set_zlabel('b0')

plt.savefig(os.path.join(carpeta, "Nube de puntos planta 3 y 4.pdf"))


# Comparativa resultados para la planta 3 y 4

fig = plt.figure(figsize=plt.figaspect(0.5))
fig.suptitle('Comparativa planta 3 y 4 (SP del 60%)', fontsize=18, fontweight='bold')
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
sp = 60
ax1.scatter(Data[Data.SP == sp].a0, Data[Data.SP == sp].a1, Data[Data.SP == sp].b0, c = colores[0], label = "Planta 3", s=4)
ax1.scatter(Data_2[Data_2.SP == sp].a0, Data_2[Data_2.SP == sp].a1, Data_2[Data_2.SP == sp].b0, c = colores[1], label = "Planta 4", s=4)
ax2.scatter(Data[Data.SP == sp].a0, Data[Data.SP == sp].a1, Data[Data.SP == sp].b0, c = colores[0], label = "Planta 3", s=4)
ax2.scatter(Data_2[Data_2.SP == sp].a0, Data_2[Data_2.SP == sp].a1, Data_2[Data_2.SP == sp].b0, c = colores[1], label = "Planta 4", s=4)
ax1.legend()
ax1.set_xlim(limites_a0)
ax1.set_ylim(limites_a1)
ax1.set_zlim(limites_b0)
ax1.set_xlabel('a0')
ax1.set_ylabel('a1')
ax1.set_zlabel('b0')
ax2.legend()
ax2.view_init(elev=0, azim=-45)
ax2.set_xlim(limites_a0)
ax2.set_ylim(limites_a1)
ax2.set_zlim(limites_b0)
ax2.set_xlabel('a0')
ax2.set_ylabel('a1')
ax2.set_zlabel('b0')

plt.savefig(os.path.join(carpeta, "Comparativa planta 3 y 4.pdf"))

plt.show()

