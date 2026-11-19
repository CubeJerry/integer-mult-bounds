# Donor coordinate mixing cannot repair the frozen triangle middle cuts

## Result and scope

Freeze the S026 native triangle's five-class GF(32) source maps, actual
Vandermonde H arrays, and original H-to-D and D-to-K-to-F flags. Its donors
are 29, 36 and 77, and its receivers are 10, 33, 80 and 95. The decompressed
source witness has SHA-256
`362a7ea7798acae4c9d92d2035f41e016aae9d9f8af8a127c6bfd359026410af`.
One independent stripe has a 240-dimensional bank at each donor and one
field symbol per physical H-to-D or D-to-K flag. The frozen coefficient
construction is a source-only fragment, not an admitted full supplier.

**Theorem.** For every positive number rho of independent stripes, no
invertible change of the original coordinates at each donor can make this
source implement the sum of the three original donor banks through the
retained downstream capacities at all four receivers. The coordinate
changes may differ between donors, mix all five classes, and mix all rho
stripes. The theorem allows arbitrary deterministic downstream processing.
It is already false on the jointly required receiver set {33,80,95}.

The conclusion holds for linear coordinate changes over any extension of
GF(32). It also holds for arbitrary binary linear coordinate changes after
expanding the field representation, including arbitrary positive whole-record
body width. It does not exclude changing the actual source quotient spaces,
changing the H port arrays, changing physical routes, or admitting additional
informative return data. This is a fixed-source coordinate-change obstruction,
not a lower bound for every coupled source.

## 1. The required donor lift at a middle chart

Write F_(c,j,H) for the frozen 3-by-48 source matrix of class c and donor j
on plane H. At receiver i, its sixteen visible H matrices stack to an
invertible 48-by-48 matrix M_(c,i,j). Write A_(c,i,H,j) for the invertible
3-by-3 minor of the actual V9 array on the three visible ports and that
donor's three source columns. The contribution to the desired donor identity
from the physical H ports is therefore uniquely

    L_(c,i,H,j) = (the H block of M_(c,i,j)^(-1)) A_(c,i,H,j)^(-1).

Embed the columns in their actual 48-coordinate class block within F^240.
For a D chart contained in F_i and containing donor j, exactly four H
through j are contained in D. They contribute four actual port columns.
Let S_(i,D,j) be their four-dimensional span in F^240.

Their independence needs no generic assumption: all 240 visible port
columns for one donor are the columns of an invertible matrix obtained by
the five inverse source stacks followed by invertible local minors.
Consequently every four-element subset at one D is independent.

Let the donor source be changed from F_j X_j to F_j P_j X_j, with P_j
invertible, and put Q_j=P_j^(-1). The unique inverse lift is then Q_j L.
Thus the middle contribution subspace becomes Q_j S_(i,D,j). A change of
output coordinates multiplies both donor spaces by the same invertible map
and does not affect the following necessary equality.

## 2. The physical four-symbol cut forces equality

For a fixed receiver, the aggregate visible H-port boundary of the original
three-donor source is surjective: its dimensions are 144 to 135 in every
class, hence 720 to 675 across the five classes. Composing the three input
banks with invertible P_j preserves this surjectivity. The visible boundary
variables at distinct D charts are therefore independent coordinates.

If the changed source admits the desired sum at receiver i, that sum is a
unique function of the full visible boundary. Its restriction obtained by
varying one donor alone gives exactly the inverse lifts in Section 1.
Because the full boundary map and the desired sum are linear, the unique
decoder is linear even when a proposed downstream implementation is not.

Only four actual D-to-K flags can reach receiver i. For rho stripes their
total alphabet has size |F|^(4rho). All outside D boundary values can be
held fixed. Thus the image of the unique contribution from D has dimension
at most 4rho. It contains both required donor spaces, each of dimension
4rho. Hence every active donor pair in D must satisfy

    Q_j (S_(i,D,j) tensor F^rho)
      = Q_k (S_(i,D,k) tensor F^rho).                 (1)

This argument includes stationary caches, nonlinear recoding and mixing
among receiver-bound flags. An early closure at Hub is not a proper path
back into the receiver. An additional informative descent is outside the
retained interface. No assertion about a nonlinear ground-preloaded full
programme is made: this is the explicitly fixed proper sum computation.

## 3. An indexed subspace-rank invariant

If (1) holds for an indexed collection C of shared receiver/D cuts, summing
the corresponding spaces gives

    Q_j sum_(a in C) S_(a,j) = Q_k sum_(a in C) S_(a,k).

Invertibility preserves dimension. Therefore

    dim sum_(a in C) S_(a,j) = dim sum_(a in C) S_(a,k)             (2)

is necessary. This tests a common donor change of coordinates across all
receivers; allowing a separate change at every receiver/donor incidence
would discard the original-source interface and does not satisfy (2).

For donors j=29 and k=36, use these eighteen actual cuts:

| Receiver | Middle charts D |
| --- | --- |
| 33 | 97, 101, 395, 473, 771 |
| 80 | 88, 94, 97, 278, 573, 640, 726 |
| 95 | 82, 94, 101, 573, 726, 771 |

The 72 port lift columns on the donor-29 side have rank **72** over GF(32).
The corresponding 72 columns on the donor-36 side have rank **71**.
These ranks contradict (2). They are exact Gaussian-elimination results
on the frozen coefficient witness, not search-based infeasibility claims.
The cut set was found by deleting entries from the larger invariant witness;
its minimality is neither needed nor asserted globally.

A larger audit uses all sixty cuts shared by this donor pair across the four
receivers. The ranks are respectively **232** and **223**. Restricting to
all forty-five cuts at receivers 33,80,95 gives **180** and **178**.
These larger values corroborate the small witness but are not additional
necessary premises.

Independent repetition tensors the spaces with F^rho and multiplies every
dimension by rho. Field extension leaves the original ranks unchanged.
Binary expansion of GF(32) multiplies dimensions by five; tensoring an
arbitrary positive body width multiplies them again. Arbitrary invertible
binary donor gauges preserve those binary dimensions. Thus the 72-to-71
contradiction persists under each stated extension, without assuming that
the gauges preserve the five original classes.

## 4. Verification and interpretation

The accompanying checker reads only authenticated layout, partition and
coefficient data, reconstructs the actual minors and inverse source stacks,
and recomputes each of the eighteen four-dimensional donor spaces. It checks
the incidence, the four actual right flags at every witness cut, the two
72-column ranks, and the larger audit ranks. A sparse exact null relation on
the donor-36 columns is emitted and checked. Removing one of its nonzero
terms is a rejecting control; replacing the deficient side by the donor-29
side removes this particular rank obstruction, as a scope control.

This closes the attempt to rescue the frozen source by a donor-dependent
mixing of classes or copies. It does not close the constructive question.
A revised source must change its indexed receiver/D subspace arrangement,
not only its coordinates. The next positive target is to construct common
middle subspaces together with the H source quotients and right-K packet
factorizations, with actual two-wave timing and ordinary costs included.

No new complete kappa, complete BIT supplier, or foundational discharge is
claimed. Credit @CubeJerry, the retained native and balanced-atlas authors,
S026 Worker A's source witness, S026 Worker B's middle-cut proof, and S027
Worker A's indexed-rank obstruction, with substantial OpenAI assistance.

## Reproduction

    python3 -B check.py --repo REPOSITORY --triangle-author TRIANGLE_AUTHOR --out OUTPUT

The triangle witness remains an explicit pinned dependency even if it is
integrated at a different programme path. No search optimizer is required.
