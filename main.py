"""The 3AM Fridge Text — make.fun entry.

Writes one line of text, the message a smart fridge would text its
owner at 3am, to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).
Deterministic: the line is a constant, validated, then written
byte-exact with no trailing newline.
"""

import os
import sys

# The entry: a smart fridge, awake all night, keeping count.
ENTRY = (
    "3am. This is your fifth visit tonight. "
    "The contents have not changed. "
    "Neither has the problem. Go to bed."
)


def validate(line: str) -> bytes:
    """Check the line against the gate, return its UTF-8 bytes."""
    if not isinstance(line, str):
        raise ValueError("entry must be a string")
    if not 1 <= len(line) <= 140:
        raise ValueError(f"entry must be 1-140 chars, got {len(line)}")
    if line != line.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    if any(ch in line for ch in "\r\n"):
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("entry must not contain control characters")
    if any(ch.isspace() and ch != " " for ch in line):
        raise ValueError("entry must use plain spaces only, no exotic whitespace")
    if any(ch in line for ch in "\u200b\u200c\u200d\ufeff"):
        raise ValueError("entry must not contain zero-width characters")
    if not line.strip():
        raise ValueError("entry must not be only whitespace")
    data = line.encode("utf-8")
    if data.decode("utf-8") != line:
        raise ValueError("entry failed UTF-8 round-trip")
    return data


def main() -> int:
    data = validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as fh:
        fh.write(data)
    # Re-read and verify the file holds exactly the validated bytes.
    with open(path, "rb") as fh:
        written = fh.read()
    if written != data:
        raise ValueError("entry.txt does not match the validated entry")
    print(f"wrote {path}: {len(ENTRY)} chars, {len(data)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
