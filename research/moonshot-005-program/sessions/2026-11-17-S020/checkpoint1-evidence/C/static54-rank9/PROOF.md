# A fourteen-role obstruction fixes the static whole-record count at nine

## Status and exact statement

**Proved for the pinned 54-unknown native-neighbor interface. No new complete kappa.**
Let `U` be the 54 unfinished roles in the S019 masked-Hub word, whose SHA256 is
`f21de38f4a8adc1a55920c16b684285f62607829fe512a0088fe5ecb217fcfdd`.
The other 57 inputs are supplied as known side information. For `i,j in U`,
receiver `i` knows `x_j` precisely when the pinned real native roots are
orthogonal. It demands `x_i`. The source roots have SHA256
`8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`.

For every field `K`, every positive block length `m`, and every linear static
broadcast code for this interface, the total broadcast dimension is **strictly
greater than `8m`**. Consequently at least nine whole records of width `m` are
needed. Over every field of characteristic two, nine whole records suffice,
by the explicit canonical fitting code below. In particular scalar minrank is
exactly nine in characteristic two.

This does **not** prove a vector-linear rank lower bound of `9m`. A code of
dimension between `8m` and `9m` is not excluded. The statement about nine
whole records uses the integer number of width-`m` records. Nor does this
linear theorem assert a lower bound for arbitrary nonlinear codes.

At the actual admitted source cut immediately before operation 1129, a fresh
audit of all 392 live fields proves that their unknown-coordinate dependencies
inside each receiver's facet downset are contained in the same native-neighbor
set. The initial-chart transcript argument therefore implies that every
fixed-schedule linear continuation needs at least **nine future strict owned
downward transfers**. This counts transfers, not distinct owned lifetimes.
One lifetime can make several transfers. The previously admitted nonlinear
eight-lifetime bound remains a separate result.

## 1. The exact fourteen-role certificate

Use the pairwise nonorthogonal frame

    J = (14,18,31,35,55,56,105,109).

Its fitting principal block is the identity. Put

    E = (66,69,70,89,93),
    T = (18,55,56,105,109),
    z = 15.

The exact frame-neighbor sets of the five edge roles are:

| Role | Orthogonal neighbors in J |
|---|---|
| 66 | 55, 109 |
| 69 | 56, 105 |
| 70 | 55, 105 |
| 89 | 18, 109 |
| 93 | 18, 105 |

Their union is precisely `T`. Two distinct roles of `E` either have disjoint
frame-neighbor sets, or share one frame coordinate and are real nonorthogonal.
The six shared-coordinate pairs are

    (66,70), (66,89), (69,70), (69,93), (70,93), (89,93).

Each has nonzero real root dot product. The other four pairs have disjoint
frame-neighbor sets. Finally, `z=15` has frame-neighbor set exactly `T`, and
is nonorthogonal to every role of `E`. The source-derived certificate records
every ordered frame dot product, all these supports, and all five final dot
products. No numerical tolerance is used: the source roots are integers.

## 2. General block-factor lemma

A block fitting matrix `F` has `m by m` blocks, `F_ii=I_m`, and `F_ij=0`
whenever distinct roles `i,j` are not neighbors. A linear code of total
dimension `d` gives a factorization `F=A B` through `K^d`: its broadcast is
`B x`, and its decoding rows are `A`; local side-information terms are moved
to the fitting matrix.

Suppose `d <= 8m`. Since `F_JJ=I_(8m)`, necessarily `d=8m` and the square
matrices `A_J` and `B_J` are inverse. Changing the intermediate basis makes
both frame matrices the standard block identity. For any outside role `i`,
the row `A_i` and column `B_i` now have nonzero coordinate blocks only at
`N(i) intersect J`. This follows respectively from `F_iJ` and `F_Ji`.

Apply this to `E`. Every off-diagonal block in `A_E B_E` is zero. If the two
frame supports are disjoint, the product is zero structurally. If they
intersect, the exact nonorthogonality certificate requires the fitting entry
to be zero. The diagonal blocks are identities. Thus

    A_(E,T) B_(T,E) = I_(5m).

Both factors are square `5m by 5m` matrices, hence invertible. Role `z` is
nonadjacent to all of `E`, while its factor row is supported entirely in `T`.
Therefore

    A_(z,T) B_(T,E) = F_(z,E) = 0,

which forces `A_(z,T)=0`. All other coordinate blocks of `A_z` were already
zero. This contradicts `F_zz=A_z B_z=I_m`. The argument applies to every
field and every positive `m`. It uses no scalar-only endpoint assignment,
positivity, commutation between blocks, or finite-width extrapolation.

## 3. Matching upper bound for the integer whole-record count

Over characteristic two, form the binary matrix on `U`

    K_ij = 1 if i=j or the real native roots i,j are orthogonal, else 0.

Its diagonal is one and its off-diagonal support is allowed side information.
Fresh binary elimination gives rank nine. The checker emits nine actual
independent rows and, for each of the 54 rows, its exact binary linear
combination of them. These identities hold in every characteristic-two field.
Broadcast the nine basis linear forms. Receiver `i` forms row `K_i x`, then
adds its known neighbor sum, obtaining `x_i`. Applying the same coefficients
to width-`m` records gives nine whole-record messages for every positive `m`.

The lower bound excludes eight such messages, so the integer whole-record
count is exactly nine. This abstract static code does not supply any physical
co-location, delivery, restoration, or free source service.

## 4. Actual source-cut application

The source audit replays the exact pinned word through its operation-1129
cut using full 222-coordinate binary coefficient vectors. Its sole reuse of
previous work is the already admitted validity of that source word; it
imports no author checker or source-summary inventory. Real chart inclusion
is freshly determined by rational row operations on the chart definitions.

For each unfinished `i`, let `D_i` be the set of real subspaces contained in
the native facet `F_i`. Every live field at a chart in `D_i`, after known
inputs and the arbitrary initial Y inputs are conditioned, depends only on
unknown native neighbors of `i`. The audit checks this for every one of the
392 live fields and all 54 unfinished roles. It finds no nonlocal dependency.

Now retain a finite input-independent continuation schedule, linear co-chart
processing, ascending original carriers, and whole-record owned carriers
whose strict moves descend. Grant every value carried by a future strict
owned downward transfer to every receiver as a static broadcast. If there
are `q` transfers, its total dimension is at most `qm`.

Receiver `i` can simulate all computation within `D_i` from its initial
inside data and that broadcast. An ascending original cannot enter `D_i`
from outside: if `H <= H' <= F_i`, then `H <= F_i` already. Local operations,
zero births, and erasures introduce no external dependence. Every owned
entry is among the granted transfers. Chronological simulation therefore
recovers the final demanded `x_i` after fixing initial Y values. It is a
linear decoder. If `q <= 8`, this would contradict Section 2. Hence `q >= 9`.

Uncharged input-dependent scheduling, wider incoming records, a new inward
carrier class, nonlinear operations, or an earlier changed source require a
different theorem. In particular no nine-lifetime assertion follows.

The current source has necessary limiting movement room about
`18.424702560565...`, so this nine-transfer floor does not rule out a
budget-compatible completion. A fresh source with altered initial inside
information must be audited separately. The full supplier invoice and all
five foundational assumptions remain open.

## 5. Verification and scope controls

`check.py` authenticates source bytes, reconstructs all 54 neighbor sets,
checks the fourteen-role geometry, verifies the canonical rank-nine code,
and independently audits every actual source-cut field. The general
block-factor argument above is the proof; finite checks authenticate its
exact source premises.

Two constructive controls delimit the obstruction. Removing demand 15 from
the fourteen-role witness permits an explicit rank-eight fitting code.
Keeping it but granting the missing symmetric side-information edge
`15 <-> 66` also permits an explicit rank-eight fitting code. Thus the proof
does not survive an arbitrary side-information enlargement. A negative
geometry control changing that forbidden edge is rejected by the witness
validator. These controls make no claim that the complete modified
54-vertex graph has rank eight.

Credit the pinned native source, the admitted S019 masked-Hub construction,
the earlier initial-chart transcript and canonical-code authors, and
@CubeJerry. This S020 certificate, block-factor proof, and source-cut audit
were independently reconstructed by Worker C with substantial OpenAI
assistance. Independent agent checking is not human or proof-kernel
certification. No new kappa is claimed.
