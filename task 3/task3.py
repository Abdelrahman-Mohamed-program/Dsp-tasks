import cmath
import math
from tkinter import filedialog, simpledialog
import matplotlib.pyplot as plt
from signalcompare import SignalComapreAmplitude, SignalComaprePhaseShift
from CompareSignals import SignalsAreEqual

amplitudes = []
phases = []
fs = 1


def read_signal(path):
    f = open(path)
    lines = f.readlines()
    f.close()
    x = []
    y = []
    for line in lines[3:]:
        parts = line.split()
        x.append(int(parts[0]))
        y.append(float(parts[1]))
    return x, y


def read_spectrum(path):
    f = open(path)
    lines = f.readlines()
    f.close()
    a = []
    p = []
    for line in lines[3:]:
        parts = line.replace("f", "").split()
        a.append(float(parts[0]))
        p.append(float(parts[1]))
    return a, p


def show(x, y, title):
    plt.subplot(1, 2, 1)
    plt.plot(x, y)
    plt.title(title + " (continuous)")
    plt.subplot(1, 2, 2)
    plt.stem(x, y)
    plt.title(title + " (discrete)")


def show_spectrum():
    N = len(amplitudes)
    peak = max(amplitudes)
    freqs = []
    normalized = []
    for k in range(N):
        freqs.append(k * fs / N)
        normalized.append(amplitudes[k] / peak)
    print("Dominant frequencies:")
    for k in range(N):
        if normalized[k] > 0.5:
            print(freqs[k], "Hz")
    plt.subplot(1, 2, 1)
    plt.stem(freqs, normalized)
    plt.title("Frequency vs Amplitude")
    plt.subplot(1, 2, 2)
    plt.stem(freqs, phases)
    plt.title("Frequency vs Phase")
    plt.show()


def fourier(values, inverse):
    # one function for both DFT and IDFT, only the sign and the 1/N change
    N = len(values)
    sign = -1
    if inverse:
        sign = 1
    result = []
    for k in range(N):
        total = 0
        for n in range(N):
            total = total + values[n] * cmath.exp(sign * 2j * math.pi * k * n / N)
        if inverse:
            total = total / N
        result.append(total)
    return result


def to_spectrum(samples):
    a = []
    p = []
    for c in fourier(samples, False):
        a.append(abs(c))
        p.append(cmath.phase(c))
    return a, p


def to_signal(a, p):
    values = []
    for k in range(len(a)):
        values.append(cmath.rect(a[k], p[k]))
    samples = []
    for c in fourier(values, True):
        samples.append(c.real)
    return samples


def dft():
    global amplitudes, phases, fs
    file = filedialog.askopenfilename(title="Choose a signal")
    fs = simpledialog.askfloat("DFT", "Sampling frequency (Hz):")
    x, y = read_signal(file)
    amplitudes, phases = to_spectrum(y)
    file = filedialog.askopenfilename(title="Choose the expected output file")
    if file:
        a, p = read_spectrum(file)
        mine = []
        expected = []
        for k in range(len(a)):
            mine.append(round(amplitudes[k], 3))
            expected.append(round(a[k], 3))
        if SignalComapreAmplitude(mine, expected) and SignalComaprePhaseShift(phases, p):
            print("DFT Test case passed successfully")
        else:
            print("DFT Test case failed")
    show_spectrum()


def modify():
    k = simpledialog.askinteger("Modify", "Component index (0 to " + str(len(amplitudes) - 1) + "):")
    amplitudes[k] = simpledialog.askfloat("Modify", "New amplitude:")
    phases[k] = simpledialog.askfloat("Modify", "New phase (radians):")
    show_spectrum()


def remove_dc():
    file = filedialog.askopenfilename(title="Choose a signal")
    x, y = read_signal(file)
    a, p = to_spectrum(y)
    a[0] = 0
    p[0] = 0
    result = to_signal(a, p)
    file = filedialog.askopenfilename(title="Choose the expected output file")
    if file:
        SignalsAreEqual("Remove DC", file, x, result)
    show(x, result, "Remove DC")
    plt.show()


def idft():
    file = filedialog.askopenfilename(title="Choose an amplitude/phase file")
    a, p = read_spectrum(file)
    result = to_signal(a, p)
    x = []
    for n in range(len(result)):
        x.append(n)
    file = filedialog.askopenfilename(title="Choose the expected output file")
    if file:
        SignalsAreEqual("IDFT", file, x, result)
    show(x, result, "IDFT")
    plt.show()


def reconstruct():
    result = to_signal(amplitudes, phases)
    x = []
    for n in range(len(result)):
        x.append(n)
    show(x, result, "Reconstructed")
    plt.show()
