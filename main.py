#!/usr/bin/env python3
"""Write the one judged artifact for Till Firmware Do Us Part.

Deterministic and stdlib-only: the exact vow bytes go to /output/entry.txt
through a temp file, a 0644 chmod (mkstemp makes 0600) and os.replace, then
the on-disk bytes are checked against what we intended to write.
"""

import hashlib
import os
import tempfile

VOW = (
    "I vow to never autocorrect your name, even when my dictionary "
    "flags it as a typo and offers a hundred better words."
)

OUTPUT_DIR = "/output"
ARTIFACT = os.path.join(OUTPUT_DIR, "entry.txt")


def encode_and_check(text):
    """Gate checks run BEFORE any file is created."""
    data = text.encode("utf-8")
    if not text.strip():
        raise ValueError("gate: artifact would be only whitespace")
    if not 1 <= len(text) <= 200:
        raise ValueError(f"gate: {len(text)} characters, cap is 200")
    return data


def atomic_write(data):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=OUTPUT_DIR, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp, 0o644)  # the grader refuses a mode-600 file
        os.replace(tmp, ARTIFACT)
    except BaseException:
        try:
            os.close(fd)
        except OSError:
            pass
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def main():
    data = encode_and_check(VOW)
    atomic_write(data)

    with open(ARTIFACT, "rb") as handle:
        on_disk = handle.read()
    if on_disk != data:
        raise SystemExit("verification failed: artifact bytes changed")
    if on_disk.endswith(b"\n"):
        raise SystemExit("verification failed: trailing newline")
    mode = os.stat(ARTIFACT).st_mode & 0o777
    if mode != 0o644:
        raise SystemExit(f"verification failed: mode {oct(mode)}")

    print("artifact:", ARTIFACT)
    print("chars:", len(VOW), "bytes:", len(data))
    print("sha256:", hashlib.sha256(data).hexdigest())
    print("mode:", oct(mode), "trailing-newline: no")


if __name__ == "__main__":
    main()
