from pylab import *
import numpy as np
from scipy import *
import scipy.io.wavfile
from scipy import signal
import matplotlib.pyplot as plt
import glob
import matplotlib.colors

fig = plt.figure(figsize=(15, 15), dpi=80)


def sprawdzacz(signalData,w):
    low=120
    high=6000
    signalData=np.array(signalData)
    if (len(signalData.shape) > 1):
        signalData = [s[0] for s in signalData]

    signal = []
    if w*3<len(signalData):
        for i in range(int(w*1), w*3):
            signal.append(signalData[i])
    else:
        signal=signalData
        #for i in range(w*1, len(signalData)):
        #    signal.append(signalData[i])
    signalfft = fft(signal)
    signalfft = abs(signalfft)

    signal = []
    freqs = range(0, int(len(signalfft)/2))
    for i in freqs:
        signal.append(signalfft[i])

    for i in range(0, int(len(signalfft)/2)):
        if i<low or i>high:
            signal[i]=0
    output = []
    wynik = signal.copy()
    output.append(signal)
    for i in range(1, 8):
        output.append(scipy.signal.decimate(signal, i))
        for j in range(len(output[i])):
            wynik[j] = wynik[j] * output[i][j]

    for i in range(len(wynik)):
        if wynik[i] < 1:
            wynik[i] = 0

    #ax = fig.add_subplot(211)
    #ax.stem(freqs, wynik, '-')
    #plt.yscale('log')
    #ax = fig.add_subplot(212)
    #ax.stem(freqs, signal, '-')
    #plt.yscale('log')
    #plt.show()
    print(freqs[argmax(wynik,0)])
    if freqs[argmax(wynik,0)] > 350:
        return("K")
    else:
        return("M")

def checkall():
    listaPlikow = glob.glob("./trainall/*.wav")
    listaPoprawnych = []
    for i in range(len(listaPlikow)):
        listaPlikow[i] = listaPlikow[i][2:]
        listaPlikow[i] = listaPlikow[i].replace('\\', '/')
        listaPoprawnych.append(listaPlikow[i][-5])

    wygranko = 0
    przegranko = 0
    for i in range(0, len(listaPlikow)):
        try:
            w, signalData = scipy.io.wavfile.read(listaPlikow[i])
            wynik=sprawdzacz(signalData, w)
        except:
            wynik='K'
        if wynik == listaPoprawnych[i]:
            wygranko=wygranko+1
        else:
            przegranko=przegranko+1
        print(listaPlikow[i], wynik)
    print("wygranka ",wygranko, "przegranka", przegranko)

#w, signalData = scipy.io.wavfile.read("trainall/067_K.wav")
#sprawdzacz(signalData, w)
checkall()