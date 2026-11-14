# A quadratic pivot filter with proper-cover charge120

**Author finite source construction, independent review pending. No new kappa.**

This is the algebraic fitting proposed by the construction worker, evaluated
on its pivot92. It is not an assembled physical nine-route supplier. The
contribution here is its exact real proper-cover certificate and rank
accounting, supporting that worker's chronological construction attempt.

Let K be the authenticated native111 fitting, C its rank9 scalar code, and
k any characteristic-two field. Put h=K_92. Define

    A_jk = K_jk [1+h_j+h_k].

Since h has binary values, the bracket is1 exactly when h_j=h_k. Thus
A_j=K_j star h when h_j=1, and A_j=K_j+K_j star h otherwise. The own
entry is1 and every forbidden entry remains0. In particular A is a valid
scalar fitting, and its whole-block tensor extension A tensor I_V is
valid at every width.

All scalar rows lie in C+h star C, whose dimension is16. Exact binary
elimination gives

    rank A =15,
    dim(row A+C)=16,
    dim((row A+C)/C)=7.

These ranks remain valid over every characteristic-two extension field.
There is no assertion that canonical C is contained in row A: the
enlargement rank16 is intentionally distinct from the actual rank15.

For every receiver, the foreign support spans the full real facet of
rank7, so chi_j is never0. The exact two-proper-subspace cover decision
finds102 receivers with chi_j=1 and9 with chi_j=2. Hence chi(A)=120.
The explicit102 cover partitions alone certify the sufficient upper
bound chi(A)<=120; independently reproducing the negative search is
unnecessary when only that upper bound is used in a feasibility budget.

The nine receivers with chi2 are

    21,33,45,51,68,76,84,92,99.

Receiver92 retains all57 canonical foreign contacts. Each of the other
eight retains27 contacts, the complete exclusive-neighbour configuration.

## Constructive two-distance geometry of the covers

The primary certificate is now `check_geometry.py` / `GEOMETRY.json`.
It does not invoke the exploratory cover search below. Instead it gives
explicit rational chart normals and proves the obstruction at each of
the nine exceptional rows.

Normalize the source roots to squared length4 and first nonzero
coordinate positive. Their fourteen four-coordinate supports, completed
with all eight sign patterns on each support and the eight coordinate
roots2e_a, give120 distinct root lines. The certificate checks that the
native111 are a subset and that every pair of distinct completed roots
has inner product0 or+/-2. Let M be the nine omitted root lines.

Fix pivot root r and another native root s. If r is orthogonal to s,
the retained foreign support is the rank6 common-flat support together
with the pivot line. This gives a rank6-plus-rank1 cover and chi<=1.

Now suppose r dot s is+/-2. The full exclusive configuration is

    X(r,s)={x : x dot s=0 and x dot r is nonzero},

of size27. If an omitted line z lies in X(r,s), orient its norm4 vector
so r dot z=2. Every retained x in X(r,s) is on a different line from z.
Orient x likewise so r dot x=2. The projection

    a=r-(r dot s)s/4

has squared norm3 and is orthogonal to s. If x dot z=-2, then
||x+z||^2=4 but a dot(x+z)=4, contradicting Cauchy--Schwarz since
16>3*4. The completed root angle set therefore forces x dot z to be0
or2. Equivalently, without choosing a sign for x,

    (x dot z)(x dot(z-r))=0.

Thus every retained exclusive contact lies in one of the two explicit
proper receiver subspaces

    F_s intersect z-perp,
    F_s intersect (z-r)-perp.

Both are proper: z is a nonzero vector orthogonal to s, while z-r has
squared norm4 and inner product+/-2 with s, so it cannot be parallel to
s. These rational normals are recorded for all45 such native receivers.
This is a constructive root-geometric explanation for the successful
two-chart covers, not a heuristic inferred from a rank-deficient
quadratic evaluation matrix.

If X(r,s) contains no omitted line, all27 contacts remain. Their exact
quadratic evaluation span in Sym^2(F_s) has dimension27, checked by a
nonzero minor modulo101. They satisfy the real quadratic equation

    Q(x)=||x||^2-(r dot x)^2=0.

On F_s, the associated symmetric matrix is I-a a^T. Since ||a||^2=3,
it has six eigenvalues1 and one eigenvalue-2, hence rank7. The kernel
of the quadratic evaluation map, not of this nonsingular matrix, is
therefore the one-dimensional span of Q. A union of two proper subspaces would yield the product of
two nonzero linear forms vanishing on the support; such a product has
symmetric rank at most2. This contradiction proves chi=2.

At pivot92 there are57 orthogonal receivers,45 nonorthogonal receivers
with a missing exclusive root, and8 nonorthogonal receivers retaining
the full27-point exclusive configuration. The pivot row itself retains
full canonical support and has quadratic span28. Every row's foreign
support has real rank7, independently certified modulo101. These facts
give exactly102 charges1 and9 charges2.

The chart-normal statement is geometric. Availability or compilation of
the stated chart frames at the required physical price is a separate
obligation; an omitted source root is used as a public rational normal,
not as an unprovided input data value.

## Exploratory decision procedure and certificate scope

The source pin is checked by the shared author loader in
`quadratic-exterior/author/check.py`:
`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.
The final integrated checker should either preserve that dependency path
or inline the same transparent source-loading routine.

At receiver j, delete a coordinate at which its rational normal is
nonzero. This identifies its real rank7 facet with R^7. A two-proper
subspace cover exists exactly when the support vectors can be partitioned
into two subsets each of rational rank at most6. Rational rank suffices:
any real cover can be replaced by the rational spans of its assigned
source roots. Conversely such spans give a real proper cover.

Reduce the integer source vectors modulo101. A real cover gives a
modular cover, because reducing an integer matrix cannot increase rank.
To decide modular covers, maintain two generated subspaces U,W, initially
zero. If their union covers all support points, succeed. Otherwise choose
the first uncovered point x. Any eventual cover extending U,W must put x
in one of the two spaces, so branch by adjoining x to U or to W, provided
that the resulting dimension remains at most6. Adding an uncovered point
strictly increases the chosen dimension. Branch depth is at most12.
Memoize unordered pairs of reduced-row-echelon bases and omit the
redundant symmetric branch when U=W.

This finite recursion is complete by induction on the remaining rank
budget: a solution assigns the chosen uncovered point to one of its two
covering spaces, preserving a feasible branch. A failed modular search
therefore proves failure of a real cover. For every successful modular
search, the output partition is independently checked with exact rational
elimination before it is accepted. Thus no positive modular coincidence
is mistaken for a real cover.

The exploratory code stores each accepted partition as native source indices. The
102 positive partitions can be checked with any independent rational
rank implementation, without importing the search code or trusting its
negative decisions. Every support has a nonzero rank7 minor modulo101,
proving that one proper subspace does not suffice.

## Physical and recursive obligations retained

The filtering identity says which linear forms should be available. It
does not supply acquisition order, simultaneous storage, original-input
restoration, dirty-cache erasure, pointwise ownership, or full recursion.
Its seven canonical quotient directions cannot be translated directly
into seven physical packet paths. The actual rank15 and enlargement16
must remain distinct in any interface admission. The complex companion,
ordinary BIT completion, precision, uniformity and all foundational
assumptions are unchanged.

The construction worker's existing one-pivot chronological prefix is
separate evidence. Whether that prefix can implement this entire fitting
within the marked nine-route budget remains open.

## Reproduction

```sh
python author/check_geometry.py --repo /path/to/integer-mult-bounds --output author/GEOMETRY.json
python author/probe.py --repo /path/to/integer-mult-bounds --pivot 92 --output author/PIVOT92.json
```

The primary expected status is `PASS_AUTHOR_PIVOT92_ROOT_GEOMETRY`.
Both summaries give rank15, enlargement16, chi120, histogram{1:102,2:9}.
Credit the construction worker for the pivot-filter proposal, the native
source and prior proper-cover definitions, @CubeJerry, and AI assistance.
