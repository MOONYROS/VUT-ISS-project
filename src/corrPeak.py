import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import IPython
import scipy.signal as sp

def find(condition):
    res, = np.nonzero(np.ravel(condition))
    return res

s, fs = sf.read('../audio/a_orig.wav')
N = s.size
sSegSpec = np.fft.fft(s)
G = 10 * np.log10(1/N * np.abs(sSegSpec)**2 + 10e-5)

# Calculate autocorrelation and throw away the negative lags
corr = sp.fftconvolve(s, s[::-1], mode='full')
corr = corr[int(len(corr)/2):]

# Find the first low point
d = np.diff(corr)
start = find(d > 0)[0]

# Find the next peak after the low point (other than 0 lag).  This bit is 
# not reliable, due to peaks that occur between samples.
peak = np.argmax(corr[start:]) + start

print('../audio/a_orig.wav max peak is:', fs / peak)
f = np.arange(G.size) / N * fs
plt.figure(figsize=(15,5))
plt.plot(f[:f.size//2+1], G[:G.size//2+1])
plt.xlabel('$f[Hz]$')
plt.title('Spektralni hustota vykonu [dB]')
plt.grid(alpha=0.5, linestyle='--')
plt.show()
