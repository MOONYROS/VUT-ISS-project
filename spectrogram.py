import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import IPython
import scipy.signal as sp

s, fs = sf.read('audio/out_8k.wav')
f, t, Sxx = sp.spectrogram(s, fs, window=('tukey', 0.3), noverlap=0, nfft=512)
plt.pcolormesh(t, f, Sxx, shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

f, t, Zxx = sp.stft(s, fs, window=('tukey', 0.3), noverlap=0, nfft=512)
plt.pcolormesh(t, f, np.abs(Zxx), vmin=0, shading='gouraud')
plt.title('STFT Magnitude')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

s, fs = sf.read('audio/out_48k.wav')
f, t, Sxx = sp.spectrogram(s, fs, window=('tukey', 0.3), noverlap=0, nfft=2048)
plt.pcolormesh(t, f, Sxx, shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

f, t, Zxx = sp.stft(s, fs, window=('tukey', 0.3), noverlap=0, nfft=2048)
plt.pcolormesh(t, f, np.abs(Zxx), vmin=0, shading='gouraud')
plt.title('STFT Magnitude')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
