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

---

## 2025-03-02 13:45

### Thoughts So Far

The Vigenère cipher has been in my head since yesterday. I kept thinking about whether to handle non-letter characters or just reject them. The spec says "The Vigenère cypher only works on letters" and "you may assume that it always receive input in uppercase." So the encryption program itself can assume valid letter-only uppercase input — the driver handles validation before sending anything.

### Plan for This Session

Implement `encryption.py`:
1. Read commands from stdin in a loop.
2. Parse command and argument.
3. Implement `PASSKEY`, `ENCRYPT`, `DECRYPT`, `QUIT` handling.
4. Implement Vigenère encrypt and decrypt functions.
5. Test manually using the example from the spec: `PASSKEY HELLO`, then `ENCRYPT HELLO` → `OIWWC`.

### Coding Notes

The Vigenère cipher formulas:
- Encrypt: `C_i = (P_i + K_i) mod 26`
- Decrypt: `P_i = (C_i - K_i + 26) mod 26`
  - The `+26` is needed because Python's `%` operator can return negative values for negative operands in some edge cases. Adding 26 ensures we always stay in [0, 25].

I convert letters to 0-25 by doing `ord(ch) - ord('A')` and back with `chr(x + ord('A'))`.

The key repeats — `key[key_idx % len(key)]` handles the cycling.

**Important:** I only increment `key_idx` when the character is a letter. For non-letters, I would just pass them through unchanged. This way the key position stays aligned with the letters.

Tested with the spec example:
```
echo -e "ENCRYPT HELLO\nPASSKEY HELLO\nENCRYPT HELLO\nDECRYPT OIWWC\nQUIT" | python3 encryption.py
```
Output:
```
ERROR Password not set
RESULT
RESULT OIWWC
RESULT HELLO
```

All correct! ✓

Also made sure `sys.stdout.flush()` is called after every print, otherwise the driver would block forever waiting for a response that is sitting in a buffer.

### End-of-Session Reflection

Encryption program is done. The cipher math was not bad once I worked through the formula. The main gotcha is flushing stdout.

Next session: start the driver program. This will be the hardest part — launching subprocesses with `subprocess.Popen`, connecting the pipes, and building the interactive menu.

---

## 2025-03-04 15:20

### Thoughts So Far

I have been thinking about how the driver connects to the subprocesses. The key insight is:
- The **logger** only needs its stdin connected (the driver writes to it; the logger writes to a file, not to the driver).
- The **encryption program** needs both stdin and stdout connected (the driver sends commands and reads results).

So:
- `logger_proc = Popen(["python3", "logger.py", logfile], stdin=PIPE, text=True)`
- `enc_proc = Popen(["python3", "encryption.py"], stdin=PIPE, stdout=PIPE, text=True)`

The `text=True` flag makes the streams work with strings instead of bytes — much easier.

### Plan for This Session

Build the complete `driver.py`:
1. Launch logger and encryption as subprocesses with the right pipes.
2. Log `START` on startup.
3. Build the main command loop: `password`, `encrypt`, `decrypt`, `history`, `quit`.
4. Implement `history` as an in-memory list — all strings entered/produced by encrypt/decrypt (but NOT passwords).
5. On `quit`, send `QUIT` to both child processes and wait for them to terminate.

### Coding Notes

**Subprocess setup** worked on the first try. The key was passing `text=True` so I can use `.write(str)` and `.readline()` instead of dealing with bytes.

**Flush is critical.** Every time I write to a pipe, I need to flush. Otherwise the data stays in the buffer and the child process never sees it. I call `.flush()` after every `.write()`.

**`send_to_enc`** function: writes the command + newline, flushes, then reads one response line. This is a simple request/response pattern — send one line, get one line back.

**Input validation** in the driver: `only_letters(s)` checks `s.isalpha()`. This rejects spaces, digits, punctuation. The error message explains what went wrong.

**History logic:**
- `password` command: user picks from history OR enters new. Password is **never** added to history.
- `encrypt`/`decrypt` command: if entering a new string, it IS added to history. The result is also added to history. If picking from history, the item is already there.

**Shutdown sequence:**
1. Log `QUIT`.
2. Send `QUIT` to the encryption program and wait for readline (it won't respond, so I just close its stdin).
3. Send `QUIT` to the logger via its stdin.
4. Close both stdin pipes.
5. Call `.wait()` on both processes so they clean up before the driver exits.

Quick test — just `quit`:
```
echo "quit" | python3 driver.py test.log
```
Output: `Goodbye!`
Log file: `2025-03-04 15:31 [START] Driver started.` and `2025-03-04 15:31 [QUIT] Driver exiting.`

It works! ✓

### End-of-Session Reflection

Got the skeleton of the driver running. The subprocess setup was easier than I expected once I understood `text=True`. Tomorrow I will do a full end-to-end test: set a password, encrypt something, decrypt it back, check history, then quit.

Next session: full end-to-end testing of the driver.

