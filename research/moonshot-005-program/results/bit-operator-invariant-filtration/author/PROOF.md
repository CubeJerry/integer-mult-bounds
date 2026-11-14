# Invariant operator layers require additive canonical innovation

**Author theorem; independent review pending. No physical source, strict
supplier, foundational discharge, or new complete kappa.**

This identifies a structural limitation of operator-code proposals. A
fractional canonical quotient cannot be obtained merely by taking commuting
matrix coefficients or upper-triangular noncommuting ones. Small common
invariant layers each incur their own quotient requirement.

## 1. Precise statement

Let `k` be any characteristic-two field and let `V>=1`. On the actual pinned
111-port BIT graph, let `K` be the canonical binary fitting, `C=row(K)` its
nine-dimensional scalar code, and `C_V=C tensor k^V`. Let `A` be a block
fitting with `V` by `V` blocks, identity diagonal, and zero blocks wherever
`K` has prescribed zeros. Define

    d(A) = dim((row(A)+C_V)/C_V),
    ell_i(A) = 1[foreign block support(A_i)>36]
               +1[foreign block support(A_i)>52].

Suppose `sum_i ell_i(A)<=194`. No symmetry, foreign-block invertibility,
commutativity, or separability is assumed unless explicitly stated below.

**Theorem A (common invariant filtration).** Suppose that, over `k` or any
field extension `L/k`, every coefficient block `A_ij` preserves the same
flag of value subspaces

    0=M_0 < M_1 < ... < M_s=L^V,
    v_a=dim_L(M_a/M_(a-1)).

Then

    d(A) >= V + sum_(a=1)^s ceil(v_a/17).             (F)

If `b` original rows satisfy `ell_i(A)=0`, set `c=17-min(b,9)`. Then the
stronger bound

    d(A) >= V + sum_(a=1)^s ceil(v_a/c)               (F_b)

holds. A still sharper version may use each diagonal layer's own value
`c_a=17-min(b_a,9)`.

If every layer has dimension at most `r`, (F) implies

    d(A) >= V + ceil(V/min(r,17)).                    (R)

In particular, a complete invariant flag (`v_a=1` for all `a`) forces

    d(A) >= 2V.                                     (T)

**Theorem B (commuting coefficients).** If the coefficient blocks `A_ij`
commute pairwise, then (T) holds. This includes non-diagonalizable commuting
families, nilpotent parts, and fields over which the matrices do not split.

**Sharp algebraic control.** There is an explicit binary scalar fitting with
`ell=193`, canonical quotient dimension two, and rank eleven. Its identity
tensor lift attains `d=2V` for every `V` and has commuting coefficients.
Thus (T) is sharp as a code statement at this arrival threshold. The control
has no physical decoder here and remains subject to the point-retained
handoff obstruction.

If a historical space `W` supplies `row(A)`, these lower bounds apply to
`dim((W+C_V)/C_V)` as well. If `C_V` is actually contained in `W`, then
`dim W>=9V+d(A)`, in particular `dim W>=11V` in (T). None of these statements
is the unrestricted claim `rank A>=11V` or a count of physical packets.

## 2. Rectangular upper-triangular rank lemma

Let a matrix have row and column decompositions into the same number of
layers. Its diagonal blocks may be rectangular and may have different
sizes from one another. If every block below the diagonal is zero, then

    rank M >= sum_a rank M_aa.                       (U)

For each diagonal block choose a nonsingular square minor of order its
rank. Select all these rows and columns in the full matrix. The resulting
square matrix is block upper triangular, with these nonsingular square
minors on the diagonal. Its determinant is their nonzero product. This
proves (U) without a claim of equality and without any matching rectangular
row/column counts beyond the selected minors.

The hypothesis is essential: the matrix `[[1,1],[1,1]]` has two diagonal
blocks of rank one but total rank one. Its below-diagonal block is nonzero.

## 3. Passing to the value layers and applying the quotient gap

Work over `L` if needed. Matrix ranks and the dimension `d(A)` do not change
under scalar extension: a nonzero minor remains nonzero and all larger
zero minors remain zero. Choose one value-space basis adapted to the common
flag and apply the same change of basis to every source/output block.
Each `A_ij` becomes block upper triangular with layer widths `v_a`.

Let `A^(a)` be the diagonal-layer fitting. It has identity diagonal blocks,
the same prescribed-zero graph, and widths `v_a`. Every nonzero foreign
block of `A^(a)` comes from a nonzero foreign block of `A`. Hence

    ell_i(A^(a)) <= ell_i(A)  for every i,
    sum_i ell_i(A^(a)) <= 194,
    b_a >= b.

The independently proved proportional canonical-quotient theorem applies
to each layer, over this same characteristic-two field `L`. If

    d_a = dim((row(A^(a))+C tensor L^(v_a))/(C tensor L^(v_a))),

it gives

    d_a >= v_a+ceil(v_a/17),
    d_a >= v_a+ceil(v_a/c_a)
        >= v_a+ceil(v_a/c).

Choose a fixed nine-row basis matrix `B` for the canonical code and form

    M = vertical_stack(A, B tensor I_V).

Its rank is `9V+d(A)`. After ordering its rows and columns first by value
layer and then by source/output port, it is block upper triangular. Its
diagonal layer is precisely

    M_aa = vertical_stack(A^(a), B tensor I_(v_a)),
    rank M_aa = 9v_a+d_a.

The extra canonical rows are essential; applying this statement to `A`
alone would not compute the quotient dimension. Lemma (U) now yields

    9V+d(A) >= sum_a (9v_a+d_a),
    d(A) >= sum_a d_a.

Substituting the layer inequalities proves (F) and (F_b).

For (R), if `r<=17`, every positive layer contributes at least one ceiling
term and there are at least `ceil(V/r)` layers. If `r>=17`, the sum of
ceilings is at least `ceil(V/17)`. This proves the stated minimum formula.
Refining an invariant layer cannot decrease the sum of ceiling terms.

For a complete flag all layer dimensions are one, so the sum is `V` and
(T) follows. This applies to any simultaneously triangularizable family,
including noncommuting upper-triangular coefficient blocks.

## 4. Why commuting blocks triangularize over an extension

Pass to an algebraic closure of `k`; ranks and `d(A)` stay unchanged.
The finite commuting family of coefficient blocks has a common eigenvector.
Here is an elementary proof requiring no characteristic-zero theorem.

Start with the whole nonzero value space. For the first operator, select
an eigenspace. It is nonzero and invariant under every remaining operator
because the family commutes. Restrict the next operator to that space and
select a nonzero eigenspace there. Continue through the finite family.
The resulting nonzero space consists of common eigenvectors; any line in
it is invariant under every operator. The induced operators on the quotient
by that line still commute. Induction on dimension gives a complete common
invariant flag.

Apply (T) over the algebraic closure and transfer the unchanged rank
inequality back to `k`. No semisimplicity, common diagonalization, finite
field search, or assumption on Jordan blocks is used. No claim about a
general Lie-solvable family in positive characteristic is made.

## 5. Exact target-threshold code attaining the commuting bound

Use these actual rank-three source-root sets:

    S1={2,9,12,30,38,42},
    S2={2,26,63,65,81,87}.

Let `h_a` be their binary indicators. For each `a`, let `I_a` be the native
receivers orthogonal to all of `S_a` whose canonical foreign degree is at
most 58. Direct exact source reconstruction gives

    |I1|=|I2|=17, |I1 intersect I2|=5,
    |I1 union I2|=29.

Define a scalar fitting `F` by

    F_i = K_i+h1,  i in I1;
    F_i = K_i+h2,  i in I2 minus I1;
    F_i = K_i,     otherwise.

Each changed row deletes exactly six permitted foreign contacts, preserves
its diagonal and all prescribed zeros, and has remaining foreign degree
between 49 and 52. All other rows retain canonical degree at least 55.
Thus `ell(F)=222-29=193`. Exact binary elimination gives

    rank F=11,
    rank vertical_stack(F,B)=11,
    d(F)=2.

These binary rank identities persist over every characteristic-two field.
Tensoring with `I_V` gives `rank=11V`, `d=2V`, and unchanged whole-block
support, establishing algebraic sharpness of (T).

The eleven-port support `S1 union S2` is small; adding the actual retained
pivot's coordinate `e_0` gives only twelve ports. Under the declared handoff
premises, a static continuation using this supported history and stationary
point copies therefore remains excluded by the independently reviewed
point-retained handoff theorem.
This control is deliberately a fitting, not an actual codeword acquisition
schedule, decoder, or supplier. Passing the arrival proxy does not settle
physical availability.

The sets come from the previously reviewed seventeen-savings geometric
maximizers; predecessor credit is retained. No global novelty claim is made
for combining scalar patches. Here it supplies the exact boundary control
for the new operator-filtration theorem.

## 6. Controls, scope, and next construction

The finite verifier independently reconstructs the explicit fitting and
its tensor lifts. It checks actual fitting examples with non-diagonalizable
commuting blocks, commuting blocks with no eigenvector over F2, and
noncommuting upper-triangular blocks. It also checks the rectangular rank
lemma on exact constructed matrices and its below-diagonal counterexample.

Two opposite nilpotent matrix units provide a family with no common
invariant line even over an algebraic closure: each operator has only the
zero eigenvalue and their kernels are different coordinate lines. This
guards against silently triangularizing arbitrary coefficient families.
Conversely, two strictly upper-triangular three-dimensional matrix units
do not commute but preserve a complete flag. Thus noncommutativity alone
does not escape (T).

To seek canonical innovation below two full widths, the coefficient family
must fail simultaneous triangularization even over an algebraic closure.
If, over a chosen extension, a common invariant flag has every layer at most
two-dimensional, (R) still requires
`d>=V+ceil(V/2)`; analogous bounds hold for larger bounded factors. These
are necessary representation conditions, not constructions or complete
cost savings.

The physical target corollary retains the all-route proof's complete
caller, chronological linear model, whole widths, and every charged
operation. No operation is made free here. Both strict suppliers, physical
acquisition, all endpoints, compiler, ownership/erasure, precision, cover,
recursion and all five foundations remain open.

Next: construct an actual useful code using irreducible operator factors,
or prove stronger native restrictions on those factors, while respecting
the mixed-bank/point-handoff distinction and the complete invoice.

Prepared for @CubeJerry with substantial OpenAI assistance. Credit the
native/canonical source, scalar gluing/savings authors and reviewers,
the companion forced-injection and proportional quotient-gap results,
and the point-retained handoff work. This package's new contribution is
the additive invariant-layer bound and the consequent double-width gate
for commuting or simultaneously triangularizable coefficients. No human
or formal-kernel verification is claimed.
