# Receiver-downset projection excludes the fifteen rank16 candidates

**Author proof with exact source certificate; independent review pending.
No new complete kappa.** The result excludes a specified historical-code
family. It is not a general q8 impossibility theorem.

## 1. Statement

Use the actual111-root BIT source and its fifteen-class code U. Let C be the
canonical rank-nine binary fitting code. The predecessor canonical-coset
classification gives dim(U)=15, dim(C)=9, dim(U+C)=19, and one distinct
nonzero coset in C/(C intersect U) for each of the fifteen classes.

Fix a class c and any representative i in it. Write

    W_c = U + span(K_i),    dim W_c = 16.

Let k be any characteristic-two field, V>=1, and W_(c,V)=W_c tensor_k k^V.
Assume a complete word in the admitted monotone whole-record model has the
all-history X-projection normal form

    row_x(H at chart A) subset W_(c,V) + LocalX(A).       (NF_c)

For example, the admitted Y-feedback normalization implies this whenever its
actual historical code satisfies row(G_x) subset W_(c,V). This is a hypothesis
on actual histories, not physical availability of an abstract code.

Original X and Y follow their prescribed upward paths. There are q persistent
whole-V packet paths, each born at Hub and moving monotonically downward,
without restart. Other generated records are zero-born stationary caches;
additional upward local records do not weaken the argument. Arbitrary
cocharted linear block arithmetic and original-Y feedback are allowed, with
the stated normal form maintained. There is no uncounted downward traffic or
preloaded nonlocal record born inside a receiver region.

**Theorem.** Every such complete word has q>=14. Therefore none of the fifteen
advertised W_c candidates can be the historical code of a q8 realization
under this model, including arbitrary noncommuting block operations satisfying
(NF_c). This is stronger than the earlier q>=9 proper-chart quotient screen.

The conclusion applies to the specified canonical-extension codes. It does
not exclude arbitrary rank16 spaces with a different extra direction, higher
historical codes, mixed histories outside W_c, extra descending routes, or a
different physical representation.

## 2. Exact receiver shortenings

For a real chart A, LocalX(A) is the coefficient space supported on original
X indices whose starting root lines lie in A, tensored with k^V when needed.
For each actual receiver i, let d(i) be its class and define

    L_i = K_i + u_(d(i)).

The source certificate proves these binary facts:

1. U intersect LocalX(F_i) = 0 for every actual receiver.
2. (U+C) intersect LocalX(F_i) = span(L_i), of dimension1.
3. The real support of L_i spans the entire actual rank-seven F_i.
4. W_c intersect LocalX(F_i) is span(L_i) if d(i)=c, and zero otherwise.

All intersections here refer to coefficient vectors supported on the original
root lines, not real spans of coefficient vectors. The real rank in item3 is
a separate geometric check.

The checker authenticates the native bytes and the exact fifteen-class
partition. It builds K from actual rational-root orthogonality and U from the
partition, then an independent19-row basis of U+C. At each receiver it masks
to the forbidden original columns: the resulting ranks are15 for U and18
for U+C. Since nonzero L_i belongs to U+C and is supported at F_i, this proves
the stated one-dimensional kernel. Its canonical quotient coset is the one
assigned to class d(i), so item4 follows. The checker also directly verifies
all15x111 instances, instead of relying only on that implication.

These are exact finite-source linear-algebra premises. Binary matrix ranks
are unchanged by extension to any characteristic-two field: an independent
binary minor remains nonzero, and the binary row dependencies remain true.
For block width V, the forbidden-column restriction is the scalar map
tensored with the identity. Its kernel is the scalar kernel tensored with
k^V. Thus the zero intersections and dimension-V enabled shortenings hold
for every k,V; they do not assume that block arithmetic commutes.

The native pin is
`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.
The partition pin is
`7c725fc39b03e00244d31860ce76a79f0011f90b15b22bb2f7e97f8d5af64117`.
CERTIFICATE.json gives all111 masks, local vectors, quotient classes,
shortening dimensions and the complete67-subspace binary quotient check.

## 3. Choose the receiver region, not every proper chart

Let D_c consist of every chart A contained in at least one actual receiver
facet F_i with d(i)!=c. It is a union of downsets and hence downward closed.
It includes all those terminal facets and their possible predecessor charts;
it excludes Hub. The definition ranges over real geometric subspaces, not
only the native's existing chart IDs.

For every A in D_c, choose a containing outside-class receiver F_i. Then

    LocalX(A) subset LocalX(F_i),
    W_(c,V) intersect LocalX(A) = 0.

Consequently the W component in (NF_c) is unique. For an X coefficient row
h=w+l with w in W_(c,V) and l local at A, define

    pi_A(h)=w.

The map is linear. If A subset B and both are in D_c, the two projections
agree on W_(c,V)+LocalX(A): this follows from uniqueness at the LARGER chart B.
In particular, a row physically carried downward from B to A and satisfying
the normal form at both ends has the same projection at both ends. This
handles shrinking local remainders; no inverse of a packet-through block is
assumed.

The earlier global quotient argument annihilated all short-class local modes
available at arbitrary proper charts. Those charts need not lie inside any
actual receiver region. Here they do not create an ambiguity in pi: the exact
receiver shortenings are zero throughout D_c. This is why the stronger14-class
count is valid while a global quotient by all properly supported words gave
a much weaker screen.

## 4. Only q first packet entries seed the projection

For each descending packet, take its first actual arrival in D_c, if any.
Because D_c is downward closed, a monotone descending path enters it at most
once and cannot subsequently leave. Let S be the span of the V projected
rows at all such first arrivals. These are actual historical values at their
actual times. They may be linearly dependent. In all cases

    dim S <= qV.

Including a future arrival in this fixed algebraic span grants no early
physical access to it. A chronological induction proves that the projection
of every actual history inside D_c lies in S:

- An original X born inside D_c is local at its root line and has projection0.
  An X born outside cannot enter by upward movement, because D_c is downclosed.
- Original Y has zero initial X projection. Unknown original-y coefficients
  remain in the value word; taking its X projection does not set y=0.
- A generated zero cache introduces no projected X information.
- Coframe linear operations preserve the span of projections, including
  arbitrary original-Y feedback and left multiplication by block operators.
- A move between nested charts inside D_c preserves its projected row space.
  An upward path cannot enter D_c from outside.
- A first descending packet entry contributes one of the counted seed rows.

This argument concerns actual chronology. Repeated reads of a stationary
cache, singular packet-through blocks, or copies formed from existing local
histories cannot introduce an additional seed. A downward copy entering from
outside would be an additional counted route; a nonlocal initialized record
inside would violate the hypotheses. Restarting or returning a packet would
require a new entry count and is not silently covered by q.

## 5. Fourteen independent endpoint projections

For a completed receiver i outside class c, its final X coefficient block row
is e_i tensor I. The class contains mutually orthogonal actual roots, hence

    e_i tensor I = u_(d(i)) tensor I + local_i,

where local_i is supported on the other roots in the same class, all inside
F_i. In characteristic two the own coefficient cancels. Since F_i is in D_c,
uniqueness gives

    pi_(F_i)(e_i tensor I) = u_(d(i)) tensor I.

Choose one receiver from each of the14 outside classes. Their class rows have
disjoint nonempty supports, so the resulting projected row space has dimension
14V. Section4 contains it in S. Therefore14V<=qV and q>=14, proving the theorem.

No claim that every possible rank16 code is a W_c is used or made. The result
removes the specified fifteen candidates from the q8 construction search.

## 6. A broader scalar canonical-extension hierarchy

For a scalar code W=U_k+E with E subset C_k, write H for its quotient image
inside (U_k+C_k)/U_k, which has dimension4. Let h=dim_k H. A class has a
nonzero receiver shortening precisely when its nonzero canonical quotient
vector belongs to H. The classes whose vectors do not belong to H are
receiver-invisible to local W modes; applying the same downset proof to their
facets forces q at least their number.

The15 class vectors are exactly all nonzero vectors of a binary four-space.
Their intersection with any k-linear H is a binary subspace of dimension at
most h, because binary linear independence persists over k. At most2^h-1
classes are enabled, so

    q >= 16 - 2^h.

For binary H this count is exact. The complete67-subspace check gives:

| Added canonical quotient dimension h | dim W | Necessary q |
|---|---:|---:|
|0|15|15|
|1|16|14|
|2|17|12|
|3|18|8|
|4|19|0 from this gate|

Thus, for a scalar historical code containing U and contained in U+C, q8
requires at least three additional canonical directions, hence dimension18.
The dimension18 row passes this gate only; it is not a physical construction.
The same packet bound holds when a fixed scalar W is tensored across width V.
No18V lower bound is asserted for arbitrary non-tensor block subspaces between
U tensor k^V and (U+C) tensor k^V.

## 7. Controls, provenance, and next step

The checker retains the true one-dimensional local kernel at own-class facets;
it does not incorrectly make pi unique there. Adding the own coordinate to
any L_i violates its local-support test. It checks every actual facet, class
orthogonality, all canonical quotient labels and all67 binary subspaces.
These checks supply finite source premises; Sections3–6 prove the unbounded
chronological and field/block statements.

The argument is a refinement of the programme's historical-class quotient
method, using its admitted Y-feedback normal form and exact canonical cosets.
It preserves all native/source and prior contributor credit. Prepared for
@CubeJerry with substantial OpenAI research-agent assistance. Independent
human or formal-kernel approval is not claimed.

The next construction must leave the ruled-out W_c family. A mixed-Y exchange
with outgoing X projection K_i+e_i is one concrete candidate because e_i is
outside U+C; its actual word, unknown-Y cancellation, physical costs and
remaining endpoints must be verified separately. Higher canonical extensions
also remain open subject to the new hierarchy. Both strict suppliers and all
five foundations remain; No new complete kappa.
