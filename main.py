#!/usr/bin/env python3
"""Absurd clause writer: terms of service, with one soul-sized catch.

CLAUSE is a fixed string. It is handed to validate(), which applies
each rule in RULES in turn; a rule is a (message, test) pair, and the
first failing test prints its message and exits with status 1. A
clause that passes everything is written to /output/entry.txt, one
line, with a trailing newline. No input, no network, no randomness.
"""

import sys

CLAUSE = "By using this service, you agree that your soul may be used for training purposes, and that your soul is non-refundable."
CHAR_LIMIT = 200
OUT = "/output/entry.txt"
ENDERS = (".", "!", "?")
PUNCT_SET = frozenset(".,!?;:'\"-() ")


def fail(reason):
    print(f"invalid clause: {reason}", file=sys.stderr)
    raise SystemExit(1)


def _exists(text):
    return bool(text and text.strip())


def _short(text):
    return len(text) <= CHAR_LIMIT


def _clean(text):
    return all(ord(c) >= 32 for c in text)


def _tidy(text):
    return text == text.strip() and "  " not in text and "\n" not in text


def _lettered(text):
    return any(c.isalpha() for c in text)


def _substantial(text):
    return not all(c in PUNCT_SET for c in text)


def _not_numeric(text):
    return not text.strip().isdigit()


def _closed(text):
    return text.rstrip().endswith(ENDERS)


def _opens_like_terms(text):
    return text.startswith("By using")


def _ascii_only(text):
    # A clause written in plain ASCII reads the same on every screen;
    # anything beyond it is decoration the fine print does not need.
    return all(ord(c) < 128 for c in text)


RULES = [
    ("clause is empty", _exists),
    ("clause is over the 200 character limit", _short),
    ("clause has control characters", _clean),
    ("clause has leading/trailing/double spaces or a newline", _tidy),
    ("clause has no letters", _lettered),
    ("clause is only punctuation", _substantial),
    ("clause is only digits", _not_numeric),
    ("clause must end with punctuation", _closed),
    ("the clause must open like terms of service: 'By using'", _opens_like_terms),
    ("the clause must be plain ASCII", _ascii_only),
]


def validate(text):
    for message, test in RULES:
        if not test(text):
            fail(message)


def main():
    validate(CLAUSE)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(CLAUSE + "\n")


if __name__ == "__main__":
    main()
