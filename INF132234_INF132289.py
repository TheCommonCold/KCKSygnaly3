#!/usr/bin/python

import sys
# from pylab import *
import numpy as np
from scipy import *
import scipy.io.wavfile
from scipy import signal
import matplotlib.pyplot as plt
import glob
import matplotlib.colors
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def sprawdzacz(signalData, w):
    low = 120
    high = 6000
    signalData = np.array(signalData)
    if (len(signalData.shape) > 1):
        signalData = [s[0] for s in signalData]

    signal = []
    if w * 3 < len(signalData):
        for i in range(int(w * 1), w * 3):
            signal.append(signalData[i])
    else:
        signal = signalData
        # for i in range(w*1, len(signalData)):
        #    signal.append(signalData[i])
    signalfft = fft(signal)
    signalfft = abs(signalfft)

    signal = []
    freqs = range(0, int(len(signalfft) / 2))
    for i in freqs:
        signal.append(signalfft[i])

    for i in range(0, int(len(signalfft) / 2)):
        if i < low or i > high:
            signal[i] = 0
    output = []
    wynik = signal.copy()
    output.append(signal)
    # signal2=[]
    # for i in signal:
    #     signal2.append(tuple(i))
    for i in range(1, 8):
        x = scipy.signal.decimate(signal, i)
        output.append(x.copy())
        for j in range(len(output[i])):
            wynik[j] = wynik[j] * output[i][j]

    for i in range(len(wynik)):
        if wynik[i] < 1:
            wynik[i] = 0
    if freqs[argmax(wynik, 0)] > 350:
        return "K"
    else:
        return "M"


def checkOne(argument):
    wynik = 'K'
    try:
        w, signalData = scipy.io.wavfile.read(argument)
        wynik = sprawdzacz(signalData, w)
    except:
        wynik = 'K'
    finally:
        print(wynik)


if __name__ == "__main__":
    checkOne(sys.argv[1])
