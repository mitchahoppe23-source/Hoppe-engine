# Scale Propagation In and Out, and the Triangle Closure Partition
— worked showing, 2026-11-13

Addendum to the construction core (stated 2026-11-08). This
showing is COMPUTED from the core's Sections 1–2 and the
author's stated fold and closure words, quoted where his.
It does not alter the core statement. Runnable forms:
scale-propagation-in-out.py and triangle-closure-partition.py
(stdlib only, all checks pass).

## 1. Propagation in and out from the center

The center is 5. The author's fold words (2026-11-11): at
4.89 (2√6) mass starts to fold in on itself; from 5, the
numbers go 5 − 2√6 inward and 5 + 2√6 outward.

- Inward: 5 − 2√6 = ε = 0.1010205144
- Outward: 5 + 2√6 = η = 9.8989794856
- ε·η = 1, ε + η = 10 (checked)

Each rung n of the ladder (computed, exact integers):

- ηⁿ = xₙ + yₙ√6, εⁿ = xₙ − yₙ√6, with xₙ² − 6yₙ² = 1
- Rung midpoints xₙ: 1, 5, 49, 485, 4801, 47525, 470449
- Traces εⁿ + ηⁿ = 2xₙ: 2, 10, 98, 970, 9602, 95050, 940898
- 5 is rung 1's midpoint: the middle and boundary at once,
  at every rung the midpoint is xₙ.

In and out are the same ladder read from two ends: εⁿ·ηⁿ = 1
at every rung (checked). An inward step multiplies by ε,
which is dividing by η; an outward step multiplies by η.
The author's candidate reading direction: look back toward
the start through square-root numbers, outward by the
reciprocal. The half-steps: √ε = √3 − √2, √η = √3 + √2,
and squaring returns ε and η (checked — this is the
Lemma 2A squaring, fixed form).

The return goes only through the center (author's words):
out n steps then in n steps returns to 1, the pair
un-separated, at every rung.

## 2. The triangle closure point: below or above the line

The author's naming (2026-11-13): the point is the
TRIANGLE CLOSURE POINT, and numbers are either below or
above the √2 line.

The √2 line is the diagonal that closes the square into 2
triangles (core, Section 2). Unit square, side 1: the
diagonal is √(1² + 1²) = √2. The closure value is √2.

The partition, computed three ways:

1. No rational number sits on the line. Classic proof
   (checked): if (p/q)² = 2 in lowest terms, p² = 2q²
   forces p even, then q even, contradicting lowest
   terms. Searched to q ≤ 10000: none found. Every
   rational is strictly below or strictly above √2.
2. Rationals converge from both sides and never land on
   it: 1, 7/5, 41/29, 239/169 below; 577/408, 99/70,
   17/12, 3/2, 2 above (each placed by exact square
   comparison, computed).
3. The construction's own ladder straddles the line:
   rung midpoint 1 below, then 5, 49, 485… above;
   εⁿ below and ηⁿ above for every n ≥ 1; √ε below
   and √η above. Nothing in the ladder sits on the line.

Plain: every grid number is below the √2 line or above
it. Nothing sits on it. The line is the divider the
triangle closes on — the closure point no number occupies.

## Standing

- The fold words, the return-through-center words, and
  the triangle-closure naming are the author's, quoted.
- The ladder walk, the partition, and the irrationality
  proof are computed showings from the core arithmetic.
  The irrationality proof is the classic proof, a known
  proof, not a new claim.
- What this does NOT do: it shows discrete propagation
  and the discrete partition. It does not build the
  continuum bridge (carrying a discrete result into the
  smooth limit) — that gap stands as stated.
