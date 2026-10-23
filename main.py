import subprocess
import sys
import tkinter as tk

root = tk.Tk()
root.title("DSP Tasks")
root.geometry("200x150")

tk.Button(root, text="adding signals", command=lambda: subprocess.Popen([sys.executable, "main.py"], cwd="task 1")).pack(pady=20)
tk.Button(root, text="quantization", command=lambda: subprocess.Popen([sys.executable, "main.py"], cwd="task 2")).pack(pady=20)

root.mainloop()
