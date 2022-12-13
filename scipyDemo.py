import matplotlib.pyplot as plt
from scipy.misc import electrocardiogram
from scipy.signal import find_peaks
import numpy as np

x = electrocardiogram()[2000:4000]

peaks, _ = find_peaks(x)

plt.plot(x)
plt.plot(peaks, x[peaks], "x")
plt.show()

print("NUMBER OF PEAKS:", len(peaks))
print("FIRST FOUR PEAKS:", peaks[0], peaks[1], peaks[2], peaks[3])

plt.show()