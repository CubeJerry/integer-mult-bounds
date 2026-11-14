## What changed and why it matters

The preceding Gaussian tensor lower bounds fix a lexicographic coordinate
order. This package constructs an arbitrary simultaneous row/column order
with a strictly smaller ordinary Toeplitz generator bound in a homogeneous
regime, and records the costs that still prevent a transform/runtime claim.

For an even-dimensional centrosymmetric factor B, a power-of-two number ell
of equal factors, and any spectator matrix C, the tensor `B^ell tensor C`
has an explicit orbit ordering with ordinary Stein rank at most `T/ell`.
The same order gives that bound for its inverse when it exists. The proof
provides concrete ordinary lower-times-upper Toeplitz generators, not just
an existence rank factorization. Common structure-preserving factor rounding
retains the symmetry; inverse nonsingularity remains a separate premise.

For `B_ij=q^((i-j)^2)`, `0<q<1`, take ell as the largest power of two at most
d. The lexicographic minimum is `2T/n`; the new upper bound is `T/ell`, an
improvement factor at least `2ell/n` when this exceeds one. For n=2,d=4,
the displayed 16-label orbit order has exact forward and inverse rank 4 at
q=1/2, compared with lexicographic rank 16.

## Novelty and exact provenance

Canonical base: `e54523517d0f03e58352e647c403a5af3e525a57`. SOURCES.json
contains six exact canonical Git-blob/SHA256 pins. The proof restates its
algebra, and the verifier has no external runtime inputs.

This addresses the arbitrary-coordinate-order question left by the
[rank package at 326844a](https://github.com/CubeJerry/integer-mult-bounds/tree/326844a3e0c570fdafa4f3737095cd37154743a6/research/tensor-gaussian-displacement-rank)
and [rounding-margin package at 575491d](https://github.com/CubeJerry/integer-mult-bounds/tree/575491d5fc353eac26010e45e9ced60fc9870017/research/gaussian-generator-rounding-margin).
It changes the shift through a permutation; it does not contradict either
fixed-order theorem.

The complemented-rotation automorphism and binary orbit-length fact are
credited to Gregor, Merino and Mütze,
[*The Hamilton Compression of Highly Symmetric Graphs*](https://doi.org/10.1007/s00026-023-00674-y),
section 3.3, equation (13), Lemma 3.4. They are not claimed new. The scoped
contribution is the explicit ordinary-generator consequence, even-n/spectator
extension, exact controls and paid cost/precision boundary. Preserve the
originating source authors' credit, including Vlado Vojdanovski's
capped-phase-fusion work. No literature-wide priority claim is made.

## Reproduction and executed checks

```sh
python3 -I -W error -B research/gaussian-orbit-generator-order/verify.py
python3 -I -O -W error -B research/gaussian-orbit-generator-order/verify.py
python3 scripts/research_package.py --package research/gaussian-orbit-generator-order --check-only
python3 scripts/research_package.py --package research/gaussian-orbit-generator-order
```

Both standalone runs passed with identical JSON: 15 rational fixtures,
30 forward/inverse targets, 22 literal ordinary Toeplitz reconstructions,
and eight negative controls. The checks use independent direct orbit powers,
literal coordinate kernels, rational elimination, literal shift products and
triangular Toeplitz multiplication. Unsupported odd dimensions, nonpower
cycle counts, broken factor/shift symmetry, reversed gauge orientation,
unstructured perturbation, singular inversion and a forged rank bound are
detected under optimized Python as well. Written proofs supply the universal
claims; finite checks do not establish a global minimum.

## Costs, limitations and open obligations

Explicitly materializing the displayed generators takes `T^2/ell` scalar
slots and loses to direct axis application for fixed n as d grows. The proof
charges uniform order generation, fixed-tape sorting in both directions,
generator access, accumulation and restoration; it does not admit a native
repository controller or a complete three-transform recurrence.

Shifted kernels have an exact paid diagonal conjugation, with
`log cond_2(D)=sum_i (n_i-1)|log v_i|`. A black-box normwise conversion must
charge that precision. The package gives a narrowly scoped fixed-shift cap
obstruction; it does not silently undo the retained gauge-free construction
or claim the shifted matrix itself has low ordinary rank.

The all-order minimum, fast implicit generator use, and a stable actual-source
caller remain open. **No new kappa:** selected #7000 remains
`363005817/100000000000`, conditional on all five inherited assumptions.

Prepared for @CubeJerry with substantial OpenAI ChatGPT assistance. The
orchestrator proposed the orbit application and scoped precision obstruction;
the worker independently derived and checked the proof and costs, identified
the classical overlap and packaged the result. New files are Apache-2.0.
