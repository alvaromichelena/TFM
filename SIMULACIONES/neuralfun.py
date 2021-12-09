# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 19:14:26 2020

@author: Oscar
"""
from numpy import log, exp, ones

# Logsig activation function -----------------------------------------

def logsig(x):

    return 1 / (1 + exp(-x));

def ilogsig(x):
    
    return -log((1/x)-1);

def dlogsig(x):

    return 1/((1+exp(-x))**2)*exp(-x);

# ReLu activation function -----------------------------------------

def relu(x):
    
    return log(1+exp(x));

def irelu(x):  # El x debe tener valores > 0 porque es el rango de salida de la función ReLu

    return log(exp(x)-1);

def drelu(x):
    
    return 1 / (1 + exp(-x)); # It is the logistic function

# Linear activation function -----------------------------------------

def linear(x):
    
    return x;

def ilinear(x):

    return x; # the inverse of a linear function is the same function

def dlinear(x):
    
    return ones(len(x)); 
