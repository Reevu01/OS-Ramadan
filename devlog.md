# Development Log

---

## 2025-02-28 14:12

### Thoughts So Far

Just got the project assignment. Reading through both PDFs right now. The project is for CS4348 Operating Systems and is due March 13th, 2025. I have about two weeks, which feels okay, but I want to start early so I am not rushing at the end.

The project requires building three separate programs that talk to each other through pipes:
1. **Logger** – reads log messages from stdin, writes them with a timestamp to a log file.
2. **Encryption program** – uses a Vigenère cipher to encrypt or decrypt strings. Takes commands from stdin, outputs results to stdout.
3. **Driver** – the main program the user runs. It launches the logger and encryption program as child processes, connects to them with pipes, and handles a menu-driven interface.

The grading breakdown is interesting:
- 30 pts for following specs
- 20 pts for passing tests
- **50 pts for devlog/commit history**

That last one is huge. Half the grade is the devlog and commit history, so I need to be consistent about writing entries and committing often. I am going to keep this file open while I code.

### Plan for This Session

I just want to read the project description carefully and figure out my approach before I write any code. Key things to decide:
- **Language**: I am going to use Python because the project says to use the `subprocess` module for Python, and I feel comfortable with Python.
- **Architecture**: I need to understand exactly how the three programs talk to each other.

### Notes While Reading

**Logger program:**
- Takes a single command-line argument: the log file name.
- Reads lines from stdin. First word is the action, rest is the message.
- Formats each line as: `YYYY-MM-DD HH:MM [ACTION] MESSAGE`
- Stops when it receives "QUIT".

**Encryption program:**
- Commands arrive on stdin, responses go to stdout.
- Commands: `PASSKEY <key>`, `ENCRYPT <text>`, `DECRYPT <text>`, `QUIT`
  - Note: the spec heading says "PASS" but the example in the PDF shows `PASSKEY HELLO`. Going with `PASSKEY`.
- Responses start with `RESULT` (success) or `ERROR` (failure).
- Vigenère cipher: only works on letters, case insensitive. All uppercase assumed for the encryption backend.
- No passkey set → ENCRYPT/DECRYPT returns `ERROR Password not set`.

**Vigenère cipher** (I need to look this up on Wikipedia):
- It is a polyalphabetic substitution cipher using a keyword.
- Encryption: `C_i = (P_i + K_i) mod 26` (where letters are 0-25)
- Decryption: `P_i = (C_i - K_i + 26) mod 26`
- Example from spec: `PASSKEY HELLO`, then `ENCRYPT HELLO` → `OIWWC`
  - H+H = 7+7 = 14 = O ✓
  - E+E = 4+4 = 8 = I ✓
  - L+L = 11+11 = 22 = W ✓
  - L+L = 22 = W ✓
  - O+O = 14+14 = 28 mod 26 = 2 = C ✓
  - Great, my understanding is correct.

**Driver program:**
- Starts logger and encryption as subprocesses with pipes.
- Presents a menu: `password`, `encrypt`, `decrypt`, `history`, `quit`.
- Maintains a history of strings (all entered strings and results, but NOT passwords).
- Passwords are never logged.
- Input validation: only letters allowed, case insensitive (convert to uppercase before sending to encryption program).

### End-of-Session Reflection

Good planning session. I have a clear picture of what to build. Tomorrow I will start with the logger since it is the simplest piece. I want to make sure my understanding of the timestamp format is right: `YYYY-MM-DD HH:MM [ACTION] MESSAGE`.

The trickiest part will probably be the driver's subprocess/pipe management. I remember from class that `subprocess.Popen` lets you set `stdin=subprocess.PIPE` and `stdout=subprocess.PIPE`. I will need to be careful about flushing — if I forget to flush, the subprocess will block waiting for data that is sitting in a buffer.

Next session: implement `logger.py`.

---

## 2025-03-01 10:30

### Thoughts So Far

No new thoughts since yesterday. Ready to code.

### Plan for This Session

Implement `logger.py`. It is the simplest of the three programs:
- Accept log file name as command-line argument.
- Read lines from stdin.
- Parse first token as action, rest as message.
- Write `YYYY-MM-DD HH:MM [ACTION] MESSAGE` to the file.
- Stop on `QUIT`.

The tricky parts: making sure I flush after every write (so the driver gets real-time updates), and making sure the timestamp format is exactly right per the spec.

### Coding Notes

Started writing `logger.py`. The `datetime.now().strftime("%Y-%m-%d %H:%M")` gives me exactly what I need for the timestamp.

Used `split(None, 1)` to split the line into at most two parts — first token is the action, everything after the first space is the message. That cleanly handles cases where the message contains spaces.

Opened the log file in append mode (`'a'`) so if the driver is restarted, old logs are preserved.

Made sure to call `f.flush()` after each write so entries appear immediately in the file rather than buffering.

Tested it manually:

```
echo -e "START Logging Started.\nENCRYPT User encrypted HELLO\nQUIT" | python3 logger.py test.log
cat test.log
```

Output:
```
2025-03-01 10:35 [START] Logging Started.
2025-03-01 10:35 [ENCRYPT] User encrypted HELLO
```

Format looks correct. ✓

### End-of-Session Reflection

Logger is done. It was straightforward. Only thing I had to think about was the `strip()` vs `rstrip('\n')` — I want to strip the newline but preserve leading spaces in the message (though in practice the spec messages won't have them). Used `rstrip('\n')` to be safe.

Next session: implement `encryption.py` with the Vigenère cipher.

