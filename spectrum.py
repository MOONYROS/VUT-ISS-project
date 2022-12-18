import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import scipy.signal as sp

def spectrumPrint(fileName):
    s, Fs = sf.read(fileName)
    N = s.size
    s_seg_spec = np.fft.fft(s)
    G = 10 * np.log10(1/N * np.abs(s_seg_spec)**2)
    f = np.arange(G.size) / N * Fs

    plt.figure(figsize=(10, 3))
    plt.plot(f[:f.size//2+1], G[:G.size//2+1])
    plt.xlabel('$frekvence [Hz]$')
    graphTitle = 'Spektrum', fileName
    plt.title(graphTitle)
    plt.show()

spectrumPrint('audio/a_orig.wav')
spectrumPrint('audio/b_orig.wav')
spectrumPrint('audio/c_orig.wav')