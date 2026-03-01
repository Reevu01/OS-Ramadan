#!/usr/bin/env python3
"""
driver.py – Driver program for CS4348 Project 1.

Usage: python3 driver.py <logfile>

Launches logger.py and encryption.py as child processes connected via pipes.
Presents an interactive menu: password, encrypt, decrypt, history, quit.
"""

import sys
import subprocess


# --------------------------------------------------------------------------- #
# Helpers for communicating with child processes
# --------------------------------------------------------------------------- #

def send_log(logger_proc, action, message=""):
    """Send a log message to the logger process."""
    msg = f"{action} {message}\n" if message else f"{action}\n"
    logger_proc.stdin.write(msg)
    logger_proc.stdin.flush()


def send_to_enc(enc_proc, cmd):
    """Send a command to the encryption process and return its response line."""
    enc_proc.stdin.write(cmd + "\n")
    enc_proc.stdin.flush()
    return enc_proc.stdout.readline().rstrip('\n')


def only_letters(s):
    """Return True if s is non-empty and contains only ASCII letters."""
    return bool(s) and s.isalpha()


# --------------------------------------------------------------------------- #
# History menu helper
# --------------------------------------------------------------------------- #

def pick_from_history(history):
    """
    Display the history as a numbered menu.
    Returns the selected string, or None if the user chooses to enter a new one.
    """
    print("  0. Enter a new string")
    for i, item in enumerate(history, 1):
        print(f"  {i}. {item}")
    choice = input("Select (0 for new): ").strip()
    if choice == "0":
        return None
    try:
        idx = int(choice)
        if 1 <= idx <= len(history):
            return history[idx - 1]
    except ValueError:
        pass
    print("Invalid selection. Entering new string.")
    return None


# --------------------------------------------------------------------------- #
# Main driver
# --------------------------------------------------------------------------- #

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 driver.py <logfile>", file=sys.stderr)
        sys.exit(1)

    logfile = sys.argv[1]
    history = []

    # Launch the logger
    logger_proc = subprocess.Popen(
        ["python3", "logger.py", logfile],
        stdin=subprocess.PIPE,
        text=True
    )

    # Launch the encryption program
    enc_proc = subprocess.Popen(
        ["python3", "encryption.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )

    send_log(logger_proc, "START", "Driver started.")

    while True:
        print("\nCommands: password, encrypt, decrypt, history, quit")
        try:
            command = input("> ").strip().lower()
        except EOFError:
            command = "quit"

        # ------------------------------------------------------------------ #
        # quit
        # ------------------------------------------------------------------ #
        if command == "quit":
            send_log(logger_proc, "QUIT", "Driver exiting.")
            send_to_enc(enc_proc, "QUIT")
            logger_proc.stdin.write("QUIT\n")
            logger_proc.stdin.flush()
            logger_proc.stdin.close()
            enc_proc.stdin.close()
            logger_proc.wait()
            enc_proc.wait()
            print("Goodbye!")
            break

        # ------------------------------------------------------------------ #
        # password
        # ------------------------------------------------------------------ #
        elif command == "password":
            send_log(logger_proc, "PASSWORD", "User setting password.")
            passkey = None

            if history:
                opt = input("Use history (h) or enter new (n)? ").strip().lower()
                if opt == "h":
                    passkey = pick_from_history(history)

            if passkey is None:
                passkey = input("Enter password: ").strip()

            if not only_letters(passkey):
                print("Error: Password must contain only letters.")
                send_log(logger_proc, "ERROR", "Invalid password entered.")
            else:
                send_to_enc(enc_proc, f"PASSKEY {passkey.upper()}")
                send_log(logger_proc, "PASSKEY", "Password updated.")
                print("Password set successfully.")

        # ------------------------------------------------------------------ #
        # encrypt
        # ------------------------------------------------------------------ #
        elif command == "encrypt":
            send_log(logger_proc, "ENCRYPT", "User requested encryption.")
            text = None

            if history:
                opt = input("Use history (h) or enter new (n)? ").strip().lower()
                if opt == "h":
                    text = pick_from_history(history)

            if text is None:
                text = input("Enter string to encrypt: ").strip()
                if only_letters(text):
                    history.append(text.upper())

            if not only_letters(text):
                print("Error: Input must contain only letters (no spaces or special characters).")
                send_log(logger_proc, "ERROR", "Invalid input for encryption.")
            else:
                resp = send_to_enc(enc_proc, f"ENCRYPT {text.upper()}")
                print(f"Result: {resp}")
                send_log(logger_proc, "RESULT", resp)
                parts = resp.split(None, 1)
                if len(parts) == 2 and parts[0] == "RESULT":
                    history.append(parts[1])

        # ------------------------------------------------------------------ #
        # decrypt
        # ------------------------------------------------------------------ #
        elif command == "decrypt":
            send_log(logger_proc, "DECRYPT", "User requested decryption.")
            text = None

            if history:
                opt = input("Use history (h) or enter new (n)? ").strip().lower()
                if opt == "h":
                    text = pick_from_history(history)

            if text is None:
                text = input("Enter string to decrypt: ").strip()
                if only_letters(text):
                    history.append(text.upper())

            if not only_letters(text):
                print("Error: Input must contain only letters (no spaces or special characters).")
                send_log(logger_proc, "ERROR", "Invalid input for decryption.")
            else:
                resp = send_to_enc(enc_proc, f"DECRYPT {text.upper()}")
                print(f"Result: {resp}")
                send_log(logger_proc, "RESULT", resp)
                parts = resp.split(None, 1)
                if len(parts) == 2 and parts[0] == "RESULT":
                    history.append(parts[1])

        # ------------------------------------------------------------------ #
        # history
        # ------------------------------------------------------------------ #
        elif command == "history":
            send_log(logger_proc, "HISTORY", "User viewing history.")
            if not history:
                print("History is empty.")
            else:
                print("History:")
                for i, item in enumerate(history, 1):
                    print(f"  {i}. {item}")

        # ------------------------------------------------------------------ #
        # unknown
        # ------------------------------------------------------------------ #
        else:
            if command:
                print("Unknown command. Try: password, encrypt, decrypt, history, quit")


if __name__ == "__main__":
    main()
