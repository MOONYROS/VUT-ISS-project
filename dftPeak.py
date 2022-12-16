import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import IPython
import scipy.signal as sp

s, fs = sf.read('audio/a_orig.wav')
N = s.size
sSegSpec = np.fft.fft(s)
G = 10 * np.log10(1/N * np.abs(sSegSpec)**2 + 10e-5)

#maxPeak = G[0]
'''maxPeak = sSegSpec[0]
ourIndex = 0
for index, peak in enumerate(np.split(sSegSpec, 2)[0]):
    if(np.abs(peak) > np.abs(maxPeak)):
        maxPeak = peak
        ourIndex = index'''
        
i = np.argmax(abs(sSegSpec)) 
print('audio/b_orig.wav max peak is:', fs * i / N)
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
