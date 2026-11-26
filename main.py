"""Fix Human Sleep: Funniest Patch Note.

Writes one line of patch notes announcing that human sleep is fixed
to /output/entry.txt. Pure stdlib only (os, sys).
"""

import os
import sys

LINE = "Fixed: human sleep no longer crashes at 3 AM to replay every embarrassing thing you've said since 2009."

MAX_CHARS = 160


def check_gate(line):
    """Gate: 1-160 chars, single line, no control characters, not blank.

    Returns an error string, or None when the line passes.
    """
    if not line or not line.strip():
        return "line is empty or whitespace-only"
    if len(line) > MAX_CHARS:
        return "line is %d chars, over %d" % (len(line), MAX_CHARS)
    if "\n" in line or "\r" in line:
        return "line is not a single line"
    if any(ord(ch) < 32 for ch in line):
        return "line contains control characters"
    return None


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")

    # Self-check gate before writing anything.
    gate_error = check_gate(LINE)
    if gate_error is not None:
        print("gate failed: %s" % gate_error, file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    # Harden modes: the grader collects /output as another user, so the
    # file must stay readable (0644) and the directory traversable (0755).
    # Best effort only: the grader runs as user 65534 on a read-only
    # filesystem and /output is not ours, so chmod may raise PermissionError
    # (OSError). Never let that fail the run — the write below is what matters.
    try:
        os.chmod(out_dir, 0o755)
    except OSError:
        pass
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass

    # Read-back verification: byte-exact, valid UTF-8, no trailing newline.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != LINE.encode("utf-8"):
        print("verification failed: file bytes differ", file=sys.stderr)
        return 1
    text = raw.decode("utf-8")
    if len(text) != len(LINE) or "\n" in text:
        print("verification failed: length or line check", file=sys.stderr)
        return 1
    if text.strip() != LINE or text != text.strip():
        print("verification failed: unexpected surrounding whitespace", file=sys.stderr)
        return 1

    print("wrote %s (%d chars)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
