import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from ConvTest import ConvTest


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


def convolution():
    file1 = filedialog.askopenfilename(title="Choose the first signal")
    file2 = filedialog.askopenfilename(title="Choose the second signal")
    x1, y1 = read_signal(file1)
    x2, y2 = read_signal(file2)
    x = []
    result = []
    for n in range(len(y1) + len(y2) - 1):
        x.append(x1[0] + x2[0] + n)
        result.append(0)
    for i in range(len(y1)):
        for j in range(len(y2)):
            result[i + j] = result[i + j] + y1[i] * y2[j]
    ConvTest(x, result)
    show(x, result, "Convolution")
    plt.show()


root = tk.Tk()
root.title("Task 5")
root.geometry("250x350")

ops = tk.LabelFrame(root, text="Convolution")
ops.pack(pady=10, padx=10, fill="x")
tk.Button(ops, text="Convolve Two Signals", command=convolution).pack(pady=5)

root.mainloop()
