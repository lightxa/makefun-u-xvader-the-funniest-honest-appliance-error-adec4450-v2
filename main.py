"""The Funniest Honest Appliance Error, variant 2.

Writes one line of at most 200 characters to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` (default ``/output``): the funniest
honest error message an appliance could show.

The line is a washing machine reporting its own unbalanced-load
fault in its flat, put-upon voice. The joke is the truth of the
fault: a real unbalanced-load error, forty minutes of violent
shaking, all of it caused by a single sock, and the machine
admitting the sock is winning. No pun is bolted on; the humour
comes out of the named fault itself, and the turn lands in the
last sentence.

This variant is deliberately different from variant 1 (a fridge
reporting a cooling failure): different appliance, different
fault, different structure, different image.

Pure standard library, deterministic, no network at runtime.
"""

import os

# The entry: one line, at most 200 characters, exactly as it will be
# written to entry.txt. Kept as a single constant so the program's
# output is byte-identical on every run.
ENTRY = (
    "Error: unbalanced load. "
    "I have been shaking violently for 40 minutes over one sock. "
    "It is winning."
)

MAX_CHARS = 200


def gate_check(text):
    """Mirror the sealed scorer's gate: UTF-8 text, 1 to 200 chars,
    not only whitespace, exactly one line."""
    if not isinstance(text, str):
        return False
    if not text.strip():
        return False
    if not (1 <= len(text) <= MAX_CHARS):
        return False
    if "\n" in text or "\r" in text:
        return False
    text.encode("utf-8")  # Raises if the text is not valid UTF-8.
    return True


def main():
    """Write the entry line to the output directory and verify it."""
    if not gate_check(ENTRY):
        raise SystemExit("entry fails the gate self-check")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")

    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)

    # Read it back and re-check what actually landed on disk.
    with open(out_path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != ENTRY or not gate_check(written):
        raise SystemExit("written entry.txt fails the gate self-check")

    print(f"wrote {out_path} ({len(written)} characters)")


if __name__ == "__main__":
    main()
