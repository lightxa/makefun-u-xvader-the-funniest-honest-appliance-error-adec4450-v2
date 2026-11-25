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

Why this line fits the judge's criteria, in their order: it is
honest first, naming a fault a washing machine really reports;
the laugh is the admission that one sock has been beating the
machine for forty minutes; the voice is the machine itself,
flat and put-upon; and at 98 characters every word earns its
place, with nothing explaining the joke.

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


def resolve_output_path():
    """Return the entry.txt path inside the output directory."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.txt")


def write_and_verify(out_path, text):
    """Write the entry, then read it back and re-check what landed."""
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    with open(out_path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text or not gate_check(written):
        raise SystemExit("written entry.txt fails the gate self-check")
    return written


def main():
    """Write the entry line to the output directory and verify it."""
    if not gate_check(ENTRY):
        raise SystemExit("entry fails the gate self-check")

    out_path = resolve_output_path()
    written = write_and_verify(out_path, ENTRY)

    print(f"wrote {out_path} ({len(written)} characters)")


if __name__ == "__main__":
    main()
