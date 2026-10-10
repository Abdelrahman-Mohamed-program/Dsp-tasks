import os
import tkinter as tk
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
    files = filedialog.askopenfilenames(title="Choose signals")
    x, result = read_signal(files[0])
    for file in files[1:]:
        x2, y2 = read_signal(file)
        for i in range(len(y2)):
            if i < len(result):
                result[i] = result[i] + y2[i]
            else:
                x.append(x2[i])
                result.append(y2[i])
    AddSignalSamplesAreEqual(os.path.basename(files[0]), os.path.basename(files[1]), x, result)
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


root = tk.Tk()
root.title("Task 1")
root.geometry("250x350")

tk.Button(root, text="Display Signal", command=display).pack(pady=10)

ops = tk.LabelFrame(root, text="Arithmetic Operations")
ops.pack(pady=10, padx=10, fill="x")
tk.Button(ops, text="Addition", command=addition).pack(pady=5)
tk.Button(ops, text="Multiplication", command=multiplication).pack(pady=5)

root.mainloop()
