import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import IPython
import scipy.signal as sp

def manIFFTexp(ft):
    N = ft.size
    outSignal = np.zeros(N, dtype = complex)
    x = np.linspace(0, N-1, N)
    for i in range(int(N / 2)):
        if i == 0:
            outSignal += ft[i] * np.ones(N)
        else:
            if i == N-i:
                outSignal += ft[i] * np.exp(1.0j*2 * np.pi * (i) * x / N)
            else:
                outSignal += ft[i] * np.exp(1.0j * 2 * np.pi * (i) * x / N) 
                outSignal += ft[N-i] * np.exp(1.0j * 2 * np.pi * (N-i) * x / N)
    outReal = outSignal.real / N
    return outReal

def manIFFTcos(ft):
    N = ft.size
    outSignal = np.zeros(N, dtype = complex)
    x = np.linspace(0, N-1, N)
    for i in range(int(N / 2)):
        if i == 0:
            outSignal += ft[i] * np.ones(N)
        else:
            if i == N-i:
                outSignal += ft[i] * np.exp(1.0j*2 * np.pi * (i) * x / N)
            else:
                outSignal += ft.real[i] * np.cos(2 * np.pi * (i) * x / N) * 1.732
                #outSignal += sSegSpec.imag[i] * np.sin(2 * np.pi * (i) * x / N) 
                #outSignal += np.abs(sSegSpec[i]) * np.cos(2 * np.pi * (i) * x / N) 
                outSignal += ft.real[N-i] * np.cos(2 * np.pi * (N-i) * x / N) * 1.732
                #outSignal += sSegSpec.imag[N-i] * np.sin(2 * np.pi * (N-i) * x / N)
                #outSignal += np.abs(sSegSpec.real[N-i]) * np.cos(2 * np.pi * (N-i) * x / N)
    outReal = outSignal.real / N
    return outReal

def manIFFTcosLen(ft, l):
    N = ft.size
    outSignal = np.zeros(N*l, dtype = complex)
    x = np.linspace(0, N*l-1, N*l)
    for i in range(int(N / 2)):
        if i == 0:
            outSignal += ft[0] * np.ones(N*l)
        else:
            if i == N-i:
                outSignal += ft[i] * np.exp(1.0j*2 * np.pi * (i) * x / N)
            else:
                outSignal += ft.real[i] * np.cos(2 * np.pi * (i) * x / N) * 1.732
                #outSignal += sSegSpec.imag[i] * np.sin(2 * np.pi * (i) * x / N) 
                #outSignal += np.abs(sSegSpec[i]) * np.cos(2 * np.pi * (i) * x / N) 
                outSignal += ft.real[N-i] * np.cos(2 * np.pi * (N-i) * x / N) * 1.732
                #outSignal += sSegSpec.imag[N-i] * np.sin(2 * np.pi * (N-i) * x / N)
                #outSignal += np.abs(sSegSpec.real[N-i]) * np.cos(2 * np.pi * (N-i) * x / N)
    outReal = outSignal.real / N
    return outReal

def syntTone(srcFile, dstFile, toneFreq):
    s, fs = sf.read(srcFile)
    N = s.size
    sSegSpec = np.fft.fft(s)

    period = 1 / toneFreq
    sample = N * period * 10 * 2
    plt.figure(figsize=(10, 3))
    graphTitle = '10 period', srcFile
    plt.title(graphTitle)
    plt.plot(s[:int(sample) + 1])
    outExp = manIFFTexp(sSegSpec)
    plt.plot(outExp[:int(sample) + 1])
    outCos = manIFFTcos(sSegSpec)
    plt.plot(outCos[:int(sample) + 1])
    plt.show()

    outSec = manIFFTcosLen(sSegSpec, 2)
    sf.write(dstFile, outSec, fs)

syntTone('../audio/a_orig.wav', '../audio/a.wav', 82.41)
syntTone('../audio/b_orig.wav', '../audio/b.wav', 659.26)
syntTone('../audio/c_orig.wav', '../audio/c.wav', 3520.00)