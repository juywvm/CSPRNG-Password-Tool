# Truly Randomized Password Generator

A secure, terminal-based password generator written in Python. It generates passwords using operating system-level randomness instead of standard time-based algorithms, making the outputs completely unpredictable.

## Why Truly Randomized?

Most standard password generators use the computer's clock to generate random numbers. If someone knows the exact time a password was generated, they can potentially recreate it. This tool uses Python's `secrets` module. It pulls random data from the OS itself, making it impossible to predict or reverse-engineer the result.

## Why is it unpredictable?

To make guessing mathematically impossible, the script uses a few specific methods:

* **Hardware Noise over Math (`secrets` module):** It doesn't use math equations to generate random numbers. Instead, it pulls data from unpredictable physical events inside your machine (like micro-fluctuations in CPU voltage or kernel operations).
* **Zero Modulo Bias (`secrets.randbelow`):** Standard random functions often have a slight bias, picking certain characters slightly more often than others. `randbelow` ensures every single character in your pool has the exact same mathematical probability of being chosen.
* **The Double Shuffle (`SystemRandom().shuffle`):** Picking random characters isn't enough. After the script selects the characters, it shuffles the entire string using the Fisher-Yates algorithm, powered by that same hardware-level noise. This destroys any microscopic sequence patterns before you even see the password.
* **Massive Pool Sizes:** By allowing you to mix obscure alphabets (like Georgian or Amharic) with standard symbols, the combination pool becomes so massive that typical dictionary attacks or brute-force attempts become physically impossible to complete.

## RAM Wiping

Usually, when a script finishes running, the generated data stays in your computer's memory (RAM) until it gets overwritten by something else. To prevent memory scraping, this tool uses the `ctypes` library to find the exact memory address of your password and overwrites it with random bytes the moment you are done.

## Secure Shredding

If you choose to save your passwords locally, they are stored as `.vault` files. Normal file deletion does not actually remove the data from your drive. The shred feature in this tool overwrites the physical file with random bytes before deleting it, ensuring that no data recovery software can restore your files.

## Usage

No external libraries are required. Simply run the script:

```bash
python main.py
```

## Note: The README file is AI-generated, but the source code is entirely my own original work. Online tools was used exclusively to format the code and improve readability.
