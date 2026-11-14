# One arbitrary packet-width quotient cannot sparsify the canonical BIT code enough

**Author theorem, independent review pending. This is an all-field/all-width
code theorem and a conditional target exclusion, not a physical source,
supplier, or new complete kappa.**

The new step is a basis-free injectivity argument. It promotes the earlier
scalar one-direction obstruction to an arbitrary operator-valued extension
of quotient dimension at most one whole record width. The extension need not
be a tensor product, its blocks need not commute, and its row maps may initially
be singular. A support-saving row itself forces the relevant map to be
invertible. No simultaneous diagonalization is assumed.

## 1. Exact proposition and inherited source facts

Let `k` be any field of characteristic two, let `V >= 1`, and let `K` be the
pinned binary canonical fitting of the actual 111-port BIT source. Thus
`K_ii = 1`, `K_ij = 1` at every permitted foreign real-orthogonal contact, and
`K_ij = 0` at every forbidden contact. Its binary row code `C` has dimension
nine. Write

    C_V = C tensor k^V <= k^(111 V).

For a block fitting `A`, each block has size `V` by `V`, `A_ii = I_V`, and
`A_ij = 0` whenever `K_ij = 0`. No symmetry, invertibility of foreign blocks,
or commutativity is imposed. Set

    d = dim_k((row(A) + C_V) / C_V),
    ell_i(A) = 1[foreign block support of row i > 36]
             + 1[foreign block support of row i > 52].

Here a foreign block belongs to the support when the entire matrix is
nonzero, even if its rank is one.

**Theorem.** If `d < V`, every permitted foreign block of `A` is nonzero and
`sum_i ell_i(A) = 222`. If `d <= V`, then

    sum_i ell_i(A) >= 205.

The bound 205 is sharp as an algebraic block-support statement for every
`V`: tensor the already admitted scalar seventeen-savings witness with
`I_V`. This does not establish that 205 paid visits suffice, or that its
logical fitting has a physical realization.

Consequently, the independently reviewed all-route retained-caller condition
`sum ell_i <= 194` implies

    dim((row(A) + C_V) / C_V) >= V+1.                 (Q)

If the whole relevant historical X-row space is `W` and `row(A) <= W`, it
also implies `dim((W+C_V)/C_V) >= V+1`. In particular, no such successful
history containing `C_V` can have dimension at most `10V`.

This is not a lower bound `rank A > 10V` for arbitrary fittings: `row(A)`
need not contain `C_V`. Nor is it a bound on the number of packet identities;
actual evolving histories can exceed their current packet dimension.

The source facts used below are precisely the admitted one-extra-coset and
seventeen-savings geometry, at the baseline commit recorded in SOURCES.json:

1. For `Z_i = {j:K_ij=0}`, the canonical restriction has rank eight and
   `C|Z_i` has kernel `span(K_i)`.
2. The canonical evaluation columns on `Z_i intersect Z_j` have rank seven
   for all distinct receivers. The canonical coefficient normals `a_i` are
   distinct nonzero binary vectors in dimension nine.
3. The actual foreign degree census is
   `{55:1,56:11,57:16,58:36,59:28,60:13,61:5,62:1}`.
4. The admitted exact real-root geometry bounds the scalar support envelope
   in Section 4 by seventeen. That envelope depends only on support sets,
   not on the scalar nature of the values. Its exceptional finite geometric
   premises and independent reconstruction remain dependencies here.

Binary restriction ranks are unchanged under characteristic-two scalar
extension. Tensoring the restriction kernel with `k^V` is exact over a field.

## 2. A deleted block forces full quotient injection

This step is basis-free and applies to any scalar canonical code with the
one-dimensional local-kernel property above.

For receiver `i`, map a coefficient row `u in k^(1 x V)` to the quotient:

    phi_i(u) = u A_i + C_V.

Its image lies in the `d`-dimensional quotient in the proposition. Suppose
`u` belongs to the kernel. Then `u A_i` is a canonical block row, and it
vanishes on `Z_i` because `A` is a fitting. The local canonical kernel forces

    u A_ij = K_ij v       for all j

for one `v in k^(1 x V)`. At the diagonal, `A_ii=I` and `K_ii=1`, so `v=u`.
If even one permitted foreign block `A_ij` is zero, then

    0 = u A_ij = u.

Therefore `phi_i` is injective whenever row `i` deletes any canonical
contact block. Such a row requires `d >= V`. This proves the first part of
the theorem: when `d<V`, all canonical contacts survive. Their degrees are
at least 55, so every `ell_i` is two.

For `d=V`, every row deleting a canonical contact maps isomorphically onto
the SAME full quotient. This forced common quotient is the feature absent
from a general higher-dimensional operator extension.

## 3. Operator gluing for the deletion rows

Let `I` be all receivers deleting at least one permitted foreign block.
Rows outside `I` have `ell_i=2`. If `|I| <= 3`, they can save at most six
visits, already stronger than required. Assume `|I| >= 4` and `d=V`.

Choose a matrix `H` of `V` rows representing a basis of the quotient. For
every `i in I`, the preceding isomorphism gives

    A_i = R_i + M_i H,

where each row of `R_i` belongs to `C_V` and `M_i` is an invertible `V` by
`V` matrix. Let `Q_i=M_i^-1 R_i`. Express this canonical matrix row in the
nine fixed binary basis words, with matrix coefficients `B_i,1,...,B_i,9`.
At a forbidden source column, `Q_i,j + H_j=0`.

For `i,l in I`, the coefficient tuple `B_i-B_l` therefore annihilates the
canonical evaluation columns on `Z_i intersect Z_l`. Their exact rank-seven
certificate gives, entry by entry,

    B_i-B_l in span_k(a_i,a_l) tensor Mat_V(k).

Any four distinct binary normals span at least three dimensions, also over
`k`. Apply the earlier elementary three-normal gluing argument to each
matrix entry. There is ONE common coefficient tuple `B` and matrices `L_i`
such that

    B_i = B + a_i L_i.

This step is linear over `k`. It never multiplies two unknown matrix
coefficients, swaps their order, or assumes a common invariant subspace.
Let `G = H + B` interpreted as a canonical matrix row added to `H`. Then

    support(G) <= intersection_(i in I) T_i,
    A_ij = K_ij (I_V - M_i G_i) + M_i G_j.           (1)

Here `T_i={j:K_ij=1}`. The support statement follows from the same forbidden
equations. The identity diagonal determines `M_i L_i=I-M_i G_i` and gives
(1) with its stated multiplication order. In characteristic two the minus
sign equals plus; it is retained to show the diagonal normalization.

The quotient classes of the rows of `G` are still a basis. Hence `G` is
nonzero, and its block support is nonempty. This is a matrix-valued common
representative; it is not a claim that the quotient is generated by a scalar
coset tensored with `k^V`.

## 4. The geometric seventeen-savings envelope is unchanged

Put `S=support(G)`, `s=|S|`, and let `r` be the real dimension spanned by
the native source root lines in `S`. Put `J=I intersect S`, `j=|J|`, and
`U=I minus S`.

For `i in U`, `G_i=0`, so (1) becomes

    A_ij = K_ij I_V + M_i G_j.

Only columns in `S` can disappear. This row loses at most `s` foreign
nonzero blocks, regardless of the ranks or commutators of the matrices
`G_j`. For `i in J`, grant both visits saved without imposing any further
algebraic restriction.

Every root in `U` is orthogonal to all of `S`; every root in `J` is
orthogonal to every other root in `S`. Thus the same exact root-flat
inequalities as in the credited scalar proof hold:

    r <= s <= N_r,
    0 <= j <= min(r,s),
    s <= j + N_(r-j),
    |U| <= N_(8-r).

The source bounds are `N_0=0,N_1=1,N_2=3,N_3=6,N_4=12,N_5=20,N_6=36`,
with the safe bounds `N_7=N_8=111`. If `F(t)` counts source rows with
canonical foreign degree at most `t`, the total savings obey

    sum_i (2-ell_i)
      <= min(N_(8-r),F(52+s))
         + min(N_(8-r),F(36+s)) + 2j.                (2)

The earlier exact 569-case enumeration and finite geometric refinements
bound this expression by seventeen for every realizable support. For
clarity, the only loose-envelope cases requiring the finite refinements are
`(r,s,j)=(3,5,0),(3,6,0),(4,4,3),(4,4,4)`. The rank-three cases have at most
seventeen orthogonal rows of the required degree; the orthogonal-four cases
have at most seven such rows and therefore save at most fifteen. Every
other envelope case gives at most sixteen.

Those geometric premises count only actual root lines and canonical degrees.
They apply to the block support `S` exactly as they apply to a scalar support.
No enumeration of operator matrices is being extrapolated to all widths.
Thus `sum ell_i >= 222-17=205`, proving the theorem.

## 5. Scope, gauges, sharpness, and physical consequences

The sharp scalar witness has support set
`S={0,2,38,41,42,45}`, takes `h=1_S`, and changes the twenty rows orthogonal
to its real span by adding `h`. Its scalar fitting has quotient dimension
one, rank ten and `ell=205`. Tensoring it with `I_V` gives quotient dimension
exactly `V` and the same whole-block support statistic for every `V`.

For any invertible block-diagonal coordinate gauge `D`, replace the reference
code by `C_V D` and conjugate the fitting by `D`. Quotient dimensions and
whole-block supports are unchanged. The theorem therefore holds relative to
every canonical vertex gauge, with the reference code named explicitly.

The target implication uses only the separately proved all-route `ell<=194`
condition, under its complete retained caller, operation and ownership
assumptions. It introduces no changed movement invoice. The scalar theorem's
older no-Y-feedback physical arrival premise is not imported. Actual arbitrary
Y feedback and public/owned turns are covered only to the extent stated by
the all-route dependency.

Condition (Q) constrains the canonical quotient of the **whole relevant
history** when that history supplies the fitting. A terminal core of rank
three and a static six-mode complement do not identify this quotient. A
history can obey the condition without being physically acquirable or
useful. Conversely, the theorem does not exclude an arbitrary rank-ten-V
code whose sum with the canonical reference has larger quotient dimension.

Controls include the sharp tensor witness, genuinely noncommuting matrix
representatives and quotient maps, singular maps that cannot erase a block,
and an explicit `V=2,d=3` fitting whose deletion rows project onto distinct
two-dimensional quotient subspaces. The last control prevents extending the
common-full-quotient argument to `d>V`. A separate eight-coordinate fitting
has `ell=183` and lies outside this theorem's quotient bound; it prevents an
unrestricted canonical-extension impossibility claim.

Both strict suppliers and all five foundational assumptions remain open.
No new complete kappa is claimed.

## Open next questions

1. Construct an actual retained-pivot continuation whose historical quotient
   exceeds one whole width and which retains enough current useful modes to
   finish the six-mode residual within the complete signed caller budget.
2. For quotient dimensions strictly between `V` and `2V`, quantify how the
   distinct injective deletion-row images can overlap. The present proof
   identifies the required subspace arrangement but does not bound its
   multi-image savings.
3. Extend the forced-injection argument to a useful general code/local-kernel
   setting. The algebraic lemma is abstract; the constant seventeen is tied
   to this exact native geometry.

Prepared for @CubeJerry with substantial OpenAI assistance. Credit the
one-extra-coset and quotient-direction-savings authors/reviewers for gluing
and finite source geometry; the all-route authors/reviewers for the target
cap; and the native/canonical code contributors. This package's new claim
is the forced quotient injection and consequent arbitrary-operator
packet-width gate. No human or formal-kernel review is represented.
