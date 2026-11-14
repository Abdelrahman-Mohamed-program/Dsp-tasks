from tkinter import filedialog, simpledialog
import matplotlib.pyplot as plt
from CompareSignals import SignalsAreEqual
from Shift_Fold_Signal import Shift_Fold_Signal
from DerivativeSignal import DerivativeSignal


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


def fold(x, y):
    rx = []
    ry = []
    for i in range(len(y) - 1, -1, -1):
        rx.append(-x[i])
        ry.append(y[i])
    return rx, ry


def shift(x, k):
    rx = []
    for i in range(len(x)):
        rx.append(x[i] + k)
    return rx


def smoothing():
    file = filedialog.askopenfilename(title="Choose a signal")
    window = simpledialog.askinteger("Smoothing", "Number of points:")
    x, y = read_signal(file)
    rx = []
    result = []
    for i in range(len(y) - window + 1):
        total = 0
        for j in range(window):
            total = total + y[i + j]
        rx.append(x[i])
        result.append(total / window)
    file = filedialog.askopenfilename(title="Choose the expected output file")
    if file:
        SignalsAreEqual("Moving Average", file, rx, result)
    show(rx, result, "Moving Average")
    plt.show()


def sharpening():
    DerivativeSignal()
    file = filedialog.askopenfilename(title="Choose a signal")
    x, y = read_signal(file)
    x1 = []
    first = []
    for i in range(1, len(y)):
        x1.append(x[i])
        first.append(y[i] - y[i - 1])
    x2 = []
    second = []
    for i in range(1, len(y) - 1):
        x2.append(x[i])
        second.append(y[i + 1] - 2 * y[i] + y[i - 1])
    show(x1, first, "First Derivative")
    plt.show()
    show(x2, second, "Second Derivative")
    plt.show()


def delay_or_advance():
    file = filedialog.askopenfilename(title="Choose a signal")
    k = simpledialog.askinteger("Shift", "Steps (positive = delay, negative = advance):")
    x, y = read_signal(file)
    rx = shift(x, k)
    show(rx, y, "Shifted")
    plt.show()


def folding():
    file = filedialog.askopenfilename(title="Choose a signal")
    x, y = read_signal(file)
    rx, ry = fold(x, y)
    file = filedialog.askopenfilename(title="Choose the expected output file")
    if file:
        Shift_Fold_Signal(file, rx, ry)
    show(rx, ry, "Folded")
    plt.show()


def shift_folded():
    file = filedialog.askopenfilename(title="Choose a signal")
    k = simpledialog.askinteger("Shift Folded", "Steps (positive = delay, negative = advance):")
    x, y = read_signal(file)
    rx, ry = fold(x, y)
    rx = shift(rx, k)
    file = filedialog.askopenfilename(title="Choose the expected output file")
    if file:
        Shift_Fold_Signal(file, rx, ry)
    show(rx, ry, "Shifted Folded")
    plt.show()


def remove_dc():
    file = filedialog.askopenfilename(title="Choose a signal")
    x, y = read_signal(file)
    total = 0
    for v in y:
        total = total + v
    mean = total / len(y)
    result = []
    for v in y:
        result.append(v - mean)
    file = filedialog.askopenfilename(title="Choose the expected output file")
    if file:
        SignalsAreEqual("Remove DC", file, x, result)
    show(x, result, "Remove DC")
    plt.show()
