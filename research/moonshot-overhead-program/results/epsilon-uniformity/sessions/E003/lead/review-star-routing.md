# Lead review of the exposed star-routing mechanism

Disposition: **accept A's source-specific normal form and monomial-sum
obstruction, and B's support-monotone shared-sum obstruction**, with their
separate models and limits. Neither supplies a new multiplier bound or
a physical routing lower bound.

Read in full:

* `../route-a/ROUTING-STAR-TRANSPOSE-NORMAL-FORM.md` and its verifier;
* `../route-b/STAR-SHARED-SUM-OBSTRUCTION.md`;
* the source kernel's routing block and complete shared-endpoint argument,
  rechecked against the previously read full primary file.

## Exact source identity

For the binary pair kernel C, spectral conjugation of its sign multiplier
proves C^2=I. Its ordinary kernel has denominator 2^f, not the pair alphabet
size 2^(2f). Swapping the auxiliary pair with pair j conjugates C_0 to C_j.
Consequently `P_j C_j C_0=C_0 P_j C_0` follows by multiplication of
actual operators; both common endpoints are independent of j.

For an arbitrary orthogonal pair of norm-one label directions, their span
is a nondegenerate two-plane. Its perpendicular complement permits paired
dual auxiliary bases. Changing to these bases is independent of j, and the
remaining pair transforms can be absorbed into an auxiliary endpoint.
This proves the general individual-pair form. It does not establish that
one such gauge works simultaneously for every label pair in a rectangle,
or that separately executing all pairs preserves the source incidence bill.

The numerator identity and source ordering passed an independent replay:
4,368 spectral entries, 4,368 involution entries, 2,242,816 nonzero kernel
entries and 13,456 complete-array output coordinates, with adverse controls.
The receipt is `star-routing-replay.json`. The universal argument above is
separate from these finite checks; the replay does not execute tape movement.

## Representation and shared arithmetic

A's support witness uses only two alphabet symbols. The output address
`(a,b,...,b)` has m distinct input neighbors under hub swaps, so any sum
of matrices with at most one nonzero per row needs at least m terms.
Nonzero signed coefficients cannot cancel because those inputs differ.
Monomial gauges preserve this row-support constraint. This check is sound
even when m exceeds the alphabet size.

B's stronger circuit argument uses a different sector: all m+1 register
symbols are distinct. Two hub-swap neighborhoods intersect in at most one
point, because a product of two distinct hub transpositions is a uniquely
oriented three-cycle. Faithfulness on an injective tuple is essential.
A gate with support at least two cannot feed two of these outputs in a
support-monotone circuit. Each m-variable output requires m-1 binary sums
by the connected fan-in graph count. The resulting exact lower bound is
`(m-1)(Q)_(m+1)`, not `(m-1)Q^(m+1)` without an alphabet guard.

The union bound gives at least half the full volume when Q>=m(m+1).
With Q=2^(2f), the stated sufficient condition
`f>=ceil(log2(m+1))` is valid. Repeated symbols are correctly excluded
from the unique-three-cycle argument; the finite receipt includes a
counterexample to extending it indiscriminately.

## What remains open

The circuit count concerns scalar additions at an exposed middle cut.
It does not multiply those additions by an interchange cost, and does
not require m separate physical passes. Shared movement could coexist
with m scalar additions per record. Dense endpoint transforms can also
change supports, and the full label identity uses signed cancellations
between rectangles. No lower bounds may be summed through those boundaries
without new hypotheses. B's coupled Walsh certificate retains its explicit
normalized routing toll rather than deriving it from these two results.

The surviving constructive task is therefore concrete: route the weighted
hub-swap terms together with a fixed number of payload arrays, or use a
cancellation-based transform whose endpoint and inverse costs are charged.
Any individual-pair improvement must lift to complete free rectangles.

Review type: AI-assisted independent mathematical/source check and the
specified finite replay. No general circuit lower bound, formal refinement,
full multiplier execution or human refereeing is claimed.
