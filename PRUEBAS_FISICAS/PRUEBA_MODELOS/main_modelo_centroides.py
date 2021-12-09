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
    global on_off, sp, pin_salida_control, frecuencia, Num_modelo, Den_modelo, diccionario_centroides

    if str(message.topic) == "plant{}/on_off".format(numero_planta):
        on_off=int(str(message.payload.decode("utf-8")))
        print("on_off: ", on_off)
        if (on_off == 0):
            print("Planta apagada.")
            PWM.start(pin_salida_control, 0, frecuencia)
        
    if str(message.topic) == "plant{}/update_setpoint".format(numero_planta):
        sp = int(str(message.payload.decode("utf-8")))
        Num_modelo, Den_modelo = modelo_interpolacion(diccionario_centroides,sp)
        print("Valor de SP: ", sp)

    if str(message.topic) == "plant{}/get_setpoint".format(numero_planta):
        get_param=str(message.payload.decode("utf-8"))
        print("get_param: ", get_param)
        if get_param == " ":
            client.publish("plant{}/setpoint".format(numero_planta), str(sp) + ';' + str(on_off))
    
    
def main():

    global sp, on_off, numero_planta, ip_broker, pin_salida_control, frecuencia
    global Num_modelo, Den_modelo
    global diccionario_centroides
    numero_planta = 1
    ip_broker = "10.20.31.19"
    pin_entrada_nivel = "P9_40"
    pin_salida_control = "P9_14"
    frecuencia = 200000 # en Hz
    senal_control = 0
    sp = 50
    on_off = 0
    tiempo_anterior = time.time()

    # Inicializamos MQTT
    Inicializacion_MQTT()

    # Ejecución inicial
    # Creamos todas las variables que se van a utilizar
    P = np.array([])
    X = np.array([])
    Tm = 1 # Tiempo de muestreo en segudos (librería time funciona con seg.) 
    numerador = random.random()
    denominador = [1, random.random(), random.random()]
    
    #valores iniciales de la señal de error y la señal de entrada u
    error = [0, 0] # ya que en el pid intervienen 2 valores anteriores
    u = [0] # ya que interviene el valor anrterior de la señal de entrada u

    #MODELO

    diccionario_centroides = {}
    diccionario_centroides[20] = [-0.7801481260302818, 0.03722973066491977, 0.15888479602049999]
    diccionario_centroides[40] = [-0.7303542921439213, -0.07231343083663493, 0.19946571764034232]
    #diccionario_centroides[55] = [-0.7801762523865541, -0.0503569170966224, 0.21036651049545538]
    #diccionario_centroides[60] = [-0.8960007942231842, 0.03985423776472927, 0.1884299237495106]  
    #diccionario_centroides[80] = [-0.7620268404780519, -0.06922334234856307, 0.26323949545357445]

    #OBTENEMOS EL VALOR DEL MODELO

    Num_modelo, Den_modelo = modelo_interpolacion(diccionario_centroides,sp)

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












