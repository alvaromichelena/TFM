# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 13:59:20 2020

@author: Oscar
"""
import numpy as np
from neuralfun import logsig, ilogsig, dlogsig, relu, irelu, drelu, linear, ilinear, dlinear

#########################################################################################            
# Syntax:
# ------
# w = onelayer_reg(W,x,f)
#
# Parameters of the function:
# --------------------------
# X : inputs of the network (size: m x n).
# d : desired outputs for the given inputs.
# finv : inverse of the activation function. 
# fderiv: derivative of the activation function.
# lam : regularization term (lambda)
#
# Returns:
# -------
# Optimal weights (w) of the network
    
def onelayer_reg(Xp, dp, finv, fderiv, lam, M_k = np.empty([]), U_k = np.empty([]), S_k = np.empty([])):

    # Number of data points (n)
    n = np.size(Xp,1);
    
    # The bias is included as the first input (first row)
    Xp = np.insert(Xp, 0, np.ones(n), axis=0);
    
    # Inverse of the neural function
    d_p = eval(finv)(dp);
    
    # Derivate of the neural function
    f_p = eval(fderiv)(d_p);

    # Diagonal matrix
    F_p = np.diag(f_p);

    if (M_k.shape == () and U_k.shape == () and S_k.shape == ()):
        #print("First time")
        H = np.dot(Xp, F_p); 
        U_kp, S_kp, V = np.linalg.svd(H, full_matrices=False);
        M_kp = np.dot(Xp, np.dot(F_p, np.dot(F_p, d_p)));
    else:
        #print("Second time")
        M_kp = M_k + np.dot(Xp, np.dot(F_p, np.dot(F_p, d_p)));
        H = np.dot(Xp, F_p); 
        U_p, S_p, V = np.linalg.svd(H, full_matrices=False);
        S_p = np.diag(S_p)
        H = np.concatenate((np.dot(U_k, S_k), np.dot(U_p, S_p)), axis=1) 
        U_kp, S_kp, V = np.linalg.svd(H, full_matrices=False);
    
    I = np.eye(np.size(S_kp));
    S_kp = np.diag(S_kp)
    
    # Optimal weights: the order of the matrix and vector multiplications has been done to optimize the speed
    w = np.dot(U_kp, np.dot(np.linalg.pinv(S_kp*S_kp+lam*I), np.dot(U_kp.T, M_kp)));
    return w, M_kp, U_kp, S_kp;

#########################################################################################            
# Syntax:
# ------
# Output = nnsimul(W,x,f)
#
# Parameters of the function:
# --------------------------
# W : weights of the neural network (size: m+1 x 1). The 1st element is the bias.
# X : inputs of the network (matrix of size: m x n).
# f : neural function. 
# 
# Returns:
# -------
# Outputs of the network for all the input data.

def nnsimul(W,X,f):

    # Number of variables (m) and data points (n)
    m,n=X.shape;
    print(m,n)
    print(W.shape)

    # Neural Network Simulation
    return eval(f)(np.dot(W.T, np.insert(X, 0, np.ones(n), axis=0)));
                        
#########################################################################################    