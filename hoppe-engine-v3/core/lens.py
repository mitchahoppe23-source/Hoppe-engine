"""Hoppe Engine v3 — the M=0 LENS as an operation (working part 2).

Mitch Hoppe's position, in his words (2026-10-29): "M=0 is a lens
used to unify quantum physics and gr. It shows that starting from
.1010205 instead of true zero and taking the correct measurements
resolves all the inconsistencies."

The lens is a step the engine RUNS on a problem, not a label in a
data file. It does three things, in order:

(a) START FROM THE SEED, NOT TRUE ZERO. The floor of any scale is
    epsilon = 5 - 2 sqrt(6) = 0.1010205144..., never 0. A quantity
    stated as a multiple n of a unit is re-based as n - eps at the
    floor end when the floor is what matters (demonstrated in the
    singularities solve: the smallest volume is the node volume,
    not zero volume).
(b) RESTATE AS DIMENSIONLESS RATIOS. The mismeasurement, in the
    author's words, is "putting the observers view plus human
    numbers rather than dimensionless ratios". Every stated
    quantity is divided by the reference quantity on the same
    stick, so the human-chosen unit cancels.
(c) SAME STICK AT BOTH ENDS. "The actual label doesnt matter but
    if you use it at one end, you must use it at the other end the
    same exact way" (the author's words). The checked example is
    the Planck pair: products derived with h but stated against
    hbar are off by exactly 2 pi — a mixed stick, flagged here by
    the same split-stick arithmetic the sabotage suite uses.
"""
from decimal import Decimal, getcontext

import invariants as inv

getcontext().prec = 60

EPSILON = Decimal(5) - 2 * Decimal(6).sqrt()     # 0.101020514433644...
ETA = Decimal(5) + 2 * Decimal(6).sqrt()         # 9.898979485566356...


def seed_floor():
    """(a) The starting point of the lens: epsilon, not true zero."""
    return EPSILON


def restate_as_ratios(quantities, reference=None):
    """(b) Restate stated quantities as dimensionless ratios.

    quantities: list of {'value': Decimal, 'unit': str, ...} as
    parsed from the problem (core/problem.py). The reference is the
    first quantity on the same stick (same unit) unless one is
    named. Quantities on other sticks are carried unstated-in-ratio
    and flagged, never silently divided by a different stick."""
    if not quantities:
        return [], "no quantities with units were stated in the problem; " \
                   "nothing to restate (said plainly, not filled in)"
    ref = reference or quantities[0]
    ratios = []
    for q in quantities:
        if q["unit"] == ref["unit"]:
            ratios.append({"as_stated": q["as_stated"],
                           "ratio": q["value"] / ref["value"],
                           "stick": q["unit"],
                           "dimensionless": True})
        else:
            ratios.append({"as_stated": q["as_stated"],
                           "ratio": None,
                           "stick": q["unit"],
                           "dimensionless": False,
                           "note": "different stick (%s vs %s): not divided; "
                                   "a common stick must be chosen first"
                                   % (q["unit"], ref["unit"])})
    return ratios, "reference stick: %s (the first quantity stated)" % ref["unit"]


def check_same_stick(derive_with="hbar", state_against="hbar"):
    """(c) The same-stick check, run on the Planck products.

    derive_with / state_against each take 'h' or 'hbar'. On one
    stick every Planck product is 1. Mixed sticks move the
    products by exactly 2 pi. Returns (same, worst_deviation,
    detail) — the deviation the M=0 lens catches BEFORE solving."""
    consts = {"h": inv.H_PLANCK, "hbar": inv.HBAR}
    ratios = inv.planck_products_split(consts[derive_with],
                                       consts[state_against])
    worst = max(abs(r - 1) for r in ratios)
    same = worst < Decimal("1e-30")
    if same:
        detail = ("one stick (%s) at both ends: the four Planck products "
                  "are 1 (worst deviation %.3e)" % (derive_with, worst))
    else:
        detail = ("MIXED STICKS FLAGGED: derived with %s, stated against "
                  "%s — worst Planck product deviation %.3e, a factor of "
                  "2 pi. This is a mismeasurement, not an inconsistency; "
                  "correct the stick before solving."
                  % (derive_with, state_against, worst))
    return same, worst, detail


def correct_measurement(problem_text, quantities):
    """Run the whole lens on a problem: seed floor, ratios, sticks.
    Returns the lines the transcript prints under the M=0 lens
    heading, plus a verdict dict the loop carries forward."""
    lines = []
    lines.append("M=0 lens, step (a) - start from the seed, not true zero: "
                 "epsilon = 5 - 2 sqrt(6) = %s (the floor of every scale "
                 "in this run; true zero is never used as a starting point)"
                 % EPSILON.quantize(Decimal("0.0000000001")))
    ratios, note = restate_as_ratios(quantities)
    lines.append("M=0 lens, step (b) - restate as dimensionless ratios: %s" % note)
    if ratios:
        for r in ratios:
            if r["dimensionless"]:
                lines.append("    %s  ->  %s (dimensionless, stick %s cancels)"
                             % (r["as_stated"],
                                r["ratio"].quantize(Decimal("0.000001")),
                                r["stick"]))
            else:
                lines.append("    %s  ->  NOT restated: %s"
                             % (r["as_stated"], r["note"]))
    else:
        lines.append("    (the register demonstrations below each state "
                     "their own quantities and restate them the same way)")
    same, _w, detail_ok = check_same_stick("hbar", "hbar")
    lines.append("M=0 lens, step (c) - same stick at both ends: %s" % detail_ok)
    _same2, _w2, detail_mixed = check_same_stick("h", "hbar")
    lines.append("M=0 lens, step (c) - the mixed-stick case, checked: %s"
                 % detail_mixed)
    verdict = {"seed": EPSILON, "ratios": ratios,
               "same_stick_hbar": same, "mixed_stick_flagged": True}
    return lines, verdict
