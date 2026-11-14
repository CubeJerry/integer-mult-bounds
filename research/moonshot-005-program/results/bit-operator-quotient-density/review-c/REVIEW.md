# Independent review: proportional canonical quotient gap

**Accepted within the stated scope. No physical source, strict supplier,
foundational discharge, or complete kappa follows.**

The reviewed author proof is `operator-quotient-density/author/PROOF.md`.
Its exact SHA256 is recorded in RESULT.json. The review was performed directly
from that proof and its stated mathematical dependencies. The checker imports
neither the author's verifier nor the companion packet-width verifier, and
independently rebuilds its native and field examples.

## Universal argument checked

1. **Whole-width injection is valid.** A positive-saving row has at least
   one entire permitted contact block equal to zero, because its support is
   at most 52 and every canonical foreign degree is at least 55. A vector
   in the kernel of its canonical quotient map gives a canonical row that
   vanishes at all forbidden coordinates. The one-dimensional scalar local
   kernel, tensored with the value space, makes that row `K_i` times one
   vector. Its identity diagonal fixes the vector to the input coefficient;
   the erased block then makes it zero. No foreign block inversion occurs.

2. **A shared quotient vector suffices even when full quotient images differ.**
   For a nonzero shared class `q`, each active row has its own nonzero
   preimage `u_i`. The proof does not assume those preimages coincide.
   Their representatives differ by canonical block rows. The earlier
   rank-seven pair restriction and three-normal gluing argument is linear
   in each of the `V` coordinates, giving one vector-valued representative
   `g`. Its support is contained in every relevant closed receiver support.
   The identity diagonal supplies exactly equation (3), with no exchange
   of matrix multiplication order.

3. **The full-block implication in equation (3) is sound.** For a receiver
   outside `support(g)`, and a canonical contact outside that support, the
   projected coefficient is `u_i`, which is nonzero. Consequently the
   ORIGINAL coefficient block cannot be zero. This is the required bridge
   from the vector-valued equation to the original block-support statistic.
   It does not attempt to infer block support from rank or to equate the
   projected row with the whole row.

4. **The old geometric envelope applies.** The support of `g` is a subset
   of the same native root lines. Receiver roots outside that support are
   perpendicular to it, and receiver roots inside it are perpendicular to
   its other members. The cardinality/rank envelope and its two finite
   geometric refinements therefore depend on the same sets as before.
   Matrix/vector values do not enter those counts. Sets of at most three
   receivers save at most six, so the rank-three gluing exception is handled.
   The pointwise weighted multiplicity bound seventeen follows.

5. **The proportional dimension deduction is exact.** For `t` image
   subspaces of dimension `V` in dimension `d`, codimension subadditivity
   gives intersection dimension at least `V-(t-1)(d-V)`. Weight above
   seventeen forces that intersection to vanish. Taking a first set whose
   integer weight exceeds seventeen uses at most eighteen rows and gives
   `d >= V+ceil(V/17)`.

6. **The double-saving refinement has sufficient rows.** If `b<=8`, the
   total-savings premise `S>=28` leaves at least `28-2b` single-saving rows,
   more than the `18-2b` selected. The chosen size is `18-b`. If `b>=9`,
   choose nine double-saving rows. This gives the denominator
   `17-min(b,9)` exactly, with integer rounding in the stated direction.

7. **The finite-field corollary is a valid separate consequence.** Each
   image has `q^V-1` nonzero elements; summing weights over their incidences
   and applying the pointwise bound gives equation (5). The author does not
   incorrectly use this finite-field count as the all-field proof.

8. **Abstract sharpness is valid and explicitly limited.** The GF(32)
   hyperplane arrangement uses twenty-eight distinct evaluation points and
   polynomials of degree at most seventeen. A nonzero coefficient vector
   belongs to at most seventeen hyperplanes by the elementary root bound.
   Thus `V=17,d=18,S=28` attains the abstract gap. The tensor version has
   the same property because at least one component polynomial is nonzero.
   This arrangement is not asserted to be a native fitting or source.

No error requiring a change to the author proof was found.

## Independent exact checks

`check.py` reconstructs the native graph from authenticated rational roots
and verifies all 111 local rank-eight and 6,105 pair rank-seven restrictions.
It independently derives quotient images by reduction modulo the canonical
tensor code, enumerates nonzero vectors in each active image, and directly
checks weighted incidence for two actual native fitting families at widths
one, two and three:

- The sharp seventeen-savings fitting has `d=V`, showing why the theorem
  requires `S>17` rather than `S>=17`.
- The eight-coordinate fitting has savings 39 and `ell=183`. It checks a
  genuinely larger collection of quotient images and the full-block support
  count. It is an algebraic fitting, not a physical source.

The new GF(32) implementation uses the polynomial `x^5+x^2+1`, independently
checks all nonzero inverses and every associativity/distributivity triple,
checks twenty-eight representative seventeen/eighteen-row Vandermonde rank
cases, and constructs a polynomial with exactly seventeen specified roots
among the twenty-eight points. It also checks a width-two tensor lift. The
universal polynomial-root argument, not those selected matrix cases, proves
the arrangement's pointwise bound.

The checker verifies weighted selections for every possible number of
double-saving rows relevant to the `S=28` threshold, ceiling arithmetic at
several boundary widths, a below-threshold positive common intersection,
an equality case with zero intersection, and pairwise nonzero intersections
with zero total intersection. Thus it rejects these proposed overclaims:

- Replacing `S>17` by `S>=17`.
- Deducing `d>=2V` from the abstract pointwise-overlap premise alone.
- Replacing a common-intersection requirement by pairwise intersections.
- Rounding the proportional quotient threshold downward.

The independently reviewed earlier exceptional root geometry is checked by
exact SHA256 and reused. This review does not claim a fresh full replay of
its 74,396-flat census. That finite source evidence and its universal
support argument remain explicit dependencies.

## Reproduction and scope

```bash
python3 -I -B research/moonshot-005-program/results/bit-operator-quotient-density/review-c/check.py \
  --proof research/moonshot-005-program/results/bit-operator-quotient-density/author/PROOF.md \
  --native research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz \
  --programme research/moonshot-005-program \
  --output /tmp/operator-quotient-density-review
```

Expected status: `PASS_INDEPENDENT_OPERATOR_QUOTIENT_DENSITY_REVIEW`.
The normal and optimized Python runs produce identical JSON.

The physical corollary depends on the separately admitted all-route
`ell<=194` result and its retained complete caller, linear source model,
whole widths, chronology and actual paid operations. No cost term is removed
by this code theorem. In particular, the proof bounds the canonical quotient
of a fitting or a history supplying it; it does not equate that quotient
with terminal code rank, packet count, or physical availability.

Review by Worker C for @CubeJerry with OpenAI assistance. Credit the author,
the companion injection theorem and the named source/geometric/all-route
predecessors. This is independent mathematical and computational review by
another agent, not independent human review or formal-kernel acceptance.
