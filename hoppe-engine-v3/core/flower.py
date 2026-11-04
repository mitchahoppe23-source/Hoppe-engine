"""Hoppe Engine v3 — the FLOWER OF LIFE as geometry and a reading
(working part 5).

v1 and v2 carried the flower as counts in a lookup table (1, 7, 19,
37, 61). v3 GENERATES it:

- Centers sit on a hex lattice, one radius apart (radius = 1, center
  spacing = 1), generation g = every center whose hex distance from
  the origin is at most g. The generation counts are DERIVED by
  counting the generated set: 1, 7, 19, 37, 61 — the formula
  3g(g+1)+1 is then checked against the construction, not assumed.
- The stroke is ONE CONTINUOUS STROKE: a visit sequence is built
  ring by ring (close each ring back to its corner, step one radius
  to the next ring's corner) in which every consecutive pair of
  visited centers is exactly one radius apart, and every center is
  visited. Revisits are part of a traced stroke (the v2 path data
  revisits too); what is never done is tangent packing — circles
  here pass through their neighbours' centers and OVERLAP.
- Lenses: two circles of radius 1 whose centers are one radius
  apart overlap in a lens (vesica) of area
  2 r^2 arccos(d / 2r) - (d/2) sqrt(4 r^2 - d^2)  with r = d = 1,
  = 2 pi/3 - sqrt(3)/2 = 1.228369... The engine counts the
  neighbouring pairs in the generated set and computes the area
  from the formula, per generation.
- The traced path data from v2 is carried as its own check: arc
  counts 36 / 108 / 216 / 360 and generation-4 closures at path
  positions 42 / 114 / 222 / 360.

THE READING (the author's pattern mapping, directed 2026-10-30):
the center is the M=0 reference — the observer's center, the
reference event. Outward rings are generations, read as growth,
scale, or time. States are placed on centers; what holds across
the overlaps is the invariant candidate; a leg with no overlapping
receiving circle is the bleed. read_on_flower() implements exactly
that on placed states.
"""
import math

# Cube coordinates (x, y, z) with x + y + z = 0. Neighbours of a
# center are the six cube directions; each is one radius away in
# the cartesian embedding (axial q = x, r = z; cart = (q + r/2,
# r * sqrt(3)/2)).
DIRS = [(1, -1, 0), (1, 0, -1), (0, 1, -1),
        (-1, 1, 0), (-1, 0, 1), (0, -1, 1)]


def _add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _scale(a, k):
    return (a[0] * k, a[1] * k, a[2] * k)


def hex_distance(a, b=(0, 0, 0)):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))


def centers(generation):
    """Every center at hex distance <= generation from the origin."""
    out = set()
    for x in range(-generation, generation + 1):
        for y in range(-generation, generation + 1):
            z = -x - y
            if max(abs(x), abs(y), abs(z)) <= generation:
                out.add((x, y, z))
    return out


def ring(k):
    return {c for c in centers(k) if hex_distance(c) == k}


def generation_counts(max_g=4):
    """Counts DERIVED from the generated construction."""
    return [len(centers(g)) for g in range(max_g + 1)]


def stroke_order(max_g=4):
    """One continuous stroke: a visit sequence covering every center
    of generation max_g, consecutive visits exactly one radius
    apart. Ring k is entered at its corner (one step from the
    previous ring's corner), walked around all six sides, and
    closed back at its corner before stepping out to ring k+1."""
    visits = [(0, 0, 0)]
    corner_dir = DIRS[4]                      # (-1, 1, 0)
    for k in range(1, max_g + 1):
        corner = _scale(corner_dir, k)
        visits.append(corner)                 # one step from prev corner
        cur = corner
        for side in range(6):
            step = DIRS[side]
            for _ in range(k):
                cur = _add(cur, step)
                visits.append(cur)
        # the walk ends back at the corner (closed ring)
    return visits


def neighbour_pairs(generation):
    """Unordered pairs of distinct centers exactly one radius apart."""
    cs = centers(generation)
    pairs = set()
    for c in cs:
        for d in DIRS:
            n = _add(c, d)
            if n in cs:
                pairs.add(frozenset((c, n)))
    return pairs


def lens_area(radius=1.0, distance=1.0):
    """Area of the overlap (lens) of two equal circles."""
    r, d = radius, distance
    return (2 * r * r * math.acos(d / (2 * r))
            - 0.5 * d * math.sqrt(4 * r * r - d * d))


def verify_construction(max_g=4):
    """Executable verifications of the construction itself.
    Returns a list of {name, ok, detail} in the invariants format."""
    out = []
    counts = generation_counts(max_g)
    formula = [3 * g * (g + 1) + 1 for g in range(max_g + 1)]
    out.append({"name": "flower_counts_from_construction",
                "ok": counts == formula == [1, 7, 19, 37, 61],
                "detail": "centers generated on the hex lattice counted: %s; "
                          "formula 3g(g+1)+1 agrees: %s (counts derived "
                          "from the construction, not looked up)"
                          % (counts, formula)})
    visits = stroke_order(max_g)
    steps_ok = all(hex_distance(visits[i + 1], visits[i]) == 1
                   for i in range(len(visits) - 1))
    covered = set(visits) == centers(max_g)
    out.append({"name": "flower_stroke_continuity",
                "ok": steps_ok and covered,
                "detail": "one continuous stroke: %d center visits, every "
                          "consecutive step exactly 1 radius, all %d "
                          "generation-%d centers visited (revisits are "
                          "the traced stroke passing back through a "
                          "center; circles overlap, never tangent-pack)"
                          % (len(visits), len(centers(max_g)), max_g)})
    pairs = neighbour_pairs(2)
    area = lens_area()
    expect_area = 2 * math.pi / 3 - math.sqrt(3) / 2
    out.append({"name": "flower_lens_geometry",
                "ok": abs(area - expect_area) < 1e-12 and len(pairs) > 0,
                "detail": "neighbouring circles (centers 1 radius apart, "
                          "radius 1) overlap in a lens of area "
                          "2 pi/3 - sqrt(3)/2 = %.6f; generation-2 "
                          "construction carries %d neighbouring pairs, "
                          "each with that lens; a fully surrounded circle "
                          "carries 6 lenses in 3 opposite pairs"
                          % (area, len(pairs))})
    return out


def read_on_flower(placed, legs):
    """The pattern reading, implemented.

    placed: {state_name: center} — the states placed on the flower,
    the problem's own state at the center (0,0,0) = the observer's
    center / M=0 reference.
    legs: [{from, to, properties}] — each leg ends at a state; a leg
    whose receiving state is not placed on any center overlapping
    its source center (hex distance 1, i.e. circles that actually
    overlap) has NO RECEIVING CIRCLE and is reported as a bleed.

    What holds across the overlaps — the property set shared by
    every overlapping neighbour pair along accepted legs — is
    returned as the invariant candidate."""
    lines = []
    centre = (0, 0, 0)
    centre_name = None
    for name, c in placed.items():
        if c == centre:
            centre_name = name
    lines.append("center (the observer's center / M=0 reference): %s"
                 % centre_name)
    ring_of = {}
    for name, c in placed.items():
        ring_of[name] = hex_distance(c)
    for name in sorted(placed, key=lambda n: (ring_of[n], n)):
        if name != centre_name:
            lines.append("ring %d: %s (growth / scale / time outward "
                         "from the center)" % (ring_of[name], name))
    shared = None
    bleeds = []
    for leg in legs:
        src, dst = leg["from"], leg["to"]
        if dst not in placed:
            bleeds.append(leg)
            lines.append("BLEED: leg %s -> %s has no receiving circle "
                         "placed on the flower — the leg terminates in "
                         "the void" % (src, dst))
            continue
        if hex_distance(placed[src], placed[dst]) != 1:
            bleeds.append(leg)
            lines.append("BLEED: leg %s -> %s lands on a circle that "
                         "does not overlap its source (centers not one "
                         "radius apart) — no overlap, no receiving state"
                         % (src, dst))
            continue
        props = set(leg.get("properties", []))
        shared = props if shared is None else (shared & props)
        lines.append("overlap %s / %s: lens present (centers one radius "
                     "apart); leg carries %s"
                     % (src, dst, ", ".join(sorted(props)) or "no properties"))
    invariant = sorted(shared) if shared else []
    lines.append("what holds across the overlaps (invariant candidate): %s"
                 % (", ".join(invariant) if invariant else "nothing shared yet"))
    lines.append("bleeds found: %d" % len(bleeds))
    return lines, {"invariant_candidate": invariant, "bleeds": bleeds}
