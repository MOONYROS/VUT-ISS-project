import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import IPython
import scipy.signal as sp

def makeDTFT(s, fs, freq):
    N = s.size
    sampleTime = float(N) / fs
    halfWave = float(N) / freq
    """
    x = np.arange(0, freq * sampleTime * 2 * np.pi - np.pi / halfWave, np.pi / halfWave)
    if x.size < 24000:
        x = np.arange(0, freq * sampleTime * 2 * np.pi, np.pi / halfWave)
    """
    x = np.linspace(0, freq * sampleTime * 2 * np.pi, num = 24000)
    y1 = np.sin(x)
    y2 = np.cos(x)

    #print(N, fs)
    #print(halfWave, x.size)

    #plt.figure(figsize=(10, 4))
    #plt.plot(x, y1)
    #plt.plot(x, y2)
    #plt.show()

    v1 = np.dot(s, y1)
    v2 = np.dot(s, y2)

    result = np.sqrt(v1**2 + v2**2)
    return result
    #print("RESULT:", result)


def matchDTFT(s, fs, rawFreq, sweep):
    maxVal = 0
    exactFreq = rawFreq
    for i in range(int(sweep * 2 * 10)):
        freq = rawFreq - float(sweep) + float(i) / 10.0
        res = makeDTFT(s, fs, freq)
        if res > maxVal:
            maxVal = res
            exactFreq = freq
    return exactFreq

s, fs = sf.read('audio/c_orig.wav')
rawFreq = 3519
print("EXACT FREQUENCY:", matchDTFT(s, fs, rawFreq, 5))
