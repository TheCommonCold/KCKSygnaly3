from pylab import *
from numpy import *
from scipy import *
import scipy.io.wavfile
from scipy import signal
import matplotlib.pyplot as plt
import glob
import matplotlib.colors

fig = plt.figure(figsize=(15, 15), dpi=80)


def sprawdzacz(signalData,w):
    low=180
    high=3000
    if len(signalData.shape) > 1:
        signalData = [s[0] for s in signalData]

    signal = []
    if w*3<len(signalData):
        for i in range(w*1, w*3):
            signal.append(signalData[i])
    else:
        signal=signalData
    signalfft = fft(signal)
    signalfft = abs(signalfft)

    signal = []
    freqs = range(low, high)
    for i in freqs:
        signal.append(signalfft[i])

    output = []
    wynik = signal.copy()
    output.append(signal)
    for i in range(1, 9):
        output.append(scipy.signal.decimate(signal, i))
        for j in range(len(output[i])):
            wynik[j] = wynik[j] * output[i][j]

    # for i in range(len(wynik)):
    #     if wynik[i] < 1:
    #         wynik[i] = 0

    #ax = fig.add_subplot(211)
    #ax.stem(freqs, wynik, '-')
    #plt.yscale('log')
    #ax = fig.add_subplot(212)
    #ax.stem(freqs, signal, '-')
    #plt.yscale('log')
    #plt.show()
    #print(freqs[argmax(wynik)])
    return freqs,wynik
    # if freqs[argmax(wynik)] > 320:
    #     return("K")
    # else:
    #     return("M")

def checkall():
    listaPlikow = glob.glob("./trainall/*.wav")
    listaPoprawnych = []
    for i in range(len(listaPlikow)):
        listaPlikow[i] = listaPlikow[i][2:]
        listaPlikow[i] = listaPlikow[i].replace('\\', '/')
        listaPoprawnych.append(listaPlikow[i][-5])

    wygranko = 0
    wszystkie = 0
    ms=array([])
    ks=array([])
    for i in range(1, len(listaPlikow)-1):
        w, signalData = scipy.io.wavfile.read(listaPlikow[i])
        freqs,wynik = sprawdzacz(signalData, w)
        f=freqs[argmax(wynik)]
        plec = "M"
        if f > 320:
            plec = "K"
        if listaPoprawnych[i] == "K":append(ks,array([f,std(wynik),]))
        else:append(ms, array([f,std(wynik)]))
        if plec == listaPoprawnych[i]:
            wygranko=wygranko+1
        # else:
        #     print(listaPoprawnych[i],plec, f)
        wszystkie+=1
    print("wygranka {0}/{1}".format(wygranko,wszystkie))
    print("K")
    for i in ks:
        print(i)
    print("M")
    for i in ms:
        print(i)
    ax = fig.add_subplot(211)
    # ax.stem(ks[0,:], ks[1,:], '-')
    # plt.yscale('log')
    ax = fig.add_subplot(212)
    ax.plot(ms[:,0], ms[:,1], '-')

    # plt.yscale('log')
    plt.show()
    # print(freqs[argmax(wynik)])
#w, signalData = scipy.io.wavfile.read("trainall/010_M.wav")
#sprawdzacz(signalData, w);
checkall()