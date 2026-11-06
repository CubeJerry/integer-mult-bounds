# Independent open-path threshold and connector audit

Prepared for @CubeJerry with substantial OpenAI Codex assistance. Apache-2.0.
This is a separate AI mathematical/implementation review, not independent human
or proof-kernel acceptance. No predecessor full scientific replay is claimed.

## Quantified claim checked

Let P(k) minimize the largest coordinate-flip count over finite single-edge
walks of the binary k-cube starting at zero and visiting every vertex. Closure
is not required. One may require distinct endpoints without changing the upper
bounds below, since deleting an edge of a Hamilton cycle gives such a path.
The finite certificates are Hamilton paths, which are a restricted subclass of
these walks but attain the same universal lower bound.

Every covering walk has at least 2^k-1 edges, so
P(k) >= ceil((2^k-1)/k). With 2^(k-1)=qk+r and k>=2:

- If r=0, this lower bound and the balanced-cycle upper bound are both 2q.
- If r>0 and 2r-1>k, both bounds are 2q+2.
- Otherwise P(k) belongs to {2q+1,2q+2}.
- If r=1, a balanced cycle has precisely one coordinate of count 2q+2.
  Delete an edge in that coordinate, rotate/translate the path to begin at zero,
  and obtain max count 2q+1. Thus P(k)=2q+1.
- Every odd prime k has r=1 by Fermat's theorem.

The numerical certificates at k=6,9,10 attain the lower bound 11,57,103.
Together with the exact cases above this settles all k from 1 through 13;
k=1 is handled separately with P(1)=1. The physical ring interface requires
characteristic at least two, so k=1 does not provide a characteristic-one ring.
No universal attainability for every k is asserted.

## Positive-source conversion checked

For an arbitrary covering path g_t, let U(t) and D(t) count its upward and
downward coordinate flips. Let f_j be total flips and choose characteristic
c >= max f_j, c>=2. Take the source word consisting of all upward labels,
then c-f_j copies of each j, then downward labels in reverse order. Each
source is called exactly c times. At actual boundaries |U(t)| and kc-|D(t)|,
the source-prefix counts are U(t) and c*1-D(t). These boundaries are ordered:
the first lies in the initial upward block and the second in the final reverse
block. Their sum reduces to g_t modulo c. This argument never uses closure.

For each nonzero output mask, use these two reads and c-2 reads at boundary
zero. The arbitrary borrowed connector baseline appears c times and vanishes;
the requested source coefficients appear once, the other coefficients zero.
All source fields remain unchanged and the connector is restored. This proof
is valid over every nonzero unital ring of characteristic c, with compatible
linear maps A_m and B_j. It does not commute A_m with B_j: the formal terms
are A_m z0 and A_m B_j x_j throughout.

## Independent executable check

`independent.py` does not import the primary construction, test code, or verifier.
It constructs an actual source-call list from the submitted transition sequence,
executes that word and all c output calls over formal coefficient rows, and
checks every output and the dirty connector. Package inputs (the three entries of `WITNESSES.json`):

- dimension 6: 63 masks, 759 complete calls, 504 coefficients.
- dimension 9: 511 masks, 29,640 calls, 5,621 coefficients.
- dimension 10: 1,023 masks, 106,399 calls, 12,276 coefficients.

Normal and optimized Python runs both passed. Eleven mutations per fixture
rejected: invalid dimension, invalid axis, repeated vertex, changed flip count,
insufficient declared characteristic, missing source call, missing output
padding read, missing output, invalid read boundary, shifted actual read, and
moving a dirty-cancellation read to a nonzero prefix while retaining call count.
These 33 finite controls concern actual semantic obligations. The written
counting/split proofs establish the unbounded statements, not the finite tests.

The auxiliary witness search also used Pósa rotations, like the primary search;
it is not a distinct mathematical search mechanism. Only the independently
written formal action checker and mathematical review are independent evidence.

## Literature and limits

Classical balanced cyclic Gray-code existence is inherited, not newly proved.
The primary Bhat--Savage cyclic theorem therefore must not be silently used to
assert an arbitrary-dimension well-balanced path theorem. No claim of present
literature completeness or new Gray-code existence beyond the cited theorem
and supplied finite witnesses is made.

The connector improvement partly answers the open-path threshold question of
CrocSwap/integer-mult-bounds#6568 at its pinned head
0c3ff8236c103c5960ef15c45b26432ad1603f8d. It changes neither selected kappa nor
any physical caller bill. The upstream I/P/D/call invoice and restoration,
layout, storage, precision, native, compiler and outer obligations remain.
