# Independent review of the split noncommuting ordinary compiler

Accepted as a sufficient constructive implementation theorem with the exact
stated hypotheses. Reviewed proof SHA256:
`d3ed2ad13a986486ce558f1afa8093f8b06c0fa6d0917aa175415b2cc62c3704`.
The earlier draft hash is not this review's admission target. The final
version explicitly lowers inverse algebraic shears anew, so inverse ADD is
never assumed to be a free characteristic-zero primitive.

C's `review_noncommuting_compiler.py` imports no R/A/B execution code.
It reads the pinned four emitted words, reconstructs the multiplication
table by composing their literal root-four monomial tables, checks the
supplied matrix-unit certificate, and replays every unweighted ADD, fixed
SCALE and actual monomial service over the exact rational group algebra.
The receipt is `noncommuting-compiler-review/RESULT.json`.

## Universal argument

The matrix-unit multiplication law, identity sum, dimension sum and linear
independence give the declared split algebra isomorphism. This is the
required finite certificate; abstract semisimplicity or unspecified spectral
projectors are not substitutes. Scaling one whole bank by delta has
component determinant delta^d_lambda. Factoring that physical scalar
therefore leaves every component in SL_(n*d_lambda). The determinant
condition is sufficient, and invertibility of each component alone is not
this compiler's hypothesis.

Scalar Gauss-Jordan elimination over Q(i) is constructive. At most m-1
signed pivot swaps, m(m-1) row additions and m-1 balanced diagonal
scalings give at most(m-1)(m+9) transvections. The six-factor balanced
scaling identity and chronological reversal are correct. All scalar matrices
are fixed before tensor width changes, so no growing field-matrix inverse
is hidden in this step.

A scalar transvection across distinct banks lifts directly to an actual
matrix-unit cross-bank shear. For an internal transvection with a!=b,
choose another existing bank and any internal index c. Then

    X=alpha E_ij tensor e_ac, Y=E_ji tensor e_cb

have X^2=Y^2=YX=0 and XY=alpha E_ii tensor e_ab. The four-factor
commutator is exactly I+XY. The condition a!=b is what kills YX;
without it the displayed shortcut would not hold. At least two existing
banks are essential. The borrowed bank may carry arbitrary input and is
restored algebraically by the complete word; it is never initialized.
Chronological execution is right-to-left relative to the written product.

For a fixed cross-bank pair, group-coefficient shears add without cross
terms because E_ij^2=0, even though the group coefficients do not commute.
Each monomial term is physically realized by applying the monomial to the
source, scaling the source, performing the unweighted ADD, and undoing the
source scale and monomial. The source is restored after each term. Negating
and reversing the algebraic shears before fresh lowering yields a legal
inverse with the same conservative bounds. This avoids treating an inverse
unweighted ADD as identical to ADD in characteristic zero.

The bound L=4 sum_lambda F(n*d_lambda), followed by L|G| ADD,
2L|G|+1 SCALE,2L(|G|-1) monomial services, is conservative and valid.
The zero-extra-owner assertion is relative to the admitted fixed monomial
services and existing banks; their complete physical tariff remains part
of the programme. No arbitrary spectral-control service is introduced.

An identity in the literal group algebra remains an identity under the
homomorphism g maps to g tensor-power V. This proves every positive width,
including widths where some components are absent. Exterior coefficients
remain scalar coefficients, whereas literal one-column phases tensorize.
For example exterior i remains i at width2, while literal(i I) tensor2
is minus I. The proof correctly preserves this distinction. Norm-one
monomials, fixed scalars, and finitely many ADDs give width-independent
prefix bounds, while the full field volume, coefficient heights, precision,
tape, layouts and recursive caller costs still have to be paid.

## Independent exact controls

The checker derives all64 group products from actual table composition,
checks all64 matrix-unit products and coefficient basis rank8, and rebuilds
A column-by-column from the source C_b D_acd P. It reconstructs both
A^-2 D_a^2 A^2 and A^-2 D_b^2 A^2, and separately rebuilds
R2=(C_a C_b)^-1 A^2 to verify the literal transported SWAP. No projective
phase quotient is used.

| Word | ADD | SCALE | Monomial services | Prefix coefficient-l1 bound |
| --- | ---: | ---: | ---: | ---: |
|Example forward|16|32|28|3|
|Example inverse|16|32|28|2|
|General forward|628|1253|1098|111|
|General inverse|628|1253|1098|6293/18|

The example equals I+E00 tensor e12_std and restores both other arbitrary
banks. The general word's component determinants, computed independently
from its final actual coefficients, are2,2,2,2,4, exactly delta^d for
delta2. Both full inverse products are identities in the group algebra.

A separate C-authored positive primitive word uses an exterior Gaussian
coefficient and implements I+i E00 tensor e12_std. Its literal file is
`noncommuting-compiler-review/GAUSSIAN-CONTROL-WORD.json`, SHA256
`4f8ad9fb7cc94e8ed46494339c0c1db7dfad2eeaa75f06f3129fc52a082e8990`.
It uses16 ADD,32 SCALE and28 monomial services and restores the borrowed
banks. This control supplements the rational author words; the universal
Q(i) conclusion rests on the algebraic proof, not on these finite examples.

The checker independently reproduces tensor component multiplicities for
V=1,2,3,4. The absent scalar component at width1 has multiplicity16 at
width2. Thus I minus that projector on three banks is physically identity
at width1 but has a48-dimensional width2 kernel. This is a concrete
counterexample to a width-one-only unit test, with no general impossibility
claim about a different ordinary compiler. Omitted ADD/monomial controls
fail, and two consecutive positive ADDs fail to invert each other.

## Scope

This opens a concrete noncommuting ordinary class when a candidate supplies
its literal finite group, matrix units, common determinant certificate and
actual emitted recipe. It is not a claim that every group-algebra unit is
compilable by this interface, nor that the resulting large constants are
profitable. A complete independent(4,2,1) caller, strict suppliers and
recursive invoice remain open. The global native_all_columns,
owned_erasure, compiler, precision_tape, and analytic_recovery foundations
all remain open. This finite compiler theorem does not discharge the global
compiler foundation. No new kappa.
