# The balanced causal source has 3,097 additive quotient encoders

## Result and scope

Fix the 111 native roles, the 120-line completion, the A2/D4 diagram and the
integer factor in the S022 balanced causal atlas. Let `b=5760` and `p=360`.
Use any positive common binary record width `d`, so one donor's varying input
is the group `G=F_2^(bd)`. The claimed completed native task is the original
`Y_i <- Y_i + X_i`, with the real nine canonical records, arbitrary original
inputs, restoration of all X before the Y wave, and the prescribed public
routes. Keep all ordinary and recursive costs.

Assume deterministic source encoding and arbitrary deterministic processing
after emission. For each native source line `j` and incident plane `H`, the
source emission is the tuple of the genuine early-X exits and late-Y exits
from `j` towards `H`. If the late source operation also reads incoming Y,
the theorem concerns its restriction to the zero-Y, canonical-zero slice.
It does not assert linearity of that operation on every incoming-Y value.
Every source map used by the present linear programme has this restriction.

**Theorem 1.** For all **3,097 non-singleton donor-plane flags**, the source
emission on that slice is an additive quotient of `G` of size `2^(pd)`,
followed by a bijective relabelling of its output alphabet. Its fibres are
the cosets of a binary subspace of dimension `15pd`.

The eleven singleton planes have `540d` source bits, instead of `360d`.
The theorem does not classify their encoders. This is a necessary condition
for a complete code on the balanced routes, not a proof that such a code
exists. In particular it does not turn the present rank-only construction
into the target native map. No new kappa or foundational discharge follows.

## The source and visible-plane cuts

Write `m_H` for the number of native lines in H. The balanced factor gives
`x_H=12/m_H+u_H` early X lanes per native source per H-D flag, with `u_H` in
`{0,1,2}` on native-full planes and zero elsewhere. Put
`e_H=max(8,x_H)`. A donor has `45x_H` early symbols and
`45(e_H-x_H)` late symbols towards H. Hence:

* If `m_H` is two or three, its full emission has exactly `45e_H=p=360`
  symbols. The colour split changes which are early; it adds no source
  information.
* If `m_H=1`, the full emission has 540 symbols, all early.
* Every donor belongs to 28 planes. Every foreign receiver sees 16 of them.
* For each H visible to i, exactly 15 of its 45 D4 exits are visible to i.
  Those exits have 24 symbols each, giving exactly p symbols in total,
  across the early and late waves together.

The last cut includes early X continuing to a later chart and any stationary
snapshot of it. A stationary plane, middle or facet cache cannot bypass
the H-to-D exit that first brought its information there. Proper routes
remain nested. The only nonproper return allowed here is the explicitly
paid canonical bank, which is neutralized below.

Call `(j,i)` **tight** when i sees no singleton plane of j. Then all sixteen
source bundles visible to i have p symbols. There are 6,110 tight foreign
pairs; the other 360 see one extra 180-symbol emission. One hundred donors
have no singleton plane at all. The eleven exceptional donors each have
exactly one.

## Canonical information is not a free exception to saturation

Let O be the literal native orthogonality matrix and K the retained
canonical row space, `rowspan(I+O)`, of rank nine over F2. For every receiver
i, restricting K to the inputs outside its foreign set N_i still has rank
nine. The exact checker verifies this on the pinned source table.

Consequently arbitrary values of the donors in N_i can be extended by
outside inputs so all nine canonical values vanish. Set all original Y to
zero. The pure-Y preload then carries no varying source information. No
outside donor has a proper path into F_i. On this slice the native target
at i equals the sum of its independently varying foreign donors, since
`X_i + sum_(j in N_i) X_j` is a canonical row and vanishes. This justifies
the additive-sum contraction used next, without gifting canonical packets
or assuming away their physical cost.

## Coset saturation at a tight receiver

Fix a tight `(j,i)`. The sixteen p-symbol emissions of j visible to i must
jointly determine X_j: fix every other foreign donor and vary X_j in the
additive sum. Their product alphabet has exactly `|G|` elements. Thus the
sixteen-coordinate map is a bijection, and fixing any fifteen coordinates
leaves exactly `2^(pd)` input possibilities.

Let P be one of those planes, and choose another native donor k on P such
that `(k,i)` is tight as well. Fix every visible source coordinate of j and
k except their P coordinate, and fix all other donors. Let U,V be the two
resulting input fibres. Both have size `s=2^(pd)`. Only P's visible exit
tuple can vary at receiver i, and that tuple has at most s values.
Correctness therefore gives `|U+V| <= s`. The reverse bound follows by
fixing one summand, so equality holds.

For completeness, equality forces U and V to be cosets of one subgroup B
of order s. Every translate `U+v` is the same size-s subset `U+V`; hence
`V-v0` is contained in the stabilizer of U. That stabilizer has order at
most s, since U is a nonempty union of its cosets. It contains s distinct
elements, so it has order exactly s, and both fibres are its cosets.
Keeping one fibre fixed while changing the other proves that this subgroup
is independent of the chosen fibres. Denote it `B_(i,P)` for this comparison.
It preserves all of j's other fifteen visible coordinates.

## A clean tight receiver exists at every ordinary flag

For each non-singleton `(j,H)`, the checker supplies a receiver i such that:

1. H is visible to i and `(j,i)` is tight.
2. Every other visible plane P through j has a companion `k != j` for
   which `(k,i)` is tight.

This test includes the exceptional donors and tests the companion's
singleton exposure too. Merely requiring P to have two native donors is
not enough. Every one of the 3,097 flags has at least thirteen valid i.
The certificate lists the selected receiver and all fifteen companions.

For the fifteen planes P other than H, the preceding argument supplies
subgroups `B_(i,P)` of order s. Their sum is direct. Indeed, if a sum of one
increment from each is zero, isolate the increment from P. Every other
increment preserves the P coordinate, so that isolated increment preserves
P too. By definition it also preserves all other coordinates. The complete
sixteen-coordinate bijection makes it zero. This works for every P.

The direct sum of these fifteen groups has order `s^15`. It preserves
the H coordinate, whose every fibre also has size `s^15`. Therefore each
fibre is exactly one coset of this one subgroup. This proves Theorem 1.
The argument is an all-alphabet group proof; the finite certificate checks
only the literal geometry and source conditions to which it is applied.

## A constructive criterion for the actual early/late source split

The preceding theorem reduces 3,097 source maps to subspaces. It does not
say any arbitrary subspace assignment can be emitted at the required times.
Here is the exact linear source-stage bridge, stated independently of a
downstream code.

Let a proposed linear quotient source for donor j have row spaces
`U_H <= F_q^b`, of dimension `p_H`: 360 at ordinary H, and 540 at the one
singleton H if present. Put `a_H=45x_H`; their sum is b. The prescribed
source has exactly `a_H` genuine early X exits towards H and `p_H-a_H`
genuine late Y visits. The data entering the early wave must be bijective
on the original X_j, so that all X can restore at Hub before Y moves.

**Theorem 2.** The proposed quotient information can be distributed over
these actual source slots, with a linear invertible early X map, if and
only if

    dim(sum_(H in S) U_H) >= sum_(H in S) a_H    for every subset S.

No field extension is needed for this source-stage criterion.

Necessity follows because the early functions assigned to the planes in S
are independent rows inside the displayed sum. The same capacity bound is
necessary even for nonlinear early functions of the supplied quotient
values when the complete early tuple is a bijection: every such subtuple
then has its full product range, which must fit in that joint quotient.

For sufficiency, repeat U_H exactly a_H times in a list of b spaces. The
inequality ensures every sublist spans at least its length, since its
support S contains at least as many repeated slots. The independent
representatives lemma chooses one vector from each space, all independent.
One elementary proof is by induction: split off a nonempty proper tight
sublist and pass to the quotient by its span, or, when every proper sublist
has slack, choose a nonzero last vector and quotient by its line. The
remaining inequalities persist in each case. The b chosen vectors form an
invertible early source matrix. At each H, extend its a_H selected vectors
to a basis of U_H and use the remaining rows as late source additions.

This constructs the source stage and its timing. It does **not** preserve
an arbitrary pre-existing nonlinear downstream implementation, whose early
functions may differ from the newly chosen rows. A complete construction
must still supply compatible causal H, D, K and F operations with the new
early/late coordinate choice, simultaneous identity blocks and all source
restorations. The theorem therefore removes the need to guess an early
basis once viable subspaces satisfying the inequality are known; it does
not close the main synchronization obligation.

## Literal source compilation and finite ordinary bill

For a block-linear lane assignment over `F_(2^w)`, expand every field lane
into w binary native copies and act identically at every positive body
width. Let B=bw and R=w sum_H(p_H-a_H). Before changing any original X at
its native line, retain B stationary raw copies, costing B INIT and B ADD.
An invertible binary early matrix costs at most `B^2+3B` whole-record ADDs
by elimination and three-ADD swaps. Each of the R late parities costs at
most B ADDs into its actual Y owner and preserves that arbitrary owner's
baseline. The source inverse at Hub costs at most another `B^2+3B` ADDs
after any downstream early inverse has been paid. Retire the B line
snapshots using B charged dirty CLEARs after their final late use.

Thus a simple source-and-source-inverse bound is

    ADD <= 2 B^2 + B R + 7 B;  INIT = CLEAR = B;

the extra stationary ownership peak is B, and the source compiler adds
no MOVE beyond the fixed actual route diagram. All these costs are actual
finite expenses. They are additional to downstream inverse operations,
canonical formation, the nine paid descents, storage/precision and the
complete recursive supplier/caller bills. A binary subgroup theorem at
one arbitrary body width is not automatically a uniform whole-record
compiler; the latter claim here is only for the displayed block-linear
lane maps.

## Reproduction, controls and next construction

`check.py` takes the pinned layout and factor and independently reconstructs
the incidence and first-cut census. It emits all 3,097 clean-flag witnesses,
the canonical ranks, the exact early/late counts and small algebraic
controls. The negative controls fail when a tight comparison is falsely
declared at a singleton-exposed pair, when the companion is not tight, or
when the source independent-representatives rank condition is dropped.
The positive source example includes overlapping quotient subspaces and a
genuine invertible early matrix; it is not an MDS-dictionary assertion.

The immediate constructive target is an aligned, potentially non-MDS
subspace atlas satisfying the displayed weighted rank inequalities. A
separate probe asks whether a changed balanced factor makes these
inequalities consequences of convex combinations of its tight 16-plane
bases. Numerical LP outcomes alone are not universal obstructions or
exact certificates.

Credit @CubeJerry, the native source and chart authors, the S022 quotient,
balanced-atlas and coordinate packages, and substantial OpenAI assistance.
This extension and source compiler were developed in S023 Worker A from
programme baseline `8cf982065bccdd62de2856b16635a6ee06dadb0c`.
