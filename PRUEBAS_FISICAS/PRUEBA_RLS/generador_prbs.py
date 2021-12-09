import numpy as np

def PRBS (N, valor_min, valor_max):

    dic = {
        "2": [0,1],
        "3": [2,1],
        "4": [3,2],
        "5": [4,2],
        "6": [5,4],
        "7": [6,5],
        "8": [7,5,4,3],
        "9": [8,4],
        "10": [9,6],
        "11": [10,8],
        "12": [11,5,3,0],
        "13": [12,3,2,0],
        "14": [13,3,2,0],
        "15": [14,13],
        "16": [15,14,12,3]
    }


    bits = np.ones(N,dtype=np.bool_)
    prbs_signal = []

    if len(dic["{}".format(N)]) == 2:
        
        b1 = dic["{}".format(N)][0]
        b2 = dic["{}".format(N)][1]

    else:

        b1 = dic["{}".format(N)][0]
        b2 = dic["{}".format(N)][1]
        b3 = dic["{}".format(N)][2]
        b4 = dic["{}".format(N)][3]
    
   
    for x in range((2**N) - 1):

        if bits[-1]:
            prbs_signal.append(valor_max)
        else:
            prbs_signal.append(valor_min)

        if N in [8, 12, 13, 14, 16]:
            bits = np.insert(bits[:-1], 0, bits[-1]^bits[-2])
        else:
            bits = np.insert(bits[:-1], 0, bits[-1]^bits[-2])
    
    return list(prbs_signal)





