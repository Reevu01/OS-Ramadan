#!/usr/bin/env python3
"""
encryption.py – Encryption/decryption program for CS4348 Project 1.

Reads commands from standard input and writes responses to standard output.
Commands:
    PASSKEY <key>     – Set the current passkey.
    ENCRYPT <text>    – Encrypt text using the Vigenère cipher with the current passkey.
    DECRYPT <text>    – Decrypt text using the Vigenère cipher with the current passkey.
    QUIT              – Exit the program.

Responses:
    RESULT [value]    – Command succeeded.
    ERROR <message>   – Command failed.

The Vigenère cipher only operates on letters (A-Z). Input is assumed to be uppercase.
"""

import sys


def vigenere_encrypt(plaintext, key):
    """Encrypt plaintext using a Vigenère cipher with the given key."""
    result = []
    key_idx = 0
    for ch in plaintext:
        if ch.isalpha():
            p = ord(ch.upper()) - ord('A')
            k = ord(key[key_idx % len(key)].upper()) - ord('A')
            c = (p + k) % 26
            result.append(chr(c + ord('A')))
            key_idx += 1
        else:
            result.append(ch)
    return ''.join(result)


def vigenere_decrypt(ciphertext, key):
    """Decrypt ciphertext using a Vigenère cipher with the given key."""
    result = []
    key_idx = 0
    for ch in ciphertext:
        if ch.isalpha():
            c = ord(ch.upper()) - ord('A')
            k = ord(key[key_idx % len(key)].upper()) - ord('A')
            p = (c - k + 26) % 26
            result.append(chr(p + ord('A')))
            key_idx += 1
        else:
            result.append(ch)
    return ''.join(result)


def main():
    passkey = None

    for line in sys.stdin:
        line = line.rstrip('\n').strip()
        if not line:
            continue

        parts = line.split(None, 1)
        command = parts[0]
        argument = parts[1] if len(parts) > 1 else ""

        if command == "QUIT":
            break

        elif command == "PASSKEY":
            passkey = argument
            print("RESULT")
            sys.stdout.flush()

        elif command == "ENCRYPT":
            if passkey is None:
                print("ERROR Password not set")
            else:
                encrypted = vigenere_encrypt(argument, passkey)
                print(f"RESULT {encrypted}")
            sys.stdout.flush()

        elif command == "DECRYPT":
            if passkey is None:
                print("ERROR Password not set")
            else:
                decrypted = vigenere_decrypt(argument, passkey)
                print(f"RESULT {decrypted}")
            sys.stdout.flush()

        else:
            print(f"ERROR Unknown command: {command}")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
