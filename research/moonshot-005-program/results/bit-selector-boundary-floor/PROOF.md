# Exact boundary-repair floor for the selected BIT selector family

**Proved within the normalized linear grammar stated below. No new κ.**
This extends the explicit repair obstruction at fork commit
`f4ea078929202b99b34dfc2f05a7b809718e0bdf`,
`research/bit-selector-lift-price/PROOF.md`, which expressly left cheaper
repairs open. It does not prohibit a changed core chronology or prove an
all-column physical supplier. The coefficient-rank cut argument is classical;
the new source-specific application closes the endpoint-repair loophole.

## 1. A quantified cut theorem

Fix a field F, N independent distinguished source symbols X_1,...,X_N, and
any finite collection of additional independent public/dirty input symbols.
Each live field has a normalized linear value and a current chart with an
integer dimension. Fix an integer cut d. Let R be the rank over F of the
coefficient rows on the X symbols of **all** live fields whose current chart
has dimension at most d. This includes every public field and every live
owned scratch field, not only the desired outputs.

Consider any finite correction word built from:

1. Scalar linear operations on fields in the same exact current chart.
2. Initialization at any chart with zero or an X-independent new input,
   and retirement/erasure of a field. Such fields never supply preloaded
   information about X for free.
3. Permutations of whole field/chart pairs, or swaps within one chart.
4. Charged MOVE instructions taking a single whole field between distinct
   nested charts. The normalized coefficient row is unchanged; a MOVE has
   integer rank r equal to the positive dimension difference and recursive
   price r^t for a fixed real t>0.

These are semantic restrictions on the correction word. They exclude free
cross-chart additions, a swap of values while leaving unequal charts fixed,
creation of multiple independent fields by an uncharged split, and arbitrary
new native primitives. No restriction is made on the number of auxiliary
fields, amount of dirty data, direction of movement, scalar encoding,
interleaving of corrections, or reuse of the retired core *through these
listed operations*. The original selector prefix itself stays unchanged.

**Theorem 1 (rank-cut floor).** If the word begins with cut rank R_in and
ends with cut rank R_out, then the number of MOVE instructions crossing
from dimension >d to dimension <=d is at least
`max(0,R_out-R_in)`. Consequently its complete paid moment satisfies

`sum_MOVE r^t >= max(0,R_out-R_in)`.

**Proof.** A same-chart operation replaces low-side coefficient rows by
linear combinations of low-side rows, or acts entirely on the high side;
it cannot enlarge the low-side span. X-independent initialization appends a
zero coefficient row. Erasure removes a row. A field/chart permutation
leaves the multiset defining the cut unchanged. A MOVE staying on one side
leaves that multiset unchanged; an upward crossing removes one row; a
downward crossing adds exactly one row, increasing rank by at most one.
After all instructions, telescoping these inequalities gives the first
claim. Every charged MOVE has r>=1, hence r^t>=1 for t>0. The second claim
follows, even when every ordinary scalar operation is granted zero cost. ∎

The proof is not an inference from a finite search. It holds for every finite
number of fields and instructions and over every field under the specified
normalized semantics. Its application to the repository does not reprove
those semantics for every physical column multiplicity.

## 2. Actual selected BIT boundary

Canonical base: `e54523517d0f03e58352e647c403a5af3e525a57`.
The authenticated native is
`research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz`,
SHA256 `51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`,
Git blob `b718d6b2848215ad785022106dfa9f871a3d1c0c`.
It has p=111 source/target pairs, 437 arbitrary public helpers and 237 owned
labels. Its 34,137-event scalar endpoint is

`(X_j,Y_j,H) -> (X_j,Y_j+X_j,H)` for j=1,...,111 over F_2.

Its main-only endpoint is identity. Its source grammar has no main/core
SWAP and no main reset. These facts are predecessor results; the accompanying
independent source check replays them directly without importing a predecessor
verifier.

For any integer m>=2, the existing selector lift duplicates main planes,
broadcasts main<-core ADDs to every plane, reads plane 1 for core<-main ADDs,
and retains the core once. The invariant in the predecessor gives

`X_(i,j)'=X_(i,j)` and `Y_(i,j)'=Y_(i,j)+X_(1,j)`.

Every helper is restored independently of X and all original owned lifetimes
are retired. At this exact boundary **all X fields have dimension 8 and all Y
fields dimension 7**. Of the 437 restored helpers, 434 end in dimension 8,
two in dimension 4 and one in dimension 6. These three low-side helpers
are included in the cut; their X coefficient rows are zero. Frame identities
and this complete helper boundary are explicitly authenticated by the audit.

Set d=7 and distinguish the 111m independent X inputs. The low-side
coefficient rows at entry are m repeated copies of the 111 plane-1 coordinate
rows, so R_in=111. At the desired repaired endpoint they contain each of the
111m coordinate rows, so R_out>=111m, regardless of any other live fields.

**Corollary 2 (optimal endpoint repair).** Every correction word of Theorem 1
that repairs this boundary to all m independent native endpoints has

`paid repair moment >= 111(m-1)` for every t>0.

The existing literal repair attains equality: per passive plane and port,
initialize an owned zero Z in the full dimension-8 chart, add X_(i,j) and
X_(1,j), MOVE Z to the exact dimension-7 target chart, add Z to Y_(i,j),
and erase Z. This is one rank-1 MOVE and six literal events; the body chart
is a codimension-one subspace of the full chart. One owned label is reusable.
Thus the lower bound is exact for recursive paid moment. It does **not**
assert that six ordinary events are optimal or that erasure is physically free.
All ordinary operations, erasure and fresh physical constants remain charged
by a future supplier implementation. Only their recursive moment is optimized.

This is stronger than ruling out the previously displayed repair schedule:
arbitrary mixing between ports or planes, dirty relays, longer paths and
sharing between endpoint corrections cannot reduce this paid moment within
the stated grammar. Scalar splitting into additional productive targets,
an altered selector prefix, or a fundamentally different native primitive
changes the premise and is not excluded.

## 3. Complete caller consequence and rank-limited generalization

Retain exactly the selected paired E-free root caller, 18 body stages and
all root/QUERY/IDLE terms. Let H be the one-core helper target histogram;
let P_main and P_core be the actual one-native MOVE histograms by owner;
and put, at t=199/200,

`M2 = (complete two-native target minus paid moment) < -444`,
`D = sum_r (P_core[r]-H[r]) r^t < 88`.

These are prior source-bound quantities, freshly recomputed by integer
200th-root enclosures. The literal caller supplies 222 rank-127 targets,
444 targets at each rank 1+7j (j=1,...,9), 444 rank-1 QUERYs and 444 IDLEs
at each rank 7j (j=1,...,8). No empty-root credit is added.

For even m>=2, the m-main/one-core selector prefix, with any endpoint repair
in Theorem 1 and unchanged productive/root contracts, therefore obeys

`M_selector(m) <= (m/2) M2 + 18(m-1)(D-111)`
`              < -222m - 414(m-1) < 0`.

Thus **all** endpoint repairs in this declared class fail the current strict
raw-moment gate at κ=1/200. Nonnegative additional ordinary costs cannot
rescue this failed necessary gate. This is not a universal κ ceiling.

A useful architecture-level extension isolates what a stronger core must do.
Suppose m planes use q copies of the retained core, where 1<=q<=m, with exact
prefix inventory `m P_main + q P_core`, exactly q copies of H credited, and
the same m-plane root ledger. Suppose further that all low-side source
coefficient rows before correction span a space of dimension <=111q.
The last condition is explicit: it holds for a design which delivers only
q linear combinations of the m X planes per port, but need not hold for a
new history-dependent core. Then Theorem 1 gives paid correction moment
>=111(m-q), and the complete moment satisfies

`M_(m,q) <= (m/2)M2 + 18(m-q)(D-111)`
`         < -222m -414(m-q) < 0`.

This excludes rank-limited encode/share/decode-at-the-end variants under the
exact inventory, even granting arbitrary cochart scalar decoding. It does
not assert that every use of q cores has rank <=111q. A candidate with a
larger low-side rank, a different paid invoice, added productive targets,
or changed native chronology must receive a new analysis.

## 4. Frozen chronology audit and next construction

The new finite audit also checks all 755 main-frame configurations (the
initial state and all 754 main MOVE exits). Between these exits the main
frames cannot change, so they cover all 34,138 scalar-word cuts. At every
one, `min dimension(X) > max dimension(Y)`, with minimum gap one. All 628
main-only ADDs operate between X fields. Thus the frozen trajectories have
no direct X/Y cochart contact anywhere, even if one grants new bases within
the same dimension. A proposed direct temporal correction
`Y_i += X_i + X_1` therefore cannot be inserted as two legal free main ADDs
on those unchanged trajectories. This is a finite source statement, not a
theorem about every alternative itinerary.

At the native's input the X fields are dimension one and Y fields dimension
zero; the cut d=7 initially contains all 111m independent X directions.
The selector prefix reduces the cut rank to 111 before endpoint repair.
The rank-cut theorem therefore does not rule out an interleaved construction
that preserves and delivers the needed directions before this loss. Causal
core-mediated coding switches, new native trajectories or changed contracts
remain genuine escape mechanisms.

## 5. Next concrete obligation and limits

The shared-core route must avoid this cut deficit *before* the selector's
complete endpoint, or change its paid/target architecture. The next useful
construction is therefore an interleaved causal core which delivers more
than 111q independent low-side source directions without paying the above
endpoint toll. Merely choosing a different selector or more elaborate final
linear repair cannot succeed under the stated rank/invoice premises.

No covered BIT supplier above .005, completed ordinary BIT above .005,
uniform complex supplier above .005, compiler admission or multiplication
bound is constructed here. All five selected assumptions remain:
`native_all_columns`, `owned_erasure`, `compiler`, `precision_tape`,
`analytic_recovery`. This is a normalized source-bound obstruction, not
an independent all-column, tape or unconditional theorem.

Credit the selector predecessor and its independent review, Nick Petalas's
CrocSwap/integer-mult-bounds#6442 for the distinct weighted-wrapper optimal
rank-one repair theorem and #6601 for the distinct carrier-width rank method,
DreamingOfClouds,
zxv, Rohan Arun's finite bootstrap lineage, @CubeJerry and all retained native
and caller authors. The cut-rank method is standard linear algebra; no claim
of inventing it is made. Prepared for @CubeJerry with substantial OpenAI
Codex assistance. Apache-2.0. No human or formal-kernel acceptance claimed.
