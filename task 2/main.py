import math
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import matplotlib.pyplot as plt
from Task1Test import SignalSamplesAreEqual
from QuanTest1 import QuantizationTest1
from QuanTest2 import QuantizationTest2


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
    plt.plot(x, y, "k")
    plt.axhline(0, color="k")
    plt.title(title + " (continuous)")
    plt.subplot(1, 2, 2)
    plt.stem(x, y, linefmt="k-", markerfmt="ko", basefmt="k-")
    plt.grid(axis="y", linestyle="--")
    plt.title(title + " (discrete)")
    plt.show()


def test(name, x, y):
    file = filedialog.askopenfilename(title="Choose the expected output file (Cancel to skip)")
    if file:
        SignalSamplesAreEqual(name, file, x, y)


def subtraction():
    file1 = filedialog.askopenfilename(title="Choose the first signal")
    file2 = filedialog.askopenfilename(title="Choose the second signal")
    x1, y1 = read_signal(file1)
    x2, y2 = read_signal(file2)
    result = []
    for i in range(min(len(y1), len(y2))):
        result.append(y1[i] - y2[i])
    # the remaining samples from the longer signal go to the result as they are
    if len(y1) > len(y2):
        x = x1
        for i in range(len(y2), len(y1)):
            result.append(y1[i])
    else:
        x = x2
        for i in range(len(y1), len(y2)):
            result.append(y2[i])
    test("Subtraction", x, result)
    show(x, result, "Subtraction")


def squaring():
    file = filedialog.askopenfilename(title="Choose a signal")
    x, y = read_signal(file)
    result = []
    for v in y:
        result.append(v * v)
    test("Squaring", x, result)
    show(x, result, "Squaring")


def normalization():
    file = filedialog.askopenfilename(title="Choose a signal")
    choice = simpledialog.askinteger("Normalization", "Enter 0 for (0 to 1) or -1 for (-1 to 1):")
    x, y = read_signal(file)
    mn = min(y)
    mx = max(y)
    result = []
    for v in y:
        if choice == 0:
            result.append((v - mn) / (mx - mn))
        else:
            result.append(2 * (v - mn) / (mx - mn) - 1)
    test("Normalization", x, result)
    show(x, result, "Normalization")


def accumulation():
    file = filedialog.askopenfilename(title="Choose a signal")
    x, y = read_signal(file)
    result = []
    total = 0
    for v in y:
        total = total + v
        result.append(total)
    test("Accumulation", x, result)
    show(x, result, "Accumulation")


def quantization():
    file = filedialog.askopenfilename(title="Choose a signal")
    use_bits = messagebox.askyesno("Quantization", "Do you want to enter number of bits?\n(Yes = bits, No = levels)")
    if use_bits:
        bits = simpledialog.askinteger("Quantization", "Number of bits:")
        levels = 2 ** bits
    else:
        levels = simpledialog.askinteger("Quantization", "Number of levels:")
        bits = int(math.log2(levels))

    x, y = read_signal(file)
    mn = min(y)
    mx = max(y)
    delta = (mx - mn) / levels

    indices = []
    encoded = []
    quantized = []
    errors = []
    for v in y:
        # find the interval the sample falls in
        index = levels - 1
        for i in range(levels):
            if v <= mn + (i + 1) * delta:
                index = i
                break
        q = mn + index * delta + delta / 2   # midpoint of the interval
        indices.append(index + 1)
        encoded.append(format(index, "0" + str(bits) + "b"))   # index in binary with 'bits' digits
        quantized.append(q)
        errors.append(q - v)

    print("Index  Encoded  Quantized  Error")
    for i in range(len(y)):
        print(indices[i], encoded[i], round(quantized[i], 3), round(errors[i], 3))

    file = filedialog.askopenfilename(title="Choose the expected output file (Cancel to skip)")
    if file:
        if use_bits:
            QuantizationTest1(file, encoded, quantized)
        else:
            QuantizationTest2(file, indices, encoded, quantized, errors)

    plt.subplot(1, 2, 1)
    plt.plot(x, y, label="Original")
    plt.step(x, quantized, where="mid", label="Quantized")
    plt.legend()
    plt.title("Quantized Signal")
    plt.subplot(1, 2, 2)
    plt.stem(x, errors)
    plt.title("Quantization Error")
    plt.show()



root = tk.Tk()
root.title("Task 2")
root.geometry("250x350")

ops = tk.LabelFrame(root, text="Arithmetic Operations")
ops.pack(pady=10, padx=10, fill="x")
tk.Button(ops, text="Subtraction", command=subtraction).pack(pady=5)
tk.Button(ops, text="Squaring", command=squaring).pack(pady=5)
tk.Button(ops, text="Normalization", command=normalization).pack(pady=5)
tk.Button(ops, text="Accumulation", command=accumulation).pack(pady=5)

tk.Button(root, text="Quantization", command=quantization).pack(pady=10)

root.mainloop()
