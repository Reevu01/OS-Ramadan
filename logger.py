#!/usr/bin/env python3
"""
logger.py – Logging program for CS4348 Project 1.

Accepts a single command-line argument: the name of the log file.
Reads log messages from standard input until it receives "QUIT".
Each message is written to the log file in the format:
    YYYY-MM-DD HH:MM [ACTION] MESSAGE
where ACTION is the first non-whitespace token of the message.
"""

import sys
from datetime import datetime


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 logger.py <logfile>", file=sys.stderr)
        sys.exit(1)

    logfile = sys.argv[1]

    with open(logfile, 'a') as f:
        for line in sys.stdin:
            line = line.rstrip('\n')

            if line.strip() == "QUIT":
                break

            parts = line.split(None, 1)
            if not parts:
                continue

            action = parts[0]
            message = parts[1] if len(parts) > 1 else ""

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            log_entry = f"{timestamp} [{action}] {message}\n"

            f.write(log_entry)
            f.flush()


if __name__ == "__main__":
    main()
