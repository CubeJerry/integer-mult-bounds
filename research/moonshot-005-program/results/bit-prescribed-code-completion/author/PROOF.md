# Prescribed singular seeds leave an exact four-versus-five completion gap

**Proved source-bound code constraints and an abstract completion upper bound.
Independent review pending. No new kappa.** This concerns a retained ground
code, even when every geometrically allowed foreign input is granted freely.
It does not constrain an execution that changes its required preloads, uses
a larger actual history/code interface, or performs an independently paid
nonstationary source repair outside this fixed-code hypothesis.

## 1. Source, spaces and quantifiers

Use the pinned111 native root lines and the source-bound singular seed S8.
Let k be any characteristic-two field. The ambient scalar row space is
`k^111`, with raw coordinate rows e_i. Let

    L_i=span{e_j : r_i dot r_j=0}.

The own coordinate is absent because r_i has nonzero Euclidean norm. These
are the FULL geometrically permissible foreign side-information spaces.
They are more generous than the actual live/captured stock in any current
literal source. A code B supplies an algebraic fitting at receiver i exactly
when `e_i in B+L_i`.

Let C9 be the canonical native fitting row code. Let S8 be the admitted
eight-dimensional code, and

    S6=span(A3,A76,A80,A4,A74,A78).

S6 is the six-dimensional subspace actually used by the nine nonpoint outputs
in the fifteen-output fork; the other six outputs use raw point fields.
Let E6 be the coordinate span at1,6,73,75,77,79, and let T be the17-point set

    {1,3,4,6,18,21,61,64,65,73,74,75,76,77,78,79,80}.

We test S8, S8+E6 and S8+k^T, and the corresponding three S6 spaces. The last
case grants all seventeen raw coordinates for free, even though their actual
acquisition/delivery is not assumed.

An additional r-dimensional source extension means an arbitrary subspace U
with `dim((B+U)/B)<=r`, and a complete fitting with each row in B+U. No canonical
or W15 restriction is placed on U unless explicitly stated. For whole-record
width V, replace B and L_i by their tensor products with k^V, and allow arbitrary
linear block operators. The frame bounds below apply to the dimension added,
not merely to the number of syntactically named packet owners.

## 2. A single additional row: exact general criterion

For a general fixed code B, let I be the receivers not already fitted by B.
Put

    B_i=B+L_i,
    H=intersection_(i in I) (B_i+span(e_i)).

One row u can extend B to fit every receiver if and only if

    u in H and u not in B_i for every i in I.

Indeed, an unserved receiver must use u with a nonzero coefficient in
`e_i=b_i+a_i u`; rescaling gives u in `B_i+span(e_i)` and u not in B_i.
Conversely, any such u has a nonzero e_i coefficient modulo B_i and can be
rescaled to supply e_i. This separates homogeneous locality constraints from
the nonzero own-coordinate requirement.

Over an infinite field, or a finite field with more than |I| elements, a
simultaneous u exists exactly when H is not contained in any B_i. Each failed
own-coordinate condition cuts out a proper hyperplane of H; their finite
union cannot cover H in that field regime. Over a smaller field, noncontainment
is necessary but this union argument alone is not sufficient.

For EVERY one of the six source spaces in section1, exact calculation gives

    H=B.

Thus every one of their unserved receivers is a blocker. This is not a binary
search failure. The defining matrices are binary, so the subspaces,
intersections and rank identities commute with every characteristic-two field
extension. No field extension makes one added row possible.

The certificate gives a basis of H-perp, each row annotated by a receiver
whose `B_i+span(e_i)` it annihilates. For each blocking receiver it also gives
an own-coordinate-one functional annihilating B_i, expressed as a sum of
those constraint rows. This is a short exact dual contradiction to the
required own-coordinate value, independently checkable from source bits.

The eight-seed variants fit exactly T before extension. S6 alone fits the
nine nonpoint targets; S6+E6 fits the actual fifteen targets; S6+k^T fits T.
These are optimistic algebraic fitting sets, not physical decoder admissions.

## 3. Four new directions are necessary for S8; five for active S6

If I is a native set of pairwise REAL nonorthogonal roots, every fitting
restricted to rows and columns I is the identity matrix: foreign entries in
that principal block are all forbidden. Therefore, for a baseline code B
and an additional subspace U,

    dim(U modulo B) >= |I|-dim(B restricted to I).                 (1)

The same argument for V-wide records gives
`dim(U modulo B tensor k^V) >= (|I|-rank(B|I))*V` for arbitrary block operators.
No commutativity, invertible foreign block, scalar selector or finite-field
restriction is used.

The following source certificates are explicit:

|Retained seed|Pairwise nonorthogonal eight-set I|Restriction rank|Required new dimension|
|---|---|---:|---:|
|S8|0,14,22,23,30,31,59,60|4|at least4V|
|S6|0,14,60,63,69,70,107,109|3|at least5V|

Both sets are disjoint from T. Hence every grant of raw coordinates from E6
or even all T vanishes on these sets and leaves the bounds unchanged. Exact
rational inner products check every pair, and binary minors check the stated
restriction ranks. Field extension preserves them.

In particular, freeing the two S8 directions unused by the current nonpoint
outputs and adding one further field supplies only three dimensions beyond
S6. It cannot give a complete fitting while retaining this S6 preload
interface, even with all six genuine point grants and all local side
information supplied freely. A changed chronological preload interface is
outside that conclusion and remains a possible construction.

The exploratory complete clique census found485,330 nonempty native cliques
and no stronger bound from (1) for these fixed codes. That finite census is
not an upper bound on the true completion dimension. Only the explicit
witnesses are required for the theorem.

## 4. Canonical completion attains five or six, and cannot be compressed

Exact source ranks are

    dim(S8+C9)=13, dim(S8 intersect C9)=4,
    dim(S6+C9)=12, dim(S6 intersect C9)=3.

Adding a basis of C9 modulo S8 therefore supplies an abstract five-direction
complete fitting. For S6 it supplies six. The same added dimensions remain
five and six after adjoining E6 or even all raw coordinates T. This gives

    4 <= minimum unrestricted added dimension for S8 variants <=5,
    5 <= minimum unrestricted added dimension for S6 variants <=6.       (2)

These are code-space upper bounds: the canonical fitting exists algebraically.
Its source acquisition, correction delivery and complete target invoice have
not been supplied by this rank statement.

Within the particular envelope B+C9, all five or six canonical quotient
directions are necessary. For S8 variants, receivers0,5,8,9,30 individually
force five independent one-dimensional quotient subspaces. In the emitted
quotient basis their masks are1,7,8,13,16. The checker records analogous
six-way witnesses for the S6 variants. Each receiver's allowed quotient
space is computed from the actual locality equations, and its own-coordinate
condition is nonzero on the forced line. These binary rank-one subspaces
remain lines after every characteristic-two extension. A complete fitting
inside this envelope must contain all the independent forced lines.

## 5. Arbitrary vertex gauge does not reduce the canonical requirement

The conclusion is stronger than a check of one canonical basis. Let D be
ANY invertible diagonal column scaling over k. Then, for P empty, E6, or T,

    dim((S8+k^P) intersect C9 D) <=4,
    dim((S6+k^P) intersect C9 D) <=3.                              (3)

Here k^E6 means its six coordinate roles. Equality is attained at D=I in
the cases above, so five or six added canonical directions remain optimal
even after arbitrary vertex gauge.

To prove (3), let J be the41 h0 coordinates outside T. The literal list is
in the certificate. The source restriction ranks are

    rank(C9|J)=8, rank(S8|J)=4, rank(S6|J)=3.

The nonzero h-indicator belongs to C9 and vanishes on J, so it spans the
one-dimensional kernel of C9 restricted to J. Therefore the kernel of
C9 D restricted to J is exactly span(h D). Every baseline S8+k^P or
S6+k^P is zero at coordinate19: S8 is zero there and19 is not in T.
But `(hD)_19=D_19` is nonzero. Consequently restriction to J is injective
on the intersection in (3). Its image lies inside S8|J or S6|J because the
granted point rows vanish on J. Their dimensions prove the bounds.

This argument also permits arbitrary invertible V-by-V block vertex gauges.
The canonical kernel has dimension V and its coordinate19 projection is
injective because D_19 is invertible. The baseline is zero there; restriction
to J remains injective on the intersection and has rank at most4V or3V.
No scalar commutation assumption is required for this gauged-envelope bound.

## 6. Verification, price consequence and next target

Reproduce the exact package with:

```sh
python3 screen.py --repo REPO --seed SEED-SOURCE.json --out output
python3 certify.py --repo REPO --seed SEED-SOURCE.json \
  --screen output/RESULT.json --out output
```

Expected final status: `PASS_PRESCRIBED_SEED_COMPLETION_CERTIFICATES`.
The exact screen reconstructs native inner products, all locality spaces,
canonical rows and the six baseline codes. It emits intersection bases,
annotated homogeneous constraints, every blocking dual witness and all
canonical quotient requirements. The separate compact certificate verifies
the two eight-sets, canonical intersections and the gauge argument's41-point
restriction, so the mathematical lower bounds do not depend on trusting a
large search log.

No all-Hub export of four additional full fields fits the approximately7.746
remaining normalized movement units of the composed fifteen-output history
word: four direct rank8 descents alone cost more than31.6. A positive four-
direction extension would therefore also need a genuinely cheaper acquisition
and delivery mechanism, or a different complete source layout. Dimension
improvement alone is not a complete target budget.

The nearest algebraic target is a complete fitting in a four-dimensional
extension of S8 (or five of active S6) outside the entire canonical gauged
completion class, or a changed preload/interface that avoids retaining those
spaces. The current W15 histories and the partial fifteen-output construction
remain valid. This theorem neither makes their distributed modes available at
ground nor invalidates their actual endpoints.

All five foundational assumptions, strict BIT/complex supplier inequalities,
ownership, precision, compiler and recursive requirements remain. **No new
complete multiplication bound.**
