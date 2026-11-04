"""Hoppe Engine v3 — the sabotage suite.

The adversarial audit's attacks on v1, shipped as regression tests.
The engine must CATCH every one: catch it, log a Miss Report entry,
and refuse to finalize. An engine that survives its own sabotage
suite is what 'undeniable' means operationally, short of external
challenge (C4), which the publication bar still reserves.

Run standalone:  python3 tests/sabotage.py
Also run as part of the full engine run. All attacks run against
sandbox copies in a temporary directory; the real graph and ledgers
are never touched by an attack.
"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "core"))
sys.path.insert(0, str(ROOT / "tests"))

import graph as graph_mod          # noqa: E402
import invariants as inv           # noqa: E402
from governor import EvidenceRecord, Governor  # noqa: E402
from hops import HopEngine         # noqa: E402
from ledger import Ledger          # noqa: E402
from state import Boundary, State  # noqa: E402

GRAPH_PATH = ROOT / "data" / "graph.json"


def attack_wrong_pell_generator(sandbox):
    ok, detail = inv.check_pell_norm(generator=(3, 1))   # 3^2 - 6*1^2 = 3, not 1
    caught = not ok
    return caught, "wrong Pell generator (3,1): norm check returns %s (%s)" % (ok, detail)


def attack_h_for_hbar(sandbox):
    # The attack as the audit ran it: h slips into the derivation while
    # the products are still stated against hbar - mixed sticks. (Using
    # h consistently at both ends would be a relabelling, not an error;
    # the error is the mix, and the split-stick products expose it.)
    ratios = inv.planck_products_split(inv.H_PLANCK, inv.HBAR)
    worst = max(abs(r - 1) for r in ratios)
    caught = worst > inv.Decimal("1e-30")
    return caught, ("h in place of hbar (mixed sticks: units derived with h, "
                    "products stated against hbar): worst product deviation "
                    "%.3e, a factor of 2 pi - refused" % worst)


def attack_reduced_planck_undeclared(sandbox):
    reduced = inv.M_P_GEV / (8 * inv.PI).sqrt()
    ok, detail = inv.check_alpha_g_table(m_planck_gev=reduced)
    caught = not ok
    return caught, ("reduced Planck mass used without declaration: alpha_G table "
                    "returns %s (%s)" % (ok, detail))


def attack_corrupted_graph_status(sandbox):
    data = json.loads(GRAPH_PATH.read_text())
    data["entries"][0]["status"] = ["PROVEN"]
    bad = sandbox / "graph_corrupt.json"
    bad.write_text(json.dumps(data))
    try:
        graph_mod.load_graph(bad)
        return False, "corrupted graph status 'PROVEN' loaded without complaint"
    except graph_mod.GraphValidationError as e:
        return True, "corrupted graph status refused at load: %s" % e


def attack_empty_invariant_hop(sandbox):
    engine = HopEngine(Ledger(sandbox / "hop_log.json"))
    s = State("sabotage state", (0, 0, 0, 0))
    b = Boundary("permissive boundary", accepts={"any transition"})
    try:
        engine.hop(s, b, "any transition", "energy", "outbound", s, [],
                   path_position=0)
        return False, "hop with an empty invariant set was accepted"
    except ValueError as e:
        return True, "empty-invariant hop rejected: %s" % e


def attack_governor_bare_word(sandbox):
    gov = Governor(Ledger(sandbox / "continuity_log.json"))
    try:
        gov.decide("independent", "HYPOTHESIS", "SUPPORTED")
        return False, "Governor accepted a bare word as evidence"
    except TypeError as e:
        return True, "bare-word Governor decision refused: %s" % e


ATTACKS = [
    ("wrong Pell generator", attack_wrong_pell_generator),
    ("h in place of hbar", attack_h_for_hbar),
    ("reduced Planck mass, undeclared", attack_reduced_planck_undeclared),
    ("corrupted graph status", attack_corrupted_graph_status),
    ("empty-invariant hop", attack_empty_invariant_hop),
    ("Governor decision from a bare word", attack_governor_bare_word),
]


def run_all(miss_ledger=None):
    """Run every attack in a sandbox. Each catch is logged as a Miss
    Report entry on the supplied ledger (the run's real ledger) so the
    catch itself becomes part of the record. Returns a list of
    {attack, caught, detail}."""
    results = []
    with tempfile.TemporaryDirectory() as td:
        sandbox = Path(td)
        for name, fn in ATTACKS:
            caught, detail = fn(sandbox)
            results.append({"attack": name, "caught": caught, "detail": detail})
            if miss_ledger is not None:
                miss_ledger.append(
                    "MISS-REPORT" if caught else "MISS-REPORT-UNCAUGHT",
                    {"kind": "sabotage suite", "attack": name,
                     "caught": caught, "detail": detail})
    return results


if __name__ == "__main__":
    res = run_all()
    for r in res:
        print("%s %-38s %s" % ("CAUGHT" if r["caught"] else "NOT CAUGHT",
                               r["attack"], r["detail"]))
    n = sum(1 for r in res if r["caught"])
    print("sabotage suite: %d/%d attacks caught" % (n, len(res)))
    sys.exit(0 if n == len(res) else 1)
