"""Hoppe Engine v3 — executable invariant checks.

Pure Python 3 standard library only. Two arithmetic lanes:

- Exact lane: surd quantities carried as (a, b) pairs in Q(sqrt(6)),
  meaning a + b*sqrt(6) with exact fractions. In this lane eps*eta = 1
  is exact, not approximate.
- Decimal lane: decimal at 60 digits of working precision for the
  worksheet numbers that are not surds (Planck products, black-hole
  ratios, the fine-structure pi-sum and its refuted psi term).

Every check returns (ok, detail). Checks accept an optional context
(the S, B, T of a transition) so a hop can verify its invariants across
the actual transition, not in the abstract; the global checks below do
not depend on the context, and say so by ignoring it.

The operator H(S, B, T) = S' is an application. It is never written as
an addition anywhere in this engine.
"""
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

# ----------------------------------------------------------------------
# Exact lane: Q(sqrt(6)) pairs
# ----------------------------------------------------------------------


class Q6:
    """An element a + b*sqrt(6) of Q(sqrt(6)), a and b exact Fractions."""

    __slots__ = ("a", "b")

    def __init__(self, a, b=0):
        self.a = Fraction(a)
        self.b = Fraction(b)

    def __add__(self, other):
        return Q6(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        return Q6(self.a - other.a, self.b - other.b)

    def __mul__(self, other):
        # (a + b s)(c + d s) = (ac + 6bd) + (ad + bc) s,  s = sqrt(6)
        return Q6(self.a * other.a + 6 * self.b * other.b,
                  self.a * other.b + self.b * other.a)

    def __pow__(self, n):
        if n < 0:
            raise ValueError("Q6 powers here are non-negative")
        out = Q6(1, 0)
        for _ in range(n):
            out = out * self
        return out

    def __eq__(self, other):
        return isinstance(other, Q6) and self.a == other.a and self.b == other.b

    def __repr__(self):
        return "Q6(%s, %s)" % (self.a, self.b)

    def describe(self):
        if self.b == 0:
            return str(self.a)
        term = "sqrt(6)" if abs(self.b) == 1 else "%s*sqrt(6)" % abs(self.b)
        if self.a == 0:
            return ("-" if self.b < 0 else "") + term
        sign = "+" if self.b > 0 else "-"
        return "%s %s %s" % (self.a, sign, term)


# The seed pair, exact. eps = 5 - sqrt(24) = 5 - 2 sqrt(6); eta = 5 + 2 sqrt(6).
EPS = Q6(5, -2)
ETA = Q6(5, 2)
SQRT24 = Q6(0, 2)          # sqrt(24) = 2 sqrt(6)
CENTER = Q6(5, 0)
FOLD = SQRT24              # the fold amount under the root


def pell_step(n, generator=(5, 2)):
    """nth solution (x, y) of x^2 - 6 y^2 = 1, by multiplying (1, 0) by
    the generator (gx + gy sqrt(6)) n times. The default generator is
    (5, 2): multiplication by eta in the (x, y) basis. The generator is
    a parameter so the sabotage suite can feed a wrong one and watch
    the norm check refuse it."""
    gx, gy = generator
    x, y = 1, 0
    for _ in range(n):
        x, y = gx * x + 6 * gy * y, gy * x + gx * y
    return x, y


# ----------------------------------------------------------------------
# Decimal lane: constants (CODATA values as used in the worksheets)
# ----------------------------------------------------------------------

PI = Decimal("3.141592653589793238462643383279502884197169399375105820974944"
             "592307816406286208998628034825342117067982148086513282306647")
HBAR = Decimal("1.054571817e-34")     # reduced Planck constant, J s
H_PLANCK = 2 * PI * HBAR              # Planck constant h = 2 pi hbar
C_LIGHT = Decimal("299792458")        # m / s (exact by definition)
G_NEWTON = Decimal("6.67430e-11")     # m^3 kg^-1 s^-2
KB = Decimal("1.380649e-23")          # J / K (exact by definition)
M_P_KG = (HBAR * C_LIGHT / G_NEWTON).sqrt()
L_P = (HBAR * G_NEWTON / C_LIGHT ** 3).sqrt()
T_P = L_P / C_LIGHT
E_P = M_P_KG * C_LIGHT ** 2
M_P_GEV = Decimal("1.2209e19")        # Planck mass, GeV/c^2 (worksheet convention, declared)

PARTICLES_GEV = {
    "electron": Decimal("0.000511"),
    "proton": Decimal("0.93827"),
    "W boson": Decimal("80.377"),
    "Z boson": Decimal("91.1876"),
    "Higgs boson": Decimal("125.25"),
    "top quark": Decimal("172.76"),
}

# Fine-structure worksheet targets (standings carried as data).
ALPHA_INV_MEASURED = Decimal("137.035999177")   # CODATA value on record
ALPHA_PISUM_TARGET = Decimal("137.036304")      # 4 pi^3 + pi^2 + pi, DERIVED
ALPHA_FORMULA_REFUTED = Decimal("136.568363")   # formula as written, REFUTED


def alpha_g(mass_gev, m_planck_gev=None):
    """Gravitational coupling on the shared hbar*c stick: (m / m_P)^2.
    The Planck-mass convention is an explicit argument: substituting
    the reduced Planck mass is legal only when declared, because every
    value then scales by exactly 8 pi (see check_hierarchy_8pi_rule)."""
    mp = M_P_GEV if m_planck_gev is None else m_planck_gev
    return (mass_gev / mp) ** 2


# ----------------------------------------------------------------------
# Checks: seed geometry (exact lane)
# ----------------------------------------------------------------------


def check_seed_fold_24_25(ctx=None):
    ok = (1 ** 2 + 24 == 25) and (CENTER - FOLD == EPS) and (CENTER + FOLD == ETA)
    return ok, "1^2 + 24 = 25 exactly; 5 - sqrt(24) = eps and 5 + sqrt(24) = eta in Q(sqrt(6))"


def check_eps_eta_product(ctx=None):
    p = EPS * ETA
    return p == Q6(1, 0), "eps*eta = %s (exact)" % p.describe()


def check_eps_eta_sum(ctx=None):
    s = EPS + ETA
    return s == Q6(10, 0), "eps + eta = %s (exact)" % s.describe()


def check_eta_minus_eps(ctx=None):
    d = ETA - EPS
    return d == Q6(0, 4), "eta - eps = %s = 4 sqrt(6) (exact)" % d.describe()


def check_square_area_96(ctx=None):
    side = ETA - EPS                      # 4 sqrt(6)
    area = side * side
    return area == Q6(96, 0), "flat square: (eta - eps)^2 = (4 sqrt(6))^2 = %s (exact)" % area.describe()


def check_cube_volume(ctx=None):
    side = ETA - EPS
    vol = side * side * side
    return vol == Q6(0, 384), "cube: (4 sqrt(6))^3 = %s = 384 sqrt(6) (exact)" % vol.describe()


def check_cube_faces_576(ctx=None):
    area = (ETA - EPS) * (ETA - EPS)
    total = Q6(0, 0)
    for _ in range(6):
        total = total + area
    ok = total == Q6(576, 0)
    return ok, ("cube surface: 6 faces x 96 = %s (exact). Arithmetic only: the "
                "identity of this six with the six degrees of movement is OPEN "
                "and is not asserted here." % total.describe())


def check_pell_norm(ctx=None, generator=(5, 2)):
    vals, ok = [], True
    for n in range(5):
        x, y = pell_step(n, generator)
        v = x * x - 6 * y * y
        vals.append("n=%d (%d,%d) -> %d" % (n, x, y, v))
        ok = ok and v == 1
    return ok, "x^2 - 6 y^2 at steps 0..4: " + " ; ".join(vals)


def check_ladder_sums(ctx=None):
    targets = [2, 10, 98, 970, 9602, 95050]
    got, ok = [], True
    for n in range(6):
        s = (EPS ** n) + (ETA ** n)
        got.append(s)
        ok = ok and s == Q6(targets[n], 0)
        # cross-check against the Pell step: eps^n = x - y sqrt(6)
        x, y = pell_step(n)
        ok = ok and (EPS ** n) == Q6(x, -y)
    detail = "eps^n + eta^n for n=0..5: %s (exact integers; each eps^n also " \
             "matches Pell step n as x - y sqrt(6))" % [g.describe() for g in got]
    return ok, detail


def check_sqrt_pair_bridge(ctx=None):
    two, three = Decimal(2), Decimal(3)
    eps_d = Decimal(5) - 2 * Decimal(6).sqrt()
    lhs = (three.sqrt() - two.sqrt()) ** 2
    diff = abs(lhs - eps_d)
    ok = diff < Decimal("1e-45")
    return ok, ("eps = (sqrt(3) - sqrt(2))^2 at 60-digit precision: "
                "|difference| = %.3e (tolerance 1e-45 declared)" % diff)


# ----------------------------------------------------------------------
# Checks: worksheet numbers (decimal lane)
# ----------------------------------------------------------------------


def planck_products_split(derive_hbar, stick_hbar):
    """The four Planck invariant products, with two sticks made
    explicit: the constant the Planck units are DERIVED with, and the
    constant the products are STATED against. The framework's rule is
    one stick at both ends: with derive == stick every product is 1.
    Mixing sticks (deriving with h, stating against hbar) moves the
    products by 2 pi - exactly the mismeasurement the h-for-hbar
    sabotage attack commits, and exactly what this split exposes."""
    e_p = (derive_hbar * C_LIGHT / G_NEWTON).sqrt() * C_LIGHT ** 2
    l_p = (derive_hbar * G_NEWTON / C_LIGHT ** 3).sqrt()
    t_p = l_p / C_LIGHT
    m_p = (derive_hbar * C_LIGHT / G_NEWTON).sqrt()
    return [e_p * l_p / (stick_hbar * C_LIGHT),
            e_p * t_p / stick_hbar,
            (l_p / t_p) / C_LIGHT,
            m_p * l_p / (stick_hbar / C_LIGHT)]


def planck_products(hbar=HBAR):
    """The four Planck invariant products on one stick (derive == state)."""
    return planck_products_split(hbar, hbar)


def check_planck_products(ctx=None, hbar=HBAR):
    tol = Decimal("1e-30")
    ratios = planck_products(hbar)
    ok = all(abs(r - 1) < tol for r in ratios)
    return ok, ("E_P*l_P/(hbar c), E_P*t_P/hbar, (l_P/t_P)/c, m_P*l_P/(hbar/c) "
                "deviate from 1 by at most %.3e (tolerance 1e-30 declared)"
                % max(abs(r - 1) for r in ratios))


def check_rs_th_invariant(ctx=None):
    tol = Decimal("1e-30")
    target = HBAR * C_LIGHT / (4 * PI * KB)
    worst = Decimal(0)
    for n in (Decimal(1), Decimal(10), Decimal("1e38")):
        m = n * M_P_KG
        r_s = 2 * G_NEWTON * m / C_LIGHT ** 2
        t_h = HBAR * C_LIGHT ** 3 / (8 * PI * G_NEWTON * m * KB)
        worst = max(worst, abs(r_s * t_h / target - 1))
    ok = worst < tol
    return ok, ("R_s*T_H at n = 1, 10, 10^38: worst relative deviation from "
                "hbar c/(4 pi k_B) is %.3e (tolerance 1e-30 declared); the "
                "product does not move with mass" % worst)


def check_alpha_g_table(ctx=None, m_planck_gev=None):
    expect = {"electron": Decimal("1.752e-45"),
              "proton": Decimal("5.906e-39"),
              "top quark": Decimal("2.00e-34")}
    outs, ok = [], True
    for name, want in expect.items():
        got = alpha_g(PARTICLES_GEV[name], m_planck_gev)
        outs.append("%s %.3e (worksheet %.3e)" % (name, got, want))
        ok = ok and abs(got / want - 1) < Decimal("0.01")
    conv = "unreduced (declared)" if m_planck_gev is None else "supplied"
    return ok, "alpha_G table, Planck-mass convention %s: %s" % (conv, " ; ".join(outs))


def check_hierarchy_8pi_rule(ctx=None):
    """Declared use of the reduced Planck mass scales every alpha_G by
    exactly 8 pi. This is the rule that makes an *undeclared*
    substitution detectable: it moves every value by that factor."""
    reduced = M_P_GEV / (8 * PI).sqrt()
    worst = Decimal(0)
    for name in ("electron", "proton", "top quark"):
        ratio = alpha_g(PARTICLES_GEV[name], reduced) / alpha_g(PARTICLES_GEV[name])
        worst = max(worst, abs(ratio / (8 * PI) - 1))
    ok = worst < Decimal("1e-40")
    return ok, ("alpha_G(reduced m_P) / alpha_G(unreduced m_P) = 8 pi for every "
                "particle; worst relative deviation %.3e (tolerance 1e-40 declared)" % worst)


def _psi_as_written():
    eta_d = Decimal(5) + 2 * Decimal(6).sqrt()
    return eta_d.ln() / Decimal(24).sqrt()


def check_fine_structure_pisum(ctx=None):
    val = 4 * PI ** 3 + PI ** 2 + PI
    ok = abs(val - ALPHA_PISUM_TARGET) < Decimal("5e-7")
    return ok, "4 pi^3 + pi^2 + pi = %s (DERIVED; worksheet 137.036304)" % val.quantize(Decimal("0.000001"))


def check_fine_structure_formula_refuted(ctx=None):
    """The formula alpha^-1 = 4 pi^3 + pi^2 + pi - psi(phi) with
    psi = ln(eta)/sqrt(24), AS WRITTEN, gives 136.568363, not the
    measured 137.035999177. This check reproduces the refutation
    exactly; it passes when the refutation reproduces. The item's
    standing stays NOT SOLVED (see the graph data)."""
    val = 4 * PI ** 3 + PI ** 2 + PI - _psi_as_written()
    reproduced = abs(val - ALPHA_FORMULA_REFUTED) < Decimal("5e-7")
    misses_measured = abs(val - ALPHA_INV_MEASURED) > Decimal("0.1")
    ok = reproduced and misses_measured
    return ok, ("psi as written = ln(eta)/sqrt(24) = %s; formula gives %s vs "
                "measured %s: refutation reproduced exactly"
                % (_psi_as_written().quantize(Decimal("0.000000001")),
                   val.quantize(Decimal("0.000001")), ALPHA_INV_MEASURED))


# ----------------------------------------------------------------------
# Checks: the flower (traced path data)
# ----------------------------------------------------------------------

FLOWER_CIRCLES = {0: 1, 1: 7, 2: 19, 3: 37, 4: 61}        # 3g(g+1)+1
FLOWER_ARCS = {1: 36, 2: 108, 3: 216, 4: 360}              # cumulative on the gen-g stroke
GEN4_CLOSURES = [42, 114, 222, 360]                        # ring completions on the gen-4 stroke


def flower_count(g):
    return 3 * g * (g + 1) + 1


def check_flower_generations(ctx=None):
    got = {g: flower_count(g) for g in range(5)}
    ok = got == FLOWER_CIRCLES
    return ok, "flower circles by generation 0..4: %s" % [got[g] for g in range(5)]


def check_flower_arcs(ctx=None):
    ok = all(FLOWER_ARCS[g] == 18 * g * (g + 1) for g in FLOWER_ARCS)
    rings = [36 * k for k in (1, 2, 3, 4)]
    ok = ok and [FLOWER_ARCS[g] - (FLOWER_ARCS[g - 1] if g > 1 else 0) for g in (1, 2, 3, 4)] == rings
    return ok, ("cumulative arcs on the generation stroke: %s; ring k adds 36k arcs: %s"
                % ([FLOWER_ARCS[g] for g in (1, 2, 3, 4)], rings))


def check_flower_gen4_closures(ctx=None):
    inc = [GEN4_CLOSURES[0]] + [GEN4_CLOSURES[i] - GEN4_CLOSURES[i - 1] for i in range(1, 4)]
    ok = (GEN4_CLOSURES == sorted(GEN4_CLOSURES) and GEN4_CLOSURES[-1] == FLOWER_ARCS[4]
          and sum(inc) == 360 and len(set(GEN4_CLOSURES)) == 4)
    return ok, ("ring completions on the generation-4 stroke at path positions "
                "%s; increments %s sum to 360" % (GEN4_CLOSURES, inc))


# ----------------------------------------------------------------------
# Checks: HE-16 energy module, carried forward from v1 as data-driven
# checks (figures are the worksheet's sourced values)
# ----------------------------------------------------------------------

ENERGY_VARIANTS = {
    "water cycle (long-term balance)":    {"F": Decimal("0.999"), "kind": "nature"},
    "atmospheric back-radiation":         {"F": Decimal("0.85"), "kind": "nature"},
    "tuna countercurrent rete":           {"F": Decimal("0.99"), "kind": "nature"},
    "human primary energy system (2023)": {"F": Decimal(209) / Decimal(589), "kind": "human"},
}
ENERGY_INSTALLATIONS = {
    "rejection-only data centre (baseline)": {"partner_at_boundary": False, "F": Decimal("0.0")},
    "EcoDataCenter, company-wide ERF 2024":  {"partner_at_boundary": False, "F": Decimal("0.06")},
    "Fortum x Microsoft Espoo (design)":     {"partner_at_boundary": True, "F": Decimal("0.75")},
    "Chinese DC + storage system (measured)": {"partner_at_boundary": True, "F": Decimal("0.6961")},
}


def check_energy_variant_separation(ctx=None):
    outs, ok = [], True
    for name, v in ENERGY_VARIANTS.items():
        r = v["F"] / (1 - v["F"])
        outs.append("%s F=%s ratio=%s" % (name, v["F"].quantize(Decimal("0.001")),
                                          r.quantize(Decimal("0.01"))))
        ok = ok and ((r > 1) == (v["kind"] == "nature"))
    return ok, " ; ".join(outs)


def check_energy_partner_rule(ctx=None):
    outs, ok = [], True
    for name, v in ENERGY_INSTALLATIONS.items():
        pred = v["F"] > Decimal("0.5")
        outs.append("%s partner=%s F=%s" % (name, v["partner_at_boundary"], v["F"]))
        ok = ok and (pred == v["partner_at_boundary"])
    return ok, " ; ".join(outs)


def check_energy_circulation_balance(ctx=None):
    bal = Decimal(20) == Decimal(17) + Decimal(3)
    return bal, "circulatory exchange: filtered 20 L/day = reabsorbed 17 + lymph return 3"


def check_energy_carrier_cycle(ctx=None):
    cycles = Decimal(60) / Decimal("0.10")
    return cycles > 100, "ATP pool 0.10 kg, turnover ~60 kg/day -> ~%s cycles/day" % format(cycles, "f")


def check_energy_stress_radiation(ctx=None):
    """DESIGNED STRESS TEST — expected to FAIL the candidate invariant as
    worded in v1 ('no leg terminates in the void'). Earth's long-term
    energy balance returns ~100% of absorbed solar flux to space: the
    planetary energy leg terminates in the void by design, and closure
    belongs to the carrier/medium, not to energy itself. If this check
    ever returns ok=True, the stress data or the check is wrong."""
    earth_energy_closure = Decimal(0)
    holds = earth_energy_closure > Decimal("0.5")
    return holds, ("Earth retains ~0 of through-flowing solar energy long-term; "
                   "energy closure = 0.00 while the system works. Candidate "
                   "invariant as worded in v1 FAILS for energy itself (designed miss).")


# ----------------------------------------------------------------------
# Registry. Each entry: (function, required, designed_fail)
# A required check that fails is a miss. The designed stress check is
# expected to fail; the run headline is computed from these flags and
# can never print PASS over a failed required check.
# ----------------------------------------------------------------------

CHECKS = {
    "seed_fold_24_25":            (check_seed_fold_24_25, True, False),
    "eps_eta_product":            (check_eps_eta_product, True, False),
    "eps_eta_sum":                (check_eps_eta_sum, True, False),
    "eta_minus_eps":              (check_eta_minus_eps, True, False),
    "square_area_96":             (check_square_area_96, True, False),
    "cube_volume_384sqrt6":       (check_cube_volume, True, False),
    "cube_faces_576":             (check_cube_faces_576, True, False),
    "pell_norm":                  (check_pell_norm, True, False),
    "ladder_sums":                (check_ladder_sums, True, False),
    "sqrt_pair_bridge":           (check_sqrt_pair_bridge, True, False),
    "planck_products":            (check_planck_products, True, False),
    "rs_th_invariant":            (check_rs_th_invariant, True, False),
    "alpha_g_table":              (check_alpha_g_table, True, False),
    "hierarchy_8pi_rule":         (check_hierarchy_8pi_rule, True, False),
    "fine_structure_pisum":       (check_fine_structure_pisum, True, False),
    "fine_structure_refuted":     (check_fine_structure_formula_refuted, True, False),
    "flower_generations":         (check_flower_generations, True, False),
    "flower_arcs":                (check_flower_arcs, True, False),
    "flower_gen4_closures":       (check_flower_gen4_closures, True, False),
    "energy_variant_separation":  (check_energy_variant_separation, True, False),
    "energy_partner_rule":        (check_energy_partner_rule, True, False),
    "energy_circulation_balance": (check_energy_circulation_balance, True, False),
    "energy_carrier_cycle":       (check_energy_carrier_cycle, True, False),
    "energy_stress_radiation":    (check_energy_stress_radiation, False, True),
}


def run_all(ctx=None):
    out = []
    for name, (fn, required, designed_fail) in CHECKS.items():
        ok, detail = fn(ctx)
        out.append({"name": name, "ok": ok, "detail": detail,
                    "required": required, "designed_fail": designed_fail})
    return out
