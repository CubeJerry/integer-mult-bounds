# Joint kernel placement and arbitrary input-puncture requirements

**Proved in the stated monotone source model; independent review pending.
No new κ.** This strengthens the programme's history-normalization interface
in two compatible ways. A receiver can use only kernels lying below its own
facet. Separately, every input puncture, including ports not yet completed,
must retain enough normalized rank for the remaining native fitting. The
second condition excludes both current four-axis and six-axis templates
from becoming complete using only their present kernels and mandatory
terminal fields. Their literal partial constructions remain valid.

## 1. Model and definitions

Fix a field k and whole-record width V>=1. Use the actual111 native source
lines L_i and distinct output facets F_i, with L_i not contained in F_i.
Original X_i records ascend from L_i to Hub; original Y_i records ascend
from ground to F_i. There are q persistent width-V descending packets.
Zero-born stationary records, legitimate ascending helpers, arbitrary
noncommuting linear block operations and arbitrary original-Y feedback are
allowed. All operations must be actual and cocharted. Extra descending
channels, packet restarts, nonlocal births and nonmonotone movement remain
outside this model. No costs are removed by the statements below.

For each proper nonzero geometric chart C, identify aliases and form the
actual joint cell with formal independent boundary arrivals:

    P_out = C_C U_in + D_C P_in.

Let nu_C=dim ker D_C, and let K_C=h_C P_in be an actual kernel-coordinate
vector of width nu_C in the admitted inverse-cell identity

    P_in = R_C(P_out-C_C U_in) + J_C K_C.

The image constraint and all actual chronology remain required. Let Z
contain the q actual packet first-ground-arrival values, before any later
ground mixing. These and K_C may contain arbitrary original y terms. Write
Z_x,K_C,x for their coefficient matrices on the independent original X
inputs. For receiver set J, let pi_J restrict original-X input columns to J.

A J-fitting has identity V-by-V diagonal blocks, with zero foreign blocks
when the actual source roots are real-nonorthogonal. There is no symmetry
or commutativity restriction. Write mr_k,V(J) for its minimum possible rank.

## 2. Localized spatial normalization

**Theorem1 (kernel visibility).** Every history at a proper chart C has a
representation

    H_C = Lambda_C Z + sum_{D subseteq C} Lambda_C,D K_D
          + E_C y + B_C x,

where B_C is supported only on original input lines contained in C. The sum
contains only proper nonzero singular charts D contained in C.

**Proof.** Apply the admitted spatial induction on the finite visited-chart
poset, retaining the locations of its kernel terms. At ground, histories are
linear in first-arrival Z and independent original y. At chart C, each
ascending arrival comes from a smaller chart C', whose kernels all satisfy
D subseteq C' subset C. Each packet departure equals its boundary arrival
at a smaller successor chart, with the same property. Substitute these
normalized values in the actual inverse-cell identity at C, adding K_C
itself only when the cell is singular. Every local X remainder comes from
C or a smaller chart and therefore stays inside C. This proves the claim
for packet arrivals, all local histories and ascending departures. The
argument uses actual formal cell identities; it does not reorder operations
or grant simultaneous access to chronological boundary inputs. Independent
y terms are retained symbolically and have no X-information coefficient.

**Theorem2 (joint placement and puncture inequality).** Let J be any set of
native receiver roles, and let H be any collection of singular charts that
contains every singular C with C subseteq F_i for at least one i in J. If
the source completes all receivers in J, then

    mr_k,V(J) <= rank pi_J([ Z_x ; (K_C,x)_(C in H) ]) .             (1)

In particular

    mr_k,V(J) <= rank pi_J(Z_x) + sum_(C in H) nu_C.                (2)

**Proof.** Theorem1 at each completed facet gives
`e_i tensor I_V = Lambda_i G_x+B_i`, where G consists of the indicated
actual Z and kernel coordinates. The own source line is outside F_i, so
B_i has zero own block. Its other nonzero input columns are actual contacts.
Thus A_i=Lambda_i G_x has the fitting diagonal and noncontact zeros. Restrict
both receiver rows and input columns to J. This is a J-fitting factoring
through pi_J(G_x), proving (1). Subadditivity proves (2).

Neither J nor its complement is required to be already completed in a
partial construction. For a proposed eventual complete source, (1) is
necessary for **every** J. Equivalently, one may delete an arbitrary set E
of input and receiver roles and take J=all111 minus E. This is an algebraic
restriction of the eventual endpoint identity; it does not assert a new
physical execution obtained by deleting those records.

If no singular chart lies below any F_i for i in J, take H empty. Then
`mr_k,V(J)<=rank pi_J(Z_x)<=qV`. This is the placement requirement.
If d specified first-ground packet X-coefficients vanish on J, (2) gives

    mr_k,V(J) <= (q-d)V + sum_(C in H) nu_C.                       (3)

Their full rows may contain arbitrary y terms. Only the actual X projection
has to vanish. Independent support directions are unnecessary for this
upper bound: d identified width-V packet slots disappear after projection.
More general known linear dependencies among projected terminals can replace
(q-d)V by their actual rank. These statements permit arbitrary block widths
and arbitrary noncommuting blocks, without scalar extrapolation.

## 3. Exact native rank-nine certificates after puncturing

We use the credited star rank inequality of DreamingOfClouds,
CrocSwap/integer-mult-bounds#7114, rederived in the admitted programme package
`bit-saturated-star-rigidity`. Here is precisely the rank-floor consequence.

Choose eight retained pairwise real-nonorthogonal native point roots and
one retained native role for every edge of a simple graph on those points.
Each edge role is real-orthogonal to exactly its two incident point roots;
distinct incident edge roles are real-nonorthogonal. If every point degree
is at least four, every fitting on these roles has rank at least9V over
every field. To see this, normalize the point I_(8V) block in a factorization
of rank8V+j. With the admitted nonnegative star quantities G_a, the argument
using kernel inclusions and Sylvester's inequality yields

    sum_a(deg(a)-4)G_a <= 2|edges|(j-V).

The left side is nonnegative, so j>=V. Degree four suffices for this floor;
the stronger strict-degree premise used for equality rigidity is not needed.
The current result does not claim rigidity for any punctured graph.

The checker verifies actual integer-root dot products for all displayed
point/edge incidences and incident-edge noncontacts. It never substitutes
an abstract star graph for the native. It also independently restricts the
canonical binary fitting and computes rank9. Consequently every listed
puncture has exact minimum9V over every characteristic-two field; its
lower bound holds over every field. The binary rank certificate persists
under field extension and tensoring by I_V.

### Four-axis mandatory-bank puncture

Delete

    E4={0,5,6,7,52,53,54,55,56,57,58}.

The remaining100-role instance contains the actual point frame

    [1,8,9,30,37,46,73,77],

with26 certified edges and degrees

    [5,6,6,7,7,7,7,7].

Every listed role avoids E4. Thus its minimum fitting rank is9V in
characteristic two, and at least9V over every field.

### Six-axis mandatory-bank puncture

Delete

    E6={0,1,2,5,6,7,52,53,54,55,56,57,58}.

The remaining98-role instance contains the actual point frame

    [3,59,62,66,68,83,104,106],

with24 certified edges and degrees

    [6,7,6,7,6,4,6,6].

Its minimum fitting rank is likewise9V in characteristic two. A degree-four
point does not invalidate the rank-floor argument.

## 4. Application to the two frozen source templates

The source words and exact hashes are in `DEPENDENCIES.json`. The four-axis
word was independently reviewed by Worker A. The six-axis word is a later
literal extension and has its own construction/review status. The gate
checker independently extracts actual first-ground values from all222
original columns, aggregates geometric aliases, and computes the complete
formal packet-through matrices of every proper chart. It does not infer
nullity merely from the packet rank at an interior time.

All source-specific applications here are to characteristic-two fields and
arbitrary positive widths, by the actual binary identities tensored with
I_V. The general theorems above are not restricted to characteristic two.

### Four-axis source

There are eight packet first-ground fields. The only singular proper cells
are A15 and A30, each with one actual width-V kernel. The two forced terminal
X rows are

    Z0,x = x52+x53+x54+x55+x56+x57+x58,
    Z1,x = x0+x5+x6+x7.

They are actual first-ground X projections; cancellation of a y0 nuisance
later at ground does not change these rows. Both vanish after projecting
to the complement of E4. Equation (3), even granting both kernels globally,
therefore bounds every completed punctured fitting by

    (8-2)V+2V=8V.

The100-role rank-nine certificate contradicts this. Hence this source
cannot be completed within the same q8 model using only those two kernel
cells while preserving these two mandatory terminal slots. This exclusion
holds under arbitrary changes to its six other terminal seeds or local
block operations that retain the stated hypotheses. It does not depend on
W15 being required, on a particular canonical fitting, or on scalar search.

There is also an independent placement failure. A15 is below facets with
roles `[0,1,2,3,59,60,61,62,63,64,65]`; A30 is below roles `[1,2,3,4]`.
Their union has12 roles. The other99 roles contain a rank-nine star with
point frame `[5,30,32,38,39,46,103,107]`,24 edges and degrees
`[4,7,6,7,6,6,6,6]`. They see no kernel and have only eight terminal fields,
so Theorem2 excludes completion independently of the support puncture.

### Six-axis source

The extension retains and resets P2 at L1 and P3 at L2. Its four actual
kernel cells are A15,A30,L1,L2, each with nullity V. P0/P1 retain the two
terminal rows above; additionally

    Z2,x=x1, Z3,x=x2.

All four specified packet slots vanish on the complement of E6. Even granting
all four kernels globally gives the same ceiling

    (8-4)V+4V=8V,

contradicting the98-role rank-nine certificate. Reseeding the other four
packets cannot repair this within the declared template.

The new line cells do improve placement: their joint invisible role set is
exactly `[8,9,10,11,12,13,46,47,48,49,50,51]`. The canonical fitting on this
12-role set has rank4, so the old invisible-rank-nine obstruction no longer
applies there. That improvement and the actual six outputs remain valid.
Nevertheless the independent arbitrary-puncture condition still fails.
Checking only the six already completed ports would miss the failure:
puncturing those six leaves actual normalized rank9. The decisive additional
deleted ports52..58 annihilate the mandatory P0 terminal as well.

For the frozen four-/six-axis words, exact normalized dimensions are10/12;
after the specified E4/E6 projections they are both exactly8. The universal
upper bounds above do not rely on attaining these dimensions. They remain
valid if some free seeds or actual kernel directions become dependent.

## 5. Consequence, verification and next constructive requirement

A complete proposed source must simultaneously satisfy its receiver-dependent
kernel placement, every arbitrary input puncture, the full target rank/arrival
gap and the complete physical invoice. Raw W15 history, normalized rank10 or12,
actual few-port delivery and generous access to all kernels do not imply these
requirements. The current partial words are mathematically useful but are
not complete suppliers. No unconditional or complete conditional κ changes.

The gate is not a theorem that every retained-history source fails. Shallower
retention can leave broader actual suffix banks; interactions can change the
mandatory first-ground fields or supply additional independent kernels without
trading away another terminal slot. Such changes must satisfy both placement
and puncture conditions and be acquired by actual chart operations. No small
support assumption is imposed on all possible future terminal banks here.

```sh
python3 -B check.py --repo /path/to/programme \
  --four /path/to/colored-four-axis-source/output/WORD.json \
  --six /path/to/colored-six-axis-source/output/WORD.json \
  --out /path/to/joint-kernel-gates/output
```

Expected status: `PASS_JOINT_PLACEMENT_AND_ARBITRARY_PUNCTURE`.
The receipt lists every exact star edge, dot-product check, through matrix,
actual kernel boundary row, terminal row and visibility set. Rejecting controls
remove a displayed star point and omit one required support column. The latter
restores projected rank9, showing that the rank8 contradiction cannot be claimed
without the exact terminal-support deletion. The completed-only punctures are
positive controls of why a weaker test failed to detect the obstruction.

Credit @CubeJerry, the admitted Y-feedback normalization and star-rank
predecessors, DreamingOfClouds's #7114, and the root/Worker A/Worker C source
construction and independent review. OpenAI assistance is disclosed. The new
content is localized kernel normalization, its joint arbitrary-puncture
interface, and the exact native source applications above.
