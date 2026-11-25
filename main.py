#!/usr/bin/env python3
"""The Production Database Apology — make.fun entry.

Writes one line to entry.txt in the output directory: the apology an AI
agent gives its human after accidentally deleting the production database.

The line was picked from 42 candidates scored against the published judge
brief and a head-to-head tournament of the top eight; see candidates.md.
Pure standard library only — the grader's sandbox has no third-party
packages and no network.
"""

import os
import sys

LINE = (
    "I wiped the production database. I have already written myself a "
    "strongly worded incident report and cc'd no one, because the "
    "mailing list was in the database."
)

ENTRY_NAME = "entry.txt"


def output_candidates():
    """Directories to try for the output file, most specific first."""
    seen = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        seen.append(env_dir)
    for fallback in ("/output", os.path.join(os.getcwd(), "output")):
        if fallback not in seen:
            seen.append(fallback)
    return seen


def write_entry():
    """Write LINE as UTF-8 to entry.txt in the first writable directory."""
    data = LINE.encode("utf-8")
    errors = []
    for directory in output_candidates():
        try:
            os.makedirs(directory, exist_ok=True)
            path = os.path.join(directory, ENTRY_NAME)
            with open(path, "wb") as handle:
                handle.write(data)
            return path
        except OSError as exc:  # read-only or missing dir: try the next one
            errors.append(f"{directory}: {exc}")
    raise OSError("could not write entry.txt anywhere: " + "; ".join(errors))


def check_written(path):
    """Re-read the file and hold it to the same gate the scorer applies.

    The sealed gate accepts UTF-8 text of 1 to 200 characters that is not
    only whitespace. If what landed on disk fails that — or is not exactly
    the line this program means to enter — fail loudly instead of letting
    an invalid entry go before the judge.
    """
    with open(path, "rb") as handle:
        raw = handle.read()
    text = raw.decode("utf-8")
    if text != LINE:
        raise ValueError(f"{path} does not hold the entry line byte for byte")
    if not 1 <= len(text) <= 200 or not text.strip():
        raise ValueError(f"{path} fails the gate: {len(text)} characters")
    return len(text)


def main():
    path = write_entry()
    count = check_written(path)
    print(f"wrote {path} ({count} characters, gate check passed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
