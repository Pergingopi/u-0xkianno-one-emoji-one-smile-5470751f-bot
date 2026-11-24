#!/usr/bin/env python3
"""One Emoji, One Smile - exactly one emoji, the warmest for a stranger.

Pure Python 3.13 standard library. The program writes one emoji to
/output/entry.txt. No network, no model call, fully deterministic: the
same code always writes the same bytes.

The entry: U+1F917 HUGGING FACE
    🤗

Why this emoji, judged against the brief's criteria in order:

1. It plainly aims to warm a stranger: a hug is an active gesture of
   warmth, not just a facial expression - it is the emoji that most
   directly says "I am sending you kindness".
2. Warmth at first glance: open arms and a smiling face read as kind,
   friendly and gently funny with no context needed.
3. Universality: a hug is understood the same way by a stranger of any
   age or background; there is no irony or in-joke in it.
4. Chosen rather than default: it is a deliberate pick for the moment,
   not the first default smiley that comes to mind, while staying
   instantly readable.
5. Right for a stranger: a virtual hug between strangers is a familiar,
   friendly online gesture - warm without sarcasm, flirtation or
   over-familiarity.

Compared with the previous pick, U+1F60A SMILING FACE WITH SMILING
EYES (a gentle smile): the smile is safe and universal, but it is also
the most default choice, and it only expresses warmth where the hug
actively offers it. On the brief's own ordering - the first criterion
where the two differ decides - the hug's direct aim at warming a
stranger and its deliberately chosen feel outweigh the smile, while
the hug stays just as readable and appropriate from a stranger.

Validation: before writing, the program asserts the entry is exactly
one Unicode character, in category So (Symbol, other - an emoji
symbol), and not whitespace, so a bad constant can never reach the
output file.

Newline decision: the gate checks that entry.txt is UTF-8 text of
1 to 8 characters, not only white space. A trailing newline would
make the file 2 characters and still pass the gate, but the task is
"exactly one emoji and nothing else", and the ranking tie-break
favours fewer bytes, so the file is written with NO trailing newline:
exactly 1 character, 4 bytes of UTF-8, nothing else.

Usage: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import unicodedata

EMOJI = "\U0001F917"  # 🤗 HUGGING FACE


def validate_emoji(value):
    """Check the entry is exactly one non-whitespace emoji character."""
    assert isinstance(value, str), "entry must be a str"
    assert len(value) == 1, f"entry must be exactly 1 character, got {len(value)}"
    assert not value.isspace(), "entry must not be whitespace"
    assert unicodedata.category(value) == "So", (
        f"entry must be an emoji symbol (category So), "
        f"got {unicodedata.category(value)}"
    )
    assert len(value.encode("utf-8")) == 4, "entry must be 4 bytes of UTF-8"


def main():
    validate_emoji(EMOJI)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = EMOJI.encode("utf-8")
    tmp = os.path.join(out_dir, ".entry.txt.tmp")
    final = os.path.join(out_dir, "entry.txt")
    with open(tmp, "wb") as f:
        f.write(data)
    os.chmod(tmp, 0o644)
    os.replace(tmp, final)
    os.chmod(final, 0o644)


if __name__ == "__main__":
    main()
