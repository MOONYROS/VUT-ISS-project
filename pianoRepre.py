import soundfile as sf
import numpy as np
import scipy.signal as sp
import matplotlib.pyplot as plt
from IPython.display import Audio

def makeDTFT(s, fs, freq):
    N = s.size
    sampleTime = float(N) / fs
    x = np.linspace(0, freq * sampleTime * 2 * np.pi, num = 24000)
    ySin = np.sin(x)
    yCos = np.cos(x)
    im = np.dot(s, ySin)
    re = np.dot(s, yCos)
    return complex(re, im)

def matchDTFT(s, fs, rawFreq, sweep):
    maxVal = 0
    exactFreq = rawFreq
    for i in range(int(sweep * 2 * 10)):
        freq = rawFreq - float(sweep) + float(i) / 10.0
        res = np.abs(makeDTFT(s, fs, freq))
        if res > maxVal:
            maxVal = res
            exactFreq = freq
    return exactFreq

def pianoRepre(fileName):
    s, fs = sf.read(fileName)
    N = s.size

    sSegSpec = np.fft.fft(s)
    G = 10 * np.log10(1/N * np.abs(sSegSpec)**2 + 10e-5)
    f = np.arange(G.size) / N * fs

    i = np.argmax(abs(np.split(sSegSpec, 2)[0]))
    rawFreq = fs * i / N 

    f0 = matchDTFT(s, fs, rawFreq, 4)

    multFreqs = range(1, 11)
    freqs = multFreqs * f0
    print(freqs)
    accFreqs = np.zeros(10, dtype = float)
    resDTFT = np.zeros(10, dtype = complex)
    for i in range(10):
        accFreqs[i] = matchDTFT(s, fs, freqs[i], 4) # doladujeme na +-2 koeficienty DFT, coz zpusobuje nepresnost pri "nasobeni chyby dft"
        resDTFT[i] = makeDTFT(s, fs, accFreqs[i])
        
    print(accFreqs)
    resMod = np.zeros(10, dtype = float)
    resPhase = np.zeros(10, dtype = float)
    for i in range(10):
        tmpRes = resDTFT[i]
        resMod[i] = np.abs(tmpRes)
        resPhase[i] = np.angle(tmpRes)
    for i in range(10):
        print("Frekvence", '{:>8.1f}'.format(accFreqs[i]), "Hz", "   Modul:", '{:>7.2f}'.format(round(resMod[i],2)), "   Faze:", '{:>7.2f}'.format(round(resPhase[i],2)))


    plt.figure(figsize=(15,5))
    plt.plot(f[:f.size//2+1], G[:G.size//2+1])
    plt.xlabel('$f[Hz]$')
    graphTitle = "Reprezentace klaviru pro", fileName
    plt.title(graphTitle)
    plt.grid(alpha=0.5, linestyle='--')

    for i in range(10):
        y = 10 * np.log10(1/N * np.abs(resMod[i])**2 + 10e-5)
        plt.plot(accFreqs[i], y, 'x')

    plt.show()

pianoRepre("audio/a_orig.wav")
pianoRepre("audio/b_orig.wav")
pianoRepre("audio/c_orig.wav")