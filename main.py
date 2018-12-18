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
    low=200
    high=3000
    if (len(signalData.shape) > 1):
        signalData = [s[0] for s in signalData]

    signal = []
    for i in range(1 * w, 3 * w):
        signal.append(signalData[i])

    signalfft = fft(signal)
    signalfft = abs(signalfft)
    signalfft = [x / (len(signal) / 2) for x in signalfft]
    signalfft[0] = signalfft[0] / 2

    signal = []
    freqs = range(low, high)
    for i in freqs:
        signal.append(signalfft[i])

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

    # ax = fig.add_subplot(211)
    # ax.stem(freqs, wynik, '-')
    # plt.yscale('log')
    # ax = fig.add_subplot(212)
    # ax.stem(freqs, signal, '-')
    # plt.yscale('log')
    # plt.show()
    # print(freqs[argmax(wynik)])
    if freqs[argmax(wynik)] > 300:
        return("K")
    else:
        return("M")

listaPlikow = glob.glob("./trainall/*.wav")
listaPoprawnych = []
for i in range(len(listaPlikow)):
    listaPlikow[i]=listaPlikow[i][2:]
    listaPlikow[i]=listaPlikow[i].replace('\\','/')
    listaPoprawnych.append(listaPlikow[i][-5])

for i in range(1,len(listaPlikow)):
    w, signalData = scipy.io.wavfile.read(listaPlikow[i])
    if sprawdzacz(signalData,w)==listaPoprawnych[i]:
        print("good")
    else:
        print("bad")
