import soundfile as sf
import numpy as np
import scipy.signal as sp
import matplotlib.pyplot as plt
from IPython.display import Audio

def find(condition):
    res, = np.nonzero(np.ravel(condition))
    return res

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

MIDIFROM = 24
MIDITO = 108
SKIP_SEC = 0.35
HOWMUCH_SEC = 0.5
WHOLETONE_SEC = 2
howmanytones = MIDITO - MIDIFROM + 1
tones = np.arange(MIDIFROM, MIDITO+1)
s, Fs = sf.read('../audio/klavir.wav')
N = int(Fs * HOWMUCH_SEC)
Nwholetone = int(Fs * WHOLETONE_SEC)
xall = np.zeros((MIDITO+1, N)) # matrix with all tones - first signals empty,
# but we have plenty of memory ...
samplefrom = int(SKIP_SEC * Fs)
sampleto = samplefrom + N
midiNumber = 24
for tone in tones:
    x = s[samplefrom:sampleto]
    x = x - np.mean(x) # safer to center ...
    xall[tone,:] = x
    samplefrom += Nwholetone
    sampleto += Nwholetone
    # misto 's' ted pracujeme s 'x'
    N = x.size
    f0 = 0.0
    if midiNumber < 47:
        # Calculate autocorrelation and throw away the negative lags
        corr = sp.fftconvolve(x, x[::-1], mode='full')
        corr = corr[int(len(corr)/2):]

        # Find the first low point
        d = np.diff(corr)
        start = find(d > 0)[0]

        # Find the next peak after the low point (other than 0 lag).  This bit is 
        # not reliable, due to peaks that occur between samples.
        peak = np.argmax(corr[start:]) + start
        freq = Fs / peak
        f0 = freq
    else:
        sSegSpec = np.fft.fft(x)
        i = np.argmax(abs(np.split(sSegSpec, 2)[0]))
        freq = Fs * i / N 
        f0 = matchDTFT(x, Fs, freq, freq/96)
    #print('FFT or corelation for midi', '{:>3}'.format(midiNumber), 'is:', '{:>6}'.format(round(freq, 1)), "Hz", "  DTFT:", '{:>6}'.format(round(matchDTFT(x, Fs, freq, 4), 1)), "Hz", f0)

    multFreqs = range(1, 11)
    freqs = multFreqs * f0
    #print(freqs)
    accFreqs = np.zeros(10, dtype = float)
    resDTFT = np.zeros(10, dtype = complex)
    for i in range(10):
        accFreqs[i] = matchDTFT(x, Fs, freqs[i], f0/96) # doladujeme na +-2 koeficienty DFT, coz zpusobuje nepresnost pri "nasobeni chyby dft"
        resDTFT[i] = makeDTFT(x, Fs, accFreqs[i])
        
    #print(accFreqs)
    resMod = np.zeros(10, dtype = float)
    resPhase = np.zeros(10, dtype = float)
    for i in range(10):
        tmpRes = resDTFT[i]
        resMod[i] = np.abs(tmpRes)
        resPhase[i] = np.angle(tmpRes)
    print("[ ", sep='', end='')
    for i in range(9):
        print('{:.2f}'.format(accFreqs[i]), ", ", '{:.2f}'.format(round(resMod[i],2)), '{:+0.2f}'.format(round(resPhase[i],2)), "j, ", sep='', end='')
    print('{:.2f}'.format(accFreqs[9]), ", ", '{:.2f}'.format(round(resMod[9],2)), '{:+0.2f}'.format(round(resPhase[9],2)), "j ],", sep='')

    midiNumber = midiNumber + 1
