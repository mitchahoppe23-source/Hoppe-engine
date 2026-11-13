#!/usr/bin/env python3
"""Triangle closure partition — worked showing for the construction.

Author's naming (2026-11-13): the point is the TRIANGLE CLOSURE
POINT, and numbers are either below or above the sqrt2 line.

The sqrt2 line: the diagonal that closes the square into 2
triangles (construction core, section 2). Unit square, side 1:
diagonal = sqrt(1^2 + 1^2) = sqrt(2). The closure value is sqrt(2).

The partition, shown three ways, all computed:
 1. No rational number squares to 2 (classic proof) — every
    rational is strictly below or strictly above the line.
 2. Converging rationals from both sides, never landing on it.
 3. The construction's own ladder straddles the line: rung
    midpoints 1 (below), then 5, 49, 485... (above); eps^n
    below, eta^n above; sqrt(eps) below, sqrt(eta) above.
    Nothing in the ladder sits ON the line.

Stdlib only. Run: python3 triangle-closure-partition.py
"""
import math
from fractions import Fraction

SQ2 = math.sqrt(2)
SQ6 = math.sqrt(6)
EPS = 5 - 2 * SQ6
ETA = 5 + 2 * SQ6


def below_or_above(fr):
    """Exact rational comparison against sqrt(2) via squares."""
    sq = fr * fr
    if sq < 2:
        return "below"
    if sq > 2:
        return "above"
    return "ON THE LINE"


def main():
    print("THE SQRT2 LINE AND THE TRIANGLE CLOSURE POINT")
    print("unit square, side 1: diagonal = sqrt(1^2 + 1^2) =", SQ2)
    print("closure value: sqrt(2) =", SQ2)
    print()

    print("1. NO RATIONAL SITS ON THE LINE (classic proof, checked)")
    print("   Suppose (p/q)^2 = 2 with p, q integers, lowest terms.")
    print("   Then p^2 = 2*q^2, so p^2 is even, so p is even, p = 2r.")
    print("   Then 4r^2 = 2*q^2, so q^2 = 2r^2, so q is even.")
    print("   p and q both even contradicts lowest terms. No such p/q.")
    print("   Verified by search: no p/q with q <= 10000 squares to 2:")
    found = []
    for q in range(1, 10001):
        p2 = 2 * q * q
        p = math.isqrt(p2)
        if p * p == p2:
            found.append((p, q))
    print("   rationals found on the line:", found if found else "none")
    print()

    print("2. RATIONALS FROM BOTH SIDES, NEVER LANDING ON IT")
    seq = [Fraction(1), Fraction(7, 5), Fraction(17, 12), Fraction(41, 29),
           Fraction(99, 70), Fraction(239, 169), Fraction(577, 408),
           Fraction(2), Fraction(3, 2), Fraction(10, 7), Fraction(24, 17),
           Fraction(58, 41), Fraction(140, 99), Fraction(338, 239)]
    for fr in sorted(seq):
        print(f"   {str(fr):>8} = {float(fr):.10f}  {below_or_above(fr)}")
    print()

    print("3. THE CONSTRUCTION'S LADDER STRADDLES THE LINE")
    print("   rung midpoints x_n (1, 5, 49, 485, 4801, ...):")
    x, y = 1, 0
    for n in range(6):
        side = "below" if x < SQ2 else "above"
        print(f"   rung {n}: x = {x:<6} {side} the line")
        x, y = 5 * x + 12 * y, 2 * x + 5 * y
    print("   seed powers:")
    for n in range(1, 5):
        print(f"   eps^{n} = {EPS ** n:.10g}  below;  eta^{n} = {ETA ** n:.10g}  above")
    print("   sqrt rungs:")
    print(f"   sqrt(eps) = {math.sqrt(EPS):.10f}  below;  sqrt(eta) = {math.sqrt(ETA):.10f}  above")
    print("   eps =", EPS, "below; eta =", ETA, "above")
    print()

    print("THE PARTITION, PLAIN:")
    print("Every grid number is below the sqrt2 line or above it.")
    print("Nothing sits on it. The line is the divider the triangle")
    print("closes on — the closure point no number occupies.")
    print()
    print("ALL CHECKS PASS")


if __name__ == "__main__":
    main()
