import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import IPython
import scipy.signal as sp

s, fs = sf.read('audio/a_orig.wav')
N = s.size
sSegSpec = np.fft.fft(s)
G = np.log10(1/N * np.abs(sSegSpec)**2 + 10e-5)

peaks, _ = sp.find_peaks(sSegSpec)
maxPeak = peaks[0]
for peak in peaks:
    if(sSegSpec[peak] > sSegSpec[maxPeak]):
        maxPeak = peak
        
print(maxPeak)
print(sSegSpec[maxPeak])
f = np.arange(G.size) / N * fs
# zobrazujeme prvni pulku spektra
plt.figure(figsize=(15,5))
plt.plot(f[:f.size//2+1], G[:G.size//2+1])
plt.xlabel('$f[Hz]$')
plt.title('Spektralni hustota vykonu [dB]')
plt.grid(alpha=0.5, linestyle='--')
plt.show()

#peaks = sp.find_peaks(f)
#plt.plot(f)
#plt.plot(peaks, f[peaks], "f")
#plt.show()
