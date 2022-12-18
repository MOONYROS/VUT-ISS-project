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
    else:
        sSegSpec = np.fft.fft(x)
        i = np.argmax(abs(np.split(sSegSpec, 2)[0]))
        freq = Fs * i / N 
    print('FFT or corelation for midi', '{:>3}'.format(midiNumber), 'is:', '{:>6}'.format(round(freq, 1)), "Hz", "  DTFT:", '{:>6}'.format(round(matchDTFT(x, Fs, freq, 4), 1)), "Hz")
    midiNumber = midiNumber + 1

#vypujceno z https://gist.github.com/endolith/255291/0c0dbc8995bf5c22f56a31036e3094d15bf1b783
