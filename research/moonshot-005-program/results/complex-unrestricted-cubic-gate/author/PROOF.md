# Three native LUL stages cannot give three independent cubic heads

**Proved within the fixed finite collective-tail model. No new kappa.**
This closes the all-cubic endpoint left outside the S022 unrestricted-quartic
proof. It does not close the still-profitable profiles (3,2,2), (3,3,1), or
(3,3,2). It places no spectator-preservation, scalar, commutation or fixed
endpoint assumption on the two ordinary interstages.

## Statement and inherited contract

Let `a=I_prefix tensor A^(tensor W)` on a whole bank of dimension D, with
the actual four-bit source `A=C_b R` and input sign `(-1)^(abd)` in the
rotation `R(a,b,c,d)=(b,c,d,a)`. Retain

```
L = [[a,0,0], [I,a,0], [0,0,I]],
U = [[a,-a²,0], [0,a,0], [0,0,I]].
```

The prefix is fixed before W varies. Ordinary operators are finite sums of
collective root-four tail monomials with arbitrary fixed-prefix coefficient
matrices; their scalar coefficients may depend on W. Every claimed ordinary
unit has an ordinary inverse. Let C,Q and the endpoint encodings O,Iin be
arbitrary such three-bank units. All original banks are arbitrary and retained.

**Theorem.** An all-width identity

`L C U Q L = O diag(F_r0,F_r1,F_r2) Iin`

with three independent invertible Gaussian heads cannot have all `rj>=3`.
In particular, the profile (3,3,3) is impossible. Each rank-r head has
`2^r` flat entries per one-letter row and column, of modulus `2^(-r/2)`, up
to separately retained monomial gauges. The theorem concerns arbitrarily
large faithful collective widths, not the full matrix algebra at one width.

The proof uses the admitted finite-word tensor-separation lemma. Distinct
projective one-letter unitary labels become linearly independent after
sufficiently large tensor powers, after their true width phases have been
combined. Fixed prefix matrix units do not change this statement. A finite
catalogue of nonmonomial labels has zero intersection with the ordinary
catalogue. Ordinary units preserve the ordinary span and its complement.

## Two inverse pullbacks force physical flags

Write `E=L C U Q L` and suppose all three heads have rank at least three.
The literal inverse is

```
L^-1 = [[a^-1,0,0], [-a^-2,a^-1,0], [0,0,I]].
```

Every one-letter term of `L^-1 E`, when E is written in its proposed endpoint
form, has largest entry at most `2 / sqrt(8) < 1`. Indeed an inverse a has
two flat entries per row; an inverse a² has four, and their respective row
l1 norms are sqrt(2) and 2. Ordinary monomials preserve those bounds.
Consequently `L^-1 E = C U Q L` has no ordinary component. Multiplication by
the ordinary inverse C^-1 preserves this absence, so `U Q L` has no ordinary
component either. Its last row is

`(q20 a + q21, q21 a, q22)`.

Class-one terms and ordinary terms are disjoint. Hence

`q21=q22=0`.                                                    (1)

The right-sided argument uses column l1 norms and `E L^-1=L C U Q`.
It likewise has no ordinary component, and neither does `L C U` after
right multiplication by Q^-1. Its last column is

`(a c02, c02 + a c12, c22)^T`.

Thus

`c02=c22=0`.                                                    (2)

These are exact zero blocks at the faithful width. They are obtained from
the whole endpoint, not from a projected matrix rank estimate.

## The remaining active block cannot carry the last input

By (2), C has the form

```
[[c00,c01,0],
 [c10,c11,c12],
 [c20,c21,0]].
```

Its invertibility makes

`B = [[c00,c01],[c20,c21]]`

an invertible two-bank operator: after exchanging the last two block rows,
C is block lower triangular with diagonal blocks B and c12.

The last input column of E satisfies

```
E22 = c20 a q02 - c20 a² q12 + c21 a q12,
E02 = a (c00 a q02 - c00 a² q12 + c01 a q12).
```

Every word in E22 has at most four nonzeros per one-letter column, whereas
every word in the assumed endpoint has at least eight. Thus E22=0. Its
one- and two-Gaussian support classes are disjoint, giving in particular

`c20 a q02 + c21 a q12=0`.                                      (3)

In E02, compare the one-Gaussian inner component
`c00 a q02+c01 a q12` with the two-Gaussian inner component
`-c00 a² q12`. Their projective labels are disjoint before the common left
factor a and remain disjoint after it, because left multiplication by an
invertible one-letter A is injective on projective labels. The first
component has at most four entries after multiplication by a, so it cannot
contribute any permitted rank-three-or-higher endpoint label. It therefore
vanishes as a whole:

`c00 a q02 + c01 a q12=0`.                                      (4)

Equations (3)-(4) give `B (a q02, a q12)^T=0`. Invertibility of B and a
forces `q02=q12=0`. Together with (1), Q's last column is zero. This
contradicts invertibility of Q and proves the theorem.

## Scope and next construction

The existing quartic theorem bounds every profile containing rank four by
(4,2,0). The present theorem removes (3,3,3) without using that quartic
argument. The open nonquartic profiles with total rank at least seven have
minimal representatives (3,2,2) and (3,3,1), and also include (3,3,2).
Their quadratic or linear heads can carry the low-support components that
the proof just forced to zero; assuming those components vanish would be
an invalid extension of this theorem.

All original native movements, inactive-body services, ordinary passes,
prefix normalization, target restoration, precision, compiler, ownership,
recursion and the five framework foundations remain charged or open. This
is a source-specific structural result, not a completed supplier.

Credit @CubeJerry, the retained four-bit source and collective-separation
authors, the S022 unrestricted-quartic construction/review, and S023 Worker C
with substantial OpenAI assistance. Baseline programme commit:
`8cf982065bccdd62de2856b16635a6ee06dadb0c`.
