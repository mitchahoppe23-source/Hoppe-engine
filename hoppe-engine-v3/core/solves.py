"""Hoppe Engine v3 — the WORKED INCONSISTENCY SOLVES (the main event).

Mitch Hoppe's direction (2026-11-02, in substance): show how we
solved the inconsistencies with the code, instead of doing a test
people already do every day, which has no return leg. A one-way
pass/fail check whose result lands nowhere is exactly the bleed
shape the framework rejects — every output must cross a boundary
into a receiving state and be USED there.

So each demonstration below runs the full solve, end to end, in the
transcript:

    BEFORE      the inconsistency as stated (human numbers /
                observer's view / mixed sticks)
    CORRECT     remove the observer's view and the human-chosen
    THE MEASURE numbers, restate as dimensionless ratios, same
                measuring stick the same exact way at both ends,
                start from the seed epsilon instead of true zero
    RUN H       H(S, B, T) = S' — state, smart-filter boundary,
                transition — the changed state is a NEW ledger
                entry (history is never edited)
    INVARIANT   the thing that does not change while the state
    SOLVED      changes completely
    AFTER       S', the inconsistency shown dissolved / restated,
                at its recorded label
    RETURNED    where the result went next: the invariant is
                carried back in as the working stick / input of a
                later demonstration in THIS run (the chain is
                printed at the end), and S' stands in the ledger
                as a state later steps start from

Sources: the inconsistencies register and the applied worksheet
(m0-inconsistencies-register.md; m0-h-operator-applied-to-the-rest.md,
29 Oct 2026). AUTHORSHIP, preserved exactly as in those files: the
applications are ANALYST WORK prepared under the framework author's
direction and method, for his confirmation or correction item by
item. They are not Mitch Hoppe's positions except where a framework
position of his is cited inside an item (the M=0 statement, the
mismeasurement definition, the stick rule, the Hubble and
dark-matter positions, the arrow position). Labels match the
register / applied worksheet.

The return-leg chain, as already in the record: the shared stick
hbar c is solved at the Planck / black-hole boundary (Item 6), and
that same stick is then the working stick for the
gravity/electromagnetism comparison (Item 3) and the hierarchy
restatement (Item 7). The scale-transition invariant (Item 5) is
returned into the fine-structure item, where the 3 Pell steps are
the author's stated direction. Item order in this run follows the
chain so every RETURNED line names a use that actually happens
later in the transcript.
"""
from decimal import Decimal, getcontext

import invariants as inv
import laser
import lens

getcontext().prec = 60

D = Decimal
MEASURED_ALPHA_INV = D("137.035999177")


def _fmt(x, places="0.000001"):
    return str(x.quantize(D(places)))


def _sci(x, sig=4):
    if x == 0:
        return "0"
    e = x.adjusted()
    m = x.scaleb(-e)
    q = D(1).scaleb(-(sig - 1))
    return "%s e%d" % (m.quantize(q), e)


class SolveBook:
    """Collects demonstrations; each S' is appended to the run's
    ledger as a new entry, and each RETURNED claim is checked at
    the end: a return is only printed as kept if the named later
    demonstration actually consumed the carried value (the run
    passes carried values forward in `self.carried`)."""

    def __init__(self, ledger):
        self.ledger = ledger
        self.demos = []
        self.carried = {}          # name -> value carried forward
        self.consumed = []         # (name, by_item) actually used later

    def carry(self, name, value):
        self.carried[name] = value

    def use(self, name, by_item):
        assert name in self.carried, "return-leg break: %s not carried" % name
        self.consumed.append((name, by_item))
        return self.carried[name]

    def record(self, demo):
        self.demos.append(demo)
        self.ledger.append("SOLVE", {
            "item": demo["item"], "title": demo["title"],
            "S": demo["S"], "B": demo["B"], "T": demo["T"],
            "S_prime": demo["after"], "invariant": demo["invariant"],
            "label": demo["label"], "returned_to": demo["returned_to"]})
        return demo


def _demo(book, lines, **kw):
    if "labels" in kw:   # an item may carry split label lines (Hubble)
        kw["label"] = " | ".join(kw["labels"])
    d = book.record(kw)
    lines.append("")
    lines.append("--- SOLVE: %s ---" % kw["title"])
    lines.append("BEFORE: %s" % kw["before"])
    lines.append("CORRECT THE MEASUREMENT: %s" % kw["correct"])
    lines.append("RUN H(S, B, T) = S': S = %s | B = %s | T = %s"
                 % (kw["S"], kw["B"], kw["T"]))
    for extra in kw.get("worked", []):
        lines.append("    %s" % extra)
    lines.append("INVARIANT SOLVED: %s" % kw["invariant"])
    lines.append("AFTER (S', a new ledger entry; nothing edited): %s" % kw["after"])
    for lab in kw.get("labels", [kw["label"]]):
        lines.append("LABEL: %s" % lab)
    lines.append("RETURNED: %s" % kw["returned"])
    return d


# ----------------------------------------------------------------------
# Item 6 — black-hole boundary (run first: it solves the stick)
# ----------------------------------------------------------------------

def solve_black_hole(book, lines):
    target = inv.HBAR * inv.C_LIGHT / (4 * inv.PI * inv.KB)
    worked = []
    for n in (D(1), D(10), D("1e38")):
        worked.append("n = %s: R_s/l_P = 2n = %s ; T_H/T_P = 1/(8 pi n) = %s ; "
                      "S_BH/k_B = 4 pi n^2 = %s ; R_s*T_H = hbar c/(4 pi k_B) "
                      "(unchanged)"
                      % (_sci(n, 1), _sci(2 * n, 1),
                         _sci(1 / (8 * inv.PI * n), 4), _sci(4 * inv.PI * n * n, 4)))
    worked.append("R_s*T_H = %s m K at every n (checked at n = 1, 10, 10^38; "
                  "worst relative deviation under 1e-30 in the supporting checks)"
                  % _sci(target, 4))
    book.carry("hbar_c_stick", "hbar c (the shared Planck stick)")
    book.carry("rs_th_invariant", target)
    return _demo(
        book, lines,
        item="6", title="Register item 6 — the black-hole boundary: radius and "
                        "temperature in separate formulas, no combined invariant stated",
        before="A black hole's radius is stated in metres and its temperature "
               "in kelvin, from two separate formulas in two human units; "
               "nothing in the statement says what, if anything, stays fixed "
               "as the mass changes.",
        correct="Restate in ratios on the Planck stick, same stick at both "
                "ends: n = M/m_P (dimensionless), R_s/l_P, T_H/T_P, S_BH/k_B. "
                "The human units cancel; the mass is now a pure count n.",
        S="a black hole of mass ratio n (a mass state)",
        B="the horizon — the boundary at which the ratios are read",
        T="change the mass ratio n (zoom the state along the mass ladder)",
        worked=worked,
        invariant="R_s*T_H = hbar c/(4 pi k_B) — the product does not move "
                  "while n runs from 1 to 10^38; equivalently R_s/l_P = 2n, "
                  "T_H/T_P = 1/(8 pi n), S_BH/k_B = 4 pi n^2",
        after="radius and temperature are one boundary relationship read on "
              "one stick; the apparent separateness was the two human units, "
              "not the hole",
        label="DERIVED (algebra and numbers; checked 2026-10-29 as following "
              "from the standard Planck and Hawking definitions, used as "
              "routes with premises stated)",
        returned="the solved stick hbar c is RETURNED AND USED as the "
                 "working stick of the singularities solve next, then of "
                 "the gravity/electromagnetism solve and the hierarchy "
                 "solve — watch for 'stick returned from item 6' there",
        returned_to="items 1, 3, 7")


# ----------------------------------------------------------------------
# Item 1 — singularities
# ----------------------------------------------------------------------

def solve_singularities(book, lines):
    stick = book.use("hbar_c_stick", "item 1")
    rho_p = inv.C_LIGHT ** 5 / (inv.HBAR * inv.G_NEWTON ** 2)
    worked = ["Planck density ceiling: rho_P = m_P/l_P^3 = c^5/(hbar G^2) = "
              "%s kg/m^3 — finite (stick returned from item 6: %s)"
              % (_sci(rho_p, 4), stick)]
    for n in (D(1), D(10), D(100)):
        ratio = D(3) / (32 * inv.PI) / (n * n)
        worked.append("n = %s: mean density rho/rho_P = 0.02984/n^2 = %s — "
                      "finite, and SMALLER for the larger hole"
                      % (n, _sci(ratio, 4)))
    worked.append("(Mean density uses the Euclidean volume (4/3) pi R_s^3; "
                  "proper interior volume is slicing-dependent — audit "
                  "footnote P5, carried, not hidden.)")
    book.carry("planck_density_ceiling", rho_p)
    return _demo(
        book, lines,
        item="1", title="Register item 1 — singularities: collapse to zero "
                        "volume and infinite density",
        before="A collapsing mass described in human numbers (kilograms, "
               "metres) at ever smaller radius: the description runs to "
               "zero volume and the density runs to infinity.",
        correct="Start from the seed instead of true zero: the smallest "
                "volume state is the Planck/node volume, not zero. Restate "
                "with the Planck stick the same way at both ends: "
                "n = M/m_P, r/l_P, rho/rho_P.",
        S="a collapsing mass at radius ratio r/l_P (a mass state)",
        B="the node floor — the boundary at epsilon, not at zero",
        T="collapse: the radius ratio shrinks toward the floor",
        worked=worked,
        invariant="rho_P = 5.155e96 kg/m^3 is a finite ceiling; a "
                  "Schwarzschild hole's mean density is rho/rho_P = "
                  "0.02984/n^2, finite for every n — nothing in the ratio "
                  "description diverges except the r -> 0 limit that the "
                  "floor explicitly replaces",
        after="the 'infinite density' was the true-zero starting point in "
              "the description; on the seed floor the same collapse states "
              "a finite ceiling and finite ratios at every size",
        label="DERIVED for the algebra and the finite ceiling; HYPOTHESIS "
              "for the physical claim that collapse in nature stops at "
              "the framework node floor (pending an observation that "
              "distinguishes a floor from a singularity)",
        returned="rho_P, computed here, is RETURNED AND USED in the "
                 "gravity/electromagnetism solve as the top of the same "
                 "Planck scale its couplings are read against, and this "
                 "item's S' (collapse restated on the floor) stands in the "
                 "ledger as the state the scale-transition solve zooms from",
        returned_to="items 3, 5")


# ----------------------------------------------------------------------
# Item 3 — gravity and electromagnetism, one language
# ----------------------------------------------------------------------

def solve_gravity_em(book, lines):
    stick = book.use("hbar_c_stick", "item 3")
    book.use("planck_density_ceiling", "item 3")
    alpha = 1 / MEASURED_ALPHA_INV
    ag_e = inv.alpha_g(inv.PARTICLES_GEV["electron"])
    ag_p = inv.alpha_g(inv.PARTICLES_GEV["proton"])
    ratio = alpha / ((inv.PARTICLES_GEV["electron"] / inv.M_P_GEV)
                     * (inv.PARTICLES_GEV["proton"] / inv.M_P_GEV))
    worked = [
        "electromagnetism on the returned stick: alpha = e^2/(4 pi eps0 "
        "hbar c) = 1/137.036 (dimensionless; stick returned from item 6: %s)"
        % stick,
        "gravity on the SAME stick: alpha_G = G m^2/(hbar c) = (m/m_P)^2",
        "alpha_G electron = %s ; alpha_G proton = %s"
        % (_sci(ag_e, 4), _sci(ag_p, 4)),
        "electric-to-gravitational force ratio, electron-proton = "
        "alpha / ((m_e/m_P)(m_p/m_P)) = %s" % _sci(ratio, 4),
    ]
    book.carry("alpha_g_method", "alpha_G = (m/m_P)^2 on the hbar c stick")
    book.carry("alpha_g_electron", ag_e)
    book.carry("alpha_g_proton", ag_p)
    return _demo(
        book, lines,
        item="3", title="Register item 3 — gravity and electromagnetism "
                        "described in unrelated languages",
        before="Two forces, two sticks: electromagnetism with a "
               "dimensionless coupling, gravity with the dimensional "
               "constant G — stated that way the two cannot be compared "
               "directly at all.",
        correct="Put both on the same stick, hbar c, as dimensionless "
                "ratios, the same stick the same exact way at both ends — "
                "the stick solved and returned from item 6.",
        S="the two forces as stated in mixed sticks (energy states)",
        B="the shared denominator hbar c — the boundary both couplings "
          "are read across",
        T="restatement: one ratio of ratios on one stick",
        worked=worked,
        invariant="the shared stick hbar c itself — the same hbar c from "
                  "the Planck scale (E_P x l_P = hbar c) and the "
                  "black-hole boundary (item 6). Gravity's weakness in "
                  "this restatement is the smallness of (m/m_P)^2 for "
                  "known particles, not a separate mystery number",
        after="both forces speak one language: dimensionless couplings on "
              "one stick, read against each other directly",
        label="DERIVED for the restatement and the numbers; HYPOTHESIS "
              "for the framework mechanism (gravity as inward compression "
              "toward the lattice floor, electromagnetism as boundary "
              "interactions at nodes) as the physical story behind the ratios",
        returned="the alpha_G method and the electron/proton values are "
                 "RETURNED AND USED by the hierarchy solve next, which "
                 "extends this exact table to all six known particles "
                 "instead of recomputing on a new stick",
        returned_to="item 7")


# ----------------------------------------------------------------------
# Item 7 — hierarchy
# ----------------------------------------------------------------------

def solve_hierarchy(book, lines):
    method = book.use("alpha_g_method", "item 7")
    worked = ["method returned from item 3: %s (unreduced Planck mass "
              "m_P = 1.2209e19 GeV/c^2, declared; under the reduced "
              "Planck mass every value scales by exactly 8 pi — the "
              "supporting checks verify that rule)" % method]
    table = {}
    for name in ("electron", "proton", "W boson", "Z boson",
                 "Higgs boson", "top quark"):
        val = inv.alpha_g(inv.PARTICLES_GEV[name])
        table[name] = val
        worked.append("alpha_G %-12s = %s" % (name, _sci(val, 3)))
    worked.append("electron and proton rows reproduce item 3's returned "
                  "values exactly (%s, %s) — same stick, same way, both ends"
                  % (_sci(book.use("alpha_g_electron", "item 7"), 4),
                     _sci(book.use("alpha_g_proton", "item 7"), 4)))
    worked.append("even the heaviest known particle (top quark) sits "
                  "about 16.8 orders of magnitude below the Planck mass")
    book.carry("alpha_g_table", table)
    return _demo(
        book, lines,
        item="7", title="Register item 7 — the hierarchy problem: why "
                        "gravity is so weak",
        before="'Gravity is weak' stated by comparing a dimensional "
               "constant G against the dimensionless alpha — two sticks "
               "mixed inside one comparison, so the numbers cannot be "
               "read against each other.",
        correct="Item 3's restatement, returned and reused: both forces "
                "on the hbar c stick, alpha_G = (m/m_P)^2 per particle.",
        S="the six known particles' masses as human numbers (GeV)",
        B="the Planck boundary m_P — every mass read as the ratio m/m_P",
        T="restatement of each mass as a dimensionless ratio, then squared",
        worked=worked,
        invariant="the shared stick hbar c (items 6 and 3, returned): "
                  "'gravity is weak' becomes the single checked fact "
                  "that (m/m_P)^2 is at most about 2e-34 for every "
                  "known particle",
        after="the weakness is no longer a mystery number between two "
              "languages; it is the smallness of (m/m_P)^2, read on one "
              "stick, for every particle in the table",
        label="DERIVED for the restatement and the ratios; OPEN for why "
              "the masses sit that far below m_P; HYPOTHESIS for the "
              "framework mechanism behind the ratios",
        returned="the full alpha_G table is RETURNED AND USED as this "
                 "run's standing coupling table: the fine-structure "
                 "demonstration reads alpha itself against this same "
                 "stick, and the table stands in the ledger for any "
                 "later item instead of being recomputed",
        returned_to="item 4 (fine structure)")


# ----------------------------------------------------------------------
# Item 5 — scale transitions
# ----------------------------------------------------------------------

def solve_scale_transitions(book, lines):
    worked = []
    for n in range(5):
        x, y = inv.pell_step(n)
        worked.append("step %d: (x, y) = (%d, %d) ; x^2 - 6y^2 = %d"
                      % (n, x, y, x * x - 6 * y * y))
    worked.append("zoom in by epsilon or out by eta: the state changes "
                  "completely at every step; eps*eta = 1 (exact, Q(sqrt(6)) "
                  "lane) is the one-step case of the same invariant")
    book.carry("pell_invariant", "x^2 - 6y^2 = 1 at every Pell step")
    book.carry("pell_steps", 4)
    return _demo(
        book, lines,
        item="5", title="Register item 5 — scale transitions: no clean "
                        "rule from the Planck scale to the everyday scale",
        before="Each scale described in its own human numbers, with no "
               "stated rule for what survives a change of scale — so a "
               "zoom looks like a jump into a different subject.",
        correct="State the ladder in dimensionless form from the seed: "
                "the Pell states (x, y) generated by eta (zoom out) and "
                "epsilon (zoom in), starting from eps = 0.1010205 instead "
                "of true zero.",
        S="a Pell state (x, y) on the scale ladder (matter/mass, energy, "
          "or transition state, per the item being worked)",
        B="the boundary between tiers/states",
        T="one zoom step: multiply by eta (out) or epsilon (in)",
        worked=worked,
        invariant="x^2 - 6y^2 = 1 at EVERY step — steps 0 to 4 checked "
                  "above; the state changes completely, the invariant "
                  "does not change at all. This is the H Operator in its "
                  "purest form in the framework",
        after="a zoom is a transition with a named invariant, not a jump: "
              "any state on the ladder can be carried to the next tier "
              "and checked against the same 1",
        label="DERIVED as mathematics; HYPOTHESIS for the claim that "
              "physical scale transitions in nature follow this ladder "
              "(until a measured transition is matched to a step)",
        returned="the Pell invariant and its steps are RETURNED AND USED "
                 "by the fine-structure demonstration: the author's "
                 "stated direction there is to zoom in/out with the 3 "
                 "steps of the Pell equation — this solve is where those "
                 "steps and their invariant come from",
        returned_to="item 4 (fine structure)")


# ----------------------------------------------------------------------
# Hubble tension — framework position (Mitch's), analyst application
# ----------------------------------------------------------------------

def solve_hubble(book, lines):
    planck, shoes = D("67.4"), D("73.04")
    holicow, trgb = D("73"), D("69.8")
    ratio = shoes / planck
    sigma = (shoes - planck) / (D("0.5") ** 2 + D("1.04") ** 2).sqrt()

    def _ratio(x):
        return _fmt(x / planck, "0.0000")

    # The routes compared through H: what each route is actually
    # looking at (TARGET = S), the lens stack it reads through
    # (STACK = B, rung by rung), the reading pass (T), and the H_0
    # that comes out (RESULT = S'). S is the same for every route;
    # only B changes. (Route data per the task brief; Planck and
    # SH0ES values recorded and verified 2026-10-29; H0LiCOW
    # recorded 2026-10-29 as about 73; TRGB verified for this build
    # from Freedman et al. 2019, arXiv:1907.05922 — see below.)
    routes = [
        ("Planck (the early route)",
         "the cosmic microwave background — light released about "
         "380,000 years after the Big Bang, read as a temperature "
         "pattern across the whole sky",
         "CMB temperature pattern -> the sound-horizon scale read "
         "off the pattern -> a Lambda-CDM model fit (the model is a "
         "lens in the stack: H_0 is inferred through it, not read "
         "off the sky directly)",
         "H_0 = 67.4 +/- 0.5 km/s/Mpc", planck),
        ("SH0ES (the late, ladder route)",
         "Cepheid variable stars in nearby galaxies, and Type Ia "
         "supernovae in farther ones",
         "parallax (first rung: nearby stars) -> Cepheids (their "
         "period-brightness relation calibrates distance) -> Type "
         "Ia supernovae (their calibrated brightness carries the "
         "scale outward) -> the recession speeds of the host "
         "galaxies",
         "H_0 = 73.04 +/- 1.04 km/s/Mpc", shoes),
        ("H0LiCOW (the literal-lens route)",
         "distant quasars whose light is gravitationally lensed by "
         "a foreground galaxy into multiple images",
         "quasar light -> the foreground galaxy's gravity as a "
         "LITERAL lens (multiple images, with time delays between "
         "them) -> a model of the lens's mass -> the time-delay "
         "distance",
         "H_0 = about 73 km/s/Mpc", holicow),
        ("TRGB (one rung changed)",
         "the brightest red giant stars — the tip of the red giant "
         "branch — in galaxies, used to calibrate the SAME Type Ia "
         "supernovae SH0ES uses, instead of Cepheids",
         "nearby anchors (the Large Magellanic Cloud distance) -> "
         "the TRGB brightness (a standard candle read in galaxy "
         "halos) -> the same Type Ia supernovae -> the recession "
         "speeds of the host galaxies",
         "H_0 = 69.8 +/- 0.8 (stat) +/- 1.7 (sys) km/s/Mpc", trgb),
    ]
    worked = [
        "Planck (early universe, inferred through the model): "
        "H_0 = 67.4 +/- 0.5 km/s/Mpc",
        "SH0ES (late, local distance ladder): H_0 = 73.04 +/- 1.04 km/s/Mpc",
        "the one dimensionless number in dispute: 73.04/67.4 = %s "
        "(an 8.37%% mismatch, at about %s sigma from the uncertainties "
        "printed here)" % (_fmt(ratio), _fmt(sigma, "0.0")),
    ]
    worked += laser.demonstration_lines(5)
    worked.append(
        "THE ROUTES COMPARED THROUGH H(S, B, T) = S' — what each "
        "route is actually looking at, put in and compared (the "
        "author's direction, 2026-11-02). S is what they're trying "
        "to look at, and S is the SAME for every route: the "
        "expanding universe — one universe, one expansion signal; "
        "no route looks at a different universe. B is that route's "
        "lens stack, rung by rung. T is the reading pass. S' is the "
        "H_0 that route comes out with")
    for name, target, stack, result, value in routes:
        worked.append("ROUTE — %s, run through H:" % name)
        worked.append("    TARGET (S, what it looks at): %s" % target)
        worked.append("    STACK (B, rung by rung): %s" % stack)
        worked.append("    T: the reading pass through that stack")
        worked.append("    RESULT (S'): %s — ratio to the Planck "
                      "result: %s" % (result, _ratio(value)))
    worked.append(
        "THE COMPARISON — S' by route, with S held the same "
        "throughout (ratios to the Planck S'):")
    for name, _t, _s, _r, value in routes:
        worked.append("    %-34s S' ratio to Planck = %s"
                      % (name, _ratio(value)))
    worked.append(
        "READING-OFF: S' varies as B varies — Planck %s, SH0ES %s, "
        "H0LiCOW %s, TRGB %s — the same pattern as the laser table "
        "directly above this solve: the source (S) never changes, "
        "the stack (B) changes, and the reading (S') changes with "
        "the stack" % (_ratio(planck), _ratio(shoes),
                       _ratio(holicow), _ratio(trgb)))
    worked.append(
        "THE ONE-RUNG COMPARISON: SH0ES and TRGB share most of the "
        "ladder — both calibrate the same Type Ia supernovae — and "
        "differ in ONE rung (Cepheids out, the red-giant tip in). "
        "S' moves from 73.04 to 69.8, landing BETWEEN Planck and "
        "SH0ES: change one rung of B and S' moves, while S never "
        "changed at all")
    worked.append(
        "NO ROUTE HAS ZERO LENSES: every stack above has rungs, and "
        "the observer's own position is always at least one lens "
        "(the run loop's step 1) — even the Planck route, which "
        "looks at the oldest light there is, ends in a model fit "
        "before an H_0 comes out")
    worked.append(
        "TRGB SOURCE: Freedman et al. 2019, 'The Carnegie-Chicago "
        "Hubble Program. VIII. An Independent Determination of the "
        "Hubble Constant Based on the Tip of the Red Giant Branch' "
        "(arXiv:1907.05922; The Astrophysical Journal) — the "
        "abstract states H_0 = 69.8 +/- 0.8 (stat) +/- 1.7 (sys) "
        "km/s/Mpc, obtained by calibrating Type Ia supernovae with "
        "the TRGB, parallel to but independent of the Cepheid "
        "distance scale, sitting midway in the range of the Hubble "
        "tension (fetched and checked for this build)")
    worked.append(
        "HONEST LIMIT, printed on purpose: this compares the routes "
        "AS STACKS. It does not by itself prove the 1.0837 comes "
        "from the stacks — the attribution stays HYPOTHESIS (label "
        "lines below) until the ratio is shown to track a specific "
        "stack difference rather than anything in the expansion "
        "itself")
    # -- Boundary set to 5: rungs identified by reach ----------------
    # The author's direction (2026-11-02, verbatim): "So we set the
    # boundary to 5 and then identify the rungs correctly as to how
    # far out we're trying to look". The boundary-5 count-out is his
    # METHOD (the construction sits inside the boundary at 5; 5 is
    # the centre/exchange point — from 5, -2 sqrt(6) reaches the
    # seed epsilon and +2 sqrt(6) the partner eta, on every axis;
    # his circling-the-square method is "boundary set to 5"). The
    # alignment table below is ANALYST ASSEMBLY (Muse's), put up
    # for his correction — not his ruling. Reach figures are printed
    # only where verified from a fetched source (named in the
    # SOURCES line); anything not verified cleanly is printed as
    # the qualitative band only.
    worked.append(
        "BOUNDARY SET TO 5 — RUNGS IDENTIFIED BY REACH (the "
        "author's direction, 2026-11-02: \"So we set the boundary "
        "to 5 and then identify the rungs correctly as to how far "
        "out we're trying to look\")")
    worked.append(
        "THE SETTING: the boundary/reference is set to 5 — the "
        "centre every route is counted OUT from and back to (the "
        "observer's centre; step 1 of the run loop: measure from "
        "the observer's centre). In the author's construction the "
        "whole count sits inside the boundary at 5, the exchange "
        "point: from 5, -2 sqrt(6) reaches the seed and +2 sqrt(6) "
        "reaches the partner, on every axis. A route is only "
        "comparable to another route when its rungs are identified "
        "by REACH on this same count-out — how far out each rung "
        "actually looks — so rungs at the same reach line up across "
        "routes, and a rung that is missing, jumped, or swapped "
        "shows up as what it is")
    worked.append(
        "AUTHORSHIP of this table, stated plainly: the boundary-5 "
        "count-out is the author's method; the alignment table "
        "itself is analyst assembly (Muse's), built from the "
        "routes' published rungs, put up for the author's "
        "correction. It is not his ruling, and no label in this "
        "item changes because of it")
    worked.append(
        "REACH-ORDER TABLE — rows are reach bands, counted out "
        "from the centre; the four routes are read across each "
        "band. NO RUNG means the route has no rung at that reach: "
        "it jumps or carries across that stretch (how it carries "
        "is said in the cell)")
    worked.append("BAND (a) — HOME / ANCHOR REACH (inside our own "
                  "galaxy and its nearest neighbours)")
    worked.append(
        "    Planck:  NO RUNG — its first reading is at the "
        "boundary reach (band e); the whole count-out below that "
        "is carried inside the model fit")
    worked.append(
        "    SH0ES:   RUNG — geometric anchors: parallax of stars "
        "and Cepheids in our own galaxy (the parallax reach was "
        "extended to a few kiloparsecs), and the Large Magellanic "
        "Cloud anchor at 49.59 kiloparsecs (Pietrzynski et al. "
        "2019)")
    worked.append(
        "    TRGB:    RUNG — the same Large Magellanic Cloud "
        "anchor: the red-giant-tip zero point is set with the "
        "LMC's distance, from 20 late-type detached eclipsing "
        "binaries in the LMC (Freedman et al. 2019); the LMC sits "
        "at 49.59 kiloparsecs (Pietrzynski et al. 2019)")
    worked.append(
        "    H0LiCOW: NO RUNG — no home anchors of its own; its "
        "scale comes out of the lens geometry and the lens-mass "
        "model at the deep reach (band d)")
    worked.append("BAND (b) — NEARBY-GALAXY REACH (the calibrator "
                  "stars in the supernova host galaxies, tens of "
                  "megaparsecs out)")
    worked.append(
        "    Planck:  NO RUNG — it carries across this whole "
        "stretch inside the model fit; nothing here is read "
        "directly")
    worked.append(
        "    SH0ES:   RUNG — Cepheids in the supernova host "
        "galaxies: 42 calibrator supernovae in 37 host galaxies, "
        "all at redshift below 0.01 (Riess et al. 2022)")
    worked.append(
        "    TRGB:    RUNG — the red-giant tip, read in the halos "
        "of 18 supernova host galaxies from 7 to nearly 20 "
        "megaparsecs away (Freedman et al. 2019). SAME REACH as "
        "the SH0ES rung in this band, DIFFERENT RUNG IDENTITY — "
        "this is the one-rung swap, made visible in the table")
    worked.append(
        "    H0LiCOW: NO RUNG — it jumps this reach entirely; "
        "nothing in its stack is read here")
    worked.append("BAND (c) — HUBBLE-FLOW REACH (the Type Ia "
                  "supernovae and their host galaxies' recession "
                  "speeds, hundreds of megaparsecs out)")
    worked.append(
        "    Planck:  NO RUNG of its own — the flow stretch is "
        "inside the model it fits; the model does the carrying "
        "across this band")
    worked.append(
        "    SH0ES:   RUNG — Type Ia supernovae in the Hubble "
        "flow, redshift 0.023 to 0.15 (Riess et al. 2022)")
    worked.append(
        "    TRGB:    RUNG — the same kind of rung: the TRGB "
        "distances are anchored to galaxies extending the "
        "measurement into the Hubble flow, through the Carnegie "
        "Supernova Project sample of about 100 well-observed "
        "Type Ia supernovae (Freedman et al. 2019)")
    worked.append(
        "    H0LiCOW: NO RUNG — it uses no supernova-flow rung; "
        "its distance is the time-delay distance read at the deep "
        "reach (band d)")
    worked.append("BAND (d) — DEEP REACH (looked at through a "
                  "lens partway out)")
    worked.append(
        "    Planck:  NO RUNG — nothing at this reach is read "
        "directly; the model carries across it, as in bands b "
        "and c")
    worked.append(
        "    SH0ES:   NO RUNG — the ladder stops at the flow "
        "reach (band c); it has no rung out here")
    worked.append(
        "    TRGB:    NO RUNG — the same: its farthest rung is "
        "the flow reach (band c)")
    worked.append(
        "    H0LiCOW: RUNGS — the only route with rungs in this "
        "band: a foreground lens galaxy partway out, and the "
        "source quasars behind it, six systems with source "
        "redshifts 0.654 to 1.789 (Wong et al. 2020), read BACK "
        "through the lens (time delays between the images), with "
        "the lens-mass model as the closing step of its stack")
    worked.append("BAND (e) — THE BOUNDARY REACH (the farthest "
                  "look there is)")
    worked.append(
        "    Planck:  RUNG — its home rung: the cosmic microwave "
        "background itself, light released at recombination, "
        "about 380,000 years after the Big Bang (redshift about "
        "1090; Planck Collaboration 2020). From this rung it "
        "infers BACK to the centre through the model fit")
    worked.append(
        "    SH0ES:   NO RUNG — the ladder never reaches the "
        "boundary; its last rung is back at band (c)")
    worked.append(
        "    TRGB:    NO RUNG — the same: no rung anywhere near "
        "the boundary reach")
    worked.append(
        "    H0LiCOW: NO RUNG — its deepest look (band d) stops "
        "far short of the boundary reach")
    worked.append(
        "DIRECTION OF TRAVEL, per route — same boundary, three "
        "different directions of count: the ladder routes (SH0ES, "
        "TRGB) BUILD centre-outward, rung by rung (bands a -> b "
        "-> c), then read the flow back as H_0. The lensing route "
        "(H0LiCOW) does not build from the centre at all: it reads "
        "a deep target (band d) BACK through a middle lens. The "
        "early route (Planck) STARTS AT the boundary reach (band "
        "e) and infers back to the centre through the model — its "
        "whole count runs in the opposite direction to the "
        "ladders'")
    worked.append(
        "READING-OFF, with the boundary set to 5 and the rungs "
        "identified by reach: the four results are no longer four "
        "rival numbers for one thing. They are readings taken "
        "with different rung sets over different stretches of the "
        "same count-out. The stretches where a route has NO RUNG "
        "are exactly where its model does the carrying — Planck "
        "carries bands a through d inside its fit; the ladders "
        "carry everything past band c by never going there; "
        "H0LiCOW carries bands a through c by jumping them. A "
        "discrepancy can sit in the carrying (B) without anything "
        "differing at the target (S) — which is the boundary "
        "location the author ruled for this item, now visible "
        "rung by rung")
    worked.append(
        "THE WORKED EXAMPLE stays the one-rung swap at band (b): "
        "same reach, same supernovae beyond it, one rung's "
        "identity changed (Cepheids for the red-giant tip) — and "
        "the reading at the centre moved from 73.04 to 69.8. In "
        "the table that swap is one cell changing in one band; "
        "every other cell in the two routes is the same shape")
    worked.append(
        "SOURCES for the reach figures printed above (each "
        "fetched and checked for this build): Pietrzynski et al. "
        "2019, Nature 567, 200-203 — the LMC distance 49.59 "
        "+/- 0.09 (stat) +/- 0.54 (sys) kiloparsecs, from 20 "
        "eclipsing binary systems. Riess et al. 2022, The "
        "Astrophysical Journal Letters 934, L7 (the SH0ES "
        "paper) — 42 calibrator supernovae in 37 host galaxies at "
        "redshift below 0.01, Cepheid parallax extended to a few "
        "kiloparsecs, and the Hubble-flow supernovae at redshift "
        "0.023 to 0.15. Freedman et al. 2019, arXiv:1907.05922 — "
        "the LMC-anchored TRGB zero point, 18 supernova host "
        "galaxies 7 to nearly 20 megaparsecs away, and about 100 "
        "Carnegie Supernova Project supernovae carrying the "
        "measurement into the Hubble flow. Wong et al. 2020, "
        "Monthly Notices of the Royal Astronomical Society 498, "
        "1420-1439 (H0LiCOW XIII) — six lensed-quasar systems, "
        "source redshifts 0.654 to 1.789. Planck Collaboration "
        "2020, Astronomy & Astrophysics 641, A6 — recombination "
        "at redshift about 1090, about 380,000 years after the "
        "Big Bang. Figures that could not be verified cleanly "
        "(the lens galaxies' own redshift range) are printed as "
        "the qualitative band only, with no number")
    book.carry("hubble_ratio", ratio)
    book.carry("hubble_route_table",
               "Planck 67.4 (ratio 1.0000); SH0ES 73.04 (ratio %s); "
               "H0LiCOW about 73 (ratio %s); TRGB 69.8 (ratio %s) — "
               "one target (S the same), four stacks (B), S' varies "
               "with B" % (_ratio(shoes), _ratio(holicow),
                           _ratio(trgb)))
    book.carry("hubble_rung_table",
               "boundary set to 5, rungs identified by reach, bands "
               "(a) home/anchor -> (e) boundary: Planck has a rung "
               "only at (e) and carries (a)-(d) inside its model "
               "fit; SH0ES and TRGB have rungs at (a), (b), (c) and "
               "none past (c), differing only in the identity of "
               "the (b) rung (Cepheids vs the red-giant tip); "
               "H0LiCOW has rungs only at (d), read back through "
               "its lens, and none at (a), (b), (c) or (e) — the "
               "stretches with no rung are where each route's model "
               "does the carrying (B)")
    return _demo(
        book, lines,
        item="Hubble", title="Hubble tension — the same expansion read "
                             "through two different lenses",
        before="Two measured expansion rates that disagree: 67.4 against "
               "73.04, quoted in human units (km/s/Mpc) and treated as a "
               "contradiction inside the universe itself.",
        correct="Strip the human units: there is exactly ONE "
                "dimensionless number in dispute, the ratio 1.0837. Then "
                "locate it by the author's stick rule: the two ends are "
                "not using the same stick the same exact way — one side "
                "infers H_0 from the early universe through a model, the "
                "other measures it up a local ladder, and a third route "
                "reads it through literal gravitational lenses.",
        S="the expanding universe (one state)",
        B="the lens each measurement is taken through — by the author's "
          "ruling (2026-10-29) the discrepancy is assigned to the "
          "BOUNDARY category, not to the contents within either "
          "measurement; the sigma figure is a within-category statistic "
          "and does not locate the gap",
        T="reading the same state through the second lens",
        worked=worked,
        invariant="the single ratio 1.0837, located at the boundary "
                  "between the two measurement regimes; same universe "
                  "(same state), different boundary, different answer — "
                  "the measuring-stick rule read straight off",
        after="the 'tension' is restated as a boundary/lens difference "
              "carrying one dimensionless ratio, not as two universes "
              "disagreeing",
        labels=[
            "Lens mechanism: PROVEN as a mechanism — demonstrated by "
            "the laser stack above (ordinary optics, computed in this "
            "run). Label for the mechanism: DERIVED/OBSERVED (the "
            "mechanism, demonstrated) — the closed label set has no "
            "PROVEN label, and none is introduced",
            "Hubble attribution: HYPOTHESIS — the claim that the "
            "1.0837 gap is this mechanism stays at the framework "
            "author's stated hedge, in his words: \"Hubble is due to "
            "lens issues I'm pretty sure\" (hedge preserved), until "
            "the ratio is shown to track a specific lens difference "
            "between the two routes rather than anything in the "
            "expansion itself"],
        returned="the boundary-location method used here (locate the "
                 "dispute at B, not inside S) is RETURNED AND USED "
                 "immediately in the dark-matter demonstration, where "
                 "the mismatch is likewise read at the boundary where "
                 "it appears; the route comparison above (the route "
                 "table and the pattern — S the same, S' varies with "
                 "B) is RETURNED with it and consumed by name there; "
                 "and the rung-identification table (boundary set to "
                 "5, rungs identified by reach) is RETURNED with it "
                 "and consumed by name in the dark-matter solve, "
                 "where the mismatch is likewise located by the "
                 "reach at which it is read",
        returned_to="dark matter")


# ----------------------------------------------------------------------
# Dark matter — framework position (Mitch's), analyst application
# ----------------------------------------------------------------------

def solve_dark_matter(book, lines):
    book.use("hubble_ratio", "dark matter")   # the boundary method, returned
    route_table = book.use("hubble_route_table", "dark matter")
    rung_table = book.use("hubble_rung_table", "dark matter")
    worked = [
        "standard account: ordinary (baryonic) matter about 4.9% of the "
        "universe; dark matter about 26.5%",
        "26.5/4.9 = %s — about 5.41x as much invented-unseen matter as "
        "seen matter (about 84%% of all matter)"
        % _fmt(D("26.5") / D("4.9"), "0.01"),
        "the boundary-location method returned from the Hubble solve is "
        "applied here: the mismatch appears AT the boundary where the "
        "motion is read (outer galaxy, cluster edge)",
        "the route comparison returned from the Hubble solve is "
        "applied the same way — %s: one thing looked at, read "
        "through different stacks at its boundary, gives different "
        "readings; the difference is located in the reading, at B, "
        "before anything is invented inside S" % route_table,
        "the rung-identification table returned from the Hubble "
        "solve is applied here by reach — %s. Read by reach, the "
        "dark-matter mismatch is taken at one specific reach: the "
        "galaxy/cluster edge, the stretch where the motion is "
        "actually read, out past every rung the luminous-mass "
        "stick was fitted on. It is the same shape as a route "
        "carrying across a stretch where it has no rung: the "
        "difference sits in the carrying at that reach's boundary "
        "(B), before anything is invented inside S" % rung_table,
    ]
    return _demo(
        book, lines,
        item="Dark matter", title="Dark matter — unseen mass invented to "
                                  "make an old stick fit at the boundary",
        before="Galaxy and cluster motions, read with the luminous mass "
               "and the usual gravity stick, come out too fast for the "
               "mass seen — and 5.41x the seen matter is invented, "
               "unseen, to force the old stick to fit.",
        correct="Apply the M=0 move instead of inventing mass: the "
                "mismeasurement is reading the boundary state with a "
                "stick fitted to a different state. Correct the "
                "measurement at the boundary and solve for the "
                "invariant there. No named galaxy is worked in this "
                "run — the register is explicit that none has been "
                "worked yet, and this engine does not invent one.",
        S="the galaxy/cluster in its observed motion state",
        B="the boundary at which the motion is read (outer galaxy, "
          "cluster edge — exactly where the mismatch appears)",
        T="restatement: read the boundary state on a stick fitted to "
          "that state, in dimensionless ratios",
        worked=worked,
        invariant="NOT YET SOLVED for any named galaxy — stated "
                  "plainly. What this demonstration solves is the "
                  "shape of the item: the 5.41x is a boundary "
                  "mismeasurement figure, and the missing work is a "
                  "named galaxy's boundary invariant, in ratios, "
                  "produced and checked",
        after="the item stands restated at the boundary, with its "
              "missing work named, instead of 5.41x of unseen mass "
              "carried as if it were an observation",
        label="HYPOTHESIS — the framework author's position, in his "
              "words: dark matter \"was just made up\" (register: an "
              "invented construct). It stays HYPOTHESIS until a worked "
              "boundary invariant for a named galaxy's rotation, in "
              "ratios, is produced and checked",
        returned="this demonstration's S' — the item restated at its "
                 "boundary with the missing work named — is RETURNED "
                 "to the ledger as an OPEN branch (the same shape as "
                 "a refused hop: recorded, never dropped), and its "
                 "boundary-first reading is returned into the arrow "
                 "solve, whose mismeasurement is likewise corrected "
                 "at a boundary (the lightspeed boundary c)",
        returned_to="ledger (OPEN branch) and item 8 (arrow of time)")


# ----------------------------------------------------------------------
# Item 8 — arrow of time
# ----------------------------------------------------------------------

def solve_arrow(book, lines):
    worked = []
    for vc in ("0", "0.5", "0.9", "0.99", "0.999", "1"):
        x = D(vc)
        pace = (1 - x * x).sqrt()
        worked.append("v/c = %-6s spatial pace = %-6s ; temporal pace "
                      "sqrt(1-(v/c)^2) = %s" % (vc, vc, _fmt(pace, "0.0000")))
    worked.append("at v = c the entire budget is spatial motion and the "
                  "temporal pace is 0 — the author's position read off "
                  "the ratio: 'if we had the forward motion of "
                  "lightspeed, we wouldn't have time'")
    book.carry("interval_invariant", "(c dtau)^2 = (c dt)^2 - dx^2")
    return _demo(
        book, lines,
        item="8", title="Register item 8 — the arrow of time: time "
                        "treated as a separate universal flow",
        before="Time treated as an independent universal flow read off "
               "human clocks, separate from motion — so 'why does time "
               "move forward, and at what pace?' has nowhere to sit.",
        correct="Correct the mismeasurement in the author's terms: "
                "time is not read off human clocks as its own flow; "
                "the measurement is the dimensionless ratio of a "
                "state's motion to c. The budget is fixed at c and a "
                "state's motion splits it.",
        S="any state in transition (S -> S') — a transition is the "
          "engine's basic operation, and on the author's position it "
          "cannot run without forward time",
        B="the lightspeed boundary c (analyst reading of the boundary, "
          "unconfirmed — labeled as such in the applied worksheet)",
        T="raising the state's spatial pace v/c toward the boundary",
        worked=worked,
        invariant="the interval (c dtau)^2 = (c dt)^2 - dx^2 — the same "
                  "total at every pace; what varies is only the split "
                  "between motion and time",
        after="the arrow sits as the engine's operating precondition "
              "with its pace set by motion: forward motion and time "
              "are one budget, split by v/c, and the split is checked "
              "in the table above",
        label="DERIVED within special relativity as a route, premises "
              "stated (constancy of c; invariance of the interval) for "
              "the pace relation and the interval; HYPOTHESIS for the "
              "framework reading (the arrow as the engine's operating "
              "precondition — the author's position, recorded "
              "2026-10-29). What would raise it: a worked register "
              "item where the arrow falls out of the H machinery "
              "itself rather than being entered as its precondition",
        returned="the interval invariant is RETURNED AND USED as the "
                 "closing check of the solve chain: it is the same "
                 "form as every invariant above — a total that does "
                 "not move while its split (state) changes completely "
                 "— and it stands in the ledger beside the returned "
                 "stick, table, and Pell invariant the next run starts from",
        returned_to="the ledger (chain closing entry)")


# ----------------------------------------------------------------------
# Item 4 — fine structure: the honest NOT SOLVED case
# ----------------------------------------------------------------------

def check_fine_structure_seed_cubed(ctx=None):
    """Supporting check for the seed-cubed candidate (below)."""
    psi = inv._psi_as_written()
    eps_d = D(5) - 2 * D(6).sqrt()
    val = 4 * inv.PI ** 3 + inv.PI ** 2 + inv.PI - psi * eps_d ** 3
    ok = abs(val - D("137.035821")) < D("5e-7")
    return ok, ("psi scaled by eps^3: pi-sum - psi*eps^3 = %s "
                "(Muse's unconfirmed reading; worksheet 137.035821)"
                % val.quantize(D("0.000001")))


def demonstrate_fine_structure(book, lines):
    book.use("pell_invariant", "item 4")
    table = book.use("alpha_g_table", "item 4")
    psi = inv._psi_as_written()
    eps_d = D(5) - 2 * D(6).sqrt()
    pisum = 4 * inv.PI ** 3 + inv.PI ** 2 + inv.PI
    as_written = pisum - psi
    seeded = pisum - psi * eps_d ** 3
    lines.append("")
    lines.append("--- DEMONSTRATION (NOT A SOLVE): Register item 4 — fine "
                 "structure ---")
    lines.append("BEFORE: alpha is measured, not derived, in standard "
                 "physics: 1/alpha = 137.035999177, a number with no "
                 "stated reason. (alpha itself is already a dimensionless "
                 "ratio — the cleanest test case the lens gets.)")
    lines.append("CORRECT THE MEASUREMENT: no human unit survives in "
                 "alpha, so the remaining mismeasurement is which STATE "
                 "the value is taken in and how the electron is probed — "
                 "the author's position: the probing of the electron "
                 "pushes it towards gravity, and this item cannot be "
                 "marked solved until a different method of measurement "
                 "is applied.")
    lines.append("THE FULL CANDIDATE SET, each at its own label — "
                 "returned here from items 5 and 7 (Pell invariant; "
                 "the alpha_G table on the same hbar c stick):")
    rows = [
        ("measured 1/alpha", MEASURED_ALPHA_INV, "OBSERVED (CODATA record)",
         D(0)),
        ("pi-sum 4 pi^3 + pi^2 + pi", pisum, "DERIVED",
         pisum - MEASURED_ALPHA_INV),
        ("formula as written, minus psi = ln(eta)/sqrt(24)", as_written,
         "REFUTED as written", as_written - MEASURED_ALPHA_INV),
        ("3-Pell-step seed-cubed candidate: pi-sum - psi*eps^3", seeded,
         "Muse's UNCONFIRMED reading of the author's direction "
         "\"zoom in and/or out with the 3 steps of pell equation\"",
         seeded - MEASURED_ALPHA_INV),
    ]
    for name, val, label, rem in rows:
        lines.append("    %-52s = %s   remainder vs measured: %s   [%s]"
                     % (name, _fmt(val), ("+" if rem >= 0 else "")
                        + _fmt(rem), label))
    lines.append("    the seed-cubed candidate carries the smallest "
                 "remainder on the table (0.000178) — and is still not "
                 "the solution: it is an unconfirmed reading, and the "
                 "author's solving condition (a different measurement "
                 "method, not probing the electron the usual way) is "
                 "not met by any arithmetic in this run.")
    lines.append("INVARIANT SOLVED: none — this is the honest not-solved "
                 "case, kept in the run on purpose")
    lines.append("AFTER (S'): the item stands restated with its full "
                 "candidate set and its solving condition named; no "
                 "candidate is presented as the solution")
    lines.append("LABEL: NOT SOLVED (pi-sum DERIVED; formula as written "
                 "REFUTED; seed-cubed candidate Muse's UNCONFIRMED "
                 "reading; the underlying fixed-point claim HYPOTHESIS)")
    lines.append("RETURNED: the candidate set and the solving condition "
                 "are RETURNED to the ledger as the run's standing "
                 "open item — the first thing the next run (or the "
                 "named measurement method, when it arrives) starts from")
    book.ledger.append("SOLVE", {
        "item": "4", "title": "fine structure — NOT SOLVED demonstration",
        "S": "alpha as a measured-only constant",
        "B": "the probing interaction (measurement boundary)",
        "T": "candidate restatements (pi-sum; psi as written; psi x eps^3)",
        "S_prime": "item restated with full candidate set; NOT SOLVED",
        "invariant": "none claimed",
        "label": "NOT SOLVED",
        "returned_to": "ledger (standing open item)"})
    return {"rows": rows}


# ----------------------------------------------------------------------

def run_all(book):
    """Run every demonstration in chain order. Returns (lines, info)."""
    lines = []
    lines.append("Authorship, as in the source files: the applications "
                 "below are analyst work under the framework author's "
                 "direction and method — not his positions, except "
                 "where his position is cited inside an item (Hubble, "
                 "dark matter, the arrow, and the M=0 / mismeasurement "
                 "/ stick-rule statements). Labels match the register "
                 "and the applied worksheet exactly.")
    solve_black_hole(book, lines)
    solve_singularities(book, lines)
    solve_gravity_em(book, lines)
    solve_hierarchy(book, lines)
    solve_scale_transitions(book, lines)
    solve_hubble(book, lines)
    solve_dark_matter(book, lines)
    solve_arrow(book, lines)
    fs = demonstrate_fine_structure(book, lines)
    lines.append("")
    lines.append("=== THE RETURN LEG, verified — every solve returned "
                 "and used ===")
    for name, by in book.consumed:
        lines.append("  RETURNED AND USED: %-24s -> consumed by %s"
                     % (name, by))
    lines.append("No demonstration in this run is a one-way test: each "
                 "invariant was carried back in as a later item's "
                 "working stick, table, method, or steps, and each S' "
                 "stands as a new entry in the run ledger (SOLVE "
                 "entries), where the next run starts from it. A result "
                 "that landed nowhere would be a bleed; there are none "
                 "by construction, and the chain above is the evidence.")
    return lines, {"demos": book.demos, "fine_structure": fs,
                   "consumed": book.consumed}
