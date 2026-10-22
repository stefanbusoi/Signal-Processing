import numpy as np
import matplotlib.pyplot as plt
import time as t

def sawTooth(freq):
    return lambda t:(np.mod(t,1/freq)*freq-0.5)*2

sawTooth(20)
