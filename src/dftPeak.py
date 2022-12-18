import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import IPython
import scipy.signal as sp

s, fs = sf.read('../audio/b_orig.wav')
N = s.size
sSegSpec = np.fft.fft(s)
G = 10 * np.log10(1/N * np.abs(sSegSpec)**2 + 10e-5)

for i in range(100):
    print(i, abs(sSegSpec[i]), sSegSpec[i])
plt.figure(figsize=(12, 5))
plt.plot(sSegSpec)
plt.show()

i = np.argmax(abs(sSegSpec)) 
print('../audio/b_orig.wav max peak is:', fs * i / N)
#print(sSegSpec[maxPeak])
#print(G.size, N, fs, G[0], sSegSpec[0], sSegSpec[ourIndex])
f = np.arange(G.size) / N * fs
# zobrazujeme prvni pulku spektra
plt.figure(figsize=(15,5))
plt.plot(f[:f.size//2+1], G[:G.size//2+1])
plt.xlabel('$f[Hz]$')
plt.title('Spektralni hustota vykonu [dB]')
plt.grid(alpha=0.5, linestyle='--')
plt.show()
