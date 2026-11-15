# A unique source in a common chart forces an unavailable branch

**Scoped source-preparation obstruction; no new kappa.**

## Theorem: first-exit obstruction

Consider a finite chronological linear source-preparation word over any field.
Original records X_j start with independent values x_j on distinct native lines
L_j and move monotonically upward. Zero-born owned caches may be initialized,
read, modified, copied and cleared at their stationary birth charts; they do
not move. Arbitrary cocharted original recoding is allowed, even if it is
singular or otherwise fails an eventual restoration obligation. There are no
original-Y relays, additional ascending records, downward preprocessing
transport, or pre-existing nonlocal data.

Suppose the word must acquire specified linear cache outputs at distinct
proper facets F_1,...,F_s. For some independent input x_j, let J be a set of
at least two demanded facets whose outputs have nonzero x_j coefficient. Put
I=intersection(i in J) F_i. If L_j is the ONLY original source line contained
in I, no such preparation word exists.

### Proof

Follow the coefficient of x_j. Initially only original X_j contains it.
Every original X_l always occupies a chart containing its own initial line
L_l. Thus no other original record can ever enter a chart contained in I.

While X_j remains in I, all stationary caches to which it can transfer x_j
information are also at charts contained in I. Only X_j can read any such
cache. The arbitrary number and algebraic contents of these caches cannot
create another moving carrier there.

If X_j never leaves I, it cannot acquire outputs at the distinct larger
facets F_i: because at least two different facets are involved, their
intersection I is a proper subspace of each. No other original can transport
the saved x_j information out of I.

Otherwise consider the first MOVE of X_j to a chart C not contained in I.
Choose a demanded facet F_t which does not contain C. All saved earlier
x_j caches are in I and are hence inert: X_j cannot return to a proper lower
chart after this move, and no other original can visit them. The moving X_j
is now outside F_t. Every subsequently influenced original must first meet
an already influenced moving record or cache at a chart outside F_t. Any
such recipient is then also outside F_t and remains so under monotone upward
movement. Every new x_j cache produced there stays outside F_t as well.

Induction through the remaining chronological operations proves that no
nonzero x_j coefficient can ever appear at F_t. This contradicts the demanded
cache coefficient. The proof uses physical cocharts and source lines, not
the purity, rank or invertibility of the original-value transform. QED.

The statement extends componentwise to arbitrary-width blocks whenever the
demanded source coefficient block is nonzero. It is a preparation theorem,
not a prohibition on later descending packets conveying the input.

## Application to the exact singular target

The retained eight-seed/seven-addition target uses the six spinor facet modes
hK_i for i in [1,3,5,10,30,61], and the omitted-root proper mode K_b, where
b=(0,0,1,1,0,0,1,-1). The initial seed space has dimension eight and the seven
additions extend it to the rank-fifteen singular code W.

Input role6 is the only native source line in the intersection of the six
listed native facets. It has coefficient1 in every one of those six modes.
The first-exit theorem therefore excludes acquiring those six modes entirely
in the stated original-X-only preparation grammar, EVEN WITH arbitrary
reversible recoding. The earlier unchanged-original overlap obstruction is
strictly weaker in its allowed value operations.

This does not contradict the two-facet construction in PROOF.md. The pair's
common chart contains two actual original donor lines, and the construction
uses them. Nor does it exclude interleaved descending histories, Y carriers,
additional paid transport or a changed set of local modes.

## All 64 complementary orientations of this six-mode basis

The singular partners of the six normals are respectively
[18,21,15,27,50,73]. Replacing normal r_i by r_i+s replaces its filtered mode
hK_i by hK_i+h. The initial eight-seed space already contains h, so every one
of the 64 independent complementary choices preserves the rank-fifteen target
span after the seventh K_b addition.

The exact source check examines all native input columns for each orientation.
For a source j it intersects the real facets at which the chosen modes have
coefficient1, and records a witness if that intersection contains only L_j.
There is no numerical rank tolerance: source membership is an integer dot
product test against explicit normals.

For the six modes alone, precisely orientations26,28,41,47,53 avoid this
particular singleton-source gate. The other59 have a witness. In the original
orientation, role6 supplies a witness.

After adding the seventh K_b mode, ALL64 orientations have a witness. The
five former exceptions have the following explicit examples (mode6 is K_b):

| Orientation | Source | Demanded mode indices |
|---|---:|---|
|26|60|1,2,3,4,6|
|28|32|1,2,3,4,6|
|41|17|1,2,3,4,6|
|47|94|1,2,3,4,6|
|53|32|0,1,2,4,5,6|

The finite exact incidence certificate plus the first-exit theorem therefore
rules out this entire 64-member local-mode family under the stated preparation
grammar. This is not a failed finite circuit search and not a universal
obstruction for every basis of W.

## Changed-basis negative control and next obligation

The certificate also supplies seven different proper W modes which extend
the SAME eight initial seeds to W while passing the singleton-source test.
Two modes share the omitted-normal facet b. Their explicit coefficient rows,
normals, source membership and joint rank are verified, and every input
column is checked for this gate. The existence of this alternative basis
prevents the fixed-family obstruction from being represented as a theorem
against all singular-code preparation.

Passing the gate is a necessary condition only. It does not prove that the
seven modes have a compatible network of original carriers, that the
originals can all be restored, or that any full invoice is favorable. The
concrete next source problem is to realize this alternative mode basis, or
legitimately use interleaved descending/ascending carriers in the old family.

## Reproduction and provenance

From repository root run the `worker-a/first_exit_gate.py` script. Expected:
`PASS_FIRST_EXIT_GATE_64_ORIENTATIONS`,64 rejected seven-mode families and a
changed-basis necessary-gate control. The checker pins source recovery blob
8eba43d142c819c206dce5df87ea4571aaead287; all exact witness lists are in
`output/FIRST-EXIT-RESULT.json`.

The singular source, eight-seed/seven-mode family and complementary root
relation are inherited from the admitted singular-pivot package. Worker C's
independent local-code classification supplied the candidate-mode catalogue
for finding the changed-basis control; the control checker verifies its
literal words and normals directly and does not import that catalogue or
classify the complete space independently.

Credit @CubeJerry, prior native and singular-code contributors, the independent
localization work, and separately identified reviewers. Substantial OpenAI
assistance. No complete supplier, foundational assumption discharge, formal
proof-kernel result, or new kappa is claimed.
