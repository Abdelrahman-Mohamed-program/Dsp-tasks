import os
from tkinter import filedialog, simpledialog
import matplotlib.pyplot as plt
from Task1Test import AddSignalSamplesAreEqual, MultiplySignalByConst


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


def display():
    files = filedialog.askopenfilenames(title="Choose signals")
    for file in files:
        x, y = read_signal(file)
        show(x, y, "Signal")
    plt.show()


def addition():
    file1 = filedialog.askopenfilename(title="Choose the first signal")
    file2 = filedialog.askopenfilename(title="Choose the second signal")
    x1, y1 = read_signal(file1)
    x2, y2 = read_signal(file2)
    result = []
    for i in range(min(len(y1), len(y2))):
        result.append(y1[i] + y2[i])
    if len(y1) > len(y2):
        x = x1
        for i in range(len(y2), len(y1)):
            result.append(y1[i])
    else:
        x = x2
        for i in range(len(y1), len(y2)):
            result.append(y2[i])
    AddSignalSamplesAreEqual(os.path.basename(file1), os.path.basename(file2), x, result)
    show(x, result, "Addition")
    plt.show()


def multiplication():
    file = filedialog.askopenfilename(title="Choose a signal")
    c = simpledialog.askfloat("Multiplication", "Enter constant:")
    x, y = read_signal(file)
    result = []
    for v in y:
        result.append(v * c)
    MultiplySignalByConst(c, x, result)
    show(x, result, "Multiplication")
    plt.show()
