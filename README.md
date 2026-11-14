# Dsp-tasks

All tasks run from one window:

```
python3 main.py
```

## Task 2

Arithmetic operations (subtraction, squaring, normalization, accumulation) and quantization.

Testing (after each operation the app asks for the expected output file and prints the result in the terminal):

- Subtraction: pick Signal2 then Signal1, expected file `OUTPUT Arithmetic operations/signal1-signal2.txt` (same for signal3: pick signal3 then Signal1, expected `signal1-signal3.txt`)
- Squaring: Signal1, expected `Output squaring signal 1.txt`
- Normalization: Signal1 with -1, expected `normalize of signal 1 (from -1 to 1)-- output.txt`. Signal2 with 0, expected `normlize signal 2 (from 0 to 1 )-- output.txt`
- Accumulation: Signal1, expected `output accumulation for signal1.txt`
- Quantization test 1: `Quantization/Quan1_input.txt`, choose bits = 3, expected `Quantization/Quan1_Out.txt`
- Quantization test 2: `Quantization/Quan2_input.txt`, choose levels = 4, expected `Quantization/Quan2_Out.txt`
