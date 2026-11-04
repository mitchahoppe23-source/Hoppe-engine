# The Hubble Item — Standing as of 2026-11-03

**Author:** Mitch Hoppe. **Co-author checks:** Gemini (independent recomputation), GPT (frame audit). **Assembly from the author's record:** Muse.
**Feedback:** Timeline Feedback Log, Entry 17 (2026-11-03).
**Status labels used:** OBSERVED / DERIVED / HYPOTHESIS / SUPPORTED / OPEN / REFUTED. No label upgrades on internal evidence alone.

## The author's position

The Hubble discrepancy is a lens and boundary issue in how the measurement is made — the two chains read the same expanding universe through different measurement stacks, and the disagreement lives in the stacks, not in the universe. (HYPOTHESIS — the author's stated position, held since 2026-10-29, with his hedge "I'm pretty sure.")

The two chains: the early chain (Planck) reads H0 = 67.4 forward from the early universe through a computed sound-horizon ruler; the ladder (SH0ES) reads H0 = 73.04 outward from geometric anchors through calibrated stars to supernovae. Other routes: TRGB ≈ 69.8–70.4, lensing ≈ 73.3, megamasers ≈ 73.9.

## The method (the closest usable method, as ruled by the author 2026-11-03)

1. Do not pick a winner between disagreeing chains. Restate both the same way — dimensionless ratios, the same measuring stick at both ends — and find the layer the chains share.
2. In the shared layer, state the disagreement in the data's own units. Here the shared layer is the Type Ia supernovae, and the whole tension inside it is a brightness offset of **0.17450 magnitudes**.
3. Test correction shapes against that layer, and keep the failures in the record.
4. The correction that stands is applied at the two ends of the measurement (emission floor and observer floor — the same stick at both ends), not accumulated along the light's travel.
5. Publish the standings with their labels, including what is still open.

## What was run (2026-11-03, at the author's direction)

**Pantheon+SH0ES, full covariance** (1,701 supernovae; 77 calibrator light curves; 277 Hubble-flow supernovae; the full published covariance matrix, not diagonal errors):

- Required offset: 0.17450 mag, full-covariance error **0.0310 mag**.
- Seed correction at (1−ε)^¾ strength, ε = 5 − 2√6: offset **0.17344 mag** — consistent with the required offset (miss −0.03 standard errors against the published H0 pair). Equivalently it moves 67.4 → **73.004**.
- Flat seed (1−ε): offset 0.23125 mag — overshoots; **disfavored** on this test (+1.83 standard errors). (An earlier diagonal-error run marked this REFUTED at 3.04 standard errors; that label is superseded — the diagonal error bar was too small.)
- Correction accumulating with light travel: **REFUTED** — the tilt it requires sits 6.0 standard errors from the measured tilt.

**DES-SN5YR, independent dataset** (1,829 supernovae, redshift to ~1.12, full covariance; each run performed twice with matching results):

- The constant offset's size cannot be tested in this set (it is degenerate with the supernovae's absolute brightness). The trend can: residuals are flat, and the accumulating form is excluded at roughly **48–67 standard errors**. Independent data supports the same split: constant at the ends stands; accumulating along the path is refuted.

**Independent recomputation (Gemini):** the laser-stack invariants behind the lens demonstration, the product of the four 5-lens return-to-true settings (= 5⁷ exactly), the reciprocal pairing (differences of exactly 1/25), and all Hubble arithmetic above — CONFIRMED from fixed givens with steps shown.

**Frame audit (GPT):** "Both ways, different lenses" is coherent as a hypothesis provided it predicts the shared invariant in advance rather than explaining disagreement afterward. The endpoint correction, the growing boundary, and the petal geometry form a stack (representation → mechanism → prescription), not one claim in three forms.

## The one open piece

The exponent: the exact power the data wants is **0.754610**; ¾ is the nearest simple fraction and lands within the data's noise, but **¾ is not derived**. A strict derivation task (Gemini, fixed givens) returned: not derivable from the givens; the missing step is a structural rule connecting the (1−ε) scaling to a ¾ power. The standing candidate reason, named independently from three seats — the author's construction (a correction born in the 4-part address (X, Y, Z, K) is read out through the 3 space directions; the fraction carries a 3D stretch that a flatter reading cannot show directly) — is **3 of 4, a dimension-ratio projection**. Label: OPEN, candidate reason standing, no derivation yet.

Two related seams, named by the frame audit and awaiting the author's ruling:

- "Same stick at both ends" vs "the boundary grows between the ends": these coexist if the stick is the same dimensionless measuring *rule*, not the same physical length.
- Which ruler the correction modifies must be named exactly: the sound horizon at photon decoupling, r_s(z*), is the early chain's acoustic setting; the drag-epoch ruler (≈147.09 Mpc) used in the ratio arithmetic is a related but distinct quantity.

## Standings summary

| Claim | Label |
|---|---|
| Hubble discrepancy is a lens/boundary issue in the measurement | HYPOTHESIS (author's) |
| Correction is constant at the two ends, not accumulated along the path | SUPPORTED (two datasets, trend scope) |
| Accumulating-with-travel correction | REFUTED |
| Flat (1−ε) correction at full strength | Disfavored on the Pantheon+ test (supersedes an earlier REFUTED) |
| (1−ε)^¾ lands on the required offset within noise | DERIVED (arithmetic, independently recomputed); fit, not derived |
| Why the exponent is ¾ | OPEN — projection (3 of 4) is the standing candidate |
| The endpoint-transformation equation (predicting the correction without fitting) | OPEN — named as the strongest missing piece |

*This document is the Hubble item's standing for the engine's second release piece (Bite 2: engine v3, the engine working on the inconsistencies). It states what was run, what survived, and what is still open — nothing more.*
