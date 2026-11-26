import math
from tkinter import filedialog, simpledialog
import matplotlib.pyplot as plt
from CompareSignal import Compare_Signals


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


def show(x, y, title):
    plt.subplot(1, 2, 1)
    plt.plot(x, y)
    plt.title(title + " (continuous)")
    plt.subplot(1, 2, 2)
    plt.stem(x, y)
    plt.title(title + " (discrete)")


def correlate(y1, y2):
    # same length: N = length, different length: pad both with zeros to N1 + N2 - 1
    N = len(y1)
    if len(y1) != len(y2):
        N = len(y1) + len(y2) - 1
    a = []
    b = []
    for n in range(N):
        a.append(0)
        b.append(0)
    for n in range(len(y1)):
        a[n] = y1[n]
    for n in range(len(y2)):
        b[n] = y2[n]
    sum1 = 0
    sum2 = 0
    for n in range(N):
        sum1 = sum1 + a[n] * a[n]
        sum2 = sum2 + b[n] * b[n]
    bottom = math.sqrt(sum1 * sum2) / N
    result = []
    for j in range(N):
        total = 0
        for n in range(N):
            total = total + a[n] * b[(n + j) % N]
        r = total / N
        result.append(r / bottom)
    return result


def cross_correlation():
    file1 = filedialog.askopenfilename(title="Choose the first signal")
    file2 = filedialog.askopenfilename(title="Choose the second signal")
    x1, y1 = read_signal(file1)
    x2, y2 = read_signal(file2)
    result = correlate(y1, y2)
    x = []
    for j in range(len(result)):
        x.append(j)
    file = filedialog.askopenfilename(title="Choose the expected output file")
    if file:
        Compare_Signals(file, x, result)
    show(x, result, "Cross Correlation")
    plt.show()


def auto_correlation():
    file = filedialog.askopenfilename(title="Choose a signal")
    x1, y1 = read_signal(file)
    result = correlate(y1, y1)
    x = []
    for j in range(len(result)):
        x.append(j)
    show(x, result, "Auto Correlation")
    plt.show()


def time_delay():
    file1 = filedialog.askopenfilename(title="Choose the first signal")
    file2 = filedialog.askopenfilename(title="Choose the second signal")
    Ts = simpledialog.askfloat("Time Delay", "Sampling period Ts (seconds):")
    x1, y1 = read_signal(file1)
    x2, y2 = read_signal(file2)
    result = correlate(y1, y2)
    best = 0
    for j in range(len(result)):
        if abs(result[j]) > abs(result[best]):
            best = j
    print("Max correlation at lag", best)
    print("Time delay =", best * Ts, "seconds")
    x = []
    for j in range(len(result)):
        x.append(j)
    show(x, result, "Correlation")
    plt.show()
