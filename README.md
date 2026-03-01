# CS4348 Project 1 — Vigenère Cipher System

## Files

| File | Description |
|------|-------------|
| `driver.py` | **Main program.** Launch this to run the system. Starts the logger and encryption program as child processes, then presents an interactive menu. |
| `encryption.py` | **Encryption/decryption program.** Reads commands from stdin, replies to stdout. Implements the Vigenère cipher. |
| `logger.py` | **Logger program.** Reads log messages from stdin, writes timestamped entries to a log file. |
| `devlog.md` | Development log with day-by-day entries documenting the project's progress. |

## How to Compile / Run

No compilation is required — the project is written in Python 3.

### Run the system

```bash
python3 driver.py <logfile>
```

Example:

```bash
python3 driver.py activity.log
```

The driver will launch `logger.py` and `encryption.py` automatically (they must be in the same directory).

### Run the logger standalone (for testing)

```bash
python3 logger.py <logfile>
```

Type log messages in the format `ACTION message`, one per line. Send `QUIT` to stop.

### Run the encryption program standalone (for testing)

```bash
python3 encryption.py
```

Type commands: `PASSKEY <key>`, `ENCRYPT <text>`, `DECRYPT <text>`, `QUIT`.

## Usage

Once the driver is running, you will see:

```
Commands: password, encrypt, decrypt, history, quit
>
```

| Command | Description |
|---------|-------------|
| `password` | Set the encryption passkey. You may type a new string or select one from the history. Passwords are **not** stored in the history. |
| `encrypt` | Encrypt a string using the current passkey. You may type a new string or select one from the history. The input and result are both saved in the history. |
| `decrypt` | Decrypt a string using the current passkey. You may type a new string or select one from the history. The input and result are both saved in the history. |
| `history` | Display all strings currently in the history. |
| `quit` | Exit the program. Sends `QUIT` to both child processes before exiting. |

## Input Rules

- All input strings for `password`, `encrypt`, and `decrypt` must contain **only letters** (A-Z, case insensitive).
- Spaces, digits, and special characters are **not** allowed.
- Input is automatically converted to uppercase before processing.

## Notes for the TA

- Python 3 standard library only — no external packages needed.
- Tested on Linux. Works on cs1/cs2 machines.
- `logger.py` appends to the log file (so multiple runs accumulate in the same file).
- The encryption program flushes stdout after every response to prevent pipe buffering issues.
- Passwords are never written to the log file.
