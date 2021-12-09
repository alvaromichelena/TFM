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
import random
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM
import time 
import paho.mqtt.client as mqtt #LIBRERÍA MQTT

import pid_autoajustable as pid_auto


#Setup convertidor ADC
ADC.setup()

#funcion del modelo
def modelo_interpolacion(bbdd_centroides, bbdd_planos, SP):

    valores_sp_bbdd = sorted(list(bbdd_centroides.keys()))

    if SP in valores_sp_bbdd:
        Numerador = bbdd_centroides[SP][2]
        Denominador = [1, bbdd_centroides[SP][0], bbdd_centroides[SP][1]]
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
        #valor_proximo= min(valores_sp_bbdd, key=lambda x:abs(x-SP))
        valor_proximo = 40
        print(valor_proximo)
        centroide = bbdd_centroides[valor_proximo]
        plano_mayor = bbdd_planos[valor_mayor]
        plano_menor = bbdd_planos[valor_menor]
        #interpolacion_lineal
        # Calculo del centroide
        #a0 = centroide_menor[0]+((centroide_mayor[0] - centroide_menor[0])/(valor_mayor-valor_menor))*(SP-valor_menor)
        #a1 = centroide_menor[1]+((centroide_mayor[1] - centroide_menor[1])/(valor_mayor-valor_menor))*(SP-valor_menor)
        a0 = centroide[0]
        a1 = centroide[1]
        # calculo del plano interpolado
        coef_1 = plano_menor[0]+((plano_mayor[0] - plano_menor[0])/(valor_mayor-valor_menor))*(SP-valor_menor)
        coef_2 = plano_menor[1]+((plano_mayor[1] - plano_menor[1])/(valor_mayor-valor_menor))*(SP-valor_menor)
        indep = plano_menor[2]+((plano_mayor[2] - plano_menor[2])/(valor_mayor-valor_menor))*(SP-valor_menor)
        #obtenemos el valor de b0 
        b0 = a0 * coef_1 + a1 * coef_2 + indep
        Numerador = b0
        Denominador = [1, a0, a1]

        

    return Numerador, Denominador, coef_1, coef_2, indep


################################################################
# Conexion al broker y suscripcion a los topics de la planta #
################################################################
def Inicializacion_MQTT():
    global client, numero_planta, sp, on_off, ip_broker
    client = mqtt.Client("Planta_{}".format(numero_planta))
    client.on_message = on_message
    client.connect(ip_broker) 
    print("Conectado")
    time.sleep(0.5)
    # Suscripcion a los topics de la planta 
    client.subscribe("plant{}/on_off".format(numero_planta))
    client.subscribe("plant{}/update_setpoint".format(numero_planta))
    client.subscribe("plant{}/get_setpoint".format(numero_planta))
    time.sleep(0.1)
    client.publish("plant{}/setpoint".format(numero_planta), str(sp) + ';' + str(on_off))

    print("plant{}/on_off".format(numero_planta))
    print("plant{}/update_setpoint".format(numero_planta))
    print("plant{}/get_setpoint".format(numero_planta))
    
    client.loop_start() #start loop to process received messages

################################################
# Funcion a ejecutar antes de cerrar el script #
################################################
def Unsubscribe_and_Disconnect():
    client.unsubscribe("plant{}/on_off".format(numero_planta))
    client.unsubscribe("plant{}/update_sepoint".format(numero_planta))
    client.unsubscribe("plant{}/get_setpoint".format(numero_planta))
    client.disconnect()
    print("Desuscripcion de los topics y desconexion exitosas")

############################################
# Funcion para recepcion de los datos MQTT #
############################################
def on_message(client, userdata, message):
    global on_off, sp, pin_salida_control, frecuencia, Num_modelo, Den_modelo, diccionario_centroides, diccionario_planos
    global coef_1, coef_2, indep
    if str(message.topic) == "plant{}/on_off".format(numero_planta):
        on_off=int(str(message.payload.decode("utf-8")))
        print("on_off: ", on_off)
        if (on_off == 0):
            print("Planta apagada.")
            PWM.start(pin_salida_control, 0, frecuencia)
        
    if str(message.topic) == "plant{}/update_setpoint".format(numero_planta):
        sp = int(str(message.payload.decode("utf-8")))
        Num_modelo, Den_modelo, coef_1, coef_2, indep = modelo_interpolacion(diccionario_centroides, diccionario_planos, sp)
        print("Valor de SP: ", sp)

    if str(message.topic) == "plant{}/get_setpoint".format(numero_planta):
        get_param=str(message.payload.decode("utf-8"))
        print("get_param: ", get_param)
        if get_param == " ":
            client.publish("plant{}/setpoint".format(numero_planta), str(sp) + ';' + str(on_off))
    
    
def main():

    global sp, on_off, numero_planta, ip_broker, pin_salida_control, frecuencia
    global Num_modelo, Den_modelo
    global diccionario_centroides, diccionario_planos
    global coef_1, coef_2, indep
    numero_planta = 1
    ip_broker = "10.20.24.148"
    pin_entrada_nivel = "P9_40"
    pin_salida_control = "P9_14"
    frecuencia = 200000 # en Hz
    senal_control = 0
    sp = 50
    on_off = 0
    tiempo_anterior = time.time()

    # Inicializamos MQTT
    Inicializacion_MQTT()

    #MODELO

    diccionario_centroides = {}
    diccionario_centroides[20] = [-0.7801481260302818, 0.03722973066491977, 0.15888479602049999]
    diccionario_centroides[40] = [-0.7303542921439213, -0.07231343083663493, 0.19946571764034232]
    #diccionario_centroides[55] = [-0.7801762523865541, -0.0503569170966224, 0.21036651049545538]
    #diccionario_centroides[60] = [-0.8960007942231842, 0.03985423776472927, 0.1884299237495106]  
    #diccionario_centroides[80] = [-0.7620268404780519, -0.06922334234856307, 0.26323949545357445]
    diccionario_planos = {}
    diccionario_planos[20] = [0.615749493821694, 0.6163726825781344, 0.6163132207679911]
    diccionario_planos[40] = [1.0091668706980124, 1.010228528376166, 1.0095681639600107]
    #diccionario_planos[55] = [1.2362096415395685, 1.2357885693137538, 1.2370584183298075]
    #diccionario_planos[60] = [1.309573803167701, 1.3110621162370386, 1.3095577101768066]
    #diccionario_planos[80] = [1.5615997836967874, 1.561491020156731, 1.561312072177763]

    #OBTENEMOS EL VALOR DEL MODELO

    Num_modelo, Den_modelo, coef_1, coef_2, indep = modelo_interpolacion(diccionario_centroides, diccionario_planos, sp)

    # Ejecución inicial
    # Creamos todas las variables que se van a utilizar
    P = np.array([])
    X = np.array([])
    Tm = 1 # Tiempo de muestreo en segudos (librería time funciona con seg.) 
    
    numerador = Num_modelo
    denominador = Den_modelo
    
    #valores iniciales de la señal de error y la señal de entrada u
    error = [0, 0] # ya que en el pid intervienen 2 valores anteriores
    u = [0] # ya que interviene el valor anrterior de la señal de entrada u

    #contador de ciclos
    i=0

    #factor de olvido
    f_olvido=0.95
    #valores necesarios para el detector de anomalias
    numerador_ant = numerador
    denominador_ant = denominador
    P_ant = P
    X_ant =X

    # Ejecución del PID autoajustable

    while True:

        try:

            if (on_off == 1 and time.time() - tiempo_anterior >= Tm): 

                # Tomamos registro de tiempo en el inicio de la ejecución
                tiempo_anterior = time.time()

                # leemos nivel y lo convertimos a porcentaje

                salida_sistema = ADC.read(pin_entrada_nivel) * 100 # para pasarlo a porcentaje
                print("Salida sistema: ", salida_sistema)

                #calculamos el error

                error.append(sp-salida_sistema)

                # Ejecutamos algoritmo de identificacaión

                numerador, denominador, P, X = pid_auto.RLS(senal_control, salida_sistema, numerador, denominador, P, X) # Ejecutamos RLS

            
                

                # despues de 100 iteraciones detectamos anomalias
                b0_modelo =  coef_1 * denominador[1] + coef_2 * denominador[2] + indep
                diferencia = abs(b0_modelo - denominador[1])
                print("diferencia: ", diferencia)
                if i<100:
                    i=i+1
                else:
                    if diferencia > 0.15:
                        print("*****ANOMALIA DETECTADA******")
                        numerador = numerador_ant
                        denominador = denominador_ant
                        P = P_ant
                        X = X_ant

                    else:
                        print("****FUNCIONAMIENTO NORMAL****")
                        numerador_ant = numerador
                        denominador_ant = denominador
                        P_ant = P
                        X_ant =X

                # Obtenemos la señal de control del PID
                
                senal_control = pid_auto.PID_dahlin(Num_modelo, Den_modelo, error, u, Tm, B=1)
                u.append(senal_control)

                # Enviamos la señal de salida por el pin correspondiente


                PWM.start(pin_salida_control, senal_control, frecuencia)
                print("Senal control: ", senal_control)

                #enviamos los datos por mqtt
 
                client.publish("plant{}/data".format(numero_planta), str(sp) + ';' + str(salida_sistema) + ';' + str(senal_control) + ';' + str(Tm) + ';' + str(numerador) + ';' + str(denominador[1]) + ';' + str(denominador[2]))
                 

        except KeyboardInterrupt:

            #PWM.start(pin_salida_control, 0, frecuencia)
            Unsubscribe_and_Disconnect()
            print("Programa finalizado.")
            break

        
    

if __name__ == "__main__":
    main()












