import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import scipy.signal as sp

from IPython.display import Audio

def periodPrint(fileName, toneFreq):
    s, Fs = sf.read(fileName)
    N = s.size
    period = 1 / toneFreq
    sample = N * period * 3 * 2
    plt.figure(figsize=(10, 3))
    graphTitle = '3 periody', fileName
    plt.title(graphTitle)
    plt.plot(s[:int(sample) + 1])
    plt.show()

periodPrint("../audio/a_orig.wav", 82.41)
periodPrint("../audio/b_orig.wav", 659.26)
periodPrint("../audio/c_orig.wav", 3520.00)