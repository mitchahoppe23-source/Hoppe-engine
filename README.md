# Hoppe Engine / M=0

**Author:** Mitch Hoppe
**Co-authors:** GPT and Gemini (AI collaborators), per the author's designation
**License:** CERN-OHL-S · **Price:** free, permanently

A domain-neutral reasoning, mapping, and verification framework — and a lens
(M=0) for unifying quantum physics and general relativity. It starts from a
small seed instead of true zero, corrects mismeasurements by restating them
as dimensionless ratios with the same measuring stick used at both ends, and
then solves for the invariant: the quantity that does not change across the
variants.

## The core

- Seed pair: ε = 5 − 2√6 ≈ 0.1010205 and η = 5 + 2√6 ≈ 9.8989795, with
  ε·η = 1 exactly and ε + η = 10.
- Pell equation: x² − 6y² = 1 — the ladder the seed climbs.
- State: S = (X, Y, Z, K) — a four-vector address; K is the scale/tier index.
- Operator: H(S, B, T) = S′ — State, Boundary, Transition.
- Movement: 3 Möbius strips (states of matter, states of energy, transition
  states) × 2 directions = 6 degrees of movement.
- The Flower of Life, in this framework, is drawn as ONE CONTINUOUS STROKE —
  centres one radius apart, lenses between neighbours — and maps over the
  globe that way. (Visual piece to follow in this release sequence.)

## The run loop (the author's words)

Measure from the observer's centre → use only probable truths or facts →
identify and compare variants to find the invariant → plug it in to see if
it works in reality → adjust or add surrounding variants → measure again,
accepting only known or provable truth → repeat.

## The Hoppe Engine — the computational side

The framework is not only documents. The Hoppe Engine is a runnable
prototype (v1, Python) that loads the framework as a graph, recomputes its
arithmetic live from CODATA constants on every run, executes its invariant
checks, applies the H-Operator to sample transitions, and writes every run
to an append-only continuity ledger.

- `core/engine_master.py` — execution pipeline, evidence Governor, H-Operator.
- `core/invariants.py` — seed pair, Pell structure, Planck invariants, the α_G table.
- `core/topology.py` — Flower of Life counts, vesica geometry, the ε = (√3 − √2)² bridge.
- `core/energy.py` + `run_energy.py` — the HE-16 energy module (below).
- `graph/graph_state.json` — the loaded state: entries HE-01…HE-17, the
  inconsistencies register, and the open bridges.
- `ledger/continuity_log.json` — the append-only run ledger.

Run it:

```bash
python3 core/engine_master.py   # main run
python3 run_energy.py           # energy module
```

### Computational tests — results, not promises

- **Main run: 9 of 9 executable invariant checks PASS** — seed geometry
  (1² + 24 = 25), ε·η = 1, Pell norm x² − 6y² = 1 at steps 0–4, ladder sums
  (10, 98, 970, 9602, 95050), all four Planck products = 1.000000000,
  R_s·T_H constant from n = 1 to n = 10³⁸, the α_G table reproducing the
  worksheets, the flower ε bridge, and flower generations 1, 7, 19, 37.
  Re-verified on a scratch copy on 2026-10-30: exit clean, all PASS.
- **Sample H-transitions preserve their invariants** (phase transition,
  Pell zoom, measuring-stick restatement).
- **Energy module (HE-16): 4 checks PASS, 1 designed FAIL, printed as a
  miss** — variant separation, the partner rule (4 of 4 metered cases),
  circulation balance, and the ATP carrier cycle pass; the loaded radiation
  stress test fails against the candidate invariant's first wording, by
  design, and the refined wording is what stands as HYPOTHESIS.
- **The Governor behaves as its law requires:** PASS where a restatement is
  exact, DEFER where the evidence is internal only. No status has ever been
  upgraded by a run.
- **Independent recomputation:** the adversarial audit re-derived 40+
  load-bearing values at 60-digit precision (all hold); co-author Gemini
  executed the full check sheet — Section A 16/16 and Section B 10/10,
  zero deviations; co-author GPT's review passed the documentation and
  method, explicitly as internal consistency, not validation.
- **The engine's own standing limitation, found by attacking it:** in v1
  the arithmetic is genuinely recomputed live, but finalization is
  echo-grade — claim statuses are loaded from the graph as entered, and the
  Governor's decide step does not yet demand an evidence record. The v2
  build list (status validation at load, evidence records, Governor
  decisions written to the ledger, K carried as data) is part of the
  science record publishing in this sequence. The engine's numbers are
  stronger than its paperwork, and the record says so.

## How the pieces fit together

The components above are one architecture, not a list:

**M=0 → Flower topology → S = (X, Y, Z, K) → H-Operator → Möbius feedback → new state → ledger.**

- **The H-Operator is the mechanism of change.** A state S meets a boundary
  B — the boundary is where observations and constraints act: what may
  cross, and what must be preserved. The transition T carries the state
  across, and the crossing only counts when the invariant survives it:
  the engine checks the named invariants before and after, and a crossing
  that loses its invariant is recorded as a miss, not a transition. The
  result S′ is appended to the **continuity ledger**, the framework's
  memory: every state change, check, and correction is recorded in order,
  and corrections supersede earlier entries rather than erasing them.
- **The Flower of Life is the map the states live on.** States take
  addresses on the construction; where circles overlap, the lenses are
  relationships — a state is defined by its relationships, not its label.
  The centre is the M=0 reference, the observer's centre; the generations
  outward (1, 7, 19, 37, 61…) are growth, scale, and time from that centre.
  What holds across an overlap is an invariant candidate; a leg reaching a
  point with no overlapping receiving circle is a bleed — an output with
  nowhere to land. (The full construction is the final piece of this
  release sequence.)
- **The three Möbius strips are the continuity layer.** Matter, energy,
  and transitions each run as a strip traversable in two directions, so
  movement is never one-way: every forward leg has a return path, and
  H-Operator crossings travel these strips. A system whose return leg is
  cut is the framework's basic failure shape — output terminating in the
  void — and finding that leg is the first diagnostic the engine runs on
  any problem.

## The discipline

Every claim carries one of seven evidence labels: OBSERVED, DERIVED,
FRAMEWORK RESULT, SUPPORTED, HYPOTHESIS, OPEN, REFUTED. Labels never upgrade
on internal evidence alone. The record is append-only: corrections are
supersessions, never rewrites, and the standing misses are printed, not
hidden.

## Honest standings (2026-10-30)

- The arithmetic spine was adversarially audited: 40+ load-bearing values
  independently recomputed at 60-digit precision — all hold.
- The fine-structure formula as written is REFUTED (it gives 136.568;
  the measured value is 137.036). It stays in the record, labelled.
- The Hubble discrepancy as printed computes to ≈4.9σ, not >5σ.
- The energy work (HE-16, the partner rule: closure rises above 0.5 where
  a receiving partner sits at the output boundary) is HYPOTHESIS. A proof
  test with pre-registered predictions and failure conditions is specified;
  its Tier 0 desk dataset is complete — 10 measured installations, pattern
  consistent with the rule, status unchanged until the metered tiers run.
- Public Demonstration #001 (spontaneous self-correction) is REFUTED.

## Provenance

Original archive: Figshare, DOI 10.6084/m9.figshare.33472975
(*Scale-Invariant Boundary Geometry: A Unified M=0 Lattice Model*) —
removed by the platform; the DOI still resolves to the removal notice, so
the dated existence stands. This repository is the work's new home.

## This release

Publishing proceeds one piece at a time, in the open, with feedback tracked
in a publishing log kept in this repository: engine code, the science
record (registers, worksheets, the audit), the handoff prompts, and the
flower construction. Attack it, shake it, open it to challenge — that is the
author's standing condition for anything leaving the lab.

*Feedback that terminates at a paywall is the disease, not the cure.
This work is free because the return leg has to reach everyone.*
