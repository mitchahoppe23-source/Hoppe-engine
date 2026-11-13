#!/usr/bin/env python3
"""Scale propagation in and out — worked showing, computed from the
Hoppe construction core (seed pair, Pell ladder, fold).

Center: 5. From 5, inward 5 - 2*sqrt(6) = eps, outward
5 + 2*sqrt(6) = eta (author's fold words, 2026-11-11).
Each rung n: eta^n = x_n + y_n*sqrt(6), eps^n = x_n - y_n*sqrt(6),
with x_n^2 - 6*y_n^2 = 1 exactly (integers). Midpoint of rung n is
x_n; 5 is rung 1's midpoint. In and out are the same ladder read
from two ends: eps^n * eta^n = 1 at every rung.

Stdlib only. Run: python3 scale-propagation-in-out.py
"""
import math

SQ6 = math.sqrt(6)
EPS = 5 - 2 * SQ6
ETA = 5 + 2 * SQ6


def main():
    print("SEED PAIR")
    print("eps = 5 - 2*sqrt(6) =", EPS)
    print("eta = 5 + 2*sqrt(6) =", ETA)
    print("eps * eta =", EPS * ETA)
    print("eps + eta =", EPS + ETA)
    print()

    print("FOLD FROM THE CENTER 5 (author's words)")
    print("inward:  5 - 2*sqrt(6) =", 5 - 2 * SQ6, "= eps")
    print("outward: 5 + 2*sqrt(6) =", 5 + 2 * SQ6, "= eta")
    print()

    print("HALF-STEPS (sqrt rungs, Lemma 2A squaring)")
    r_eps = math.sqrt(3) - math.sqrt(2)
    r_eta = math.sqrt(3) + math.sqrt(2)
    print("sqrt(eps) = sqrt(3) - sqrt(2) =", r_eps)
    print("sqrt(eta) = sqrt(3) + sqrt(2) =", r_eta)
    print("sqrt(eps)^2 =", r_eps ** 2, "-> eps")
    print("sqrt(eta)^2 =", r_eta ** 2, "-> eta")
    print()

    print("LADDER IN AND OUT (exact integer rungs)")
    print("rung  x_n    y_n    x^2-6y^2  eps^n (in)        eta^n (out)       midpoint x_n  eps^n*eta^n")
    x, y = 1, 0  # rung 0: the pair un-separated
    for n in range(7):
        norm = x * x - 6 * y * y
        e_in = EPS ** n
        e_out = ETA ** n
        print(f"{n:<5} {x:<6} {y:<6} {norm:<9} {e_in:<17.10g} {e_out:<17.10g} {x:<12} {e_in * e_out:.12g}")
        assert norm == 1, f"rung {n} norm broken"
        assert abs(e_in - (x - y * SQ6)) < 1e-9, f"rung {n} eps^n"
        assert abs(e_out - (x + y * SQ6)) < 1e-9, f"rung {n} eta^n"
        assert abs((e_in + e_out) / 2 - x) < 1e-9, f"rung {n} midpoint"
        # step out: multiply by the unit (5 + 2*sqrt6)
        x, y = 5 * x + 12 * y, 2 * x + 5 * y
    print()

    print("TRACES (eps^n + eta^n = 2*x_n)")
    x, y = 1, 0
    traces = []
    for _ in range(7):
        traces.append(2 * x)
        x, y = 5 * x + 12 * y, 2 * x + 5 * y
    print(traces)
    print()

    print("RETURN THROUGH THE CENTER")
    print("out n steps then in n steps: eta^n * eps^n = 1 at every rung (shown above).")
    print("inward step = multiply by eps = divide by eta; outward step = multiply by eta.")
    print("look back toward the start through sqrt numbers, outward by the reciprocal (author's candidate).")
    print()
    print("ALL CHECKS PASS")


if __name__ == "__main__":
    main()
