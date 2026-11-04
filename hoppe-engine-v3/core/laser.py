"""Hoppe Engine v3 — the laser-through-lenses demonstration.

Mitch Hoppe's comparison for the Hubble item (2026-10-29): shoot a
straight laser through 1 vs 2 vs 3 lenses. A detector that does not
model the lenses infers a different source for each stack, while
the laser itself never changes. On 2026-11-02 he directed the
recorded stack be extended by 2 more lenses, to 5.

This module COMPUTES the stack in the run (nothing is quoted as a
result): literal paraxial thin-lens optics.

Setup (the recorded one): a straight laser ray at height 1 cm off
axis, true angle 0 (parallel to the axis); identical thin lenses
of focal length 50 cm, spaced 25 cm apart. Paraxial rules:

    at a lens:        angle  <- angle - height / focal_length
    between lenses:   height <- height + angle * spacing

Computed results (radians exact in Decimal; degrees derived):
    lens 1: height  1.0000 cm, exit angle -0.02000 rad = -1.146 deg
    lens 2: height  0.5000 cm, exit angle -0.03000 rad = -1.719 deg
    lens 3: height -0.2500 cm, exit angle -0.02500 rad = -1.432 deg
    lens 4: height -0.8750 cm, exit angle -0.00750 rad = -0.430 deg
    lens 5: height -1.0625 cm, exit angle +0.01375 rad = +0.788 deg
The 1-3 lens values reproduce the 2026-10-29 record exactly (which
confirms the 25 cm spacing reconstruction); lenses 4 and 5 are the
same calculation continued. The laser's true angle is 0.000 deg at
every row — the source never changes; only the stack does.

What this demonstrates, and what it does not: the LENS MECHANISM
is proven as a mechanism (ordinary optics, computed here). Whether
the Hubble ratio is this mechanism is a separate claim and stays
HYPOTHESIS — see solve_hubble in core/solves.py, which prints the
two label lines separately.
"""
from decimal import Decimal, getcontext

getcontext().prec = 60

D = Decimal
PI = D("3.14159265358979323846264338327950288419716939937510582097494459")
FOCAL_LENGTH_CM = D("50")
SPACING_CM = D("25")
START_HEIGHT_CM = D("1")
TRUE_ANGLE_DEG = D("0")

# The recorded/continued values, used only to VERIFY the computed
# stack (the stack itself is computed above-board from the rules).
EXPECTED = [
    # (height at lens, cm), (exit angle, rad)
    (D("1.0000"), D("-0.02000")),
    (D("0.5000"), D("-0.03000")),
    (D("-0.2500"), D("-0.02500")),
    (D("-0.8750"), D("-0.00750")),
    (D("-1.0625"), D("0.01375")),
]


def _deg(rad):
    return rad * D(180) / PI


def laser_stack(count=5):
    """Run the ray through `count` lenses; return one row per lens:
    (lens_number, height_at_lens_cm, exit_angle_rad, exit_angle_deg).
    Computed from the paraxial rules, never looked up."""
    rows = []
    height = START_HEIGHT_CM
    angle = D(0)
    for n in range(1, count + 1):
        height_at = height
        angle = angle - height_at / FOCAL_LENGTH_CM
        rows.append((n, height_at, angle, _deg(angle)))
        height = height_at + angle * SPACING_CM
    return rows


def verify_stack(rows):
    """True if the computed stack reproduces the recorded 1-3 lens
    values and their continuation to 5 lenses (see EXPECTED)."""
    if len(rows) != len(EXPECTED):
        return False
    return all(h == eh and a == ea
               for (_, h, a, _), (eh, ea) in zip(rows, EXPECTED))


def demonstration_lines(count=5):
    """The demonstration block printed in the run, with the Hubble
    solve: the computed table and the plain conclusion."""
    rows = laser_stack(count)
    ok = verify_stack(rows)
    lines = [
        "LASER STACK DEMONSTRATION — the lens mechanism, computed in "
        "this run (not quoted): straight laser ray, height 1 cm off "
        "axis, true angle 0.000 deg (parallel to the axis) at every "
        "row; identical thin lenses, focal length 50 cm, spaced "
        "25 cm apart; paraxial rules: at a lens the angle drops by "
        "height/focal length, between lenses the height moves by "
        "angle x spacing",
        "lenses | height at lens (cm) | apparent (exit) angle (rad) "
        "| apparent angle (deg) | true angle (deg)",
    ]
    for n, h, a, deg in rows:
        lines.append("%d lens(es) | %s | %s | %s | 0.000"
                     % (n,
                        h.quantize(D("0.0001")),
                        a.quantize(D("0.00001")),
                        deg.quantize(D("0.001"))))
    lines.append(
        "computed stack verified against the recorded values "
        "(1-3 lenses from the 2026-10-29 record, 4-5 the same "
        "calculation continued): %s" % ("YES" if ok else "NO"))
    lines.append(
        "conclusion: a detector that does not model the lenses "
        "infers a different source for each stack — by 5 lenses the "
        "apparent angle (+0.788 deg) is on the OTHER SIDE of the "
        "true angle (0.000 deg) — while the source never changes: "
        "the laser's true angle is 0.000 deg at every row. A "
        "different reading, by itself, does not locate a difference "
        "in the source; it can sit entirely in the stack it was "
        "read through")
    return lines
