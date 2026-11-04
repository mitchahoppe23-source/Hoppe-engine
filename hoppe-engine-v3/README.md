# Hoppe Engine v3 — the core pieces, in the code, working (2026-11-02)

Author: Mitch Hoppe. Co-author checks by GPT and Gemini (frame,
boundary, and documentation audit; independent numerical
recomputation), as in the prior builds.

Version 1 (`~/workspace/hoppe-engine/`) and version 2
(`~/workspace/hoppe-engine-v2/`) are untouched beside this folder.
They were scoped as number-checkers: the framework's core pieces
lived in them as labels in a data file, or as counts. The author
corrected that on 2026-11-02, in substance: of course the core
pieces we have gone through are supposed to be put into the code —
working parts, not just labels or data entries. And the run should
show how we solved the inconsistencies with the code, with a return
leg — not do a one-way test people already do every day, whose
result lands nowhere. v3 is built to that correction.

## Why this exists

The author's stated purpose: this engine exists so the work needs
no gatekeeper. No board, bulletin, credential, account, or
permission is needed to run it, check it, or reproduce its
results. The author figured this out and chose to make it readily
available for anyone to reproduce, rather than use it to control
access. Reproducibility is the protection and the hearing at once:
the author's name and date are on it, the runs are byte-for-byte
reproducible, and the results speak without the author having to
plead a case or surrender the work to an intermediary.

## Run it

```bash
python3 run_engine.py                        # the default problem: the
                                             # inconsistencies register,
                                             # worked as solves
python3 run_engine.py "your problem here"    # a problem of your own
python3 run_engine.py --problem-file f.txt   # a problem from a file
cat problem.txt | python3 run_engine.py --stdin
python3 tests/sabotage.py                    # the sabotage suite alone
```

Pure Python 3 standard library — no installs, no network, no
accounts, no cost. Same input, same output, byte for byte (verified:
repeated runs are identical; sequence numbers in the ledgers are
logical, never wall clock, and the printed transcript does not
depend on ledger length). The default run saves its transcript to
`docs/run-v3.txt`.

## What the run does, in plain words

The engine **starts from a problem**. It opens with the author's
friendly startup — "What's the problem you'd like to work on?" —
prints the problem under `PROBLEM:`, and carries that problem
through the whole run.

Then the **M=0 lens** runs on it. The author's position, in his
words:

> "M=0 is a lens used to unify quantum physics and gr. It shows
> that starting from .1010205 instead of true zero and taking the
> correct measurements resolves all the inconsistencies."

The lens is three operations, not a slogan: (a) start from the seed
epsilon = 5 − 2√6 ≈ 0.1010205 instead of true zero; (b) restate the
problem's quantities as dimensionless ratios (the mismeasurement,
in the author's definition, is putting the observer's view plus
human numbers rather than dimensionless ratios); (c) use the same
measuring stick the same exact way at both ends — and flag it when
a problem mixes sticks, with the checked example being h used at
one end and ħ (hbar) at the other, which moves the Planck products
by exactly 2π.

The **main event is the worked solves**, run inside the author's
HE-15 loop (measure from the observer's center → only probable
truths or facts in → compare variants to find the invariant → plug
it in and test in reality → adjust or add surrounding variants →
measure again accepting only known or provable truth → repeat).
For each register item the transcript shows the full solve:

BEFORE (the inconsistency as stated) → CORRECT THE MEASUREMENT →
RUN H(S, B, T) = S′ → INVARIANT SOLVED → AFTER (the changed state
S′, at its recorded label) → RETURNED (where the result went).

The items demonstrated (sources: the inconsistencies register and
the applied worksheet of 2026-10-29 — applications there are
analyst work under the author's direction and method, not his
positions, except where his position is cited inside an item):

- **Item 6, black-hole boundary** — R_s/l_P = 2n, T_H/T_P = 1/(8πn),
  S_BH/k_B = 4πn², and R_s·T_H = ħc/(4πk_B) at every n. DERIVED.
  Run first because it solves the shared stick ħc that later items
  use — that is the return leg, built into the run's order.
- **Item 1, singularities** — finite Planck density ceiling
  rho_P = 5.155×10⁹⁶ kg/m³; rho/rho_P = 0.02984/n². Algebra
  DERIVED; the node-floor physical claim HYPOTHESIS.
- **Item 3, gravity and electromagnetism, one language** — both on
  the stick returned from item 6: alpha_G electron 1.752e-45,
  proton 5.906e-39, force ratio 2.269e39. Restatement DERIVED;
  mechanism HYPOTHESIS.
- **Item 7, hierarchy** — the full alpha_G table (electron, proton,
  W, Z, Higgs, top) built by extending item 3's returned method.
  Restatement DERIVED; why the masses sit below m_P OPEN;
  mechanism HYPOTHESIS.
- **Item 5, scale transitions** — the Pell invariant x² − 6y² = 1
  at every zoom step, steps 0–4 shown. DERIVED as mathematics;
  physical claim HYPOTHESIS. Its steps are returned into item 4.
- **Hubble tension** — one dimensionless ratio in dispute, 1.0837
  (67.4 vs 73.04), located at the boundary by the author's ruling.
  This item now prints **two label lines, split** (author's
  direction, 2026-11-02), instead of one buried label:
  - *Lens mechanism: PROVEN as a mechanism* — demonstrated in the
    run by the laser stack (below): an unchanged source read
    through different lens stacks gives different apparent
    readings. Label for the mechanism: DERIVED/OBSERVED (the
    mechanism, demonstrated) — the closed label set has no
    PROVEN label, and none is introduced.
  - *Hubble attribution: HYPOTHESIS* — the claim that the 1.0837
    gap is this mechanism stays at the author's stated hedge
    (his words: "Hubble is due to lens issues I'm pretty sure")
    until the ratio is shown to track a specific lens difference
    between the two routes.
  The laser demonstration (the author's comparison, extended at
  his direction from 3 lenses to 5): a straight ray 1 cm off
  axis, true angle 0.000° throughout, through identical 50 cm
  lenses spaced 25 cm apart gives apparent (exit) angles of
  −1.146° (1 lens), −1.719° (2), −1.432° (3), −0.430° (4), and
  +0.788° (5) — by 5 lenses the apparent angle is on the other
  side of true, while the source never changes.
  The item also puts in **what the routes are actually looking
  at and compares them through the H Operator** (author's
  direction, 2026-11-02): S = what each route looks at — the
  same expanding universe for every route; B = that route's
  lens stack, rung by rung; T = the reading pass; S′ = the
  H_0 that route comes out with. Planck looks at the cosmic
  microwave background (stack ends in a Lambda-CDM model fit)
  and comes out 67.4 (ratio to itself 1.0000); SH0ES looks at
  Cepheids and Type Ia supernovae up the distance ladder and
  comes out 73.04 (ratio 1.0837); H0LiCOW looks at quasars
  through a foreground galaxy's gravity as a literal lens and
  comes out about 73 (ratio 1.0831); TRGB looks at the
  brightest red giant stars to calibrate the *same* supernovae
  SH0ES uses — one rung of the ladder changed — and comes out
  69.8 (ratio 1.0356), between the other two. S′ varies as B
  varies, the same pattern as the laser table; no route has
  zero lenses. TRGB source: Freedman et al. 2019, "The
  Carnegie-Chicago Hubble Program. VIII" (arXiv:1907.05922;
  The Astrophysical Journal) — H_0 = 69.8 ± 0.8 (stat) ± 1.7
  (sys) km/s/Mpc from the paper's abstract, fetched and
  checked for this build. Printed honest limit, unchanged:
  comparing the routes *as stacks* does not by itself prove
  the 1.0837 comes from the stacks; the attribution stays
  HYPOTHESIS. The route comparison is returned into the
  dark-matter solve, alongside the boundary-location method.
  The item now also sets **the boundary to 5 and identifies
  the rungs by reach** (author's direction, 2026-11-02, in
  his words: "So we set the boundary to 5 and then identify
  the rungs correctly as to how far out we're trying to
  look"). The boundary/reference is 5 — the centre every
  route is counted out from and back to (the observer's
  centre; from 5, −2√6 reaches the seed and +2√6 the
  partner, on every axis). The run prints a reach-order
  table — rows are reach bands from the centre outward,
  read across the four routes, each cell naming that
  route's rung at that reach or marking NO RUNG (the route
  jumps/carries across that stretch, and the cell says
  how):
  - *(a) Home/anchor reach* — SH0ES and TRGB have the
    geometric anchors (Milky Way parallax; the Large
    Magellanic Cloud at 49.59 kpc); Planck and H0LiCOW
    have no rung here.
  - *(b) Nearby-galaxy reach* — SH0ES's Cepheids and
    TRGB's red-giant tip in the supernova host galaxies:
    **same reach, different rung identity** — the one-rung
    swap made visible as one cell changing in one band.
    Planck carries this stretch inside its model fit;
    H0LiCOW jumps it.
  - *(c) Hubble-flow reach* — the Type Ia supernovae
    (SH0ES: redshift 0.023–0.15; TRGB: the Carnegie
    Supernova Project sample); Planck has no rung of its
    own here, H0LiCOW none.
  - *(d) Deep reach* — H0LiCOW's only rungs: a foreground
    lens galaxy partway out and the source quasars behind
    it (source redshifts 0.654–1.789), read back through
    the lens. Every other route has no rung here.
  - *(e) Boundary reach* — Planck's home rung: the cosmic
    microwave background, light from ~380,000 years after
    the Big Bang (redshift ~1090). No other route reaches
    it.
  Direction of travel is printed with the table: the
  ladders build centre → outward rung by rung; the
  lensing route reads a deep target back through a middle
  lens; Planck starts *at* the boundary reach and infers
  back to the centre through the model. Reading-off, in
  plain words: with the boundary set to 5 and rungs
  identified by reach, the four results are readings taken
  with different rung sets over different stretches of the
  same count-out; the stretches with no rung are exactly
  where a route's model does the carrying, and a
  discrepancy can sit in the carrying (B) without anything
  differing at the target (S). **Authorship, as printed in
  the run:** the boundary-5 count-out is the author's
  method; the alignment table is analyst assembly
  (Muse's), put up for his correction — not his ruling,
  and no label changes because of it. Reach sources,
  each fetched and checked for this build and named in
  the run: Pietrzyński et al. 2019, *Nature* 567, 200–203
  (LMC 49.59 ± 0.09 ± 0.54 kpc); Riess et al. 2022,
  *ApJL* 934, L7 (calibrators at z < 0.01; Hubble-flow
  supernovae 0.023 < z < 0.15; parallax to a few kpc);
  Freedman et al. 2019, arXiv:1907.05922 (TRGB hosts 7 to
  nearly 20 Mpc; ~100 CSP supernovae into the flow); Wong
  et al. 2020, *MNRAS* 498, 1420–1439, H0LiCOW XIII (six
  systems, source redshifts 0.654–1.789 — the verified
  range, printed in place of the roughly 1.5–2.3 figure
  in the build brief, which the fetched source does not
  support); Planck Collaboration 2020, *A&A* 641, A6
  (recombination, redshift ~1090, ~380,000 years). The
  lens galaxies' own redshift range could not be verified
  cleanly, so band (d) prints it qualitatively ("partway
  out") with no number. The rung table is carried in the
  SolveBook as `hubble_rung_table` and consumed by name
  in the dark-matter solve, where the mismatch is likewise
  located by the reach at which it is read (the
  galaxy/cluster edge).
- **Dark matter** — 5.41× invented-unseen matter vs seen (26.5%
  vs 4.9%), read as a boundary mismeasurement. The author's
  position ("dark matter was just made up") HYPOTHESIS. Plainly
  stated in the run: no invariant is solved for any named galaxy
  yet, and no galaxy case is invented.
- **Item 8, arrow of time** — the budget split v/c vs √(1−(v/c)²),
  tabulated to v = c where the temporal pace is 0; the interval
  is the invariant. Pace relation DERIVED within special
  relativity as a route with premises stated; the framework
  reading (the author's position) HYPOTHESIS.
- **Item 4, fine structure — NOT SOLVED**, demonstrated as the
  honest not-solved case, with the full candidate set (next
  section). Never presented as a solve.

**The return leg, explicitly.** An everyday test is one-way: the
result lands nowhere, the leg terminates in the void — the bleed
shape this framework rejects. In this run every solved invariant
is carried back in and USED: the ħc stick solved at item 6 is the
working stick of items 1, 3, and 7; item 1's density ceiling is
used by item 3; item 3's alpha_G method and electron/proton values
are used by item 7 (which checks that its rows reproduce them
exactly); item 5's Pell invariant and steps are used by item 4;
item 7's table is used by item 4; the Hubble solve's
boundary-location method, its route comparison (one target,
four stacks, S′ varying with B), and its rung-identification
table (boundary set to 5, rungs by reach) are used by the
dark-matter solve. The
engine enforces this in code (a later item that asks for a value
nobody returned raises an error), prints a RETURNED line per item,
and prints the verified chain at the end. Each S′ also lands as a
new entry in the run ledger — later steps start from those
entries; history is never edited.

**Fine structure, the full set, each at its label.** Measured
1/alpha = 137.035999177. Pi-sum 4π³ + π² + π = 137.036304
(DERIVED, remainder +0.000305). Formula as written with
psi = ln(eta)/√24 gives 136.568363 (REFUTED as written, remainder
−0.467636). The 3-Pell-step seed-cubed candidate — pi-sum minus
psi×eps³ — gives 137.035821, remainder −0.000178, the smallest on
the table: it is **Muse's UNCONFIRMED reading** of the author's
direction "zoom in and/or out with the 3 steps of pell equation,"
labeled that way everywhere it appears. Item status: **NOT
SOLVED**. The author's solving condition stands in the run: a
different method of measurement, not probing the electron the
usual way; no arithmetic in this run meets it, and no candidate
is presented as the solution.

**The Flower of Life is generated, then read.** Centers one radius
apart on a hex lattice; the generation counts (1, 7, 19, 37, 61)
are counted from the generated construction, not looked up. A
one-continuous-stroke visit order is built and verified (every
consecutive step exactly one radius; every center visited; circles
overlap — never tangent packing). Neighbouring circles' lenses are
computed (area 2π/3 − √3/2 ≈ 1.228370 for radius 1, spacing 1; 42
neighbouring pairs at generation 2). Traced path data carried from
v2: cumulative arcs 36/108/216/360, generation-4 closures at
42/114/222/360. Then the pattern reading runs on the problem:
center = the observer's center / M=0 reference, outward rings =
growth/scale/time, what holds across the overlaps = the invariant
candidate, and a leg with no overlapping receiving circle is
reported as a **bleed** (the run's vent leg is caught exactly this
way, and matches the hop ledger's refused branch).

**The H Operator is an application, never an addition:**
H(S, B, T) = S′. S is a State (matter/mass, energy, or transition
state), B is the Boundary as a smart filter/processor — it selects,
can change what it passes, and can refuse; a refusal is recorded
as a branch, never dropped — and T is the Transition. The hop
ledger behavior is v2's: return hops land on NEW entries and are
graded (perfect / partial / irreversible) with losses recorded.

**Underneath, not on top:** all of v2's executable checks run as
supporting arithmetic verification (seed fold 1² + 24 = 25,
eps·eta = 1, eps + eta = 10, eta − eps = 4√6, square 96, cube
384√6, faces 576 with the two-sixes identity NOT asserted, Pell
norm steps 0–4, ladder sums 2/10/98/970/9602/95050, the
eps = (√3−√2)² bridge, Planck products, R_s·T_H constancy, the
alpha_G table, the 8π rule, the HE-16 energy variants and partner
rule incl. human system F = 0.355, circulation balance, carrier
cycle), plus new v3 verifications (the seed-cubed candidate, the
flower construction checks, the lens stick checks). One designed
failure stays designed: the radiation stress test, logged as a
Miss Report with its data unadjusted. The sabotage suite (six
attacks from the audit: wrong Pell generator, h for ħ, undeclared
reduced Planck mass, corrupted graph status, empty-invariant hop,
Governor decision from a bare word) is caught 6/6.

**The Governor** holds the closed label set (OBSERVED / DERIVED /
FRAMEWORK RESULT / SUPPORTED / HYPOTHESIS / OPEN / REFUTED), grants
nothing on internal evidence alone, and refuses K changes on
internal evidence in every run. OPEN flags are preserved, not
settled: the seed-axis ends stay unassigned, the two sixes stay
distinct, generations = K stays a candidate, and the Z stepping
rule stays open.

## Standing limitation

This engine checks the framework against itself and against the
checked numbers in its data. A passing check shows exact arithmetic
and internal consistency only. It does **not** prove the
framework's physical claims; those stand at the labels the data
carries, and only independent evidence can raise them. The solves
show the framework's method working its register items end-to-end
at their recorded labels — DERIVED where the register says
DERIVED, HYPOTHESIS where it says HYPOTHESIS, OPEN where it says
OPEN, and NOT SOLVED for fine structure.

## Piece-by-piece map (which file and function does the work)

- **Problem input** — `run_engine.py: main()` (argument, file, or
  `--stdin`) and `core/problem.py: load_problem()`,
  `parse_quantities()`, `detect_mixed_sticks()`. Startup line and
  `PROBLEM:` belong to `core/problem.py` (`STARTUP_LINE`,
  `DEFAULT_PROBLEM`).
- **M=0 lens** — `core/lens.py: correct_measurement()`,
  `seed_floor()`, `restate_as_ratios()`, `check_same_stick()`
  (the h/hbar mixed-stick flag uses `planck_products_split` from
  `core/invariants.py`).
- **HE-15 loop** — `core/loop.py: Engine.run()` (steps 1–7 as the
  run's section structure; gates at steps 2 and 6).
- **Worked solves + return leg** — `core/solves.py`: one
  `solve_*` function per item (`solve_black_hole`,
  `solve_singularities`, `solve_gravity_em`, `solve_hierarchy`,
  `solve_scale_transitions`, `solve_hubble`, `solve_dark_matter`,
  `solve_arrow`), `demonstrate_fine_structure()`, and
  `SolveBook` (`carry()` / `use()` — the return leg, enforced: a
  later item cannot consume a value no earlier item returned).
  Run order follows the chain: 6 → 1 → 3 → 7 → 5 → Hubble →
  dark matter → 8 → 4 (not solved).
- **Laser stack demonstration** — `core/laser.py: laser_stack()`,
  `verify_stack()`, `demonstration_lines()`, called from
  `core/solves.py: solve_hubble()`. Computes the paraxial
  thin-lens stack (straight ray, 1 cm off axis, 50 cm lenses
  spaced 25 cm apart) out to 5 lenses in the run, and verifies
  the computed rows against the recorded values.
- **Hubble route comparison** — `core/solves.py:
  solve_hubble()` (the `routes` table in that function: each
  route's target, stack rung by rung, and result, run through
  H and compared with S held the same; the TRGB value is from
  Freedman et al. 2019, arXiv:1907.05922). The comparison is
  carried in the `SolveBook` as `hubble_route_table` and
  consumed by `solve_dark_matter()`.
- **Hubble rung identification by reach (boundary set to
  5)** — also in `core/solves.py: solve_hubble()`, after the
  route comparison: the reach-order table (bands (a)
  home/anchor → (e) boundary, the four routes read across
  each band, NO RUNG cells naming how a route carries
  across a stretch), the direction-of-travel lines, and the
  reading-off. Reach figures are verified sources named in
  the run (Pietrzyński 2019; Riess 2022; Freedman 2019;
  Wong 2020; Planck Collaboration 2020). Carried in the
  `SolveBook` as `hubble_rung_table` and consumed by name
  in `solve_dark_matter()`.
- **H Operator** — `core/hops.py: HopEngine.hop()` and
  `return_hop()`; states and smart-filter boundaries in
  `core/state.py: State`, `Boundary.admit()`; the run's hop chain
  in `core/loop.py: Engine._demo_hops()`.
- **Flower of Life** — `core/flower.py: centers()`,
  `generation_counts()`, `stroke_order()`, `neighbour_pairs()`,
  `lens_area()`, `verify_construction()`, and the reading in
  `read_on_flower()`.
- **Fine structure** — `core/solves.py:
  demonstrate_fine_structure()` (the full labeled candidate set)
  and `check_fine_structure_seed_cubed()`; pi-sum and
  formula-as-written checks in `core/invariants.py`
  (`check_fine_structure_pisum`,
  `check_fine_structure_formula_refuted`).
- **Supporting checks** — `core/invariants.py: CHECKS`,
  `run_all()` (carried from v2 without regression; v3 additions
  are registered in `core/loop.py: Engine._run_checks()`).
- **Governor** — `core/governor.py: Governor.decide()`,
  `Governor.change_k()`, `weakest_link()`; label validation at
  load in `core/graph.py: load_graph()`; ledgers in
  `core/ledger.py: Ledger` (append-only, logical sequence).
- **Sabotage suite** — `tests/sabotage.py: run_all()` (carried
  from v2).

## Layout

```
run_engine.py          entry: problem in, headline computed from the solves
core/problem.py        problem input: startup, PROBLEM:, quantity parsing
core/lens.py           the M=0 lens as an operation (seed, ratios, sticks)
core/loop.py           the HE-15 run: lens -> solves -> flower -> hops -> support
core/solves.py         the worked inconsistency solves and the return leg
core/laser.py          the laser-through-lenses demonstration (Hubble)
core/flower.py         flower construction (generated) and pattern reading
core/hops.py           H(S, B, T) = S' as recorded events (from v2)
core/state.py          states, smart-filter boundaries, strips, inlays (from v2)
core/invariants.py     executable checks, exact + 60-digit decimal (from v2)
core/governor.py       closed labels, ceilings, K rule (from v2)
core/graph.py          graph loading with label validation (from v2)
core/ledger.py         append-only ledgers, logical sequence (from v2)
data/graph.json        register graph data (carried forward, provenance noted)
tests/sabotage.py      the audit's six attacks (from v2)
docs/run-v3.txt        the delivered default-run transcript
ledger/                continuity and hop ledgers (append-only, grow by design)
```

## What is only partial — stated plainly

- A custom problem (your own words) gets the full startup, the
  M=0 lens on whatever quantities with units it states (a simple
  number-and-unit parser, declared as such), the flower reading,
  and the register solves as the engine's demonstrated work. The
  engine does **not** yet solve an arbitrary new problem
  end-to-end the way it solves the register items: building a
  solve for a new item still takes the register's working rule —
  state S, B, and the mismeasurement in framework terms first.
  The OPEN register items (dark energy's worked application, the
  measurement problem, matter-antimatter asymmetry) are in
  exactly that state in the source files and are not worked here.
- Dark matter's demonstration works the restatement and names the
  missing work; it solves no named galaxy, because the record
  contains none and the engine does not invent one.
- The flower stroke is a verified visit order over the generated
  centers (with revisits, as a traced stroke has); it is a
  construction/read model in code, not a rendering — no drawing
  is produced.
- The graph data (`data/graph.json`) is v2's register graph,
  carried forward unchanged as data (provenance line updated).
  v3's change is that the core pieces now also exist as working
  code; the graph was not re-ruled or extended.
