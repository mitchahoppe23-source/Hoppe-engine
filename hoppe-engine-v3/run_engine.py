"""Hoppe Engine v3 — one-command entry.

Run:
    python3 run_engine.py                      # the default problem:
                                               # the inconsistencies
                                               # register, worked as
                                               # solves (the main event)
    python3 run_engine.py "your problem here"  # a problem of your own
    python3 run_engine.py --problem-file f.txt
    cat problem.txt | python3 run_engine.py --stdin   # problem on stdin

The engine starts from the problem: it prints the friendly startup
and the PROBLEM: line, runs the M=0 lens on it, works the solves
with their return leg, reads the result on the generated flower,
and only underneath runs the supporting arithmetic checks and the
sabotage suite.

The headline is COMPUTED and leads with the solves, not a test
score. The transcript is written to docs/run-v3.txt when the
default problem runs (a custom problem prints to stdout only, so
the canonical transcript is never overwritten by an experiment).
Output is deterministic: same input, same output, byte for byte.
Decisions, solves, and hops are appended to the ledgers under
ledger/ (append-only; sequence numbers are logical, never wall
clock; the printed transcript does not depend on ledger length).
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "core"))
sys.path.insert(0, str(ROOT / "tests"))

import problem as problem_mod      # noqa: E402
import sabotage                    # noqa: E402
from loop import Engine            # noqa: E402

LIMITATION = ("Standing limitation: this engine checks the framework "
              "against itself and against the checked numbers in its "
              "data. A passing check shows exact arithmetic and "
              "internal consistency only. It does not prove the "
              "framework's physical claims; those stand at the labels "
              "the data carries, and only independent evidence can "
              "raise them. External challenge remains reserved by the "
              "publication bar.")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Hoppe Engine v3 — starts from a problem.")
    parser.add_argument("problem", nargs="*",
                        help="the problem, as words on the command line")
    parser.add_argument("--problem-file", default=None,
                        help="read the problem from this file")
    parser.add_argument("--stdin", action="store_true",
                        help="read the problem from standard input")
    args = parser.parse_args(argv)

    if args.problem_file or args.problem:
        text, source = problem_mod.load_problem(args)
        is_default = False
    elif args.stdin:
        piped = sys.stdin.read().strip()
        if piped:
            text, source = piped, "standard input (--stdin)"
            is_default = False
        else:
            text, source = problem_mod.DEFAULT_PROBLEM, "default (the inconsistencies register)"
            is_default = True
    else:
        text, source = problem_mod.DEFAULT_PROBLEM, "default (the inconsistencies register)"
        is_default = True

    engine = Engine(text, source)
    body, results = engine.run()
    sab = sabotage.run_all(miss_ledger=engine.ledger)

    checks = results["checks"]
    n_pass = sum(1 for c in checks if c["ok"])
    req_fail = [c["name"] for c in checks if not c["ok"] and c["required"]]
    des_fail = [c["name"] for c in checks if not c["ok"] and c["designed_fail"]]
    sab_caught = sum(1 for r in sab if r["caught"])
    demos = results["solves"]["demos"]
    n_consumed = len(results["solves"]["consumed"])

    if req_fail:
        verdict = "SOLVES WORKED BUT REQUIRED SUPPORTING CHECKS FAILED: %s" % ", ".join(req_fail)
    else:
        verdict = "SOLVES DEMONSTRATED"
    headline = ("HEADLINE (computed from the run below): %s — %d worked "
                "inconsistency solves, each shown BEFORE -> CORRECT THE "
                "MEASUREMENT -> RUN H(S, B, T) = S' -> INVARIANT SOLVED "
                "-> AFTER at its recorded label | fine structure: NOT "
                "SOLVED (the honest case, full candidate set shown) | "
                "return leg: %d invariants RETURNED AND USED by later "
                "items in this run (chain printed) | supporting "
                "arithmetic underneath: checks %d/%d passed, designed "
                "stress miss: %s | sabotage caught %d/%d"
                % (verdict, len(demos), n_consumed, n_pass, len(checks),
                   ", ".join(des_fail) if des_fail else "none",
                   sab_caught, len(sab)))

    lines = [headline, LIMITATION, "", body, "",
             "=== Sabotage suite — the audit's attacks, as regression tests ==="]
    for r in sab:
        lines.append("  %s %-38s %s" % ("CAUGHT" if r["caught"] else "NOT CAUGHT",
                                        r["attack"], r["detail"]))
    lines.append("Each catch was logged as a Miss Report entry; the suite "
                 "ran against sandbox copies, so the real graph was never "
                 "touched by an attack.")
    lines.append("")
    lines.append("=== Open bridges carried forward (from the graph data) ===")
    for b in engine.graph["open_bridges"]:
        lines.append("  " + b)
    lines.append("")
    lines.append("=== Validation status ===")
    lines.append(headline)
    lines.append("Statuses unchanged by this run except as Governor "
                 "decisions above record. Corrections belong in "
                 "supersession entries, never in edits to history.")

    text_out = "\n".join(lines) + "\n"
    if is_default:
        (ROOT / "docs" / "run-v3.txt").write_text(text_out)
    print(text_out, end="")
    return 0 if not req_fail and sab_caught == len(sab) else 1


if __name__ == "__main__":
    sys.exit(main())
