import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import IPython
import scipy.signal as sp

def periodPrint(s, toneFreq):
    N = s.size
    period = 1 / toneFreq
    sample = N * period * 3 * 2
    plt.figure(figsize=(10, 3))
    graphTitle = '3 periody'
    plt.title(graphTitle)
    plt.plot(s[:int(sample) + 1])
    plt.show()

s, fs = sf.read('audio/b_orig.wav')
N = s.size
sSegSpec = np.fft.fft(s)

outSignal = np.zeros(N, dtype = float)

for i in range(int(N / 4) - 1):
    sampleTime = float(N) / fs
    h = i + 1
    freq = 2 * h
    x = np.linspace(0, freq * sampleTime * 2 * np.pi, num = 24000)
    #plt.plot(outSignal)
    ySin = np.sin(x) / float(h)
    #plt.plot(ySin)
    outSignal = outSignal - np.imag(sSegSpec[h]) * ySin
    #print(h, np.real(sSegSpec[h]), np.imag(sSegSpec[h]))
    #plt.plot(outSignal)
    yCos = np.cos(x) / float(h)
    #plt.plot(yCos)
    outSignal = outSignal + np.real(sSegSpec[h]) * yCos
    #plt.plot(outSignal)
    #plt.show()

#periodPrint(s, 660)
#periodPrint(outSignal, 660)
period = 1 / 660
sample = N * period * 3 * 2
plt.figure(figsize=(10, 3))
graphTitle = '3 periody'
plt.title(graphTitle)
plt.plot(s[:int(sample) + 1])
plt.plot(outSignal[:int(sample) + 1])
plt.show()
