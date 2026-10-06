import tkinter as tk
from tkinter import filedialog, simpledialog
import matplotlib.pyplot as plt
from collections import Counter


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


def show(signals):
    plt.title("Value Repeats")
    plt.xlabel("Value")
    plt.ylabel("Count")
    for x, y in signals:
        counts = Counter(y)
        values = sorted(counts)
        heights = [counts[v] for v in values]
        plt.bar(values, heights, width=0.4)
    plt.show()


def display():
    files = filedialog.askopenfilenames()
    signals = [read_signal(f) for f in files]
    show(signals)


def addition():
    files = filedialog.askopenfilenames()
    total = {}
    for f in files:
        x, y = read_signal(f)
        for xi, yi in zip(x, y):
            total[xi] = total.get(xi, 0) + yi
    x = sorted(total)
    result = [total[xi] for xi in x]
    show([(x, result)])


def multiplication():
    file = filedialog.askopenfilename()
    c = simpledialog.askfloat("Multiply", "Enter constant:")
    x, y = read_signal(file)
    result = [v * c for v in y]
    show([(x, result)])


root = tk.Tk()
root.title("Task 1")
root.geometry("250x350")

tk.Button(root, text="Display Signal", command=display).pack(pady=10)

ops = tk.LabelFrame(root, text="Arithmetic Operations")
ops.pack(pady=10, padx=10, fill="x")
tk.Button(ops, text="Addition", command=addition).pack(pady=5)
tk.Button(ops, text="Multiplication", command=multiplication).pack(pady=5)

root.mainloop()
