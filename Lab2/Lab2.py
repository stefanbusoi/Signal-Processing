import numpy as np
import matplotlib.pyplot as plt
import time as t
import scipy.io.wavfile as wavfile
import scipy.signal  as signal
import sounddevice 
import inspect

def sin(freq=1,fase=0):
    return lambda t: (np.sin(t*2*np.pi*freq+fase))
def cos(freq=1,fase=0):
    return lambda t: (np.cos(t*2*np.pi*freq+fase))
def sawTooth(freq):
    return lambda t:(np.mod(t,1/freq)*freq-0.5)*2

_counters = {}
def auto_save_pdf(close=True):
    #Function generated with gemini, it creates a pdf autoindexed whth the name from what function is called
    caller = inspect.stack()[1].function
    _counters[caller] = _counters.get(caller, 0) + 1
    
    filename = f"{caller}_{_counters[caller]}.pdf"
    plt.savefig(filename, format='pdf', bbox_inches='tight')
    print(f"Salvat automat: {filename}")
    
    if close:
        plt.close()

def square(freq):
    return lambda t:np.sign(np.sin(np.pi*2*freq*t))

def plotEs(func,freq,min=0,max=1,color='white',plot=plt):
    es=[x/freq*(max-min)+min for x in range(freq)]
    plot.plot(es,[func(t) for t in es],color=color)
def plotEsLog(func,freq,min=0,max=1,color='white',plot=plt):
    es=[x/freq*(max-min)+min for x in range(freq)]
    plot.semilogy(es,[func(t) for t in es],color=color)

def stemEs(func,freq,min=0,max=1,color='white',plot=plt):
    es=[x/freq*(max-min)+min for x in range(freq)]
    plot.stem(es,[func(t) for t in es])


def ex1():
    plotEs(sin(freq=10),freq=1000,min=0,max=1,color='red')
    plotEs(cos(freq=10,fase=np.pi/2*3),freq=1000,min=0,max=1,color='blue')
    auto_save_pdf()

def ex2():
    plotEs(sin(freq=10,fase=np.pi/2),freq=1000,min=0,max=1,color='red')
    plotEs(sin(freq=10,fase=0),freq=1000,min=0,max=1,color='green')
    plotEs(sin(freq=10,fase=np.pi),freq=1000,min=0,max=1,color='blue')
    auto_save_pdf()
   
    for SNR in [0.1,1,10,100]:
        
        z=np.random.normal(1000)
        x=[sin(freq=10,fase=np.pi/2*3)(t) for t in np.linspace(0,1,1000)]
        k=np.sqrt(np.linalg.norm(x)*np.linalg.norm(x)/(SNR*np.linalg.norm(z)*np.linalg.norm(z)))

        sinWithNoise=lambda t:sin(freq=10,fase=np.pi/2*3)(t)+np.random.normal()*k
        plotEs(sinWithNoise,freq=1000,min=0,max=1,color='black')
        plotEs(sin(freq=10,fase=np.pi/2*3),freq=1000,min=0,max=1,color='red')

        auto_save_pdf()
def ex3():
    plotEs(sin(freq=400),1600,0,0.01,color='red')
    plotEs(sin(freq=800),1000,0,0.01,color='blue')
    plotEs(sawTooth(freq=240),1000,0,0.01,color='green')
    plotEs(square(freq=300),1000,0,0.01,color='black')
    rate = 44100
    wavfile.write('l1ex2a.wav', rate,np.array([sin(freq=400)(t) for t in np.linspace(0,1,rate)]))
    wavfile.write('l1ex2b.wav', rate,np.array([sin(freq=800)(t) for t in np.linspace(0,1,rate)]))
    wavfile.write('l1ex2c.wav', rate,np.array([sawTooth(freq=240)(t) for t in np.linspace(0,1,rate)]))
    wavfile.write('l1ex2d.wav', rate,np.array([square(freq=300)(t) for t in np.linspace(0,1,rate)]))
    rate, x= wavfile.read('l1ex2d.wav')
    sounddevice.play(x,rate)

    auto_save_pdf()

def ex4():
    fig, axs=plt.subplots(3)
    plotEs(sin(freq=200),1000,0,0.01,color='red',plot=axs[0])
    plotEs(sawTooth(freq=200),1000,0,0.01,color='red',plot=axs[1])
    plotEs(lambda t:sin(freq=200)(t)+sawTooth(freq=200)(t),1000,0,0.01,color='red',plot=axs[2])
    plt.tight_layout()
    auto_save_pdf()

def ex5():
    rate = 44100
    vec1=np.array([sin(freq=400)(t) for t in np.linspace(0,1,rate)])
    vec2=np.array([sin(freq=800)(t) for t in np.linspace(1,2,rate)])
    wavfile.write('l1ex2a.wav', rate,np.concatenate((vec1,vec2),axis=None))
    rate, x= wavfile.read('l1ex2a.wav')
    sounddevice.play(x,rate)
    input()#for waiting

def ex6():
    fs=10
    fig, axs=plt.subplots(3)

    plotEs(sin(fs/2),1000,0,1,color='red',plot=axs[0])
    plotEs(sin(fs/4),1000,0,1,color='green',plot=axs[1])
    plotEs(sin(0),1000,0,1,color='blue',plot=axs[2])
    stemEs(sin(fs/2),fs,0,1,plot=axs[0])
    stemEs(sin(fs/4),fs,0,1,plot=axs[1])
    stemEs(sin(0),fs,0,1,plot=axs[2])
    plt.tight_layout()
    auto_save_pdf()

def ex7():
    fig, axs=plt.subplots(3)
    sgnl=sin(freq=200)
    es=[sgnl(t)for t in np.linspace(0,0.01,10)]
    dec=[x for t,x in zip(range(10),es) if t%4==0]
    plotEs(sgnl,1000,0,0.01,color='red',plot=axs[0])
    plotEs(sgnl,1000,0,0.01,color='red',plot=axs[1])
    plotEs(sgnl,1000,0,0.01,color='red',plot=axs[2])
    axs[0].stem([x for x in np.linspace(0,0.01,10)],es)

    axs[1].stem([x for t,x in zip(range(10),np.linspace(0,0.01,10))if t%4==0],dec)
    dec=[x for t,x in zip(range(10),es) if t%4==1]
    axs[2].stem([x for t,x in zip(range(10),np.linspace(0,0.01,10))if t%4==1],dec)

    plt.tight_layout()
    auto_save_pdf()

def ex8():
    lin=lambda t:t
    plotEs(lin,1000,-np.pi/2,np.pi/2,color='red')
    plotEs(sin(1/(2*np.pi)),1000,-np.pi/2,np.pi/2,color='black')
    auto_save_pdf()
    err=lambda t: abs(lin(t)-sin(1/(2*np.pi))(t))
    plotEsLog(err,1000,-np.pi/2,np.pi/2,color='red')
    auto_save_pdf()

    paleSin=lambda t:(t-7*(t**3)/60)/(1+(t**2)/20)
    paleSinErr=lambda t:abs(paleSin(t)-sin(1/(2*np.pi))(t))
    plotEsLog(paleSinErr,1000,-np.pi/2,np.pi/2,color='red')
    auto_save_pdf()

ex1()
ex2()
ex3()
ex4()
ex5()
ex6()
ex7()
ex8()