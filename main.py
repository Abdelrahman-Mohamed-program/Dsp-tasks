import os
import sys
import tkinter as tk

BASE = os.path.dirname(os.path.abspath(__file__))
for folder in ["task 1", "task 2", "task 3", "task 4", "task 5", "task 6"]:
    sys.path.append(os.path.join(BASE, folder))

import task1
import task2
import task3
import task4
import task5
import task6


def run(folder, function):
    # open the file dialogs in that task's folder (task 1's test also needs this)
    os.chdir(os.path.join(BASE, folder))
    function()


def section(column, text):
    frame = tk.LabelFrame(column, text=text)
    frame.pack(pady=10, padx=10, fill="x")
    return frame


def button(frame, text, folder, function):
    tk.Button(frame, text=text, command=lambda: run(folder, function)).pack(pady=5, padx=10, fill="x")


root = tk.Tk()
root.title("DSP Framework")

left = tk.Frame(root)
left.pack(side="left", anchor="n")
middle = tk.Frame(root)
middle.pack(side="left", anchor="n")
right = tk.Frame(root)
right.pack(side="left", anchor="n")

signals = section(left, "Signals")
button(signals, "Display Signal", "task 1", task1.display)

arithmetic = section(left, "Arithmetic Operations")
button(arithmetic, "Addition", "task 1", task1.addition)
button(arithmetic, "Subtraction", "task 2", task2.subtraction)
button(arithmetic, "Multiplication", "task 1", task1.multiplication)
button(arithmetic, "Squaring", "task 2", task2.squaring)
button(arithmetic, "Normalization", "task 2", task2.normalization)
button(arithmetic, "Accumulation", "task 2", task2.accumulation)

quantization = section(left, "Quantization")
button(quantization, "Quantize Signal", "task 2", task2.quantization)

time = section(middle, "Time Domain")
button(time, "Smoothing", "task 4", task4.smoothing)
button(time, "Sharpening", "task 4", task4.sharpening)
button(time, "Delay or Advance", "task 4", task4.delay_or_advance)
button(time, "Folding", "task 4", task4.folding)
button(time, "Delay or Advance Folded", "task 4", task4.shift_folded)
button(time, "Remove DC", "task 4", task4.remove_dc)

convolution = section(middle, "Convolution")
button(convolution, "Convolve Two Signals", "task 5", task5.convolution)

correlation = section(middle, "Correlation")
button(correlation, "Cross Correlation", "task 6", task6.cross_correlation)
button(correlation, "Auto Correlation", "task 6", task6.auto_correlation)
button(correlation, "Time Delay", "task 6", task6.time_delay)

frequency = section(right, "Frequency Domain")
button(frequency, "DFT", "task 3", task3.dft)
button(frequency, "Modify Component", "task 3", task3.modify)
button(frequency, "Reconstruct (IDFT)", "task 3", task3.reconstruct)
button(frequency, "Remove DC", "task 3", task3.remove_dc)
button(frequency, "IDFT from file", "task 3", task3.idft)

root.mainloop()
