import numpy as np
import matplotlib.pyplot as plt
import time as t
import scipy.io.wavfile as wavfile
import scipy.signal  as signal
import sounddevice as sounddev
index=0
def save():
    global index
    plt.savefig(f"save_{str(index)}.pdf") 
    index+=1

def x(t):
    return np.cos(520*np.pi*t+np.pi/3)
def y(t):
    return np.cos(280*np.pi*t-np.pi/3)
def z(t):
    return np.cos(120*np.pi*t+np.pi/3)

def plotEs(func,freq,min=0,max=1,color='white'):
    es=[x/freq*(max-min)+min for x in range(freq)]
    plt.plot(es,[func(t) for t in es],color=color)

def stemEs(func,freq,min=0,max=1,color='white'):
    es=[x/freq*(max-min)+min for x in range(freq)]
    plt.stem(es,[func(t) for t in es])


def ex1():
    plotEs(x,1000,0,0.2,color='red')
    stemEs(x,40,0,0.2,color='red') #0.005
    save()
    plt.show()
    plotEs(y,1000,0,0.2,color='green')
    stemEs(y,40,0,0.2,color='green')
    save()
    plt.show()
    stemEs(z,40,0,0.2,color='blue')
    plotEs(z,1000,0,0.2,color='blue')
    save()
    plt.show()

def sin400(t):
    return np.sin(np.pi*2*400*t)

def sin800(t):
    return np.sin(np.pi*2*800*t)


def sawTooth(t,freq):
    return (np.mod(t,1/freq)*freq-0.5)*2


def square(t,freq):
    return np.sign(np.sin(np.pi*2*freq*t))
def ex2():
    stemEs(sin400,16,0,0.01,color='red')
    plotEs(sin400,1600,0,0.01,color='red')
    save()
    plt.show()
    plotEs(sin800,1000,0,0.01,color='red')
    save()
    plt.show()
    plotEs(lambda t:sawTooth(t,freq=240),1000,0,0.01,color='red')
    save()
    plt.show()
    plotEs(lambda t:square(t,freq=300),1000,0,0.01,color='red')
    save()
    plt.show()
    randMat=np.random.rand(128,128)
    plt.imshow(randMat)
    save()
    plt.show()
    mat0=np.zeros((128, 128))
    plt.imshow(mat0)
    save()
    plt.show()
ex1()
ex2()

#ex3
#a) 1/2000=0.0005 secunde 
#b) 4 biti * 2000 de esantioane * 3600 de secunde = 
#  8000*3600
# 28,800,000 biti
# 3,600,000 bytes = aprox 3.6 MB