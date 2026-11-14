# A subwidth extension cannot create a new scalar support pattern

**Author theorem; independent review pending. No complete multiplication
bound, source, supplier, or foundational discharge.**

This is a source-independent linear-algebra reduction, followed by a
native BIT consequence. It identifies a stronger restriction on a proposed
fractional canonical quotient: below two whole widths, a target-compatible
code cannot contain even one full scalar quotient line.

## 1. Universal support scalarization

Let `k` be any field, `n>=1`, and `V>=1`. Let `B<=k^n` be any scalar row
code and `B_V=B tensor k^V`. Let `A` be an `n` by `n` block matrix with
blocks of size `V` by `V` and identity diagonal. It may have any prescribed
zero mask, arbitrary singular foreign blocks, and noncommuting coefficients.
Define

    delta = dim((row(A)+B_V)/B_V).

**Theorem.** If `delta<V`, there is a scalar matrix `F` with every row in
`B`, `F_ii=1`, and

    F_ij=0 whenever the whole block A_ij=0.            (1)

Thus every scalar row support is contained in the corresponding block-row
support. Every prescribed-zero fitting condition is preserved. Any objective
monotone in these row support sets can only decrease on passing to `F`.
No symmetry of `F` is asserted or required.

**Proof.** For each output row `i`, consider

    phi_i : k^(1 x V) -> (row(A)+B_V)/B_V,
            u -> u A_i+B_V.

Its image has dimension at most `delta<V`, so choose a nonzero vector
`u_i` in its kernel. Then `u_i A_i` belongs to `B_V`, and its own source
block equals `u_i` because `A_ii=I`.

Choose a linear functional `f_i:k^(1 x V)->k` with `f_i(u_i)=1`; for example
select a nonzero coordinate and divide that coordinate by its value in
`u_i`. Apply `f_i` separately to each source block of `u_i A_i`. This
produces a row of `B`, since the latter row belongs to `B tensor k^V`.
Its own coefficient is one. A zero block of `A_i` stays zero under left
multiplication by `u_i` and the functional. This proves (1). Make the
choices independently for all output rows to obtain `F`.

This proof uses only ordinary vector-space dimension and the identity
diagonal. It does not factor the coefficient algebra, assume a common
kernel vector across receivers, or claim an algorithmic decoder.

**Rowwise strengthening.** The global bound is only a sufficient way to
obtain each kernel vector. For any particular row `i`, if its map `phi_i`
has a nonzero kernel, its support already contains a scalar `B` row with
own coefficient one. Contrapositively, if a block row's support admits no
such scalar `B` row, then `phi_i` is injective and its quotient image has
dimension exactly `V`. Thus every row improving on the scalar `B` row-
support minimum forces a full-width quotient image. This extends the
canonical contact-deletion injection to arbitrary reference codes without
requiring the whole quotient to contain a scalar tensor line.

## 2. Sharpness of the strict subwidth premise

Take the complete allowed graph on two source roles and the repetition
code `B=span(1,1)`. Any scalar fitting with rows in `B` must be the all-ones
matrix, whose foreign support in each row is one. Let

    A=I_2 tensor I_V.

Its foreign supports are empty and

    dim((row(A)+B_V)/B_V)=2V-V=V.

There is no scalar fitting in `B` whose supports are contained in these
empty foreign supports. Therefore `delta<V` cannot be replaced by
`delta<=V`, over any field and at every width.

The identity diagonal is also indispensable: the zero matrix has
`delta=0` but cannot yield a scalar fitting with diagonal one when `B=0`.

## 3. Native canonical-line exclusion below two widths

Return to the characteristic-two, 111-port native BIT graph. Let `C` be
the canonical nine-dimensional scalar code, `C_V=C tensor k^V`, and

    E=(row(A)+C_V)/C_V, d=dim E.

Suppose `d<2V` and `E` contains one entire scalar quotient line

    L_h=span(h+C) tensor k^V,

for some `h` outside `C`. This is a full width-`V` tensor subspace, not
merely one nonzero quotient vector. Put `B=C+span(h)`, so `dim B_V=10V`.
Because `L_h<=E`, the preimage of this line is contained in `row(A)+C_V`,
and consequently

    row(A)+B_V = row(A)+C_V,
    delta = dim((row(A)+B_V)/B_V) = d-V < V.

Apply the universal theorem to obtain a scalar fitting `F` in `B` with
support contained in the block support of `A`. The independently reviewed
scalar one-direction theorem says, over every characteristic-two field,

    sum_i ell_i(F)>=205,
    ell_i=1[foreign support>36]+1[foreign support>52].

Support containment therefore implies `sum_i ell_i(A)>=205`.

**Corollary.** Under the retained all-route target condition `ell<=194`,
if `d<2V`, the canonical quotient `E` contains NO whole scalar-line tensor
`span(h+C) tensor k^V`. In particular, a possible `V=2,d=3` construction
must avoid every such two-dimensional tensor line. Merely choosing
noncommuting coefficient matrices is insufficient.

This is stronger than excluding one particular coordinate line or demanding
nontriangularizable coefficient algebra. It is an intrinsic condition on
the canonical quotient relative to the specified scalar code.

If an available historical space `W` supplies `row(A)`, and its quotient
`(W+C_V)/C_V` both has dimension below `2V` and contains a whole scalar
line, the same conclusion follows using the upper bound on the rowwise
quotient relative to `B_V`. Equality with the actual fitting quotient is
not needed in that version. Conversely, a terminal core alone does not
identify the whole available historical space. No packet count or physical
availability is inferred from these dimensions.

## 4. Boundary controls and compatibility

The two-patch scalar fitting from the companion package has `ell=192` and
canonical quotient dimension two. Tensoring by `I_V` gives `d=2V` and
contains full scalar lines while beating 205. Hence the strict `d<2V`
boundary in the native corollary cannot be relaxed to `d<=2V`.

There are three-dimensional subspaces of `D tensor k^2` containing no full
scalar line when `dim D=3`: for example the graph

    { (z,Tz) : z in D }

under the two channel projections, for any linear `T`. Its first projection
is injective, whereas a full scalar line tensor would contain a nonzero
vector with first channel zero. This illustrates that the necessary
condition leaves a genuine class of possible operator quotient geometries.
It supplies no fitting or physical realization by itself.

The universal lemma works over every field. Only the native 205 constant
and its all-route target corollary require the pinned characteristic-two
source and the explicitly retained caller/operation contracts. The old
scalar theorem's no-Y-feedback physical arrival convention is not used;
only its algebraic support bound is imported.

The checker constructs noncommuting subwidth examples, explicitly derives
the scalar rows by different receiverwise kernel vectors/functionals, and
checks the strict-width and missing-diagonal controls. Native finite
examples test the sharp `2V` boundary. The all-field/all-width proof is
the argument above, not an extrapolation from those examples.

## Open next question

Construct a genuinely new `V=2,d=3` native fitting with a canonical quotient
containing no full scalar line tensor and enough multidimensional local
availability to save at least twenty-eight arrival units. That algebraic
construction would still owe actual acquisition, decoder access, all
endpoints, ownership, compiler, precision, complete recursive cost and a
compatible complex supplier. All five foundations remain. No new kappa.

Prepared for @CubeJerry with substantial OpenAI assistance. Credit the
native/canonical and scalar quotient-savings authors/reviewers, the
companion quotient-injection and two-patch work, and the all-route target
theorem. This package adds the source-free support-scalarization reduction
and the no-full-scalar-line consequence. No human or formal-kernel review
is claimed.
