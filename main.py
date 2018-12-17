from pylab import *
from numpy import *
from scipy import *
import scipy.io.wavfile
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.colors

fig = plt.figure(figsize=(15, 15), dpi=80)

w, signalData = scipy.io.wavfile.read("trainall/003_K.wav")
print(w)
print(signalData.shape)

if(len(signalData.shape)>1):
    signalData = [s[0] for s in signalData]

#print(w)
f, t, Sxx = signal.spectrogram(np.array(signalData), w,nfft=int(w/2), nperseg=512)
print(Sxx.shape)
print(len(f))
avg=[]
for x in Sxx:
    avg.append(np.mean(x))

maxFound=np.max(avg)
print(f[avg.index(maxFound)])
plt.pcolormesh(t, f, Sxx)
plt.ylim(1,3000)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

