import soundfile as sf
import numpy as np
import scipy.signal as sp
import matplotlib.pyplot as plt
from IPython.display import Audio

MIDIFROM = 24
MIDITO = 108
SKIP_SEC = 0.35
HOWMUCH_SEC = 0.5
WHOLETONE_SEC = 2
howmanytones = MIDITO - MIDIFROM + 1
tones = np.arange(MIDIFROM, MIDITO+1)
s, Fs = sf.read('klavir.wav')
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
    sSegSpec = np.fft.fft(x)
    G = np.log10(1/N * np.abs(sSegSpec)**2 + 10e-5)
    peaks, _ = sp.find_peaks(sSegSpec)
    maxPeak = peaks[0]
    for peak in peaks:
        if(sSegSpec[peak] > sSegSpec[maxPeak]):
            maxPeak = peak
    print('Max Peak of midi', midiNumber, 'is:', maxPeak)
    midiNumber = midiNumber + 1
