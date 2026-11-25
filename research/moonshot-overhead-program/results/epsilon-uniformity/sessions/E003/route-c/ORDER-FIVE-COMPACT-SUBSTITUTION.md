# Compact execution ledger for the order-five substitution

Status: **complete component transfer from explicitly named physical
suppliers; awaiting independent review**. This is not a new multiplication
envelope or an independent reproof of those suppliers.

The algebraic construction is in
`ORDER-FIVE-ONE-TRANSFORM-CONVERTER.md`. This ledger checks that its change
from the characteristic-two order-three base field does not reintroduce an
exponential table or a scalar-extension factor. The expanded finite
constructor in that document is unconditional; the polynomial local
invoice here additionally imports the specified E002/E003 processors.

## 1. On-demand order-five spectral values

Let `T=2^t`, `D=T-1`, and let c_beta be the ordinary shifted count from
O5-8. The same truncated-series identity used in E002 SR1 gives, for all
integer counts including negative c_beta-u,

    p_beta=zeta^(u-sum beta+((c_beta-u) mod T)),
    p_beta/z=zeta^(-T floor((c_beta-u)/T)).                 (CS1)

The proof is characteristic-two Frobenius:
`(1+X)^T=1+X^T`, so modulo X^T the integer power `(1+X)^a` depends only
on a modulo T, also for negative a because 1+X is a unit. Evaluating
the resulting finite polynomial at X=zeta-1 gives CS1. No infinite
series is evaluated at a field element.

Enumerating B0=O(m) shift seeds, computing their m dot products in F5,
counts, residues and fifth-root powers costs `m^O(1)` bit operations.
The spectral labels of each pair are 0,1,4 at equal/smaller/larger
coordinates; for target F_r multiply them by r modulo five. This is
the same three-way physical comparison problem as in the order-three
processor, with different fixed output labels.

Let `s0=floor(B0/16)`, `v=16w`, and H be the s0-by-B0 Vandermonde
matrix on distinct nodes of `E=F_(16^e)`, `e=ceil(log_16 B0)`. For the
ordered bad set J, put j=|J| and V_J=H[0:j,J]. If j=0 output the zero
correction. Otherwise compute

    e_J = V_J^-1 (HPX-z HX)[0:j],
    v_J = diag((p_beta-z)^14) e_J,
    a[0:j] = (V_J^T)^-1 v_J,   a[j:s0]=0.                 (CS2)

Return (a,z a), with unused padding coordinates zero. This is exactly
the O5-6/O5-7 identity, tensor identity on all v module coordinates.
Every matrix dimension in CS2 is O(m); every field element has O(log m)
bits. Enumerating monic degree-e polynomials over F16 and testing all
possible degree-at-most-e/2 factors costs `B0^O(1)` actual operations,
so the field constructor is polynomial in m. Schoolbook field arithmetic,
pivot-tested Gaussian elimination, coefficient generation and inversion
are likewise polynomial in m, even using sequential scans for every
finite-array access. No 5^m case table is needed.

## 2. Copied formulas and module operations

The three Boolean bits of each input digit in {0,...,4} are fixed affine
functions of four query powers. Their assigned budgets 1,2,4 dominate
their actual degree one. The existing copied carry-formula induction
therefore retains the bound `S<=m^K` for a fixed K. For D=2^t-1, use

    product_(i<t) (1+(zeta-1)^(2^i) B_i),                 (CS3)

rather than introducing a degree-D addition at the top. Every sum budget
is still a power of two. The cyclic sum twist remains one, and the full
module width w is a power of two with `log w<=poly(m)`.

E002 `route-c/succinct-cyclic-executor.md`, C3--C5, is stated over an
arbitrary fixed characteristic-two field. Applying it to F16 is direct:
its term/guard/translation list is unchanged except for at most five
affine terms per local indicator instead of three and a fixed larger
scalar table. It executes each affine coefficient matrix in polynomial-m
work per encoded volume, using a fixed number of marked payload arrays
and polynomial-m descriptors. As before, paths with the same query
are combined before the source shared pencil; this substitution does
not execute a separate spatial query for every formula path.

Scalar multiplication by an F16 coefficient acts coordinatewise on
the e F16 coordinates of E. General E arithmetic is charged separately
in CS2. There is no claim that all E coefficients lie in F16: only the
predictor's final spectral values and its formula coefficients do.

## 3. Physical interface ledger

| Interface | Exact order-five change | Cost/volume consequence |
|---|---|---|
| Query pencil | Four powers C^r each equal gamma_r Q plus a comparison diagonal | One shared-swap pencil, constant-many extra masks. |
| Rational label geometry | No change; scalar identities over F2 extend to E | Same D, lambda, rank fraction and rational address compatibility. |
| Spectral labels | 0,1,4 instead of 0,1,2 | Same equality/order scan; constant-sized labels. |
| Predictor module | Three digit input bits and four query powers | Same polynomial formula/descriptor class and masked-translation structure. |
| Shift family | Projective forms over F5, B0=O(m) | Polynomial seed, count and coefficient work. |
| Check field | F_(16^e), e=O(log m) | O(log m) encoded bits per symbol, polynomial field arithmetic. |
| Gap correction | Fixed exponent 14 instead of 2 | Constant number of field multiplications, same small check-space map. |
| Finite repair | Two children, each 1/8 of parent volume | Total mass 1/4; geometrically bounded parking. |
| Regrouping | 8 parent copies times 2 halves become 16 duplicates | Exact occupied bijection; module coordinate unchanged. |
| Final swap word | F1 and F2, with pointwise diagonals | Two sequential full-rate targets, workspace reused. |
| Binary output | Completed Q has F2 coefficients | Full-rate basis descent preserves every independent bit. |

For absolute proportional payload space, import E003 A's guarded stream,
comparison-label and fixed-array pencil schedules. Their row guards depend
on polynomial parameter heights and complete spatial suffixes, not on
whether the constant base field has four or sixteen elements. Keep every
temporary role/comparison tag out of recursive payloads. The new finite
child ratio is 1/8, still below the label-grouped spatial ratio 2/3.
Reserve descents still clear payloads before the full-volume child.

Changing fields between **completed spatial permutations** uses FP1--FP3
of E003 A's binary packing note. All F_r finite-repair children at a
given local node keep that node's E and its template. No field change is
licensed inside one F_r word.

## 4. Conditional component conclusion

If the listed E002/E003 fixed-tape suppliers meet their stated contracts,
one fixed processor implements the O5 local interchanger with

    nonrecursive time <= V m^K + poly(m,log(2V)),
    payload visited space <= C V,
    additive description/workspace <= poly(m,log(2V)),      (CS4)

for absolute K,C under the same polynomial large-field guards. The exact
spatial-call coefficient is O5-12 plus the unchanged leading padding
and reserve invoice. Every m-dependent loop, field operation, mask,
control scan, coefficient generation and return appears in the imported
polynomial local bills; no dense module matrix is accessed.

Thus the order-five substitution fits the same asymptotic physical profile
used by the proposed two-scale recursion. It does not, on its own, improve
that profile. The global theorem still requires the numerical Walsh,
nonstationary shape, precision, outer integer reduction and common-space
proofs. The rational Walsh branch must not be replaced by F16 arithmetic.

Credits: E002 structured scalar/spectral suppliers, E003 guarded stream
and binary-packing suppliers, the O5 finite word construction, the OpenAI
sources and predecessor authors, Jerry Chen (@CubeJerry), and AI-assisted
component composition. Independent human or formal-kernel review is not
claimed.
