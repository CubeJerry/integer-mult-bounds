# Verification and provenance

## S007 verification

The [component and numerical record](../../sessions/2026-11-26-S007/VERIFICATION.md) covers the new canonical factor inventory, arbitrary CRT assignments, two independently implemented order changes, first-carry formula and mod-four convolution. The full physical clocks are written arguments with AI review. Independent human refereeing remains open.

The proposition under review is the single-machine upper envelope in [the proof](README.md). The [published source at its fixed revision](https://github.com/openai/math/tree/3344da59991ed94f9ba711217b29c1d760badfa6) supplies the fixed-template identities, the short-FFT and integer caller, and the original tape layout. The branch supplies its own uniform variable-arity estimates. The comparison with the paper's unspecified excess is quantitative. Priority remains undetermined.

| Dependency | Evidence and scope |
|---|---|
| Adaptive interchange and absolute visited space | [Physical recursion proof](AQ-P.md), examined against the source order for prefix batching, label pencil and tail reserves. Earlier [global independence and space review](../../sessions/2026-11-26-S003/route-c/REVIEW-ADAPTIVE-EXTRACTION.md) covers the S003 construction. A Lean physical body for arbitrary thin records is still open. |
| Short cyclic axes | [Elementary eventual witness](coprime-axes.md) and [independent sieve and arithmetic review](../../sessions/2026-11-26-S006/review-axes-and-arithmetic.md). Finite replay checks actual downward gcd searches with and without a remainder axis. The stated explicit cutoff certifies this lemma alone. |
| Exact selected Walsh | [Modular execution](modular-walsh.md) and [independent reconstruction](../../sessions/2026-11-26-S006/review-modular-walsh.md). Direct finite butterflies and independent actual Newton repair rows test separate claims. |
| Physical residue arithmetic | [Executable fixed-head scalar](modular-scalar-machine.md). The author and an independent reviewer checked its bounded words, short Euclid, sign and tape positions. The [independent executable review](verify-scalar-heads.mjs) checks cleanup, head return, and padded widths. Execution uses only local symbols and unit moves in the arithmetic core. |
| Remaining full-width products | The [arithmetic review](../../sessions/2026-11-26-S006/review-axes-and-arithmetic.md) distinguishes short recursive coefficients from the outer stream. An independent replay performs actual signed Toom-3 recursion, including its exact interpolation divisions. |
| Exact CRT discovery | [Four-point support proof](../../sessions/2026-11-26-S006/four-point-frobenius-obstruction.md), [all-degree scalar bound](../../sessions/2026-11-26-S006/four-point-all-degrees.md) and [exact finest grouping](../../sessions/2026-11-26-S006/four-point-bundle-coarsening.md). [Full-word trace bundles](../../sessions/2026-11-26-S006/stable-four-point-bundles.md) support a growing sequence of actual forward/inverse levels for every $3\mid b$. [Independent reconstruction](../../sessions/2026-11-26-S006/REVIEW-BUNDLE-LAYERS.md) checks intermediate values, even-degree stabilizer translations and caller padding. |
| Source-linked Walsh formalization | [ModularWalshExact](formal/ModularWalshExact.lean) proves denominator support, canonical scalar division, rational row composition and exact composite-modulus evaluation of the published even-width Walsh target for every bank size and address width under the bank's sharp magnitude hypothesis. [RepairDyadic](formal/RepairDyadic.lean) proves that every published native plan is dyadic, verifies the actual $m=63$ gap and checks the general two-term obstruction under its matrix identity. The tape recursion time and space are outside these formal statements. |
| CRT formalization | [FrobeniusBundles](formal/FrobeniusBundles.lean) gives the finest stable coset partition of any additive automorphism. [TraceBundles](formal/TraceBundles.lean) proves the cubic trace split, the full period of the normal-basis two-mark direction and the exact counts of canonical fixed words on equal cycles with and without a common complement. [AdditiveTraceLayers](formal/AdditiveTraceLayers.lean) verifies evaluation in the unscaled basis and both inverse compositions for every number of independent ordered binary directions in any Mathlib field of characteristic two, including an explicit four-element case. [BundleTransport](formal/BundleTransport.lean) verifies transport between complete ordered records in any finite characteristic-two field. The actual Frobenius power, the anchor offset and the ordered directions determine the unique conjugate remainder of each binary polynomial. Reverse transport restores arbitrary source rows. The application to the full trace stream and its head movement is a written argument with separate numerical checks. |

A clean Lean 4.34.1 run compiled the contribution files from their recorded bytes, rejected warnings, checked axiom lists, and replayed the compiled declarations using Lean's kernel. The checker tests the exact names and axiom lists of 56 designated results in eight modules. Setting `S006_FRESH=1` requests replay of every module and all its imports in a fresh kernel environment. The original plan and column modules are unchanged. The test narrows the umbrella import in the published `Port.Token` source and retains every declaration in its body. [Full source and axiom receipt](../../sessions/2026-11-26-S006/lean-axioms.txt) · [Reproducible build](formal/check.sh)

The [coefficient-prefix checker](../../sessions/2026-11-26-S006/verify-trace-coefficient-prefix.js) compares the scan formulas against ordinary long division, exact reconstructed polynomials and the actual bundle roots. It checks every prefix at the tested degrees in both directions. The forward input is the literal contiguous binary coefficient list. The [formal radix split](formal/TraceCoefficientPrefix.lean) identifies both outputs with ordinary monic quotient and remainder at every actual trace-polynomial power.

The [finite receipt](../../sessions/2026-11-26-S006/finite-replay.json) includes exact counts and finite resource samples. Run the companion JavaScript files with Node.js. Independent written reviews were carried out by different AI workers and examined by the integrating author. No human referee or end-to-end multiplier execution is recorded.

The campaign's remaining open physical and asymptotic questions are in [OBLIGATIONS](../../OBLIGATIONS.md). The terminal writing convention, input-dependent choices and eventual cutoffs are part of the theorem. A numerical cutoff for the entire multiplier remains open.

From the programme directory, the complete finite component checks can be repeated with the following commands.

```bash
s=sessions/2026-11-26-S006
p=contributions/explicit-overhead
for f in "$s"/verify-*.js "$s"/verify-*.mjs; do node "$f"; done
python3 "$s/check_bundles.py"
node "$p/modular-scalar-machine.mjs"
node "$p/verify-scalar-heads.mjs"
bash "$p/formal/check.sh"
```

The complete multiplier has written-proof status. Its complexity analysis, the adaptive numerical routing and the full fixed-head CRT/carry supplier have different verification scopes. No priority claim follows from the comparison with the published unspecified excess.

The [grouped composition proof](formal/GroupedComposition.lean) proves the ordinary quotient and remainder for each compositional factor, including its degree bound. The [independent coefficient and grouped-factor checker](../../sessions/2026-11-26-S006/verify-trace-prefix-independent.js) checks both starting directions, the small-field coordinates and their literal factor products. [Output](../../sessions/2026-11-26-S006/trace-prefix-independent-receipt.json)

A separate reproduction fetched the published scientific checkpoint, verified 52 file blobs and 93 local link targets, reran all 13 finite-check drivers, and rebuilt all eight Lean modules from the fetched files. All 56 named axiom lists passed. The independent coefficient driver reproduced its raw receipt byte for byte. [Source checkpoint](https://github.com/CubeJerry/integer-mult-bounds/commit/cc75d2b35c1d6828536a0473d5e6de5426ac2ef0)

## S007 grouped coordinate change

A [fixed-tape proof](../../sessions/2026-11-26-S007/grouped-ambient-words.md) prices the power-basis to ambient-word conversion at the actual representative and its inverse. The [replay](../../sessions/2026-11-26-S007/verify-grouped-words.py) and [receipt](../../sessions/2026-11-26-S007/grouped-words-receipt.json) cover five degrees, independent binary payloads, ordinary monic division and ragged tiles. The rank-exponent source supplies an existence proof for a fixed exact algorithm over the binary field. Finite runs use the seven-product identity.
