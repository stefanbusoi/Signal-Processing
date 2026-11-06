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

def plotEs(func,freq,min=0,max=1,color='white',plot=plt):
    es=[x/freq*(max-min)+min for x in range(freq)]
    plot.plot(es,[func(t) for t in es],color=color)
def plotEsLog(func,freq,min=0,max=1,color='white',plot=plt):
    es=[x/freq*(max-min)+min for x in range(freq)]
    plot.semilogy(es,[func(t) for t in es],color=color)

def stemEs(func,freq,min=0,max=1,color='white',plot=plt):
    es=[x/freq*(max-min)+min for x in range(freq)]
    plot.stem(es,[func(t) for t in es])

def sin(freq=1,fase=0):
    return lambda t: (np.sin(t*2*np.pi*freq+fase))
def ex1():
    v=[]
    for i in range(8):
        v.append([])
        for j in range(8):
            v[i].append(np.e**(-2*np.pi*1.0j*i*j/8))
    mat=np.array(v)
    matT_mat = mat.conj().T @ mat   
    print(matT_mat)
    fig, axs=plt.subplots(8)

    for i in range(8):
        axs[i].plot(range(8),np.real(v[i]),color="Red")
        axs[i].plot(range(8),np.imag(v[i]),color="blue")
    auto_save_pdf();

    fig, axs=plt.subplots(8)
    
    for i in range(8):
        axs[i].plot(range(8),np.real(matT_mat[i]),color="Red")
        axs[i].plot(range(8),np.imag(matT_mat[i]),color="blue")
    auto_save_pdf();

def ex2():
    fig, axs=plt.subplots(2,2)
    vals=[1/2,1,3,7]
    for i in range(4):
        axs[i//2][i%2].set_xlim(-1.1,1.1)
        axs[i//2][i%2].set_ylim(-1.1,1.1)
        y=[sin(vals[i])(t) for t in np.linspace(0,10,3000)]
        x=np.linspace(0,10,3000)
        ans=[ny*(np.sin(nx*np.pi*2)+np.cos(nx*np.pi*2)*1j)for (nx,ny)in zip(x,y)]
        axs[i//2][i%2].plot(np.real(ans),np.imag(ans))
    auto_save_pdf();

def func(t):
    return sin(freq=1)(t)+sin(freq=3,fase=np.pi/2)(t)/2+sin(freq=6,fase=3)(t)/5
def ex3():
    N=128
    es = np.zeros(N, dtype=complex)
    for i in range(N):
        for n in range(N):
            t=n/N
            es[i]=es[i]+func(t)*np.exp(-2*np.pi*(1.0j)*i*n/N)
    print(es)
    plt.plot(np.abs(es),color="black")

    auto_save_pdf();
ex1()
ex2()
ex3()
