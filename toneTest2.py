import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import IPython
import scipy.signal as sp

def periodPrint(s, toneFreq):
    N = s.size
    period = 1 / toneFreq
    sample = N * period * 3 * 2
    plt.figure(figsize=(10, 3))
    graphTitle = '3 periody'
    plt.title(graphTitle)
    plt.plot(s[:int(sample) + 1])
    plt.show()

s, fs = sf.read('audio/c_orig.wav')
N = s.size
sSegSpec = np.fft.fft(s)

pi = np.pi

"""
def square_function(N, square_width):
    # Generate a square signal.
    # 
    # Args:
    #     N (int): Total number of points in the signal.
    #     square_width (int): Number of "high" points.
    # 
    # Returns (ndarray):
    #     A square signal which looks like this:
    # 
    #           |____________________
    #           |<-- square_width -->
    #           |                    ______________
    #           |
    #           |^                   ^            ^
    #     index |0             square_width      N-1
    # 
    #     In other words, the output has [0:N]=1 and [N:]=0.

    signal = np.zeros(N)
    signal[0:square_width] = 1
    return signal
"""

"""
def check_num_coefficients_ok(N, num_coefficients):
    # Make sure we're not trying to add more coefficients than we have.
    limit = None
    if N % 2 == 0 and num_coefficients > N // 2:
        limit = N/2
    elif N % 2 == 1 and num_coefficients > (N - 1)/2:
        limit = (N - 1)/2
    if limit is not None:
        raise ValueError(
            "num_coefficients is {} but should not be larger than {}".format(num_coefficients, limit))
"""

def test(s, N):
    """Test partial (i.e. filtered) Fourier reconstruction of a square signal.

    Args:
        N (int): Number of time (and frequency) points. We support both even
            and odd N.
        square_width (int): Number of "high" points in the time domain signal.
            This number must be less than or equal to N.
        num_coefficients (int): Number of frequencies, in addition to the dc
            term, to use in Fourier reconstruction. This is the number of
            positive frequencies _and_ the number of negative frequencies.
            Therefore, if N is odd, this number cannot be larger than
            (N - 1)/2, and if N is even this number cannot be larger than
            N/2.
    """
    # if square_width > N:
    #    raise ValueError("square_width cannot be larger than N")
    # check_num_coefficients_ok(N, num_coefficients)

    time_axis = np.linspace(0, N*2-1, N*2)

    # signal = square_function(N, square_width)
    ft = np.fft.fft(s)

    reconstructed_signal = np.zeros(N*2, dtype = complex)
    reconstructed_signal += ft[0] * np.ones(N*2)
    # Adding the dc term explicitly makes the looping easier in the next step.
    print(N*2)
    for k in range(int(N/2)):
        k += 1  # Bump by one since we already took care of the dc term.
        if k == N-k:
            reconstructed_signal += ft[k] * np.exp(1.0j*2 * pi * (k) * time_axis / N)
            print("SEM U SUDEHO POCTU VZORKU SNAD ANI NE")
        # This catches the case where N is even and ensures we don't double-
        # count the frequency k=N/2.

        else:
            reconstructed_signal += ft[k] * np.exp(1.0j*2 * pi * (k) * time_axis / (N))
            reconstructed_signal += ft[N-k] * np.exp(1.0j*2 * pi * (N-k) * time_axis / (N))
        # In this case we're just adding a frequency component and it's
        # "partner" at minus the frequency

    reconstructed_signal = reconstructed_signal / N
    # Normalize by the number of points in the signal. numpy's discete Fourier
    # transform convention puts the (1/N) normalization factor in the inverse
    # transform, so we have to do it here.

    plt.plot(time_axis[:24000], s,
             'b.', markersize=20,
             label='original')
    plt.plot(time_axis, reconstructed_signal.real,
             'r-', linewidth=3,
             label='reconstructed')
    # The imaginary part is zero anyway. We take the real part to
    # avoid matplotlib warnings.

    plt.grid()
    plt.legend(loc='upper right')
    plt.show()

test(s, N)