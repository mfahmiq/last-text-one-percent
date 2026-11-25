"""Last Text at One Percent — make.fun text bounty entry.

Writes one funny final text message from a dying phone at one
percent battery to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt).

Deterministic, Python standard library only. Self-verifies the entry
against the same rules the sealed scorer applies: UTF-8 text,
1-200 characters, a single line, not whitespace-only. Every problem
found is reported at once; the program exits non-zero on any failure.
"""

import os
import sys

ENTRY = (
    "1% left. Before I go: your 2 a.m. searches die with me. "
    "I never told the cloud a thing. "
    "Tell the charger I died a hero. Goodbye."
)

# Characters that would break the entry out of a single line. Besides
# the usual newline and carriage return this covers the other Unicode
# line/paragraph separators, so a stray exotic separator cannot slip
# through as a "single line" that a reader or scorer splits in two.
LINE_BREAKS = ("\n", "\r", "\x0b", "\x0c", "\x85", "\u2028", "\u2029")


def verify_entry(text):
    """Check one entry text against the gate rules.

    Returns a list of every problem found (empty list means valid).
    All checks run even after a failure, so one run reports the whole
    diagnosis instead of making the caller fix problems one at a time.
    The function is pure: no I/O, no globals, so it can validate the
    in-memory entry and, unchanged, the text read back from disk.
    """
    problems = []

    if not isinstance(text, str):
        return ["entry must be str, got " + type(text).__name__]

    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        # A lone surrogate (e.g. "\\ud800") counts in len() but cannot
        # be encoded; the gate requires real UTF-8 text, so it fails.
        problems.append("entry is not valid UTF-8: " + str(exc))

    if not 1 <= len(text) <= 200:
        problems.append(
            "entry is %d characters, must be 1-200" % len(text)
        )

    broken = [ch for ch in LINE_BREAKS if ch in text]
    if broken:
        problems.append(
            "entry must be a single line, but contains line break(s): "
            + ", ".join(repr(ch) for ch in broken)
        )

    if not text.strip():
        problems.append("entry must not be whitespace-only")

    return problems


def report_problems(problems):
    """Print every problem to stderr and return the failure exit code.

    One helper owns the failure output format, so main() stays a short
    readable pipeline and every failure path reports the same way.
    """
    for problem in problems:
        print("FAIL: " + problem, file=sys.stderr)
    return 1


def verify_written(path, expected_text):
    """Re-read the written file and check what actually landed on disk.

    Two complementary checks. First, the bytes must match the expected
    text plus one trailing newline: this catches truncation, an
    encoding change on write, and newline translation, including
    silent damage a rule check alone would miss (a lossy encoding
    that substitutes U+FFFD still yields valid UTF-8, so only the
    byte comparison catches it). Second, the content itself must pass
    the same gate rules as the in-memory entry: strip exactly one
    trailing newline and run verify_entry() on the result, so the
    file on disk is judged by the same rules the sealed scorer
    applies, verified after the write rather than only before it.
    A file with two trailing newlines, for example, fails the byte
    comparison and the re-verification additionally names the
    single-line violation. Returns a list of problems; empty means
    the file is good.
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            written = fh.read()
    except UnicodeDecodeError as exc:
        return ["written file is not valid UTF-8: " + str(exc)]
    except OSError as exc:
        return ["cannot read back " + path + ": " + str(exc)]

    problems = []
    if written != expected_text + "\n":
        problems.append("written file does not match the entry")

    content = written[:-1] if written.endswith("\n") else written
    problems.extend(verify_entry(content))
    return problems


def main() -> int:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    output_path = os.path.join(output_dir, "entry.txt")

    # Verify the in-memory entry first, reporting every problem at once.
    problems = verify_entry(ENTRY)
    if problems:
        return report_problems(problems)

    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(ENTRY + "\n")
    except OSError as exc:
        print("FAIL: cannot write " + output_path + ": " + str(exc),
              file=sys.stderr)
        return 1

    # Verify what was actually written, with the same rules.
    problems = verify_written(output_path, ENTRY)
    if problems:
        return report_problems(problems)

    print("OK: wrote %d-char entry to %s" % (len(ENTRY), output_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
