import numpy as np
import matplotlib.pyplot as plt
import time as t
import scipy.io.wavfile as wavfile
import scipy.signal  as signal
import sounddevice 
import inspect

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

def plotEs(func,freq,min=0,max=1,color='white',plot=plt,opacity=1):
    es=[x/freq*(max-min)+min for x in range(freq)]
    plot.plot(es,[func(t) for t in es],color=color,alpha=opacity)
def plotEsLog(func,freq,min=0,max=1,color='white',plot=plt):
    es=[x/freq*(max-min)+min for x in range(freq)]
    plot.semilogy(es,[func(t) for t in es],color=color)

def stemEs(func,freq,min=0,max=1,color='white',plot=plt):
    es=[x/freq*(max-min)+min for x in range(freq)]
    plot.stem(es,[func(t) for t in es])

def sin(freq=1,fase=0):
    return lambda t: (np.sin(t*2*np.pi*freq+fase))
def f(t):
    return sin(freq=1)(t)+sin(freq=3,fase=np.pi/2)(t)/2+sin(freq=6,fase=3)(t)/5

def DFT(func=f,N=128):
    es = np.zeros(N, dtype=complex)
    vals=[func(t/N) for t in range(N)]
    for i in range(N):
        for n in range(N):
            es[i]=es[i]+vals[n]*np.exp(-2*np.pi*(1.0j)*i*n/N)
    return es

def fftrec(x,n):
    if(n==1):
        return x
    else:
        m=n//2
        miu=np.exp(-2*np.pi*1.0j/n)
        zt=fftrec(x[0::2],m)
        diag=[miu**i for i in range(m)]
        aux=fftrec(x[1::2],m)
        zb=[aux[i]*diag[i]for i in range(m)]
        return [1*zt[i%m]+1*zb[i%m]*(1 if i<n else -1) for i in range(n) ] 

def FFT(func=f,N=128):
    vals=[func(t/N) for t in range(N)]

    return fftrec(vals,N)

def ex1():
    N=[128,256,512,1024]#for the rest i wait a minute 

    times_DFT=[]
    times_FFT=[]
    times_NPFFT=[]
    for i in N:
        start_time = t.perf_counter()
        DFT(N=i)
        elapsed_time = t.perf_counter() - start_time    
        times_DFT.append(elapsed_time)
        start_time = t.perf_counter()
        FFT(N=i)
        elapsed_time = t.perf_counter() - start_time    
        times_FFT.append(elapsed_time)
        start_time = t.perf_counter()
        np.fft.fft([f(n/i)for n in range(i)],i)
        elapsed_time = t.perf_counter() - start_time    
        times_NPFFT.append(elapsed_time)
    plt.plot(times_DFT,color="red",label="DFT")
    plt.plot(times_FFT,color="green",label="FFT")
    plt.plot(times_NPFFT,color="blue",label="NP_FFT")
    plt.legend()
    auto_save_pdf();

def ex2():
    plotEs(sin(freq=4),1000,0,2,color="red",opacity=0.5)
    plotEs(sin(freq=7),1000,0,2,color="blue",opacity=0.5)
    plotEs(sin(freq=10),1000,0,2,color="green",opacity=0.5)
    stemEs(sin(freq=4),6,0,2)
    auto_save_pdf()
def ex3():
    plotEs(sin(freq=4),1000,0,2,color="red",opacity=0.5)
    plotEs(sin(freq=7),1000,0,2,color="blue",opacity=0.5)
    plotEs(sin(freq=10),1000,0,2,color="green",opacity=0.5)
    stemEs(sin(freq=4),9,0,2)
    stemEs(sin(freq=7),9,0,2)
    stemEs(sin(freq=10),9,0,2)
    auto_save_pdf()
#ex4 frecventa minima e de 400 de Hz

def ex6():

    
ex1()
ex2()
ex3()
