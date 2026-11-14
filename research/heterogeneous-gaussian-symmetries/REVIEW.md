# Independent review of heterogeneous Gaussian symmetry and fine-prime widths

**Decision: the stated universal proof and its scoped source consequence pass
this model-assisted review. No substantive defect was found.** This review
does not provide human approval, a formal-kernel proof, a runtime lower bound,
or discharge of a retained multiplication assumption.

The reviewed proof has SHA256
`7ce68fdc614b28df6133682ee2e82f661c2d373ceb645f24f4a93d76a9d0955c`;
the author's verifier has SHA256
`18214b9c995512b2ef33ceaaaba6f5fbf23eaae4ed40e77355b6edb3f06dbf51`.
Both are in `research/heterogeneous-gaussian-symmetries`. The canonical
base is `e54523517d0f03e58352e647c403a5af3e525a57`.

## Universal obligations checked independently

1. **All vertex permutations, including exceptional geometry.** Multiplying
   transposed kernel entries removes the shifts and recovers the entire
   weighted Euclidean distance table. Polarization against a corner and its
   axis corners uniquely extends a finite-grid isometry to an affine ambient
   isometry. Preservation of the convex hull makes it an edge-face map.
   Equal edge lengths alone would be insufficient: a bijection of the whole
   grid must also preserve the number of grid points on each edge. The proof
   uses this correctly to force both equal cardinalities and equal widths.
   In particular, the square hull for `(n,gamma)=((2,3),(4,1))` does not admit
   an axis exchange on its six-point grid. Equal axis/diagonal distances also
   do not evade the edge-face argument.

2. **Shifts, groups, cycles and inverse.** Once the quadratic part is fixed,
   a unit displacement on axis i gives exactly
   `e_i a_(sigma(i))=a_i`. Opposite nonzero shifts can therefore exchange
   axes with the appropriate signs; a blanket prohibition on their exchange
   would be false. With distinct widths, the only remaining symmetries are
   reflections on zero-shift axes. The fixed-point count and formula (6)
   include empty zero-shift sets and odd side lengths correctly. The
   Vandermonde factorization proves invertibility of each ideal factor, and
   inversion preserves its exact simultaneous permutation symmetry group.

3. **Perturbation containment.** The `|a_i|<=1/2` premise gives unit-bounded
   ideal entries even for integer differences larger than one. Product
   error is at most `2 epsilon+epsilon^2`, also for complex perturbations.
   The edge/nonedge band and the derivative lower bound for distinct edge
   levels are valid. Under (12), each coordinate edge color is preserved.
   Connectivity in all other coordinates makes each image coordinate a
   function only of its own coordinate; injective walks on a finite path
   then give identity or reflection. This avoids needing a generic-spectrum
   premise or a lower bound on nonzero shifts. Small shifts may disappear;
   arbitrary entry errors may destroy symmetries. Inverse containment is
   conditional on invertibility of the stored matrix, as stated.

4. **Source width and precision arithmetic.** Distinct odd primes and target
   sizes `r` or `r/2` give distinct integer numerators m below r: equal-size
   pairs use prime distinctness and unequal-size pairs have opposite parity.
   The broad gap is at least `b0/r`; the narrow gap is strictly larger than
   `A/r` because the product of two numerators is below `r^2`. The explicit
   width ranges, signs in both gap bounds (15), and eventual `2^-o(p)` scale
   check. The factor error transfer is valid: for `d epsilon<=1`,
   `(1+epsilon)^d-1 <= exp(d epsilon)-1 <= 2d epsilon`.

The exact slot count `2cT` and its resulting bounds are correct for the
specified dense cycle-boundary format. They are not a lower bound on actual
displacement rank, compressed storage, other successor orderings, implicit
generation or arithmetic runtime. The proof preserves this distinction.

## Exact source authentication and application boundary

`SOURCE-CHECK.json` records independent byte-size, SHA256 and Git-blob checks.
The two historical normalized-kernel/fine-prime notes match their actual
canonical Git objects, including CRLF bytes. Their section 2 normalization,
broad/narrow coefficients, shrunken shifts, fine-prime interval and precision
scales support the uses made here. The homogeneous predecessor matches the
exact published [A5 proof at commit 2ae2fa14](https://github.com/CubeJerry/integer-mult-bounds/blob/2ae2fa14eeefe301652f62313b137a97036ab13d/research/gaussian-orbit-certificate-scale/PROOF.md).
That published commit was absent from the shared local object store, so its
entire UTF-8 content was retrieved at the exact remote commit and compared
with the retained copy; no local-history gate is claimed for it.

The source consequence concerns the ideal normalized tensor over distinct
original axes. The local tile volume is not the entire source target volume.
The final clarification correctly restricts this to square, correspondingly
indexed normalized factors of (1). Rectangular blocks or different row/column
index sets require a separate interface. Translations absorbed into shifts
must still satisfy the shift bound before the rounding corollary is applied;
the same-origin square sections supply the retained source bound.
The source notes explicitly include chirps, truncation, rounding and other
maps outside that boundary. Current whole-caller ancestry and an actual
entrywise-error interface there remain open. Prime existence and a practical
cutoff are not reproved. These are appropriate limitations, not hidden premises.

## Separate bounded computation

`independent_check.py` imports no author or predecessor executable. Its
matrix representation uses exact rational `q_i^(x_i-y_i)^2 v_i^(x_i-y_i)`
entries, distinct from the author's rational logarithmic exponent engine.
It tests every vertex permutation without a coordinate or metric prefilter
and compares the complete group with a separately constructed signed-axis
formula. Thirteen fixtures inspect **888,560 permutations**, including two
complete nine-vertex searches. They cover equal physical sides with unequal
cardinalities, repeated widths, coincident axis/diagonal lengths, opposite
shifts, mixed classes and odd fixed-point counts. Separate rational Gaussian
elimination and complete six-vertex enumeration check the inverse claim.

Three additional fine-rounding fixtures use exact rational nearest-dyadic
rounding. A rational lower bound on the theorem's logarithmic width gap
follows from `|log q_i-log q_j| >= |q_i-q_j|/max q`; no floating tolerance or
unproved numerical logarithm enters the guard. Eight semantic controls pass,
including coarse rounding that merges axis levels, tiny-shift reflections,
unequal small diagonal errors destroying every nonidentity symmetry,
equal-width order-four symmetry, invalid domains and the square-hull midpoint.
An exact `(p,r,t,s)=(2,64,(64,32),(59,29))` source-format witness checks the
sharp broad integer gap and strict narrow gap. This is finite corroboration;
the uniform conclusions rest on the written proof.

The author's exponential interval routine was read after the separate checker
was complete: its positive Taylor sum through degree 128 and tail majorant
starting at degree 129 are valid on its declared argument interval. Its
verified common rounding decisions and perturbation guards are conservative.
The author's full verifier was not rerun as part of this independent check.

## Reproduction and freeze

Both commands passed and emitted byte-identical JSON:

```sh
python3.12 -I -W error -B independent_check.py /path/to/heterogeneous-gaussian-symmetries
python3.12 -I -W error -O -B independent_check.py /path/to/heterogeneous-gaussian-symmetries
```

The script prints its receipt and makes no writes. When copied into the
reviewed package it defaults to its own directory, so the path argument is
optional. `RESULT.json` is the saved normal receipt, also matched by the
optimized execution. `FREEZE.json` records final artifact hashes.

Prepared for @CubeJerry by the analytic-recovery worker with substantial
OpenAI assistance. Construction and proof credit remains with the
heterogeneous package authors, the orchestrator's seed argument and all
predecessors cited in that package. This supplementary review is not a
separate research-paper contribution.
