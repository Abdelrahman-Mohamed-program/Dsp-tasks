import subprocess
import sys
import tkinter as tk

root = tk.Tk()
root.title("DSP Tasks")
root.geometry("220x320")

tk.Button(root, text="adding signals", command=lambda: subprocess.Popen([sys.executable, "main.py"], cwd="task 1")).pack(pady=10)
tk.Button(root, text="quantization", command=lambda: subprocess.Popen([sys.executable, "main.py"], cwd="task 2")).pack(pady=10)
tk.Button(root, text="frequency domain", command=lambda: subprocess.Popen([sys.executable, "main.py"], cwd="task 3")).pack(pady=10)
tk.Button(root, text="time domain", command=lambda: subprocess.Popen([sys.executable, "main.py"], cwd="task 4")).pack(pady=10)
tk.Button(root, text="convolution", command=lambda: subprocess.Popen([sys.executable, "main.py"], cwd="task 5")).pack(pady=10)

root.mainloop()
