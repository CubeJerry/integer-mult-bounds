# Independent agent review: compact predictor and capped restart schedule

Reviewer: Route C, independently assigned during session 2026-11-26.
Status: **passed within the stated enabling scopes**, with caller obligations
retained. This is an independent agent review, not independent human review,
a Turing-machine implementation, or Lean/kernel certification.

## Exact reviewed artifacts

| Artifact | SHA-256 of reviewed text |
| --- | --- |
| `routes/A/compact-complex-predictor.md` | `4dd9a13f9bbd4f863d51afff8c4e80663ce4fc668c4e54310eec40d5d3111c42` |
| `routes/A/scheduler-and-chunking.md` | `f0c7c42d825dd18b17a554492107968811c4992c670f3508a2010da9d39875bd` |

Later edits need delta review; these hashes identify the reviewed statements.
The relevant source `build/uniformity.tex` was read in full at
`openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`, alongside the already
read Fourier `repair.tex`, `kernel.tex`, `binary.tex`, and tape `walsh.tex`.

## Compact characteristic-zero predictor

The following steps were checked separately.

1. The polynomial-evaluation shift family is `min(t,m)`-wise independent:
   the Vandermonde evaluation map onto any such coordinate subset is
   surjective, and applying a nonzero binary functional preserves independent
   uniform bits. Translation by an arbitrary frequency pattern preserves it.
2. The pairing bound for the even Rademacher moment counts every surviving
   tuple at least once. Overcounting only strengthens the upper bound. It
   remains valid when `2r > m`; independence of all distinct positions used
   by a monomial is sufficient.
3. Clipping the count window to `[0,m]` does not create additional exceptional
   counts. The Markov estimate is uniform in frequency, rather than an
   average or an unproved simultaneous union bound.
4. Alternating values at `D+1` consecutive integers force exactly `D` simple
   real roots in the `D` disjoint open unit intervals. Exact midpoint roots
   in bisection can be retained directly. No numerical root isolation oracle
   is needed.
5. The leading coefficient is `(-1)^(u+D) 2^D/D!`, with absolute value at
   most two. The spectral range of the count operator is `[0,m]`, so the
   stated factor and telescoping perturbation bounds hold in the common
   unitary eigenbasis. Coefficient error in the leading scalar remains a
   separate charge, as the document states.
6. The independent inputs are the shift rows themselves; no initialized
   accumulator or scalar-extension coordinate is counted as an input.
   The Hermite-repair implication is algebraically valid with the specified
   row counts and distinct rational check nodes.

The proof does not cover the small-characteristic interchange template.
Its explicit warning is necessary. Nor do the factor norm estimates cover
the live arrays of a physical routed-pencil implementation. Those exclusions
are correctly retained.

## Restart schedule and chunk assembly

1. The code-length weights sum exactly to `3/16`. The bucket count makes the
   total quadratic decoding/control cost `O(2^s)` per round, including the
   many short-budget attempts. This is a necessary check; summable weights
   alone would not account for per-attempt initialization.
2. Candidate generation, input copying, length/chunk tests and output are
   inside the attempt clock. Cleanup must use the source frontier marks and
   charge only visited intervals, not rescan an entire `O(n)` allocation for
   every one-step attempt. With that inherited mechanism, the claimed round
   and common-space bounds follow.
3. The schoolbook attempt bounds the final round by `O(log n)`, so index,
   clock and descriptor bit lengths remain `O(log n)`. Very large proposed
   chunk counts are tested inside the clock; they are not materialized by
   the unclocked controller.
4. Reversing chunk order while preserving bit order within a chunk costs
   `O(n)` with a reused chunk buffer and a constant number of streams. Along
   one product diagonal, the prepared operand cursors both move forward;
   total repositioning and scanning is `O(n)` per diagonal.
5. Each added product has fewer than `2u` bits. Its addition can increment
   the high accumulator counter by at most one. Amortized ripple accounting
   applies even with a nonzero initial carry: its initial bit potential is
   charged once per diagonal. This justifies `O(nr)` rather than silently
   paying `O(r^2 log r)`.
6. The invariant `carry <= r(B-1)` follows directly from
   `D_ell <= r(B-1)^2`. The final product is below `B^(2r)`, and the padded
   `2ru`-bit output fits `O(n)` cells because `r <= n`.
7. The cap calculation keeps fixed description storage `d_j` separate from
   proportional space `c_j u`. The threshold inequalities imply
   `c_j ceil(n/r_j)+d_j <= n/2`. Candidate generation time and interpreted
   step cost remain in the final envelope, rather than disappearing into
   unquantified uniform constants.

No mathematical correction was needed in these reviewed versions. In
particular, improving the schedule cannot itself establish a useful growth
law for valid candidate constants, thresholds, or generated descriptions.

## Actual reruns

Both commands were rerun under Python 3.12.14:

```
python3 -B research/moonshot-overhead-program/routes/A/verify_compact_predictor.py
python3 -B research/moonshot-overhead-program/routes/A/verify_scheduler_chunking.py
```

The compact verifier reported PASS: 5,475 interpolation cases, 40 root-product
cases, 1,023 tail controls, and exact translated-independence/moment checks at
two toy strengths. The scheduler verifier reported passed: 1,024 rounds,
19,999 indices, 145,636 exhaustive assembly cases, 980 larger assembly cases,
3,840 cap boundary cases and its stated threshold checks. Negative controls
for the leading scalar and omitted cross-diagonal carry were detected.

These finite checks support the identified identities and failure modes;
they do not certify an implementation of the entire fixed tape machine.
