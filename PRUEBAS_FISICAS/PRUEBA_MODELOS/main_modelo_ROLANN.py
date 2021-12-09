# -*- coding: utf-8 -*-

"""
La primera l�nea es necesaria para codificar los carateres en UTF-8 ya que
Python-2 emplea la codificaci�n ASCII
"""
"""
Script principal a ejecutar.
"""
"""
Importar las librer�as necesarias
"""


import numpy as np
import random
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM
import time 
import paho.mqtt.client as mqtt #LIBRERÍA MQTT
from OL_reg import nnsimul,  onelayer_reg

import pid_autoajustable as pid_auto


#Setup convertidor ADC
ADC.setup()

# Modelo

def modelo_ROLANN ():
    # Partimos de un modelo ROLANN entrenado
    sp_entrenamiento = '20_40'

    if (sp_entrenamiento == '20_40'):
        #   w = bias, sp_coef, b0_coef, a1_coef 
        w = [[-0.8423474 ],[-0.00484544],[ 1.21016316],[-0.89091075]]
    elif (sp_entrenamiento == '20_80'):
        w = [[-0.83145881],[-0.00251801],[ 0.82324263],[-0.7824353 ]]

    b0 = random.uniform(0.1, 0.35)
    a1 = random.uniform(-0.1, 0.1)
    a0 =  w[0][0] + w[1][0] * sp + w[2][0] * b0 + w[3][0] * a1
    print("b0: ", b0)
    print("a0: ", a0)
    print("a1: ", a1)

    Num_modelo = b0
    Den_modelo = [1, a0, a1]

    return Num_modelo, Den_modelo, w



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
    global on_off, sp, pin_salida_control, frecuencia, Num_modelo, Den_modelo, w, i

    if str(message.topic) == "plant{}/on_off".format(numero_planta):
        on_off=int(str(message.payload.decode("utf-8")))
        print("on_off: ", on_off)
        if (on_off == 0):
            i = 0			
            print("Planta apagada.")
            PWM.start(pin_salida_control, 0, frecuencia)
        
    if str(message.topic) == "plant{}/update_setpoint".format(numero_planta):
        sp = int(str(message.payload.decode("utf-8")))
        Num_modelo, Den_modelo, w = modelo_ROLANN()
        i = 0
        print("Valor de SP: ", sp)

    if str(message.topic) == "plant{}/get_setpoint".format(numero_planta):
        get_param=str(message.payload.decode("utf-8"))
        print("get_param: ", get_param)
        if get_param == " ":
            client.publish("plant{}/setpoint".format(numero_planta), str(sp) + ';' + str(on_off))
    
    
def main():

    global sp, on_off, numero_planta, ip_broker, pin_salida_control, frecuencia
    global Num_modelo, Den_modelo, w
    global i
    numero_planta = 1
    ip_broker = "10.20.30.244"
    pin_entrada_nivel = "P9_40"
    pin_salida_control = "P9_14"
    frecuencia = 200000 # en Hz
    senal_control = 0
    sp = 60
    on_off = 0
    tiempo_anterior = time.time()

    # Inicializamos MQTT
    Inicializacion_MQTT()

    # Ejecutamos el modelo
    Num_modelo, Den_modelo, w = modelo_ROLANN()

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


                numerador, denominador, P, X = pid_auto.RLS(senal_control, salida_sistema, numerador, denominador, P, X, f_olvido=f_olvido) # Ejecutamos RLS

                # despues de 100 iteraciones detectamos anomalias
                a0_modelo =  w[0][0] + w[1][0] * sp + w[2][0] * numerador + w[3][0] * denominador[2]
                diferencia = abs(a0_modelo - denominador[1])
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
                #print("Senal control: ", senal_control)

                #enviamos los datos por mqtt
 
                client.publish("plant{}/data".format(numero_planta), str(sp) + ';' + str(salida_sistema) + ';' + str(senal_control) + ';' + str(Tm) + ';' + str(numerador) + ';' + str(denominador[1]) + ';' + str(denominador[2]))
                 

        except KeyboardInterrupt:

            #PWM.start(pin_salida_control, 0, frecuencia)
            Unsubscribe_and_Disconnect()
            print("Programa finalizado.")
            break

        
    

if __name__ == "__main__":
    main()
