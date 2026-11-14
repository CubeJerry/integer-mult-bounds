# Saturated high-degree stars force canonical block factors

**Author claim, independent review pending. No new kappa.**

This closes the remaining singular-Schur stratum in the programme's minimum
rank BIT fitting problem. It is an equality-case consequence of the star
inequality of DreamingOfClouds, PR #7114, followed by the programme's already
proved ordered block propagation. It does not supply a physical source,
transport schedule, or multiplication supplier.

## 1. Statements and provenance

Let `Gamma` be a finite simple graph on `n` vertices, with every degree at
least five. Form its star-configuration graph from the `n` point vertices and
one additional vertex for every edge. Different points are nonadjacent; a
point is adjacent to precisely the incident edge vertices; edge vertices
sharing an endpoint are nonadjacent. Disjoint edge vertices are permitted
contacts. A block fitting over a field `k` has identity `V` by `V` diagonal
blocks and zero blocks at noncontacts, without symmetry or commutativity
assumptions.

**Theorem A (saturated star rigidity).** If such a fitting has rank exactly
`(n+1)V`, then it is a vertex gauge of the standard signed star fitting. In
a normalized point-frame factorization, every edge's intrinsic Schur
diagonal is exactly `-I_V`, including over fields of characteristic two.
The standard factors for an edge `{a,b}` are the row with `I` at `a,b,last`
and the column with `I` at `a,b` and `-I` at `last`. The point factors are
the corresponding coordinate row/column. Thus all permitted blocks in this
star graph are invertible; in characteristic two they are identity blocks
before vertex gauge.

The degree-five hypothesis is sufficient, not asserted sharp. A degree-three
counterexample is given below. The theorem does not assert every graph at
degree four is flexible.

**Theorem B (actual BIT graph).** For every field `k` of characteristic two,
every positive integer `V`, and every fitting `K` on the actual 111-port BIT
graph with `rank K = 9V`, there are `U_i in GL_V(k)` such that

    K_ij = U_i (K0_ij I_V) U_j^{-1}.

Here `K0` is the source-pinned canonical binary fitting. In particular all
6,470 allowed foreign blocks are invertible; `rank(K-I)=108V`; and the
previously possible noncommuting, singular-Schur component is empty. This
allows arbitrary nonsymmetric and noncommuting blocks and arbitrary block
width. It is not a finite-field or finite-width search statement.

**Theorem C (rank-excess stability).** In the same star setting, for a fitting
of rank `nV+j`, define the star quantities in Section 2. Then

    sum_a (degree(a)-4) G_a <= 2 |E(Gamma)| (j-V).

Moreover

    sum_e rank(I_V + S_e) <= sum_a G_a.

Consequently if `degree >= delta > 4`,

    sum_e rank(I_V + S_e)
       <= 2 |E(Gamma)| (j-V)/(delta-4).

For the actual `K8` minus one-edge seed, `|E|=27`, minimum degree is six,
and `rank K=9V+h` implies the upper bound `27h`. No optimality of that
constant is claimed. The intrinsic Schur product has rectangular factors
when `j != V`; neither Theorem C nor a finite rank bound makes it an
available physical record.

### Exact dependence and novelty

The rank inequality used below is Proposition 10 (LR), with the summation
from Theorem 11, in DreamingOfClouds's open PR
[CrocSwap/integer-mult-bounds#7114](https://github.com/CrocSwap/integer-mult-bounds/pull/7114),
head `fc90dc68b54d613a0600e5bddd8e4f557a4b4eda`,
`research/p104-port-window-nine/THEOREM.md`. That source proves a rank floor;
it does not state the equality classification, singular-Schur closure, or
the actual 111-port conclusion proved here. The elementary rank argument is
rederived in full below so its precise application is independently
assessable. The source's open PR status is retained; no maintainer admission
is claimed.

The actual-source minimum `9V`, canonical fitting and nine-frame certificate
are prior programme results in `results/bit-minimum-rank-nine/`. The exact
35-role sparse seed, all 76 extension anchors, and invertible-Schur block
propagation are prior results in `results/bit-fitting-rigidity/global/`.
The new step is to force every Schur block to be a unit by saturation, then
apply that existing propagation without its former extra hypothesis.

## 2. Normalized star and the rank inequality

Normalize the point frame in a full-rank factorization `K=C R`. The ambient
space has `n` coordinate blocks of dimension `V`, plus a complementary
space of dimension `j`. Point row and column factors are exactly the
coordinate projection and inclusion. Every edge `e={a,b}` therefore has
factors supported only at `a,b,last`; these zeros follow from the mask.

Write

    alpha_e(a) = C_ea R_ea,
    S_e        = C_e,last R_e,last,
    gamma_e(a) = alpha_e(a) + S_e,
    g_e(a)     = rank gamma_e(a),
    G_a        = sum_{e incident to a} g_e(a).

The edge diagonal condition is

    alpha_e(a) + alpha_e(b) + S_e = I_V.                 (1)

At a fixed point `a`, restrict every incident edge row/column to the
`V+j` coordinates `a,last`. Call those matrices `A_e` and `B_e` and stack
the rows into `A`, concatenate the columns into `B`. Since distinct edges
in this star are noncontacts,

    A_e B_f = 0 (e != f),  A_e B_e = gamma_e(a).

Thus `A B` is block diagonal and has rank `G_a`. Put
`ell=rank A`, `rho=rank B`, `lambda_e=rank A_e`, `mu_e=rank B_e`.

The kernel of `z -> z B` restricted to `row A` has dimension `ell-G_a`.
The kernel of `z -> z B_e` on `row A_e` has dimension `lambda_e-g_e(a)`.
Every row of `A_e` annihilates all the other `B_f`, so the latter kernel
is contained in the former. Therefore

    lambda_e - g_e(a) <= ell - G_a.

Transposing the complete argument gives

    mu_e - g_e(a) <= rho - G_a.

Sylvester's rank inequality applied to the factorization through `V+j`
coordinates gives `ell+rho <= V+j+G_a`. Adding yields

    lambda_e + mu_e - 2 g_e(a) <= V+j-G_a.             (2)

From (1), `alpha_e(a)=I-gamma_e(b)`, hence
`rank alpha_e(a) >= V-g_e(b)`. Both `A_e` and `B_e` have rank at least
`rank alpha_e(a)`, since their appropriate point block product is
`alpha_e(a)`. So `lambda_e+mu_e >= 2V-2g_e(b)`. Substitution into (2) gives

    G_a + V <= j + 2(g_e(a)+g_e(b)).                  (LR)

This is the credited #7114 inequality. Every rank is an ordinary
nonnegative integer over `k`; no characteristic assumption, trace argument,
positive-definite form, or reordering of matrix products was used.

Sum (LR) over edges incident to `a`, then over points `a`. The left hand
side is `sum_a degree(a) G_a + 2|E|V`. Each quantity
`g_e(a)+g_e(b)` appears once from each endpoint, so the right hand side is
`2|E|j + 4 sum_a G_a`. This proves Theorem C's first inequality.

At `j=V`, all coefficients `degree(a)-4` are strictly positive and all
`G_a` are nonnegative. Thus every `G_a=0`, and every individual
`gamma_e(a)=0`. Consequently `alpha_e(a)=alpha_e(b)=-S_e`. Equation (1)
then says `-S_e=I`, or

    S_e = -I_V.                                      (3)

This is the new saturation conclusion. In characteristic two it is exactly
`S_e=I_V`. In particular the two square factors of `S_e` are invertible.

For the stability statement, (1) also gives
`I+S_e=gamma_e(a)+gamma_e(b)`, whence
`rank(I+S_e)<=g_e(a)+g_e(b)`. Sum over edges, then use the first inequality
and `degree(a)-4>=delta-4`. This proves the rest of Theorem C.

## 3. Ordered propagation on the saturated seed

This step specializes the already established programme propagation, and
is included to make Theorem A self-contained. Equation (3) gives invertible
last row/column blocks `u_e,v_e` with `u_e v_e=-I`.

Apply the legitimate edge vertex gauge `C_e -> u_e^{-1} C_e`,
`R_e -> R_e u_e`. Its last blocks become `I,-I`. Denote its point blocks
by `A_ea,D_ea`. If distinct edges `e,f` meet at `a`, their prescribed zero
is

    A_ea D_fa - I = 0.

Hence each displayed endpoint block is invertible. At a point of degree at
least three, choose a third incident edge `f` distinct from any specified
two `e1,e2`; right cancellation of `D_fa` shows
`A_e1,a=A_e2,a`. Denote the common invertible block by `A_a`. Thus
`D_ea=A_a^{-1}`. A global factor-basis change
`diag(A_0^{-1},...,A_{n-1}^{-1},I)` makes every edge row factor canonical
and every edge column factor signed canonical. Compensating point vertex
gauges restore their factors to coordinate inclusions/projections.

All transformations have specified order. At no point are two noncommuting
blocks exchanged. Undoing the vertex gauges proves Theorem A.

## 4. Actual-source application and complete rigidity

The BIT native is pinned by SHA256
`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.
Its actual roots determine the contact graph, rather than identifying it
with the complex-source mask. Use the eight-frame

    F = [0,16,17,32,36,38,67,71].

The predecessor certificate gives exactly 27 edge roles in this frame,
whose pairs are all edges of `K8` except `(0,4)`. Two vertices have degree
six and six have degree seven. All fitting zeros required by the star
theorem are actual prescribed zeros. The rank `9V` factorization has
`j=V`; Theorem A therefore forces all 27 intrinsic Schur blocks to equal
`I`, then makes all 35 seed factors canonical by ordered gauges.

For each of the remaining 76 roles `i`, the existing certificate identifies
eight noncontact seed roles whose canonical nine-bit vectors have rank
eight and whose annihilator is the canonical vector `x_i`. The same binary
coefficient equations over any characteristic-two field force

    C_i = U_i x_i^T,    R_i = x_i V_i.

The actual diagonal `C_iR_i=I`, together with `x_i dot x_i=1`, gives
`U_i V_i=I`. These are square matrices, hence mutual inverses. Applying
that role's vertex gauge completes the canonical factorization. This is
exactly the predecessor's anchor propagation; the saturation theorem is
what removes the prior invertible-Schur hypothesis.

Consequently every minimum fitting lies in the one canonical gauge orbit.
There is no additional disconnected singular-Schur component. No topological
argument or search for all components is needed. The predecessor's exact
binary rank `rank(K0-I)=108` and 6,470 foreign ones imply
`rank(K-I)=108V` and the asserted nonzero full-rank foreign blocks, since
block diagonal conjugacy preserves both properties. This proves Theorem B.

## 5. Controls and limitations

A lower-degree counterexample prevents silently dropping the high-degree
premise. Take `Gamma=K4` and ambient coordinates `0,1,2,3,*`. Keep each
point at its coordinate. Set both row and column factors of its six edges
to the following coordinate units over any field:

    01 -> 1, 02 -> 0, 03 -> *, 12 -> *, 13 -> 3, 23 -> 2.

Every diagonal is one, each edge is supported within its two endpoints and
`*`, and adjacent edges use distinct coordinates. The fitting therefore
has the required zeros and rank five, yet four of its six edge Schur
diagonals are zero; only 03 and 12 use `*`. This is outside the degree-five
theorem. The exact checker verifies the four zero and two nonzero Schur
diagonals directly.

Tests additionally reconstruct the actual 27-edge seed and 76 anchor
premises from the authenticated native, check general star inequalities on
explicit finite representations, use noncommuting vertex gauges, and reject
altered source/mask/diagonal data. The universal proof is Sections 2–4, not
those finite checks. The exploratory solver was used to locate a simple
control only; no SAT/UNSAT output is a theorem premise.

This result rules out an unrestricted minimum-rank block representation
escape. It does not exclude higher-rank global codes, changed zero masks,
nonlinear encodings, altered transport models, or physical architectures
not represented by this fitting problem. The programme's rank-16 class
candidate remains open. No supplier cost, packet count, ownership service,
precision bound, complete BIT/complex source, or new complete kappa follows.
All five foundational assumptions remain explicit and unchanged.

## Open next questions

1. Can a higher-rank fitting exploit a quantitatively small noncanonical
   Schur defect to obtain a physically cheaper source? Theorem C supplies
   a necessary defect budget, not a construction or a transport price.
2. Does a changed intermediate representation or zero mask admit a new
   source with both complete endpoints and a favorable recursive invoice?
   The present rigidity identifies precisely which minimal fitting route
   is closed; it does not constrain such alternatives without a reduction.
3. Is degree four sufficient for Theorem A, and what weaker graph condition
   characterizes its equality classification? This is a separate abstract
   question; it is unnecessary for the actual source, whose degrees are six
   and seven.

Prepared for @CubeJerry with substantial OpenAI-assisted mathematical
research. Credit DreamingOfClouds for #7114's LR inequality and rank-floor
method, its #6933 predecessor for the star framework, and all retained BIT
native/caller contributors for the pinned source. The new equality-case
classification, exact source application, and stability corollary belong
to this S011 protected discovery investigation. No independent human or
formal proof-kernel review is claimed.
