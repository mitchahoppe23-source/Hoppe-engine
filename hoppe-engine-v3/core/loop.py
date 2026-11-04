"""Hoppe Engine v3 — the run.

What changed against v2 (the author's correction, 2026-11-02): the
core pieces are WORKING parts, not labels or data entries, and the
main event is not a test score.

- The run STARTS FROM A PROBLEM (core/problem.py): the problem is
  printed under PROBLEM: and carried through every section.
- The M=0 LENS runs as an operation on that problem
  (core/lens.py): start from the seed epsilon instead of true
  zero, restate as dimensionless ratios, same stick at both ends
  (mixed sticks flagged, with the h/hbar 2 pi case checked).
- The HE-15 LOOP is the cycle the run follows (the author's
  canonical loop): measure from the observer's center -> only
  probable truths or facts in -> compare variants to find the
  invariant -> plug it in and test in reality -> adjust or add
  surrounding variants -> measure again accepting only known or
  provable truth -> repeat. Steps 2 and 6 are gates.
- The MAIN EVENT is the worked inconsistency solves
  (core/solves.py): each register item demonstrated end-to-end —
  BEFORE -> CORRECT THE MEASUREMENT -> RUN H(S, B, T) = S' ->
  INVARIANT SOLVED -> AFTER, at its recorded label — and each
  solved invariant is RETURNED AND USED by a later item in the
  same run (the return leg; the chain is printed and verified).
- The H OPERATOR runs as an application (core/hops.py, carried
  from v2): S = State (matter/mass, energy, or transition), B =
  Boundary as smart filter/processor (selects, can change what it
  passes, can refuse; a refusal is recorded as a branch, never
  dropped), T = Transition. Return hops land on NEW ledger
  entries; history is never edited.
- The FLOWER OF LIFE is generated as geometry and read as a
  pattern (core/flower.py): centers one radius apart, one
  continuous stroke, lenses computed, counts derived from the
  construction; the reading places the problem's state at the
  center, rings outward, invariant = what holds across overlaps,
  a leg with no receiving circle = a bleed.
- The v2 executable checks and the sabotage suite run UNDERNEATH
  as supporting arithmetic verification — they support the solves;
  they are not the headline.
- The GOVERNOR (core/governor.py, carried from v2) holds the
  closed label set and refuses label upgrades and K changes on
  internal evidence alone. OPEN flags are preserved.
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import flower as flower_mod        # noqa: E402
import graph as graph_mod          # noqa: E402
import invariants as inv           # noqa: E402
import lens as lens_mod            # noqa: E402
import problem as problem_mod      # noqa: E402
import solves as solves_mod        # noqa: E402
from governor import EvidenceRecord, Governor, weakest_link  # noqa: E402
from hops import HopEngine         # noqa: E402
from ledger import Ledger          # noqa: E402
from state import (ENERGY_INLAYS, SIX_DEGREES, Boundary, State)  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
GRAPH_PATH = ROOT / "data" / "graph.json"
CONTINUITY_PATH = ROOT / "ledger" / "continuity_log.json"
HOP_PATH = ROOT / "ledger" / "hop_log.json"


class Engine:
    def __init__(self, problem_text, problem_source):
        self.problem_text = problem_text
        self.problem_source = problem_source
        self.graph = graph_mod.load_graph(GRAPH_PATH)
        self.ledger = Ledger(CONTINUITY_PATH)
        self.hop_ledger = Ledger(HOP_PATH)
        self.governor = Governor(self.ledger)
        self.hops = HopEngine(self.hop_ledger)
        self.checks = []
        self.decisions = []
        self.k_probe = None

    # -- supporting checks (underneath, not the headline) -------------
    def _run_checks(self):
        self.checks = inv.run_all()
        extra = []
        ok, detail = solves_mod.check_fine_structure_seed_cubed()
        extra.append({"name": "fine_structure_seed_cubed", "ok": ok,
                      "detail": detail, "required": True,
                      "designed_fail": False})
        for v in flower_mod.verify_construction():
            extra.append({"name": v["name"], "ok": v["ok"],
                          "detail": v["detail"], "required": True,
                          "designed_fail": False})
        same, _w, detail_same = lens_mod.check_same_stick("hbar", "hbar")
        extra.append({"name": "lens_same_stick_hbar", "ok": same,
                      "detail": detail_same, "required": True,
                      "designed_fail": False})
        same2, _w2, detail_mixed = lens_mod.check_same_stick("h", "hbar")
        extra.append({"name": "lens_mixed_stick_flagged", "ok": not same2,
                      "detail": detail_mixed, "required": True,
                      "designed_fail": False})
        self.checks = self.checks + extra
        for c in self.checks:
            self.ledger.append("CHECK", {"name": c["name"],
                                         "result": "PASS" if c["ok"] else "FAIL",
                                         "required": c["required"],
                                         "designed_fail": c["designed_fail"]})
            if not c["ok"] and c["required"]:
                self.ledger.append("MISS-REPORT",
                                   {"kind": "required check failed",
                                    "check": c["name"], "detail": c["detail"]})
            if not c["ok"] and c["designed_fail"]:
                self.ledger.append("MISS-REPORT",
                                   {"kind": "designed stress miss (expected)",
                                    "check": c["name"], "detail": c["detail"]})
        return self.checks

    # -- Governor pass (HE-15 step 6), carried from v2 ------------------
    def _governor_pass(self):
        g = self.governor
        dec = []
        dec.append(g.decide(
            EvidenceRecord(
                claim_id="EPS_ETA", route="exact arithmetic in Q(sqrt(6))",
                kind="proof", checker="engine invariants, exact lane", tier="C1",
                premises=["eps = 5 - 2 sqrt(6) and eta = 5 + 2 sqrt(6) as defined",
                          "Q(sqrt(6)) multiplication: (a+bs)(c+ds) = (ac+6bd) + (ad+bc)s"],
                inputs={"product": "eps*eta"}, tolerance="exact (no tolerance)"),
            "DERIVED", "DERIVED"))
        dec.append(g.decide(
            EvidenceRecord(
                claim_id="REG-6", route="dimensionless ratios on the Planck stick; "
                                         "R_s*T_H constancy computed at n = 1, 10, 10^38",
                kind="proof", checker="engine invariants, decimal lane (60 digits)",
                tier="C1",
                premises=["Schwarzschild radius and Hawking temperature formulas "
                          "used as routes, premises stated",
                          "the claim checked is the product's independence of n"],
                inputs={"check": "rs_th_invariant"}, tolerance="1e-30 relative, declared"),
            "DERIVED", "DERIVED"))
        dec.append(g.decide(
            EvidenceRecord(
                claim_id="REG-4 (pi-sum)", route="decimal evaluation of 4 pi^3 + pi^2 + pi",
                kind="proof", checker="engine invariants, decimal lane (60 digits)",
                tier="C1",
                premises=["the pi-sum is dimensionless arithmetic"],
                inputs={"check": "fine_structure_pisum"},
                tolerance="5e-7 absolute, declared"),
            "DERIVED", "DERIVED"))
        dec.append(g.decide(
            EvidenceRecord(
                claim_id="REG-4 (formula as written)",
                route="counterexample: psi = ln(eta)/sqrt(24) as written gives "
                      "136.568363, not the measured 137.035999177",
                kind="counterexample", checker="engine invariants, decimal lane",
                tier="C1",
                premises=["the formula and the psi definition exactly as written "
                          "in the register"],
                inputs={"check": "fine_structure_refuted"},
                tolerance="5e-7 absolute on the reproduced value, declared"),
            "HYPOTHESIS", "REFUTED"))
        dec.append(g.decide(
            EvidenceRecord(
                claim_id="REG-7 (why masses << m_P)", route="none offered",
                kind="none", checker="engine run", tier="C1",
                inputs={}, tolerance=""),
            "OPEN", "DERIVED"))
        probe = copy.deepcopy(graph_mod.find_entry(self.graph, "HE-04"))
        changed, msg = g.change_k(probe, 1, EvidenceRecord(
            claim_id="HE-04 K probe", route="internal consistency of this run",
            kind="consistency", checker="engine run", tier="C1",
            inputs={"proposed_K": 1}, tolerance="n/a"))
        self.k_probe = (changed, msg, probe["address"]["K"])
        self.decisions = dec
        return dec

    # -- H-operator hop chain (v2 grammar), secondary to the solves -----
    def _demo_hops(self):
        seed = State("seed state", (0, 0, 0, 0), kind="matter",
                     inlays={"energy": "nuclear/binding", "mass": "seed (the epsilon seat)"})
        stored = State("stored chemical energy state", (1, 0, 0, 0), kind="energy",
                       inlays={"energy": "chemical", "mass": "condensed, at rest"})
        active = State("active energy state", (2, 0, 0, 0), kind="energy",
                       inlays={"energy": "electrical", "mass": "condensed, at rest"})
        reformed = State("stored chemical energy state (re-formed on return)",
                         (1, 0, 0, 0), kind="energy",
                         inlays={"energy": "chemical", "mass": "condensed, at rest"})
        vented = State("vented state (attempted)", (3, 0, 0, 0), kind="energy",
                       inlays={"energy": "thermal", "mass": "dispersed"})
        b_form = Boundary("formation boundary (smart filter)",
                          accepts={"storage into bonds"})
        b_conv = Boundary("conversion interface (smart filter)",
                          accepts={"energy conversion", "feedback return: re-storage"})
        b_vent = Boundary("open vent (no receiving partner)",
                          accepts={"venting"}, has_receiving_state=False)
        entries = []
        entries.append(self.hops.hop(
            seed, b_form, "storage into bonds", "matter", "outbound", stored,
            ["eps_eta_product", "pell_norm"], path_position=42))
        entries.append(self.hops.hop(
            stored, b_conv, "energy conversion", "energy", "outbound", active,
            ["eps_eta_product", "ladder_sums"], path_position=114))
        entries.append(self.hops.return_hop(
            active, b_conv, "feedback return: re-storage", "energy",
            reformed, resembles_state=stored, reversibility="partial",
            loss="part of the throughput recorded as heat on the return leg "
                 "(demo figure: 0.08 of the leg)",
            invariant_names=["eps_eta_product"], path_position=222))
        entries.append(self.hops.hop(
            active, b_vent, "venting", "energy", "outbound", vented,
            ["eps_eta_product"], path_position=360))
        return entries

    # -- the run ---------------------------------------------------------
    def run(self):
        g = self.graph
        L = []
        L.append("Hoppe Engine v3 — starts from a problem, not from itself.")
        L.append(problem_mod.STARTUP_LINE)
        L.append("PROBLEM: %s" % self.problem_text)
        L.append("(problem source: %s)" % self.problem_source)
        L.append("")
        L.append("=== HE-15 step 1 — measure from the observer's center; "
                 "correct the measurement first (the M=0 lens) ===")
        L.append("Graph loaded and validated (closed label set; address "
                 "fields on every entry): %d core objects, %d continuity "
                 "entries, %d register items, %d open bridges, %d caveats."
                 % (len(g["core_objects"]), len(g["entries"]),
                    len(g["register_items"]), len(g["open_bridges"]),
                    len(g["caveats"])))
        L.append("The author's position, in his words: \"M=0 is a lens "
                 "used to unify quantum physics and gr. It shows that "
                 "starting from .1010205 instead of true zero and taking "
                 "the correct measurements resolves all the "
                 "inconsistencies.\"")
        quantities = problem_mod.parse_quantities(self.problem_text)
        if problem_mod.detect_mixed_sticks(self.problem_text):
            L.append("Mixed-stick tell found in the problem as stated "
                     "(h and hbar both named): flagged before solving.")
        lens_lines, _verdict = lens_mod.correct_measurement(
            self.problem_text, quantities)
        for ln in lens_lines:
            L.append(ln)
        L.append("")
        L.append("=== HE-15 step 2 — admit only probable truths or facts, "
                 "with provenance (gate) ===")
        L.append("Admitted for this run: the register and applied "
                 "worksheet standings (m0-inconsistencies-register.md; "
                 "m0-h-operator-applied-to-the-rest.md), exact arithmetic "
                 "in Q(sqrt(6)), and 60-digit decimal evaluation of the "
                 "worksheets' checked numbers. No caller-supplied verdict "
                 "words are accepted anywhere in this engine.")
        L.append("")
        L.append("=== THE WORKED SOLVES — the main event (HE-15 steps 3–5 "
                 "run per item: compare variants, find the invariant, "
                 "plug it in, adjust nothing silently) ===")
        book = solves_mod.SolveBook(self.ledger)
        solve_lines, solve_info = solves_mod.run_all(book)
        L.extend(solve_lines)
        L.append("")
        L.append("=== FLOWER OF LIFE — generated, then read on this "
                 "problem ===")
        for v in flower_mod.verify_construction():
            L.append("  construction: %s" % v["detail"])
        L.append("  traced path data (carried from v2, checked in the "
                 "supporting checks): cumulative arcs 36 / 108 / 216 / "
                 "360 for generations 1–4; generation-4 ring closures "
                 "at path positions 42 / 114 / 222 / 360")
        placed = {
            "the problem (at the observer's center)": (0, 0, 0),
            "stored chemical energy state": (1, -1, 0),
            "active energy state": (1, 0, -1),
            "re-formed stored state (return)": (0, 1, -1),
        }
        legs = [
            {"from": "the problem (at the observer's center)",
             "to": "stored chemical energy state",
             "properties": ["receiving partner at the boundary",
                            "invariant eps*eta = 1"]},
            {"from": "stored chemical energy state",
             "to": "active energy state",
             "properties": ["receiving partner at the boundary",
                            "invariant eps*eta = 1"]},
            {"from": "active energy state",
             "to": "re-formed stored state (return)",
             "properties": ["receiving partner at the boundary",
                            "invariant eps*eta = 1"]},
            {"from": "active energy state",
             "to": "an open vent (nothing placed there)",
             "properties": ["receiving partner at the boundary"]},
        ]
        read_lines, _reading = flower_mod.read_on_flower(placed, legs)
        for ln in read_lines:
            L.append("  reading: %s" % ln)
        L.append("  reading: the vent leg is the same refusal the hop "
                 "ledger records below (HOP-004) — on the flower it is "
                 "a bleed, in the ledger a preserved branch; in neither "
                 "place is it silently dropped")
        L.append("")
        L.append("=== H OPERATOR — the hop chain (each hop a ledger "
                 "entry; returns land on NEW entries) ===")
        for e in self._demo_hops():
            if e["kind"] == "refused-branch":
                L.append("  %s REFUSED-BRANCH: %s --%s/%s--> (no state "
                         "entered) at path position %s; attempt %s for "
                         "this boundary; branch %s; reason: %s"
                         % (e["hop_id"], e["from"]["label"], e["strip"],
                            e["direction"], e["path_position"],
                            e["attempt_status"], e["branch_status"],
                            e["refusal_reason"]))
            else:
                extra = ""
                if e["direction"] == "return":
                    extra = (" | return of '%s': resembles=%s, "
                             "reversibility=%s, loss: %s"
                             % (e.get("return_of"), e.get("resembles"),
                                e.get("reversibility"), e.get("loss")))
                L.append("  %s %s: %s --[%s | %s/%s]--> %s at path "
                         "position %s; invariants preserved: %s%s"
                         % (e["hop_id"], e["mark"].upper(),
                            e["from"]["label"], e["boundary"], e["strip"],
                            e["direction"], e["to"]["label"],
                            e["path_position"],
                            e["invariants_preserved"], extra))
        L.append("")
        L.append("=== SUPPORTING ARITHMETIC — the v2 checks and the v3 "
                 "working-part verifications, underneath the solves "
                 "(not the headline) ===")
        checks = self._run_checks()
        for c in checks:
            tag = "PASS" if c["ok"] else ("FAIL (designed stress)"
                                          if c["designed_fail"] else "FAIL")
            L.append("  %-4s %-28s %s" % (tag, c["name"], c["detail"]))
        req_fail = [c["name"] for c in checks
                    if not c["ok"] and c["required"]]
        des_fail = [c["name"] for c in checks
                    if not c["ok"] and c["designed_fail"]]
        L.append("HE-15 step 5 — adjust or add variants: required-check "
                 "misses: %s ; designed stress misses (logged as Miss "
                 "Reports, data untouched): %s. A miss is answered by a "
                 "new variant or a supersession entry, never by editing "
                 "what stands."
                 % (req_fail or "none", des_fail or "none"))
        L.append("Energy variants compared (returned fraction F):")
        for name, v in inv.ENERGY_VARIANTS.items():
            L.append("  %-38s kind=%-6s F=%s"
                     % (name, v["kind"],
                        v["F"].quantize(inv.Decimal("0.001"))))
        L.append("")
        L.append("=== HE-15 step 6 — measure again, accepting only "
                 "known or provable truth (Governor gate) ===")
        for d in self._governor_pass():
            L.append("  Governor: %-28s current=%s proposed=%s -> %s%s (%s)"
                     % (d["claim_id"], d["current"], d["proposed"],
                        d["outcome"],
                        (" granted=%s" % d["granted"]) if d["granted"] else "",
                        d["reason"]))
        changed, msg, kval = self.k_probe
        L.append("  K probe: attempted K change on HE-04 with internal "
                 "evidence only -> changed=%s; %s; K still %s"
                 % (changed, msg, kval))
        L.append("  Fine structure as a composite stands at its weakest "
                 "link: weakest of [DERIVED (pi-sum), REFUTED (formula "
                 "as written), OPEN (solving condition)] = %s — NOT "
                 "SOLVED, and no part of this run raises it."
                 % weakest_link(["DERIVED", "REFUTED", "OPEN"]))
        L.append("  Internal consistency upgrades nothing (Governor law).")
        L.append("")
        L.append("=== Reading grammar and OPEN flags (preserved, not "
                 "settled by this run) ===")
        L.append("Address: S = (X, Y, Z, K), X/Y/Z spatial, K scale/tier. "
                 "Operator: H(S, B, T) = S' (an application, never an "
                 "addition).")
        L.append("Six degrees of movement (3 strips x 2 directions): %s"
                 % ", ".join("%s/%s" % sd for sd in SIX_DEGREES))
        L.append("Energy inlays (readings, not axes): %s"
                 % ", ".join(ENERGY_INLAYS))
        for name, flag in g["open_flags"].items():
            L.append("  OPEN flag %-28s status=%s — %s"
                     % (name, flag["status"],
                        flag.get("note", flag.get("map_question", ""))[:150]))
        L.append("")
        L.append("=== HE-15 step 7 — repeat ===")
        L.append("Cycle complete. The loop repeats when new evidence "
                 "arrives; the states, stick, table, and invariants "
                 "returned above are where the next cycle starts.")
        info = {"checks": checks, "decisions": self.decisions,
                "solves": solve_info}
        return "\n".join(L), info
