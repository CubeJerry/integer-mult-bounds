# Repair rank, coordinate scaling, and the limit of saturation arguments

**New exact algebraic consequences; no new κ.** This note complements the
proposed paid canonical-quotient repair bridge. It does not construct a
low-rank defect or admit a complete supplier. The native specialization uses
the same original input banks, retained canonical row code, and balanced
proper routes as programme baseline
`d8544284cbd0527cd03a0aad576a2d2c6eddcc0e`.

## 1. Native repair rank is a fixed-space problem

Let `O` be the binary 111-by-111 native orthogonality matrix. Its retained
canonical matrix `K=I+O` has rank nine. At field-bank width b, let H be any
full-row-rank matrix with row space `row(K tensor I_b)`. Let B be an actual
proper-path transfer matrix, including every donor and receiver column.
Thus `B_ij=0` at every nonedge, including the diagonal. Work over any field
of characteristic two; no commutativity assumption is made on its blocks.

Put `C=ker H` and `Delta=B-(O tensor I_b)`. The canonical-quotient defect is

    r = rank([H; Delta]) - 9b
      = rank(Delta restricted to C)
      = rank((B-I) restricted to C).                     (1)

The middle identity is the standard restriction/quotient rank identity:
the kernel of restricting row functionals to C is exactly row H. The last
identity follows because K vanishes on C, so O acts as identity there.
Consequently

    r <= R  iff  dim{v in C : Bv=v} >= 102b-R.            (2)

This is a fixed space on arbitrary native input combinations; it is not a
count of correctly delivered individual output coordinates. At b=5760,
an R=202 repair target requires at least **587,318** independent fixed
directions inside the 587,520-dimensional canonical nullspace.

There is also an inexpensive local necessary check. Write Delta_i for one
receiver's entire b-by-111b error row block. Every row is supported only on
its foreign neighbor set. The retained native canonical restriction theorem
says that no nonzero canonical row is supported there. Hence

    row(Delta_i) intersect row H = {0},
    rank Delta_i <= r.                                  (3)

In particular r<=202 forces at least 5558 independent row directions at
each receiver to annihilate its error against **all** donor columns at
once. These receiver-specific row directions need not be one common
coordinate projection. Individual foreign-block invertibility supplies
neither (2) nor (3) with a useful small R.

## 2. A rigorous isolation theorem inside the seventy-coordinate family

Assume B is one of the retained b=5760 codes with all 6470 foreign blocks
invertible and the same first k=70 output coordinates correct. More
generally let 0<=k<b. Let D_t act as identity on those k coordinates of
every native donor and as scalar t on the remaining b-k coordinates.
For t nonzero define

    B(t)=B D_t,
    r(t)=rank([H; B(t)-O tensor I_b])-9b,
    N=102(b-k).

This is a legitimate algebraic source modification of the retained code:
compose every donor's early and late source matrices with its D_t block.
The early source matrix stays invertible, every foreign block stays
invertible, and the same k corrected output rows persist. Raw caches,
Hub restoration and the actual canonical map still refer to the original
unscaled X. The paid movement word is unchanged. General finite source
matrix compilation already charges the changed ordinary maps; this is
not a free scalar-operation claim.

**Theorem 1 (isolation under unused-coordinate scaling).** For any finite
list of distinct nonzero field elements t_1,...,t_a,

    sum_j max(0, N-r(t_j)) <= N.                         (4)

In particular, at most `floor(N/(N-R))` nonzero parameters have r(t)<=R
when R<N. If R<N/2 there can be at most one. If t is such a parameter,
every other u has

    r(u) >= N-r(t) >= N-R.                              (5)

**Proof.** Let U consist of inputs in C supported only on the unselected
coordinate positions. The canonical tensor structure gives dim U=N.
For v in U, D_t v=t v and O v=v. Thus

    (B(t)-O)v=0 iff Bv=t^{-1}v.

These zero-error subspaces for different nonzero parameters are eigenspaces
of the one fixed operator B for distinct eigenvalues. They have direct
sum, even though B need not preserve all of U. Each subspace lies in U,
and its dimension is at least N-r(t), by restricting (1) further to U.
Their dimensions therefore sum to at most N. This proves (4), and the
remaining assertions follow immediately. The argument uses actual vector
subspaces, not algebraic multiplicities or a diagonalizability assumption.

**Theorem 2 (large defect for generic scale).** All but at most N field
elements t have r(t)>=N, when r(0) is interpreted only algebraically.

**Proof.** Choose a basis matrix Q for U. The matrix
`(B D_t-O)Q=t BQ-Q` has column rank N at t=0. One of its N-by-N minors is
therefore a nonzero polynomial, of degree at most N and with nonzero
constant term. If r(t)<N this minor vanishes. The univariate root bound
proves the claim. The parameter t=0 is not an admissible invertible source
map and is used only as a polynomial witness.

For the actual seventy-coordinate instance, N=580380. The proposed
R=202 movement screen therefore has the following consequences:

* At most one nonzero scalar in this family can pass the repair-rank screen.
* If one does, every other scalar has repair rank at least 580178.
* Over the retained GF(2^30), at least `(2^30-1)-580380` nonzero scalars
  have repair rank at least 580380.

This does not exclude the existence of the exceptional structured point.
It proves that common foreign invertibility and seventy correct rows are
stable properties that do **not** give a stable low-rank native completion.
A successful construction must control the large fixed subspace in (2),
rather than rely on the existing generic nonzero-minor argument alone.
The numerical R=202 screen is an external, necessary movement allowance;
this note does not establish its finite caller or ordinary-cost admission.

## 3. A sharp repair-slack version of the common-function bound

The existing varying-stripe obstruction derives a plane alphabet ceiling
538644 from exact saturated receiver recovery, against the canonical-null
input dimension 587520. The difference 48876 must **not** automatically
become a lower bound on a newly allowed repair channel. The plane ceiling
itself uses exact saturation, which the repair channel changes.

Here is the valid linear replacement. Work in a finite-dimensional space
of input row functionals over any field. A receiver i needs a target
subspace T_i of dimension p. Its visible port tuple spans Z_i, with
dim Z_i<=p. A shared repair transcript spans R, of dimension at most r,
and correctness gives T_i subset Z_i+R. Let U_D be the row space of one
port seen by i, so U_D subset Z_i. Then

    codim_(U_D)(U_D intersect T_i) <= r.                (6)

Indeed, `T_i+Z_i subset Z_i+R` implies

    dim Z_i - dim(Z_i intersect T_i)
      = dim(Z_i+T_i)-p <= dim Z_i+r-p <= r.

Restricting the quotient map to U_D proves (6). For a nonempty set S_D of s receivers seeing a common port, the shared
repair space improves the naive sum-of-codimensions bound to

    dim U_D <= dim(intersection_(i in S_D) T_i)
               + (s-1) r.                            (7)

To prove this, put U=U_D, q=dim U and A=U+R. Within Z_i+R, the dimension
formula and dim T_i>=dim Z_i give

    dim(T_i intersect A)
      >= dim T_i + dim A - dim(Z_i+R)
      >= q + dim(Z_i intersect R)-dim(U intersect R)
      >= q.

All these intersections lie in A of dimension at most q+r. Intersecting
s subspaces of dimension at least q inside that one ambient space leaves
dimension at least q-(s-1)r. The intersection is contained in every T_i,
proving (7). In fact r may be replaced by dim R-dim(U intersect R).

The factor s-1 is sharp. In particular it cannot in general be replaced
by one when s>2, even though the **same** repair is shared everywhere.

**Sharp control.** Take U=span(e_1,...,e_(s-1)), R=span(z), T_0=U, and

    T_i=span({e_j : j != i} union {e_i+z}),  1<=i<s.

All s targets have dimension s-1 and are recoverable from the common
port tuple U plus the one-dimensional common repair R. Their intersection
is zero: T_0 removes z and each other target then removes its corresponding
e_i coordinate. Thus dim U=s-1 attains (7) with r=1. Direct sums give the
same sharpness for arbitrary positive r. All maps here are linear.

The smallest version has two independent inputs x,y and one shared port
z=x. With repair x+y, two receivers recover x and y respectively. Without
repair, requiring the same one-symbol port to be an invertible label of
both independent targets would force a nonexistent common information
channel. Therefore exact-capacity factoring conclusions cannot simply be
reused after adding repair information.

Inequality (7) is a robust local gate, not a native source exclusion. In
particular it does not restore the old coloring census without proving
that the candidate still supplies the required target subspaces and their
native gluing. Arbitrary nonlinear processing needs a separate entropy or
common-function version and is not claimed here.

## 4. Finite checks and open next questions

The accompanying exact GF(8) controls check (1), (4), the root-count gate,
the local bound (6), and the sharp shared-repair counterexample. They
corroborate the written all-field proofs; they are not an asymptotic theorem
or a materialized full native coefficient table.

The 3035 pooled native source/receiver cut probes in the separate finite
screen found no rank-capacity violation. Every integer max-flow value
matched its residual cut capacity. This is bounded exploratory evidence,
not a proof that all native joint cuts pass or that a sum code exists.

Open next questions:

1. Construct a same-original-source B with at least 587318 fixed canonical-
   null directions and an admissible complete invoice, or prove an actual
   physical lower bound on its defect.
2. Find a native-specific strengthening of (7) that uses source incidence,
   causality and shared repair dependencies, rather than the invalid
   assumption that the old exact saturation ceiling survives unchanged.
3. Use actual candidate transfer matrices to test (3) before computing a
   full canonical-quotient rank. The current generic existence proof does
   not provide those matrices.

Credit @CubeJerry and the retained native, balanced atlas, source quotient,
seventy-coordinate and canonical normalization authors. This proof package
was developed by S026 Worker C with substantial OpenAI assistance. No human
or formal-kernel review is claimed.
