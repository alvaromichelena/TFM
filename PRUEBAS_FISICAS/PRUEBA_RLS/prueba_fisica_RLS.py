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
import generador_prbs as prbs


#Setup convertidor ADC
ADC.setup()


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
    global on_off, sp, sp_aux, pin_salida_control, frecuencia, numerador, denominador, flag_fin_ident, prbs_sp, flag_prbs, P, X

    if str(message.topic) == "plant{}/on_off".format(numero_planta):
        on_off=int(str(message.payload.decode("utf-8")))
        print("on_off: ", on_off)
        if (on_off == 0):
            print("Planta apagada.")
            PWM.start(pin_salida_control, 0, frecuencia)
            flag_prbs = False
            flag_fin_ident = False
        else:
            print("Planta encendida.")
            if sp not in prbs_sp:
                flag_prbs = False
                flag_fin_ident = False
            else:
                flag_prbs = True
                flag_fin_ident = True
        
    if str(message.topic) == "plant{}/update_setpoint".format(numero_planta):
        sp_aux = int(str(message.payload.decode("utf-8")))
        if sp != sp_aux:

            sp=sp_aux
            
            if sp not in prbs_sp:
                print("REINICIO SISTEMA")
                flag_prbs = False
                flag_fin_ident = False

            #se reinicializan el valor de num, den, X y P ya que se inicializa una nueva identificacion
            numerador = random.random()
            denominador = [1, random.random(), random.random()]
            P = np.array([])
            X = np.array([])
        print("Valor de SP: ", sp)

    if str(message.topic) == "plant{}/get_setpoint".format(numero_planta):
        get_param=str(message.payload.decode("utf-8"))
        print("get_param: ", get_param)
        if get_param == " ":
            client.publish("plant{}/setpoint".format(numero_planta), str(sp) + ';' + str(on_off))
    
    
def main():

    global sp, sp_aux, on_off, numero_planta, ip_broker, pin_salida_control, frecuencia, numerador, denominador, flag_fin_ident
    global prbs_sp, flag_prbs, P, X
    flag_fin_ident = False
    numero_planta = 1
    ip_broker = "10.20.30.244"
    pin_entrada_nivel = "P9_40"
    pin_salida_control = "P9_14"
    frecuencia = 200000 # en Hz
    senal_control = 0
    sp = 50
    sp_aux = 50
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
    error_abs = [100, 100] #alamacena los valores absolutos (valores iniciales altos para aumentar la media del error al inicio de la ejecucion)
    u = [0] # ya que interviene el valor anrterior de la señal de entrada u

    #otras variables de proceso
    flag_prbs = False
    i = 0
    N = 7
    prbs_sp = [0]
    salida_sistema_ant = 0 
    contador = 0

    # Ejecución del PID autoajustable

    while True:

        try:

            if (on_off == 1 and time.time() - tiempo_anterior >= Tm): 

                # Tomamos registro de tiempo en el inicio de la ejecución
                tiempo_anterior = time.time()

                #contador + 1

                contador=contador+1

                # leemos nivel (porcentaje)

                salida_sistema = ADC.read(pin_entrada_nivel) * 100 # para pasarlo a porcentaje
                
                # Aplicamos un pequeño filtro para evitar los errores en la medida

                if abs(salida_sistema - salida_sistema_ant) >= 15:
                    salida_sistema = salida_sistema_ant

                salida_sistema_ant = salida_sistema

                print("Salida sistema: ", salida_sistema)

                # comprobamos que no se produzca un error de lectura


                # calculamos el error

                e = sp-salida_sistema
                error.append(e)
                error_abs.append(abs(e))

                # Ejecutamos algoritmo de identificacaión

                numerador, denominador, P, X = pid_auto.RLS(senal_control, salida_sistema, numerador, denominador, P, X) # Ejecutamos RLS
                
            
                senal_control = e
                
                # adicción de la señal PRBS
                print("Media error: ", np.mean(error_abs))
                if (contador>40) and (flag_prbs == False) and (sp not in prbs_sp):

                    flag_prbs = True
                    senal_prbs = prbs.PRBS(N, -5, 5)
                    print("INICIO PRBS")

                if flag_prbs:

                    print("PRBS", i)
                    
                    senal_control = senal_control + senal_prbs[i]

                    if senal_control > 100:
                        senal_control = 100
                    elif senal_control < 0:
                        senal_control = 0

                    i = i + 1

                    if i == len(senal_prbs):
                        i = 0
                        flag_prbs = False
                        flag_fin_ident = True
                        prbs_sp.append(sp)
                        print("FINAL PRBS")
                

                u.append(senal_control)

                # Enviamos la señal de salida por el pin correspondiente

                PWM.start(pin_salida_control, senal_control, frecuencia)
                print("Senal control: ", senal_control)

                # Limitamos la ventana de datos del error y de u

                error = error[-5:]
                error_abs = error_abs[-5:]
                u = u[-2:]

                #enviamos los datos por uart
 
                client.publish("plant{}/data".format(numero_planta), str(sp) + ';' + str(salida_sistema) + ';' + str(senal_control) + ';' + str(Tm) + ';' + str(numerador) + ';' + str(denominador[1]) + ';' + str(denominador[2]))
                
                if flag_fin_ident:
                    print("FLAG_FIN_IDENT: ", flag_fin_ident)
                    client.publish("plant/tf", str(numero_planta) + ';' + str(sp) + ';' + str(numerador) + ';' + str(denominador[1]) + ';' + str(denominador[2]))


        except KeyboardInterrupt:

            #PWM.start(pin_salida_control, 0, frecuencia)
            Unsubscribe_and_Disconnect()
            print("Programa finalizado.")
            break

        
    

if __name__ == "__main__":
    main()












