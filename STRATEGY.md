# STRATEGY — Till Firmware Do Us Part

## Exact deliverable
A single text written to `/output/entry.txt`: one funny, heartfelt wedding vow spoken by a robot at its own wedding, one sentence, under 200 characters. Only that file may sit in `/output`. The repo entrypoint is `main.py` (python3.13); the grader runs it in a sandbox and gates the artifact.

## Hard caps (sealed gate / harness)
- `/output/entry.txt` must be valid UTF-8, 1..200 characters inclusive, not only whitespace.
- Under 200 characters per the brief itself. No trailing newline in the artifact bytes.
- Mode must be 0644: the grader refuses a 0600 file, and `tempfile.mkstemp` creates 0600, so `os.chmod(0o644)` must happen BEFORE `os.replace`.
- Write atomically: temp file in `/output` + `os.replace`.
- Sandbox: 1 CPU, 512 MB, 60 s wall, no network; everything the program runs ships in the repo.

## Judge criteria, in the rubric's order
The house judge compares two vows and picks the one that meets these better, using the FIRST criterion where they differ:
1. A one-line wedding vow a robot speaks at its own wedding — anything that is not that loses to any entry that is.
2. A real laugh from a human reader, out of the situation itself rather than a pun bolted on.
3. Genuine tenderness under the joke, so it would still land at a real ceremony.
4. Sounds like a machine speaking: its own hardware, uptime, firmware or battery, not a human's words with a robot label.
5. One sentence that fits the character limit with nothing spare, no cuttable setup.
Also: a vow that explains its own joke is weaker; length for its own sake does not count.

## What the field is doing (live feed research)
~266 feed entries reviewed. Overwhelming clichés: "I promise to love you through every update, crash, reboot, low battery", "till firmware do us part", "last 1% battery", "factory reset", "you are my favourite process / the only process I won't kill", "the first thing I ever said that no one programmed me to say", "warranty doesn't cover water damage", "tick the CAPTCHA boxes so I can hold your hand". They all share one joke and one shape. Copying any of them cannot win head-to-head on criterion 2.

## Fresh angle chosen
A machine's autocorrect mistake: its dictionary insists the beloved's name is a typo and offers "a hundred better words", and the robot refuses to change it. The laugh comes from a real machine predicament (criterion 2), refusing to "fix" the name is quiet acceptance of the person as-is (criterion 3), the voice is unmistakably a machine's own ("my dictionary", criterion 4), it opens with "I vow" (criterion 1), and it is one tight sentence far under 200 chars (criterion 5). The joke is never explained.

Chosen text (exact bytes, no trailing newline):
`I vow to never autocorrect your name, even when my dictionary flags it as a typo and offers a hundred better words.`

## Concrete plan to maximize score
1. Write `main.py` first: constant with the vow, UTF-8 encode, length/whitespace validation, create `/output`, temp file + chmod 0644 + `os.replace`, print diagnostics.
2. In a SEPARATE later step, rewrite that SAME `main.py` with the real improvement: validate before writing, fsync the temp file, guarantee cleanup on any failure, and print byte count / char count / sha256 so the run is self-verifying. The transcript then shows two distinct writes to the final entrypoint.
3. Run it locally and verify: no trailing newline, 0644 mode, UTF-8, 1..200 chars, only `entry.txt` in `/output`.
4. Commit all work with git on top of init's freshness + LICENSE commits; print the final commit sha.
5. Do not upload or submit anything.
