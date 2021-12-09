EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Device:R R1
U 1 1 5ECE9EC2
P 6800 3050
F 0 "R1" V 6593 3050 50  0000 C CNN
F 1 "6.8k" V 6684 3050 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 6730 3050 50  0001 C CNN
F 3 "~" H 6800 3050 50  0001 C CNN
	1    6800 3050
	0    1    1    0   
$EndComp
$Comp
L Device:R R2
U 1 1 5ECE9F3D
P 7200 3050
F 0 "R2" V 6993 3050 50  0000 C CNN
F 1 "1.5k" V 7084 3050 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 7130 3050 50  0001 C CNN
F 3 "~" H 7200 3050 50  0001 C CNN
	1    7200 3050
	0    1    1    0   
$EndComp
$Comp
L Device:R R4
U 1 1 5ECE9F73
P 6200 4400
F 0 "R4" V 5993 4400 50  0000 C CNN
F 1 "1.8k" V 6084 4400 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 6130 4400 50  0001 C CNN
F 3 "~" H 6200 4400 50  0001 C CNN
	1    6200 4400
	0    1    1    0   
$EndComp
$Comp
L Device:R R3
U 1 1 5ECE9FD9
P 6200 4100
F 0 "R3" V 5993 4100 50  0000 C CNN
F 1 "2.7k" V 6084 4100 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 6130 4100 50  0001 C CNN
F 3 "~" H 6200 4100 50  0001 C CNN
	1    6200 4100
	0    1    1    0   
$EndComp
$Comp
L Device:R R5
U 1 1 5ECEA01F
P 7050 3700
F 0 "R5" V 6843 3700 50  0000 C CNN
F 1 "5.6k" V 6934 3700 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 6980 3700 50  0001 C CNN
F 3 "~" H 7050 3700 50  0001 C CNN
	1    7050 3700
	0    1    1    0   
$EndComp
Wire Wire Line
	6350 4100 6600 4100
Wire Wire Line
	6900 3700 6600 3700
Connection ~ 6600 4100
Wire Wire Line
	6600 4100 6750 4100
Wire Wire Line
	7200 3700 7500 3700
Wire Wire Line
	7500 4200 7350 4200
$Comp
L Device:C C1
U 1 1 5ECEA282
P 6600 4600
F 0 "C1" H 6715 4646 50  0000 L CNN
F 1 "1uF" H 6715 4555 50  0000 L CNN
F 2 "Capacitor_THT:C_Rect_L7.2mm_W4.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2" H 6638 4450 50  0001 C CNN
F 3 "~" H 6600 4600 50  0001 C CNN
	1    6600 4600
	1    0    0    -1  
$EndComp
Wire Wire Line
	6750 4300 6600 4300
Wire Wire Line
	6600 4300 6600 4400
Wire Wire Line
	6950 3050 7000 3050
Connection ~ 7000 3050
Wire Wire Line
	7000 3050 7050 3050
$Comp
L power:GND #PWR0101
U 1 1 5ECEC756
P 6600 4800
F 0 "#PWR0101" H 6600 4550 50  0001 C CNN
F 1 "GND" H 6605 4627 50  0000 C CNN
F 2 "" H 6600 4800 50  0001 C CNN
F 3 "" H 6600 4800 50  0001 C CNN
	1    6600 4800
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0102
U 1 1 5ECF4FDD
P 9250 3150
F 0 "#PWR0102" H 9250 3000 50  0001 C CNN
F 1 "VCC" H 9267 3323 50  0000 C CNN
F 2 "" H 9250 3150 50  0001 C CNN
F 3 "" H 9250 3150 50  0001 C CNN
	1    9250 3150
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0103
U 1 1 5ECF73E4
P 7200 4000
F 0 "#PWR0103" H 7200 3850 50  0001 C CNN
F 1 "VCC" H 7217 4173 50  0000 C CNN
F 2 "" H 7200 4000 50  0001 C CNN
F 3 "" H 7200 4000 50  0001 C CNN
	1    7200 4000
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0104
U 1 1 5ECF74B5
P 7050 4450
F 0 "#PWR0104" H 7050 4200 50  0001 C CNN
F 1 "GND" H 7055 4277 50  0000 C CNN
F 2 "" H 7050 4450 50  0001 C CNN
F 3 "" H 7050 4450 50  0001 C CNN
	1    7050 4450
	1    0    0    -1  
$EndComp
Wire Wire Line
	6350 4400 6600 4400
Connection ~ 6600 4400
Wire Wire Line
	6600 4400 6600 4450
Text GLabel 6500 3050 0    50   Input ~ 0
AI_sensor
Text GLabel 7600 4200 2    50   Input ~ 0
AO_variador
Wire Wire Line
	7600 4200 7500 4200
Connection ~ 7500 4200
Wire Wire Line
	6600 3700 6600 4100
Wire Wire Line
	7500 3700 7500 4200
Text GLabel 9150 3250 0    50   Input ~ 0
+24V_DC_planta
Text GLabel 9150 3350 0    50   Input ~ 0
GND_planta
$Comp
L power:GND #PWR0105
U 1 1 6185B8AF
P 9250 3450
F 0 "#PWR0105" H 9250 3200 50  0001 C CNN
F 1 "GND" H 9255 3277 50  0000 C CNN
F 2 "" H 9250 3450 50  0001 C CNN
F 3 "" H 9250 3450 50  0001 C CNN
	1    9250 3450
	1    0    0    -1  
$EndComp
Wire Wire Line
	9150 3350 9250 3350
Wire Wire Line
	9250 3350 9250 3450
Wire Wire Line
	9150 3250 9250 3250
Wire Wire Line
	9250 3150 9250 3250
Wire Wire Line
	6500 3050 6650 3050
$Comp
L power:GND #PWR0106
U 1 1 6185CB6F
P 7400 3050
F 0 "#PWR0106" H 7400 2800 50  0001 C CNN
F 1 "GND" H 7405 2877 50  0000 C CNN
F 2 "" H 7400 3050 50  0001 C CNN
F 3 "" H 7400 3050 50  0001 C CNN
	1    7400 3050
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0107
U 1 1 618621A1
P 6000 4100
F 0 "#PWR0107" H 6000 3850 50  0001 C CNN
F 1 "GND" H 6005 3927 50  0000 C CNN
F 2 "" H 6000 4100 50  0001 C CNN
F 3 "" H 6000 4100 50  0001 C CNN
	1    6000 4100
	0    1    1    0   
$EndComp
Wire Wire Line
	6000 4100 6050 4100
Text GLabel 7100 3250 2    50   Input ~ 0
PIN_AIN0_BBB
Wire Wire Line
	7100 3250 7000 3250
Wire Wire Line
	7000 3050 7000 3250
Text GLabel 5950 4400 0    50   Input ~ 0
PIN_PWM0_BBB
Text GLabel 5200 4850 2    50   Input ~ 0
PIN_PWM0_BBB
Text GLabel 4450 4750 0    50   Input ~ 0
PIN_AIN0_BBB
$Comp
L power:GND #PWR0108
U 1 1 61889AAB
P 5150 5050
F 0 "#PWR0108" H 5150 4800 50  0001 C CNN
F 1 "GND" H 5155 4877 50  0000 C CNN
F 2 "" H 5150 5050 50  0001 C CNN
F 3 "" H 5150 5050 50  0001 C CNN
	1    5150 5050
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J1
U 1 1 6188FA18
P 9250 4000
F 0 "J1" H 9330 4042 50  0000 L CNN
F 1 "Conn_01x01" H 9330 3951 50  0000 L CNN
F 2 "Connector:Banana_Jack_1Pin" H 9250 4000 50  0001 C CNN
F 3 "~" H 9250 4000 50  0001 C CNN
	1    9250 4000
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J2
U 1 1 6188FCBD
P 9250 4150
F 0 "J2" H 9330 4192 50  0000 L CNN
F 1 "Conn_01x01" H 9330 4101 50  0000 L CNN
F 2 "Connector:Banana_Jack_1Pin" H 9250 4150 50  0001 C CNN
F 3 "~" H 9250 4150 50  0001 C CNN
	1    9250 4150
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J3
U 1 1 618902AA
P 9250 4300
F 0 "J3" H 9330 4342 50  0000 L CNN
F 1 "Conn_01x01" H 9330 4251 50  0000 L CNN
F 2 "Connector:Banana_Jack_1Pin" H 9250 4300 50  0001 C CNN
F 3 "~" H 9250 4300 50  0001 C CNN
	1    9250 4300
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J4
U 1 1 6189058C
P 9250 4450
F 0 "J4" H 9330 4492 50  0000 L CNN
F 1 "Conn_01x01" H 9330 4401 50  0000 L CNN
F 2 "Connector:Banana_Jack_1Pin" H 9250 4450 50  0001 C CNN
F 3 "~" H 9250 4450 50  0001 C CNN
	1    9250 4450
	1    0    0    -1  
$EndComp
Text GLabel 8900 4450 0    50   Input ~ 0
AO_variador
Text GLabel 8900 4300 0    50   Input ~ 0
AI_sensor
Text GLabel 8900 4000 0    50   Input ~ 0
+24V_DC_planta
Text GLabel 8900 4150 0    50   Input ~ 0
GND_planta
Wire Wire Line
	8900 4000 9050 4000
Wire Wire Line
	9050 4150 8900 4150
Wire Wire Line
	8900 4300 9050 4300
Wire Wire Line
	9050 4450 8900 4450
Wire Wire Line
	6050 4400 5950 4400
Wire Wire Line
	7400 3050 7350 3050
Wire Wire Line
	7050 4400 7050 4450
$Comp
L PLACA-ACONDICIONAMINETO-rescue:LM358-modificacion-ACONDICIONAMINETO-DAQ-rescue U1
U 1 1 5ECF89F9
P 7050 4200
F 0 "U1" H 7300 4100 50  0000 L CNN
F 1 "LM358" H 7250 4000 50  0000 L CNN
F 2 "Package_DIP:DIP-8_W7.62mm_Socket_LongPads" H 7050 4200 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/lm2904-n.pdf" H 7050 4200 50  0001 C CNN
	1    7050 4200
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_02x23_Odd_Even J0
U 1 1 618A10FD
P 4750 3950
F 0 "J0" H 4800 5267 50  0000 C CNN
F 1 "Header_BBB" H 4800 5176 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x23_P2.54mm_Vertical" H 4750 3950 50  0001 C CNN
F 3 "~" H 4750 3950 50  0001 C CNN
	1    4750 3950
	1    0    0    -1  
$EndComp
Wire Wire Line
	4450 4750 4550 4750
Wire Wire Line
	5050 5050 5150 5050
Wire Wire Line
	6600 4800 6600 4750
Wire Wire Line
	7050 4000 7200 4000
Wire Wire Line
	5050 4850 5200 4850
$EndSCHEMATC
