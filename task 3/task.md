# Task 3: Frequency Domain — Code Explanation

## 1. Imported Libraries

```python
import cmath
import math
import tkinter as tk
from tkinter import filedialog, simpledialog
import matplotlib.pyplot as plt
```

- **cmath:** Handles complex numbers, calculates their phase, and converts amplitude and phase into complex numbers.
- **math:** Provides mathematical constants and functions, such as pi.
- **tkinter:** Creates the graphical interface and its buttons.
- **filedialog:** Allows the user to select files.
- **simpledialog:** Asks the user to enter values, such as the sampling frequency.
- **matplotlib:** Displays the signals and frequency-domain graphs.

The remaining imports are used to compare our results with the expected test-case results.

```python
from signalcompare import SignalComapreAmplitude, SignalComaprePhaseShift
from CompareSignals import SignalsAreEqual
```

- `SignalComapreAmplitude` compares the calculated amplitudes with the expected amplitudes.
- `SignalComaprePhaseShift` compares the calculated phases with the expected phases.
- `SignalsAreEqual` checks whether the resulting signal matches the expected signal.

## 2. Global Variables

```python
amplitudes = []
phases = []
fs = 1
```

- `amplitudes`: Stores the magnitudes of the frequency components.
- `phases`: Stores the phase angles of the frequency components in radians.
- `fs`: Stores the sampling frequency entered by the user.

These variables are global because multiple functions need to access the same frequency-domain data.

## 3. Reading a Signal from a File

```python
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
```

This function reads a signal from a file.

**How it works:**

1. Opens the selected file.
2. Reads all its lines.
3. Skips the first three header lines.
4. Reads the first column as the sample indices and stores them in `x`.
5. Reads the second column as the signal values and stores them in `y`.
6. Returns both lists.

We use `x` for the sample indices and `y` for the actual signal values.

## 4. Reading Amplitude and Phase from a File

```python
def read_spectrum(path):
    f = open(path)
    lines = f.readlines()
    f.close()
    a = []
    p = []
    for line in lines[3:]:
        parts = line.replace("f", "").split()
        a.append(float(parts[0]))
        p.append(float(parts[1]))
    return a, p
```

This function reads a frequency spectrum from a file.

It skips the first three header lines, then reads:
- The first column into `a`, representing amplitudes.
- The second column into `p`, representing phases.

The `replace("f", "")` removes the letter `f` from the line before splitting it into values.

Finally, it returns the amplitude and phase lists.

## 5. Displaying a Signal

```python
def show(x, y, title):
    plt.subplot(1, 2, 1)
    plt.plot(x, y)
    plt.title(title + " (continuous)")
    plt.subplot(1, 2, 2)
    plt.stem(x, y)
    plt.title(title + " (discrete)")
```

This function displays a signal in two ways.

- `plt.subplot(1, 2, 1)` creates the first plot.
- `plt.plot(x, y)` displays the signal as a connected curve.
- `plt.subplot(1, 2, 2)` creates the second plot.
- `plt.stem(x, y)` displays the individual discrete samples.

The `title` parameter determines the titles of the two plots.

This function is used to visualize the original or reconstructed signal.

## 6. Displaying the Frequency Spectrum

```python
def show_spectrum():
    N = len(amplitudes)
    peak = max(amplitudes)
    freqs = []
    normalized = []
```

First, the function gets the number of frequency components, finds the maximum amplitude, and creates two empty lists.

- `freqs` stores the frequencies in Hz.
- `normalized` stores the normalized amplitudes.

### Calculating frequencies and normalized amplitudes

```python
for k in range(N):
    freqs.append(k * fs / N)
    normalized.append(amplitudes[k] / peak)
```

The frequency of each component is calculated using:

**Frequency = (component index × sampling frequency) / number of samples**

The amplitude is normalized by dividing each amplitude by the maximum amplitude.

This makes the largest normalized amplitude equal to 1.

### Finding dominant frequencies

```python
print("Dominant frequencies:")
for k in range(N):
    if normalized[k] > 0.5:
        print(freqs[k], "Hz")
```

The function checks every normalized amplitude.

If an amplitude is greater than 0.5, the corresponding frequency is displayed as a dominant frequency.

### Plotting the spectrum

```python
plt.subplot(1, 2, 1)
plt.stem(freqs, normalized)
plt.title("Frequency vs Amplitude")

plt.subplot(1, 2, 2)
plt.stem(freqs, phases)
plt.title("Frequency vs Phase")

plt.show()
```

The first graph displays frequency versus normalized amplitude.

The second graph displays frequency versus phase.

This function therefore handles frequency calculation, amplitude normalization, dominant-frequency detection, and spectrum visualization.

## 7. The Main Fourier Function: DFT and IDFT

```python
def fourier(values, inverse):
    N = len(values)
    sign = -1
    if inverse:
        sign = 1
    result = []
    for k in range(N):
        total = 0
        for n in range(N):
            total = total + values[n] * cmath.exp(
                sign * 2j * math.pi * k * n / N
            )
        if inverse:
            total = total / N
        result.append(total)
    return result
```

**This is the most important function in the program.**

It performs both the Discrete Fourier Transform (DFT) and the Inverse Discrete Fourier Transform (IDFT).

The `values` parameter contains the input data, and `inverse` determines which transformation to perform.

### Step 1: Get the number of samples

```python
N = len(values)
```

Counts the input values.

### Step 2: Choose the sign

```python
sign = -1
if inverse:
    sign = 1
```

For DFT, the sign is negative.

For IDFT, the sign is positive.

### Step 3: Calculate each output component

```python
for k in range(N):
    total = 0
    for n in range(N):
        total = total + values[n] * cmath.exp(
            sign * 2j * math.pi * k * n / N
        )
```

The outer loop goes through each output component.

The inner loop processes every input value and adds its contribution to the current output.

The complex exponential performs the mathematical operation required by the Fourier transform.

### Step 4: Apply IDFT scaling

```python
if inverse:
    total = total / N
```

For IDFT, the result is divided by the number of samples.

This division is required by the inverse-transform formula.

### Step 5: Store the result

```python
result.append(total)
return result
```

Each calculated component is added to the result list, which is returned after all components have been processed.

### Why use one function for DFT and IDFT?

The two formulas are very similar. They differ in the sign of the exponent and the scaling factor.

Instead of writing two separate algorithms, we use the `inverse` parameter to control these differences.

This directly satisfies the task's hint about using one smart function for both transformations.

## 8. Converting a Signal into Amplitude and Phase

```python
def to_spectrum(samples):
    a = []
    p = []
    for c in fourier(samples, False):
        a.append(abs(c))
        p.append(cmath.phase(c))
    return a, p
```

This function converts the original signal into its frequency-domain representation.

**How it works:**

1. Calls `fourier(samples, False)` to calculate the DFT.
2. Uses `abs(c)` to calculate the magnitude of each complex component.
3. Uses `cmath.phase(c)` to calculate its phase in radians.
4. Stores the magnitudes in `a` and phases in `p`.
5. Returns both lists.

The function separates the DFT results into the amplitude and phase information needed by the rest of the program.

## 9. Reconstructing a Signal from Amplitude and Phase

```python
def to_signal(a, p):
    values = []
    for k in range(len(a)):
        values.append(cmath.rect(a[k], p[k]))
    samples = []
    for c in fourier(values, True):
        samples.append(c.real)
    return samples
```

This function performs the reverse operation.

It takes amplitude and phase values and reconstructs the signal.

### Step 1: Convert amplitude and phase into complex numbers

```python
values.append(cmath.rect(a[k], p[k]))
```

`cmath.rect()` converts each amplitude and phase pair into a complex number.

These complex numbers represent the frequency components.

### Step 2: Apply IDFT

```python
for c in fourier(values, True):
```

Calls the shared Fourier function in inverse mode to reconstruct the signal.

### Step 3: Extract the real part

```python
samples.append(c.real)
```

Stores the real part of each reconstructed sample.

Finally, the function returns the reconstructed signal.

## 10. The DFT Button Function

```python
def dft():
    global amplitudes, phases, fs
    file = filedialog.askopenfilename(title="Choose a signal")
    fs = simpledialog.askfloat("DFT", "Sampling frequency (Hz):")
    x, y = read_signal(file)
    amplitudes, phases = to_spectrum(y)
```

This function connects the DFT algorithm to the graphical interface.

It:
1. Asks the user to select a signal file.
2. Asks the user to enter the sampling frequency.
3. Reads the signal.
4. Calculates its amplitude and phase using `to_spectrum()`.
5. Stores the results in the global variables.

Next, it asks the user to select the expected output file.

```python
file = filedialog.askopenfilename(title="Choose the expected output file")
if file:
    a, p = read_spectrum(file)
```

The expected amplitude and phase values are loaded from the selected file.

The calculated and expected amplitudes are rounded to three decimal places before comparison.

```python
if SignalComapreAmplitude(mine, expected) and SignalComaprePhaseShift(phases, p):
    print("DFT Test case passed successfully")
else:
    print("DFT Test case failed")
```

The program compares the calculated amplitudes and phases with the expected results.

It prints whether the DFT test case passed or failed.

Finally:

```python
show_spectrum()
```

Displays the frequency-domain graphs and dominant frequencies.

## 11. Modifying a Frequency Component

```python
def modify():
    k = simpledialog.askinteger(
        "Modify",
        "Component index (0 to " + str(len(amplitudes) - 1) + "):"
    )
    amplitudes[k] = simpledialog.askfloat("Modify", "New amplitude:")
    phases[k] = simpledialog.askfloat("Modify", "New phase (radians):")
    show_spectrum()
```

This function lets the user modify the amplitude and phase of a frequency component.

It:
1. Asks the user to select a component index.
2. Asks for its new amplitude.
3. Asks for its new phase in radians.
4. Updates the amplitude and phase lists.
5. Displays the updated spectrum.

The updated values are used when reconstructing the signal.

## 12. Removing the DC Component

```python
def remove_dc():
    file = filedialog.askopenfilename(title="Choose a signal")
    x, y = read_signal(file)
    a, p = to_spectrum(y)
    a[0] = 0
    p[0] = 0
    result = to_signal(a, p)
```

This function removes the DC component from a signal.

The DC component is the zero-frequency component, which is located at index zero.

The function:
1. Reads the original signal.
2. Calculates its amplitude and phase.
3. Sets the amplitude at index zero to zero.
4. Sets its phase to zero.
5. Reconstructs the signal using the modified spectrum.

It then asks the user to select the expected output file.

```python
if file:
    SignalsAreEqual("Remove DC", file, x, result)
```

This compares the reconstructed signal with the expected output.

Finally, the resulting signal is displayed using `show()`.

## 13. IDFT from a File

```python
def idft():
    file = filedialog.askopenfilename(title="Choose an amplitude/phase file")
    a, p = read_spectrum(file)
    result = to_signal(a, p)
```

This function reconstructs a signal using amplitude and phase values loaded from a file.

It:
1. Asks the user to select an amplitude/phase file.
2. Reads the amplitude and phase values.
3. Calls `to_signal()` to reconstruct the signal.

Next, it creates sample indices for the reconstructed signal.

```python
x = []
for n in range(len(result)):
    x.append(n)
```

Then it asks the user to select the expected output file and compares the reconstructed signal with the expected result using `SignalsAreEqual()`.

Finally, it displays the reconstructed signal.

**Difference between `idft()` and `reconstruct()`:** `idft()` reads amplitude and phase from a file, whereas `reconstruct()` uses the amplitude and phase already stored in the program.

## 14. Reconstructing the Current Signal

```python
def reconstruct():
    result = to_signal(amplitudes, phases)
    x = []
    for n in range(len(result)):
        x.append(n)
    show(x, result, "Reconstructed")
    plt.show()
```

This function reconstructs a signal from the current amplitude and phase arrays.

It:
1. Calls `to_signal()` to perform IDFT.
2. Creates sample indices.
3. Displays the reconstructed signal.

If the frequency components have been modified, the reconstructed signal reflects those changes.

## 15. Creating the Graphical Interface

```python
root = tk.Tk()
root.title("Task 3")
root.geometry("250x350")
```

This creates the main application window, sets its title, and defines its size.

```python
ops = tk.LabelFrame(root, text="Frequency Domain")
ops.pack(pady=10, padx=10, fill="x")
```

Creates a labeled section called **Frequency Domain**.

The following statements create the buttons:

```python
tk.Button(ops, text="DFT", command=dft).pack(pady=5)
tk.Button(ops, text="Modify Component", command=modify).pack(pady=5)
tk.Button(ops, text="Reconstruct (IDFT)", command=reconstruct).pack(pady=5)
tk.Button(ops, text="Remove DC", command=remove_dc).pack(pady=5)
tk.Button(ops, text="IDFT from file", command=idft).pack(pady=5)
```

Each button calls its corresponding function when clicked.

Finally:

```python
root.mainloop()
```

Starts the GUI event loop and keeps the application running until the user closes it.

# Final Summary

The program implements all the main features of the Frequency Domain task:

1. **DFT:** Converts a signal into frequency components.
2. **Amplitude and phase:** Extracts the magnitude and phase of each component.
3. **Frequency spectrum:** Calculates frequencies in Hz and displays amplitude and phase graphs.
4. **Dominant frequencies:** Displays components whose normalized amplitudes exceed 0.5.
5. **Component modification:** Allows the user to modify amplitude and phase.
6. **DC removal:** Removes the zero-frequency component.
7. **IDFT:** Reconstructs a signal from its frequency components.
8. **Testing:** Compares calculated results with expected output files.
9. **GUI:** Provides buttons for accessing the different operations.

The most important functions to understand are `fourier()`, `to_spectrum()`, `to_signal()`, and `show_spectrum()`. The remaining functions connect these operations to the files, test cases, plots, and GUI.