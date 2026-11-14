# A point-retained handoff needs more than twenty supported innovations

**Author theorem; independent review pending. No complete supplier or new
kappa.** This is a continuation theorem for an actual source interface, not a
lower bound on arbitrary BIT algorithms. Its proof is valid over every field
of characteristic two and every positive block width. The source-specific
finite premises are independently reconstructed by `verify.py` directly from
the pinned rational native word.

## 1. Precisely declared interface

There are 111 original input vectors `x_i` and 111 public receiver records,
whose required final values are `y_i+x_i`. The real source line is `L_i`; the
final receiver facet is `F_i=L_i^perp`. All these lines, and hence all final
facets, are distinct. Let `K_ii=1`, and, for `i!=j`, let `K_ij=1` exactly when
`L_j` is contained in `F_i`. Let `C=row(K)`, extended to the value field and
tensored with the block space as appropriate. For a set of source indices
`T`, write

    W_T = (C + span{e_t : t in T}) tensor k^V.

Start from any chronological handoff satisfying the following conditions.

1. Every public receiver's current X-coefficient rows belong to `W_T`.
   Its Y-coefficients can be arbitrary. In particular a completed pivot
   receiver `y_0+x_0` is allowed when `0 in T`.
2. Each public receiver follows an actual nested, monotone upward real-chart
   trajectory to its specified final facet. Whole chart/value relabellings
   merely relabel physical trajectories. Arbitrary cocharted linear receiver
   interactions and arbitrary, possibly singular and noncommuting, block
   maps are permitted.
3. The only information reads outside `W_T` available to a receiver are
   stationary pure copies of `x_j` at the original source line `L_j`.
   Every read is cocharted: in particular a point-copy read occurs only when
   the receiver itself is at `L_j`, not at an arbitrary chart containing it.
   Multiple copies or linear transforms of the same input at that same line
   do not change the statement. Every other non-receiver value read has its
   actual X-coefficient rows in `W_T` at the time of the read.

The last condition is about actual values, not packet names or formal input
supports before recoding. Those other records may contain original Y terms,
may interact with receivers, and may move on arbitrary legal routes. Their
actual X histories must continue to satisfy the stated condition. A new
stationary mixed bank with an X row outside `W_T`, a public downward turn,
or richer moving history is outside the theorem. In a retained-point prefix,
original X left at Hub cannot be read by monotone receivers ending at proper
facets; lowering those originals would require a new information read checked
against condition 3.

**Theorem.** Under this interface, `|T|<=20` is incompatible with completion of
all 111 outputs. Thus at least 21 supported source directions are necessary
if every non-point information value remains inside a canonical-plus-supported
history space of this form. This is not a statement that 21 suffice, nor a
rank-only restriction on arbitrary history spaces.

## 2. Two finite native facts with uniform mathematical consequences

For each receiver define

    S_i = {j!=i : K_ij=1},
    N_i = {j!=i : K_ij=0},
    D_i = {c in C : c_i=0},
    rho_i = min_{0!=c in D_i} |supp(c) intersect N_i|,
    g_i = min_{h!=i} |S_i \ S_h| - 1.

The authenticated native has binary code dimension nine. Enumerating its
512 words gives the distance census

| rho | 18 | 19 | 20 | 21 | 22 | 23 |
|---|---:|---:|---:|---:|---:|---:|
| receivers | 7 | 24 | 52 | 16 | 11 | 1 |

Direct real-orthogonality computation gives

| g | 20 | 21 | 22 | 23 | 24 | 25 |
|---|---:|---:|---:|---:|---:|---:|
| receivers | 4 | 26 | 47 | 25 | 8 | 1 |

Exactly 24 receivers satisfy both `rho_i>=21` and `g_i>=21`:

    0,9,15,16,17,20,29,36,37,44,46,47,
    50,54,60,63,65,70,77,83,90,92,107,109.

Their cardinality exceeds 20, so for every set `T` of at most 20 indices
there is a receiver `i` in this list outside `T`.

The finite binary distances persist over every characteristic-two extension
field. Express the finitely many coefficients of a field-valued codeword in
an F2-linearly independent basis. Its support is the union of the supports of
the resulting binary constituent words. If its coordinate `i` is zero, each
constituent also has coordinate `i` zero. A nonzero constituent therefore has
at least `rho_i` noncontact coordinates. Applying this argument to a nonzero
internal coordinate of an operator-valued row gives the same source-block
support bound. This argument uses neither matrix commutation nor inversion.

## 3. Separate global and point-local X contributions

Induct through the chronological operations on public receivers, separating
their X rows into `A+B`. Initially `A` belongs to `W_T` and `B=0`. At a read
whose actual X row lies in `W_T`, put the entire injected X row in `A`.
At a source-line point-copy read, put that row in `B`. Receiver-to-receiver
maps apply to these two components separately. Thus each final `A_i` remains
in `W_T`, while every contribution to `B_i` originates at an actual source
line and thereafter follows only upward public-receiver trajectories.

This induction uses actual non-receiver X rows at their read times. It does
not require those records to be pure X or independent of earlier receiver
values; it does require their actual rows to remain in `W_T`. Hence arbitrary
Y-bearing records do not silently become a free local-information relay.

Write `A_i=A_i^C+E_i` with `A_i^C` in the canonical tensor code and `E_i`
supported on `T`. Locality implies `B_ij=0` when `L_j` is not contained in
`F_i`, including `j=i`. For the receiver `i` chosen in Section 2, completion
forces `(A_i^C)_i=I` and `(A_i^C)_j=0` for `j in N_i\T`. Thus

    A_i^C - K_i tensor I

is a canonical-code row with zero own block and all noncontact support inside
`T`. Since `rho_i>|T|`, the uniform distance statement makes this difference
zero. Therefore the total canonical contribution at this receiver is exactly
`K_i tensor I`, even with arbitrary decoding, timing, block maps, and Y terms.

## 4. The last public interaction and a one-point suffix

Follow the physical receiver trajectory ending at `F_i`. If it has a last
incoming interaction with another public receiver, choose one other input
trajectory, which ends at `F_h`, `h!=i`. At the interaction chart `Q`, both
trajectories have monotone continuations, so `Q` is contained in `F_i` and
`F_h`. Every point-local contribution already present in any participating
record has an origin line contained in `Q`. In particular all such B terms
are supported on `S_h`.

After this last incoming public interaction, the local source-point reads on
the i-trajectory lie on a single nested chain. Distinct source lines are
incomparable; such a chain can meet at most one of them. Consequently

    |S_i \ supp(B_i)| >= |S_i \ S_h| - 1 >= g_i >= 21.

Self operations, outgoing reads, and further reads of W_T-valued records
cannot enlarge the point-local source support. If there is no incoming public
interaction, the entire B support has at most one source port. The canonical
foreign degrees are at least 55, so that case has an even larger gap.

At most 20 of the missing contacts lie in `T`. Choose a missing contact
`j` outside `T`. Then `E_ij=B_ij=0`, whereas the canonical contribution is
`K_ij I=I`. The required final X coefficient at `(i,j)` is zero. This is a
contradiction, proving the theorem.

The proof grants all allowed local operations, every W_T packet read, and all
ordinary/owned/precision/compiler service for free. It therefore supplies no
new numerical tariff or supplier exponent.

## 5. Application and exact remaining escape

The published retained pivot starts with current pure modes in `C+<e_0>`,
111 stationary source-line copies, all original X at Hub, one finished receiver
and 110 ground receivers. Its static canonical continuation satisfies this
theorem's handoff premises and cannot complete the source.

A distinct, uncommitted S011 WIP augments that handoff by the two actual
candidate bank rows supported on

    B1={12,48,77,84,91,99},
    B2={13,47,80,87,88,96}.

The WIP is not admitted here. Its exact observed bytes are recorded separately
in `WIP-PINS.json`, and its reported finite foreign-support charge 192 is not
a decoder certificate. Conditional on a handoff of the declared form, its
entire proposed static history is contained in `W_T0`, where

    T0={0} union B1 union B2, |T0|=13.

The theorem then excludes even an enlargement by seven arbitrary extra
coordinate directions. This is a source-location obstruction beyond the
arrival-charge screen. Copies of those same bank rows retained at their proper
birth charts still belong to `W_T0` and do not change the proof.

An actual continuation must break at least one stated premise. Concrete
possibilities are a new stationary mixed proper-chart bank outside the space,
moving records whose real X histories use more than this supported innovation
set or a non-coordinate quotient, or a paid public downward turn. Each needs
its own source word, arbitrary-Y cancellation, endpoint restoration, and full
invoice. A finite search failure is not being used to rule out those mechanisms.

## 6. Negative controls and provenance

The verifier exhibits a nonzero diagonal-zero codeword whose noncontact
support has size rho_i. Deleting exactly that support defeats the strict
distance premise; the strict inequality is essential. It also constructs
two different source lines in one receiver facet: a proper rank-two mixed
bank can contain both, while a single monotone trajectory cannot directly
read both stationary line copies. This distinguishes a genuinely new mixed
bank from an unpriced union of point reads. A downward return to zero permits
two line visits and demonstrates why public monotonicity is substantive.

Native source SHA256:
`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.
Baseline programme commit:
`a22f6932c7a57328f92bcf7a6f373c1433ec52f8`.

Credit the prior canonical-code puncturing and last-public-interaction proofs
in `bit-code-decoder-robustness`, including its pigeonhole strengthening;
the native BIT authors; S011's retained canonical pivot and point retention;
@CubeJerry; and OpenAI assistance. The new contribution is the exact
point-retained handoff interface, its one-point suffix theorem, the 24-role
distance/geometry witness yielding a twenty-port exclusion, and the explicit
continuation consequence for bank-supported innovations. Both strict
suppliers and all five foundational assumptions remain open.
