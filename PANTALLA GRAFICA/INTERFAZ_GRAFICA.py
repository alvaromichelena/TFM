###########################################################################
#LIBRERIAS IMPORTADAS

import sys
import plotdata_pesos_ft
import plotdata_variables
import time
import paho.mqtt.client as mqtt #LIBRERÍA MQTT

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

###########################################################################
#FUNCIÓN INICIALIZACIÓN MQTT

def inicializacion_mqtt():
    global client, ip_broker
    client = mqtt.Client("GUI")
    client.on_message = on_message
    client.connect(ip_broker) 
    print("cliente conectado")
    time.sleep(0.5)
    client.subscribe("plant{}/setpoint".format(planta_sel))
    print("subscribe","plant{}/setpoint".format(planta_sel))
    client.subscribe("plant{}/data".format(planta_sel))
    print("subscribe","plant{}/data".format(planta_sel))
    client.loop_start() #start loop to process received messages
    client.publish("plant{}/get_setpoint".format(planta_sel), " ")
    print("publish","plant{}/get_setpoint".format(planta_sel))

###########################################################################
#FUNCIONES DE CIERRE DE VENTANAS

def destroy_window():
    global root
    client.publish("plant{}/on_off".format(planta_sel),"0")
    time.sleep(0.5)#retardo para desubscribirse
    client.unsubscribe("plant{}/data".format(planta_sel))
    client.unsubscribe("plant{}/setpoint".format(planta_sel))
    client.disconnect
    root.quit()
    root=None

###########################################################################
#FUNCION INICIAL GUI

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global t1, ip_broker, planta_sel, planta_sel_ant
    global flag1, data
    global val, root, top
    ip_broker = "10.20.24.148"
    flag1=False
    t1=0
    planta_sel = 1
    planta_sel_ant =1
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", destroy_window)
    top = GUI (root)
    inicializacion_mqtt()
    root.mainloop()

###########################################################################
#FUNCIONES ASOCIADAS A BOTONES

def FUNCTION_BUTTON_ON_OFF():
    print('FUNCTION_BUTTON_ON_OFF')
    global flag1, t1
    flag1=not(flag1)
    if flag1==False:
        top.ButtonON_OFF.configure(text='''ON''')
        client.publish("plant{}/on_off".format(planta_sel),"0")
    else:
        top.ButtonON_OFF.configure(text='''OFF''')
        top.newgraph1.clear()
        top.newgraph2.clear()
        t1=0
        client.publish("plant{}/on_off".format(planta_sel),"1")
    sys.stdout.flush()


def FUNCTION_UPDATE_PARAMETERS():
    print('FUNCTION_UPDATE_PARAMETERS')
    sys.stdout.flush()
    print(str(top.EntrySP.get()))
    client.publish("plant{}/update_setpoint".format(planta_sel), str(top.EntrySP.get()))
    

def FUNCTION_SEL_PLANTA(p1):
    print('FUNCTION_SEL_PLANTA')
    global top, planta_sel, planta_sel_ant, t1
    sys.stdout.flush() 
    planta_sel= top.Sel_planta.current() + 1
    if planta_sel != planta_sel_ant:
        print('Se ha seleccionado la planta {}'.format(planta_sel))
        print("unsubscribe","plant{}/setpoint".format(planta_sel_ant))
        print("unsubscribe","plant{}/data".format(planta_sel_ant))
        client.unsubscribe("plant{}/setpoint".format(planta_sel_ant))
        client.unsubscribe("plant{}/data".format(planta_sel_ant))
        t1=0
        top.newgraph1.clear()
        top.newgraph2.clear()
        top.Label_ft.configure(text="                       -1\n              b0*z\nG(z) = _______________________\n                        -1         -2\n          1 + a0*z  + a1*z")
        print("subscribe","plant{}/setpoint".format(planta_sel))
        print("subscribe","plant{}/data".format(planta_sel))
        client.subscribe("plant{}/setpoint".format(planta_sel))
        client.subscribe("plant{}/data".format(planta_sel))
        client.publish("plant{}/get_setpoint".format(planta_sel), " ")
        planta_sel_ant=planta_sel

        
def FUNCTION_CHECK_SP():
        print("FUNCTION_CHECK_SP_1")
        top.newgraph1.hide_show_line([top.check_SP.get(), top.check_PV.get(), top.check_ERR.get(), top.check_CP.get()])


def FUNCTION_CHECK_PV():
        print("FUNCTION_CHECK_PV_1")
        top.newgraph1.hide_show_line([top.check_SP.get(), top.check_PV.get(), top.check_ERR.get(), top.check_CP.get()])


def FUNCTION_CHECK_CP():
        print("FUNCTION_CHECK_CP_1")
        top.newgraph1.hide_show_line([top.check_SP.get(), top.check_PV.get(), top.check_ERR.get(), top.check_CP.get()])


def FUNCTION_CHECK_ERR():
        print("FUNCTION_CHECK_ERR_1")
        top.newgraph1.hide_show_line([top.check_SP.get(), top.check_PV.get(), top.check_ERR.get(), top.check_CP.get()])


def FUNCTION_CHECK_B0():
        print("FUNCTION_CHECK_B0")
        top.newgraph2.hide_show_line([top.check_B0.get(), top.check_A0.get(), top.check_A1.get(), 0])

def FUNCTION_CHECK_A0():
        print("FUNCTION_CHECK_A0")
        top.newgraph2.hide_show_line([top.check_B0.get(), top.check_A0.get(), top.check_A1.get(), 0])

def FUNCTION_CHECK_A1():
        print("FUNCTION_CHECK_A1")
        top.newgraph2.hide_show_line([top.check_B0.get(), top.check_A0.get(), top.check_A1.get(), 0])




###########################################################################
#FUNCION DE RELLENADO DE DATOS EN LAS GRAFICAS

def rellenar_grafica():
    global t1  
    top.newgraph1.addPoint([[t1, data[0]],[t1, data[1]],[t1,abs(data[1]-data[0])],[t1,data[2]]])
    top.newgraph2.addPoint([[t1, data[4]],[t1, data[5]],[t1,data[6]], [t1, 0]])
    t1= t1 + data[3]     
    if data[5] < 0 and data[6] < 0:
        top.Label_ft.configure(text=f"                         -1\n              {data[4]:.2f}*z\nG(z) = _______________________\n                           -1           -2\n          1 - {abs(data[5]):.2f}*z  - {abs(data[6]):.2f}*z")
    elif data[5] < 0:
        top.Label_ft.configure(text=f"                         -1\n              {data[4]:.2f}*z\nG(z) = _______________________\n                           -1           -2\n          1 - {abs(data[5]):.2f}*z  + {abs(data[6]):.2f}*z")
    elif data[6] < 0:
        top.Label_ft.configure(text=f"                         -1\n              {data[4]:.2f}*z\nG(z) = _______________________\n                           -1           -2\n          1 + {abs(data[5]):.2f}*z  - {abs(data[6]):.2f}*z")
    else:         
        top.Label_ft.configure(text=f"                         -1\n              {data[4]:.2f}*z\nG(z) = _______________________\n                           -1           -2\n          1 + {data[5]:.2f}*z  + {data[6]:.2f}*z")



###########################################################################
#FUNCION DE RECEPCIÓN DE DATOS

def on_message(client, userdata, message):
   global data, parameters_1, flag1
   if str(message.topic) == "plant{}/data".format(planta_sel):
        data=list(map(float,str(message.payload.decode("utf-8")).split(";")))
        print("Data", data)
        rellenar_grafica()
   if str(message.topic) == "plant{}/setpoint".format(planta_sel):
        print("entra")
        parameters=list(map(int,str(message.payload.decode("utf-8")).split(";")))
        print(parameters)
        top.EntrySP.delete(0, 'end')
        top.EntrySP.insert(0, str(parameters[0]))
        if parameters[1] == 1:
                top.ButtonON_OFF.configure(text='''OFF''')
                flag1=True
        else:
                top.ButtonON_OFF.configure(text='''ON''')
                flag1=False

###########################################################################
#CREACIÓN DE LA CLASE DE LA GUI

class GUI:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''


        #VARIABLES ASOCIADAS A LA CLASE
        self.check_SP = tk.IntVar()
        self.check_SP.set(1)
        self.check_PV = tk.IntVar()
        self.check_PV.set(1)
        self.check_ERR = tk.IntVar()
        self.check_ERR.set(1)
        self.check_CP = tk.IntVar()
        self.check_CP.set(1)
        self.check_B0 = tk.IntVar()
        self.check_B0.set(1)
        self.check_A0 = tk.IntVar()
        self.check_A0.set(1)
        self.check_A1 = tk.IntVar()
        self.check_A1.set(1)
    


        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("1130x667+200+0")
        top.minsize(120, 1)
        top.maxsize(1370, 749)
        top.resizable(1,  1)
        top.title("GUI")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.Frame1 = tk.Frame(top)
        self.Frame1.place(relx=0.009, rely=0.075, relheight=0.625
                , relwidth=0.487)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")
        self.newgraph1 = plotdata_variables.plotdata_variables(self.Frame1)

        self.Label_visualizacion_var = tk.Label(top)
        self.Label_visualizacion_var.place(relx=0.062, rely=0.015, height=32
                , width=432)
        self.Label_visualizacion_var.configure(activebackground="#f9f9f9")
        self.Label_visualizacion_var.configure(activeforeground="black")
        self.Label_visualizacion_var.configure(background="#c0c0c0")
        self.Label_visualizacion_var.configure(borderwidth="9")
        self.Label_visualizacion_var.configure(compound='center')
        self.Label_visualizacion_var.configure(disabledforeground="#a3a3a3")
        self.Label_visualizacion_var.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.Label_visualizacion_var.configure(foreground="#000000")
        self.Label_visualizacion_var.configure(highlightbackground="#d9d9d9")
        self.Label_visualizacion_var.configure(highlightcolor="black")
        self.Label_visualizacion_var.configure(text='''VISUALIZACIÓN DE LAS VARIABLES DEL PROCESO''')


        self.Label_aux5 = tk.Label(top)
        self.Label_aux5.place(relx=0.394, rely=0.78, height=107, width=240)
        self.Label_aux5.configure(activebackground="#f9f9f9")
        self.Label_aux5.configure(activeforeground="black")
        self.Label_aux5.configure(background="#939393")
        self.Label_aux5.configure(disabledforeground="#a3a3a3")
        self.Label_aux5.configure(foreground="#000000")
        self.Label_aux5.configure(highlightbackground="#d9d9d9")
        self.Label_aux5.configure(highlightcolor="black")

        self.Label_sel_planta = tk.Label(top)
        self.Label_sel_planta.place(relx=0.414, rely=0.795, height=32, width=195)
        self.Label_sel_planta.configure(activebackground="#f9f9f9")
        self.Label_sel_planta.configure(activeforeground="black")
        self.Label_sel_planta.configure(background="#d9d9d9")
        self.Label_sel_planta.configure(disabledforeground="#a3a3a3")
        self.Label_sel_planta.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.Label_sel_planta.configure(foreground="#000000")
        self.Label_sel_planta.configure(highlightbackground="#d9d9d9")
        self.Label_sel_planta.configure(highlightcolor="black")
        self.Label_sel_planta.configure(text='''Selección de la planta''')

        self.Sel_planta = ttk.Combobox(top)
        self.Sel_planta.place(relx=0.434, rely=0.87, relheight=0.037
                , relwidth=0.136)
        self.value_list = ['Planta 1','Planta 2','Planta 3','Planta 4','Planta 5']
        self.Sel_planta.configure(values=self.value_list)
        self.Sel_planta.current(0)
        self.Sel_planta.configure(font="-family {Segoe UI} -size 13 -weight bold")
        self.Sel_planta.configure(takefocus="")
        self.Sel_planta.bind('<<ComboboxSelected>>',lambda e:FUNCTION_SEL_PLANTA(e))

        self.Label_aux4 = tk.Label(top)
        self.Label_aux4.place(relx=0.23, rely=0.78, height=127, width=160)
        self.Label_aux4.configure(activebackground="#f9f9f9")
        self.Label_aux4.configure(activeforeground="black")
        self.Label_aux4.configure(background="#939393")
        self.Label_aux4.configure(disabledforeground="#a3a3a3")
        self.Label_aux4.configure(foreground="#000000")
        self.Label_aux4.configure(highlightbackground="#d9d9d9")
        self.Label_aux4.configure(highlightcolor="black")

        self.ButtonON_OFF = tk.Button(top)
        self.ButtonON_OFF.place(relx=0.257, rely=0.87, height=44, width=97)
        self.ButtonON_OFF.configure(activebackground="#ececec")
        self.ButtonON_OFF.configure(activeforeground="#000000")
        self.ButtonON_OFF.configure(background="#d9d9d9")
        self.ButtonON_OFF.configure(command=FUNCTION_BUTTON_ON_OFF)
        self.ButtonON_OFF.configure(disabledforeground="#a3a3a3")
        self.ButtonON_OFF.configure(font="-family {Segoe UI} -size 9 -weight bold")
        self.ButtonON_OFF.configure(foreground="#000000")
        self.ButtonON_OFF.configure(highlightbackground="#d9d9d9")
        self.ButtonON_OFF.configure(highlightcolor="black")
        self.ButtonON_OFF.configure(pady="0")
        self.ButtonON_OFF.configure(text='''ON/OFF''')

        self.Label_marcha_paro = tk.Label(top)
        self.Label_marcha_paro.place(relx=0.239, rely=0.795, height=32
                , width=137)
        self.Label_marcha_paro.configure(activebackground="#f9f9f9")
        self.Label_marcha_paro.configure(activeforeground="black")
        self.Label_marcha_paro.configure(background="#d9d9d9")
        self.Label_marcha_paro.configure(disabledforeground="#a3a3a3")
        self.Label_marcha_paro.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.Label_marcha_paro.configure(foreground="#000000")
        self.Label_marcha_paro.configure(highlightbackground="#d9d9d9")
        self.Label_marcha_paro.configure(highlightcolor="black")
        self.Label_marcha_paro.configure(text='''Control on/off''')

        self.Label_aux3 = tk.Label(top)
        self.Label_aux3.place(relx=0.018, rely=0.78, height=127, width=213)
        self.Label_aux3.configure(activebackground="#f9f9f9")
        self.Label_aux3.configure(activeforeground="black")
        self.Label_aux3.configure(background="#939393")
        self.Label_aux3.configure(disabledforeground="#a3a3a3")
        self.Label_aux3.configure(foreground="#000000")
        self.Label_aux3.configure(highlightbackground="#d9d9d9")
        self.Label_aux3.configure(highlightcolor="black")

        self.Label_set_point = tk.Label(top)
        self.Label_set_point.place(relx=0.035, rely=0.795, height=32, width=170)
        self.Label_set_point.configure(activebackground="#f9f9f9")
        self.Label_set_point.configure(activeforeground="black")
        self.Label_set_point.configure(background="#d9d9d9")
        self.Label_set_point.configure(disabledforeground="#a3a3a3")
        self.Label_set_point.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.Label_set_point.configure(foreground="#000000")
        self.Label_set_point.configure(highlightbackground="#d9d9d9")
        self.Label_set_point.configure(highlightcolor="black")
        self.Label_set_point.configure(text='''Selección setpoint''')

        self.ButtonActualizar = tk.Button(top)
        self.ButtonActualizar.place(relx=0.063, rely=0.916, height=24, width=107)

        self.ButtonActualizar.configure(activebackground="#ececec")
        self.ButtonActualizar.configure(activeforeground="#000000")
        self.ButtonActualizar.configure(background="#d9d9d9")
        self.ButtonActualizar.configure(command=FUNCTION_UPDATE_PARAMETERS)
        self.ButtonActualizar.configure(disabledforeground="#a3a3a3")
        self.ButtonActualizar.configure(font="-family {Segoe UI} -size 9 -weight bold")
        self.ButtonActualizar.configure(foreground="#000000")
        self.ButtonActualizar.configure(highlightbackground="#d9d9d9")
        self.ButtonActualizar.configure(highlightcolor="black")
        self.ButtonActualizar.configure(pady="0")
        self.ButtonActualizar.configure(text='''ACTUALIZAR''')

        self.Label_sp = tk.Label(top)
        self.Label_sp.place(relx=0.044, rely=0.855, height=32, width=83)
        self.Label_sp.configure(activebackground="#f9f9f9")
        self.Label_sp.configure(activeforeground="black")
        self.Label_sp.configure(background="#939393")
        self.Label_sp.configure(disabledforeground="#a3a3a3")
        self.Label_sp.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.Label_sp.configure(foreground="#000000")
        self.Label_sp.configure(highlightbackground="#d9d9d9")
        self.Label_sp.configure(highlightcolor="black")
        self.Label_sp.configure(text='''Set Point''')

        self.EntrySP = tk.Entry(top)
        self.EntrySP.place(relx=0.124, rely=0.864, height=20, relwidth=0.048)
        self.EntrySP.configure(background="white")
        self.EntrySP.configure(disabledforeground="#a3a3a3")
        self.EntrySP.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.EntrySP.configure(foreground="#000000")
        self.EntrySP.configure(highlightbackground="#d9d9d9")
        self.EntrySP.configure(highlightcolor="black")
        self.EntrySP.configure(insertbackground="black")
        self.EntrySP.configure(selectbackground="blue")
        self.EntrySP.configure(selectforeground="white")
        self.EntrySP.configure(justify="center")


        self.Frame2 = tk.Frame(top)
        self.Frame2.place(relx=0.504, rely=0.075, relheight=0.625
                , relwidth=0.487)
        self.Frame2.configure(relief='groove')
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief="groove")
        self.Frame2.configure(background="#d9d9d9")
        self.Frame2.configure(highlightbackground="#d9d9d9")
        self.Frame2.configure(highlightcolor="black")
        self.newgraph2 = plotdata_pesos_ft.plotdata_pesos_ft(self.Frame2)

        self.Label_aux1 = tk.Label(top)
        self.Label_aux1.place(relx=0.018, rely=0.705, height=37, width=530)
        self.Label_aux1.configure(activebackground="#f9f9f9")
        self.Label_aux1.configure(activeforeground="black")
        self.Label_aux1.configure(background="#939393")
        self.Label_aux1.configure(disabledforeground="#a3a3a3")
        self.Label_aux1.configure(foreground="#000000")
        self.Label_aux1.configure(highlightbackground="#d9d9d9")
        self.Label_aux1.configure(highlightcolor="black")

        self.Label_aux2 = tk.Label(top)
        self.Label_aux2.place(relx=0.513, rely=0.705, height=37, width=530)
        self.Label_aux2.configure(activebackground="#f9f9f9")
        self.Label_aux2.configure(activeforeground="black")
        self.Label_aux2.configure(background="#939393")
        self.Label_aux2.configure(disabledforeground="#a3a3a3")
        self.Label_aux2.configure(foreground="#000000")
        self.Label_aux2.configure(highlightbackground="#d9d9d9")
        self.Label_aux2.configure(highlightcolor="black")

        self.Text1 = tk.Text(top)
        self.Text1.place(relx=0.035, rely=0.727, relheight=0.009, relwidth=0.027)

        self.Text1.configure(background="#000000")
        self.Text1.configure(font="TkTextFont")
        self.Text1.configure(foreground="black")
        self.Text1.configure(highlightbackground="#d9d9d9")
        self.Text1.configure(highlightcolor="black")
        self.Text1.configure(insertbackground="black")
        self.Text1.configure(relief="flat")
        self.Text1.configure(selectbackground="blue")
        self.Text1.configure(selectforeground="white")
        self.Text1.configure(wrap="word")

        self.Text1_1 = tk.Text(top)
        self.Text1_1.place(relx=0.152, rely=0.727, relheight=0.009
                , relwidth=0.027)
        self.Text1_1.configure(background="#0000ff")
        self.Text1_1.configure(font="TkTextFont")
        self.Text1_1.configure(foreground="black")
        self.Text1_1.configure(highlightbackground="#d9d9d9")
        self.Text1_1.configure(highlightcolor="black")
        self.Text1_1.configure(insertbackground="black")
        self.Text1_1.configure(relief="flat")
        self.Text1_1.configure(selectbackground="blue")
        self.Text1_1.configure(selectforeground="white")
        self.Text1_1.configure(wrap="word")

        self.Text1_3 = tk.Text(top)
        self.Text1_3.place(relx=0.278, rely=0.727, relheight=0.009
                , relwidth=0.027)
        self.Text1_3.configure(background="#008000")
        self.Text1_3.configure(font="TkTextFont")
        self.Text1_3.configure(foreground="black")
        self.Text1_3.configure(highlightbackground="#d9d9d9")
        self.Text1_3.configure(highlightcolor="black")
        self.Text1_3.configure(insertbackground="black")
        self.Text1_3.configure(relief="flat")
        self.Text1_3.configure(selectbackground="blue")
        self.Text1_3.configure(selectforeground="white")
        self.Text1_3.configure(wrap="word")

        self.Text1_2 = tk.Text(top)
        self.Text1_2.place(relx=0.395, rely=0.727, relheight=0.009
                , relwidth=0.027)
        self.Text1_2.configure(background="#ff0000")
        self.Text1_2.configure(font="TkTextFont")
        self.Text1_2.configure(foreground="black")
        self.Text1_2.configure(highlightbackground="#d9d9d9")
        self.Text1_2.configure(highlightcolor="black")
        self.Text1_2.configure(insertbackground="black")
        self.Text1_2.configure(relief="flat")
        self.Text1_2.configure(selectbackground="blue")
        self.Text1_2.configure(selectforeground="white")
        self.Text1_2.configure(wrap="word")

        self.CheckbuttonSP = tk.Checkbutton(top)
        self.CheckbuttonSP.place(relx=0.062, rely=0.712, relheight=0.04
                , relwidth=0.042)
        self.CheckbuttonSP.configure(activebackground="#ececec")
        self.CheckbuttonSP.configure(activeforeground="#000000")
        self.CheckbuttonSP.configure(background="#939393")
        self.CheckbuttonSP.configure(disabledforeground="#a3a3a3")
        self.CheckbuttonSP.configure(font="-family {Segoe UI} -size 9 -weight bold")
        self.CheckbuttonSP.configure(foreground="#000000")
        self.CheckbuttonSP.configure(highlightbackground="#d9d9d9")
        self.CheckbuttonSP.configure(highlightcolor="black")
        self.CheckbuttonSP.configure(justify='left')
        self.CheckbuttonSP.configure(text='''SP''')
        self.CheckbuttonSP.configure(variable=self.check_SP)
        self.CheckbuttonSP.configure(command=FUNCTION_CHECK_SP)

        self.CheckbuttonPV = tk.Checkbutton(top)
        self.CheckbuttonPV.place(relx=0.181, rely=0.72, relheight=0.025
                , relwidth=0.042)
        self.CheckbuttonPV.configure(activebackground="#ececec")
        self.CheckbuttonPV.configure(activeforeground="#000000")
        self.CheckbuttonPV.configure(background="#939393")
        self.CheckbuttonPV.configure(disabledforeground="#a3a3a3")
        self.CheckbuttonPV.configure(font="-family {Segoe UI} -size 9 -weight bold")
        self.CheckbuttonPV.configure(foreground="#000000")
        self.CheckbuttonPV.configure(highlightbackground="#d9d9d9")
        self.CheckbuttonPV.configure(highlightcolor="black")
        self.CheckbuttonPV.configure(justify='left')
        self.CheckbuttonPV.configure(text='''PV''')
        self.CheckbuttonPV.configure(variable=self.check_PV)
        self.CheckbuttonPV.configure(command=FUNCTION_CHECK_PV)

        self.CheckbuttonERR = tk.Checkbutton(top)
        self.CheckbuttonERR.place(relx=0.425, rely=0.72, relheight=0.025
                , relwidth=0.044)
        self.CheckbuttonERR.configure(activebackground="#ececec")
        self.CheckbuttonERR.configure(activeforeground="#000000")
        self.CheckbuttonERR.configure(background="#939393")
        self.CheckbuttonERR.configure(disabledforeground="#a3a3a3")
        self.CheckbuttonERR.configure(font="-family {Segoe UI} -size 9 -weight bold")
        self.CheckbuttonERR.configure(foreground="#000000")
        self.CheckbuttonERR.configure(highlightbackground="#d9d9d9")
        self.CheckbuttonERR.configure(highlightcolor="black")
        self.CheckbuttonERR.configure(justify='left')
        self.CheckbuttonERR.configure(text='''ERR''')
        self.CheckbuttonERR.configure(variable=self.check_ERR)
        self.CheckbuttonERR.configure(command=FUNCTION_CHECK_ERR)

        self.CheckbuttonCP = tk.Checkbutton(top)
        self.CheckbuttonCP.place(relx=0.31, rely=0.718, relheight=0.028
                , relwidth=0.035)
        self.CheckbuttonCP.configure(activebackground="#ececec")
        self.CheckbuttonCP.configure(activeforeground="#000000")
        self.CheckbuttonCP.configure(background="#939393")
        self.CheckbuttonCP.configure(disabledforeground="#a3a3a3")
        self.CheckbuttonCP.configure(font="-family {Segoe UI} -size 9 -weight bold")
        self.CheckbuttonCP.configure(foreground="#000000")
        self.CheckbuttonCP.configure(highlightbackground="#d9d9d9")
        self.CheckbuttonCP.configure(highlightcolor="black")
        self.CheckbuttonCP.configure(justify='left')
        self.CheckbuttonCP.configure(text='''CP''')
        self.CheckbuttonCP.configure(variable=self.check_CP)
        self.CheckbuttonCP.configure(command=FUNCTION_CHECK_CP)

        self.Label_visualizacion_pesos = tk.Label(top)
        self.Label_visualizacion_pesos.place(relx=0.541, rely=0.015, height=32
                , width=461)
        self.Label_visualizacion_pesos.configure(activebackground="#f9f9f9")
        self.Label_visualizacion_pesos.configure(activeforeground="black")
        self.Label_visualizacion_pesos.configure(background="#c0c0c0")
        self.Label_visualizacion_pesos.configure(borderwidth="9")
        self.Label_visualizacion_pesos.configure(compound='center')
        self.Label_visualizacion_pesos.configure(disabledforeground="#a3a3a3")
        self.Label_visualizacion_pesos.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.Label_visualizacion_pesos.configure(foreground="#000000")
        self.Label_visualizacion_pesos.configure(highlightbackground="#d9d9d9")
        self.Label_visualizacion_pesos.configure(highlightcolor="black")
        self.Label_visualizacion_pesos.configure(text='''VISUALIZACIÓN DE LOS PARÁMETROS DE IDENTIFICACIÓN''')

        self.Checkbuttonb0 = tk.Checkbutton(top)
        self.Checkbuttonb0.place(relx=0.602, rely=0.712, relheight=0.04
                , relwidth=0.042)
        self.Checkbuttonb0.configure(activebackground="#ececec")
        self.Checkbuttonb0.configure(activeforeground="#000000")
        self.Checkbuttonb0.configure(background="#939393")
        self.Checkbuttonb0.configure(disabledforeground="#a3a3a3")
        self.Checkbuttonb0.configure(font="-family {Segoe UI} -size 9 -weight bold")
        self.Checkbuttonb0.configure(foreground="#000000")
        self.Checkbuttonb0.configure(highlightbackground="#d9d9d9")
        self.Checkbuttonb0.configure(highlightcolor="black")
        self.Checkbuttonb0.configure(justify='left')
        self.Checkbuttonb0.configure(text='''b0''')
        self.Checkbuttonb0.configure(variable=self.check_B0)
        self.Checkbuttonb0.configure(command=FUNCTION_CHECK_B0)

        self.Text1_4 = tk.Text(top)
        self.Text1_4.place(relx=0.575, rely=0.727, relheight=0.009
                , relwidth=0.027)
        self.Text1_4.configure(background="#008000")
        self.Text1_4.configure(font="TkTextFont")
        self.Text1_4.configure(foreground="black")
        self.Text1_4.configure(highlightbackground="#d9d9d9")
        self.Text1_4.configure(highlightcolor="black")
        self.Text1_4.configure(insertbackground="black")
        self.Text1_4.configure(relief="flat")
        self.Text1_4.configure(selectbackground="blue")
        self.Text1_4.configure(selectforeground="white")
        self.Text1_4.configure(wrap="word")

        self.Text1_1_1 = tk.Text(top)
        self.Text1_1_1.place(relx=0.732, rely=0.727, relheight=0.009
                , relwidth=0.027)
        self.Text1_1_1.configure(background="#0000ff")
        self.Text1_1_1.configure(font="TkTextFont")
        self.Text1_1_1.configure(foreground="black")
        self.Text1_1_1.configure(highlightbackground="#d9d9d9")
        self.Text1_1_1.configure(highlightcolor="black")
        self.Text1_1_1.configure(insertbackground="black")
        self.Text1_1_1.configure(relief="flat")
        self.Text1_1_1.configure(selectbackground="blue")
        self.Text1_1_1.configure(selectforeground="white")
        self.Text1_1_1.configure(wrap="word")

        self.Text1_2_1 = tk.Text(top)
        self.Text1_2_1.place(relx=0.867, rely=0.727, relheight=0.009
                , relwidth=0.027)
        self.Text1_2_1.configure(background="#ff0000")
        self.Text1_2_1.configure(cursor="fleur")
        self.Text1_2_1.configure(font="TkTextFont")
        self.Text1_2_1.configure(foreground="black")
        self.Text1_2_1.configure(highlightbackground="#d9d9d9")
        self.Text1_2_1.configure(highlightcolor="black")
        self.Text1_2_1.configure(insertbackground="black")
        self.Text1_2_1.configure(relief="flat")
        self.Text1_2_1.configure(selectbackground="blue")
        self.Text1_2_1.configure(selectforeground="white")
        self.Text1_2_1.configure(wrap="word")

        self.Checkbuttona0 = tk.Checkbutton(top)
        self.Checkbuttona0.place(relx=0.759, rely=0.712, relheight=0.04
                , relwidth=0.042)
        self.Checkbuttona0.configure(activebackground="#ececec")
        self.Checkbuttona0.configure(activeforeground="#000000")
        self.Checkbuttona0.configure(background="#939393")
        self.Checkbuttona0.configure(disabledforeground="#a3a3a3")
        self.Checkbuttona0.configure(font="-family {Segoe UI} -size 9 -weight bold")
        self.Checkbuttona0.configure(foreground="#000000")
        self.Checkbuttona0.configure(highlightbackground="#d9d9d9")
        self.Checkbuttona0.configure(highlightcolor="black")
        self.Checkbuttona0.configure(justify='left')
        self.Checkbuttona0.configure(text='''a0''')
        self.Checkbuttona0.configure(variable=self.check_A0)
        self.Checkbuttona0.configure(command=FUNCTION_CHECK_A0)

        self.Checkbuttona1 = tk.Checkbutton(top)
        self.Checkbuttona1.place(relx=0.894, rely=0.712, relheight=0.04
                , relwidth=0.042)
        self.Checkbuttona1.configure(activebackground="#ececec")
        self.Checkbuttona1.configure(activeforeground="#000000")
        self.Checkbuttona1.configure(background="#939393")
        self.Checkbuttona1.configure(disabledforeground="#a3a3a3")
        self.Checkbuttona1.configure(font="-family {Segoe UI} -size 9 -weight bold")
        self.Checkbuttona1.configure(foreground="#000000")
        self.Checkbuttona1.configure(highlightbackground="#d9d9d9")
        self.Checkbuttona1.configure(highlightcolor="black")
        self.Checkbuttona1.configure(justify='left')
        self.Checkbuttona1.configure(text='''a1''')
        self.Checkbuttona1.configure(variable=self.check_A1)
        self.Checkbuttona1.configure(command=FUNCTION_CHECK_A1)

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.Label_aux6 = tk.Label(top)
        self.Label_aux6.place(relx=0.655, rely=0.78, height=137, width=332)
        self.Label_aux6.configure(activebackground="#f9f9f9")
        self.Label_aux6.configure(activeforeground="black")
        self.Label_aux6.configure(background="#939393")
        self.Label_aux6.configure(disabledforeground="#a3a3a3")
        self.Label_aux6.configure(foreground="#000000")
        self.Label_aux6.configure(highlightbackground="#d9d9d9")
        self.Label_aux6.configure(highlightcolor="black")

        self.Label_vis_ft = tk.Label(top)
        self.Label_vis_ft.place(relx=0.708, rely=0.795, height=22, width=216)
        self.Label_vis_ft.configure(activebackground="#f9f9f9")
        self.Label_vis_ft.configure(activeforeground="black")
        self.Label_vis_ft.configure(background="#d9d9d9")
        self.Label_vis_ft.configure(disabledforeground="#a3a3a3")
        self.Label_vis_ft.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.Label_vis_ft.configure(foreground="#000000")
        self.Label_vis_ft.configure(highlightbackground="#d9d9d9")
        self.Label_vis_ft.configure(highlightcolor="black")
        self.Label_vis_ft.configure(text='''Función de transferencia''')

        self.Label_ft = tk.Label(top)
        self.Label_ft.place(relx=0.673, rely=0.837, height=93, width=294)
        self.Label_ft.configure(activebackground="#f9f9f9")
        self.Label_ft.configure(activeforeground="black")
        self.Label_ft.configure(background="#ffffff")
        self.Label_ft.configure(disabledforeground="#a3a3a3")
        self.Label_ft.configure(foreground="#000000")
        self.Label_ft.configure(highlightbackground="#d9d9d9")
        self.Label_ft.configure(highlightcolor="black")
        self.Label_ft.configure(relief="ridge")
        self.Label_ft.configure(font="-family {Segoe UI} -size 9 -weight bold")
        self.Label_ft.configure(state='active')
        self.Label_ft.configure(text="                       -1\n              b0*z\nG(z) = _______________________\n                        -1         -2\n          1 + a0*z  + a1*z")

if __name__ == '__main__':
    vp_start_gui()





