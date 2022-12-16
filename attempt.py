import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import IPython
import scipy.signal as sp

s, fs = sf.read('audio/a_orig.wav')


N = s.size
sampleTime = float(N) / fs
freq = 80.0
botFreq = freq - 2
halfWave = float(N) / freq

x = np.arange(0, freq * sampleTime * 2 * np.pi - np.pi / halfWave, np.pi / halfWave)
if x.size < 24000:
    x = np.arange(0, freq * sampleTime * 2 * np.pi, np.pi / halfWave)
y1 = np.sin(x)
y2 = np.cos(x)

print(N, fs)
print(halfWave, x.size)

plt.figure(figsize=(10, 4))
plt.plot(x, y1)
plt.plot(x, y2)
#plt.show()

v1 = np.dot(s, y1)
v2 = np.dot(s, y2)

result = np.sqrt(v1**2 + v2**2)
print("RESULT:", result)

print(len(x))