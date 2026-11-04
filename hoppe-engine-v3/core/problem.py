"""Hoppe Engine v3 — PROBLEM INPUT (working part 1).

The engine starts from a problem. v1 and v2 started from their own
loaded graph and ran checks on themselves; that was the build choice
Mitch Hoppe corrected on 2026-11-02 ("Of course you're supposed to
put them into the code"). In v3 a problem comes in from outside —
a command-line argument, a problem file, or standard input — is
printed at the head of the run under PROBLEM:, and is carried
through every section of the transcript.

If no problem is supplied, the engine works the default problem:
the register of physics inconsistencies, demonstrated end-to-end
in core/solves.py. Those demonstrations ARE the problems (the
author's direction, 2026-11-02: show how we solved the
inconsistencies with the code, with a return leg — not a one-way
test whose result lands nowhere).
"""
import re
from decimal import Decimal

DEFAULT_PROBLEM = (
    "Work the register of physics inconsistencies under M=0: for each "
    "item, correct the measurement (remove the observer's view and the "
    "human-chosen numbers, restate as dimensionless ratios, same "
    "measuring stick the same exact way at both ends, start from the "
    "seed epsilon instead of true zero), run H(S, B, T) = S', solve "
    "for the invariant, and return the result into the engine so the "
    "next item can use it.")

STARTUP_LINE = "What's the problem you'd like to work on?"

_UNIT = (r"(?:km/s/Mpc|kg/m\^3|GeV/c\^2|GeV|kg|m\^3|m/s|m|km|s|K|J|hbar|h)")
_QTY_RE = re.compile(r"(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)\s*(%s)\b" % _UNIT)


def load_problem(argv):
    """Resolve the problem text from parsed CLI arguments.

    Precedence: --problem-file, then --problem / positional words,
    then piped stdin (handled by run_engine), then the default.
    Deterministic: the same arguments always give the same problem."""
    if getattr(argv, "problem_file", None):
        with open(argv.problem_file) as f:
            text = f.read().strip()
        if text:
            return text, "problem file %s" % argv.problem_file
    words = []
    if getattr(argv, "problem", None):
        words.extend(argv.problem)
    if words:
        return " ".join(words).strip(), "command line"
    return DEFAULT_PROBLEM, "default (the inconsistencies register)"


def parse_quantities(text):
    """Pull (value, unit) quantity pairs out of a problem statement.
    Deliberately simple and declared as such: it finds the numbers
    with units so the M=0 lens has something concrete to restate.
    Returns a list of dicts in the order found."""
    out = []
    for m in _QTY_RE.finditer(text):
        try:
            value = Decimal(m.group(1))
        except Exception:
            continue
        out.append({"value": value, "unit": m.group(2),
                    "as_stated": m.group(0)})
    return out


def detect_mixed_sticks(text):
    """The everyday mixed-stick tell in a problem statement: the
    Planck constant named both ways, h and hbar, inside one
    comparison without a declaration. Returns True if both appear
    as separate tokens."""
    has_hbar = ("hbar" in text) or ("ħ" in text)
    has_h = re.search(r"(?<![A-Za-z])h(?![A-Za-z])", text) is not None
    return bool(has_hbar and has_h)
