# Divided-power predictors and full-rate matrix evaluation

**Later S002 update, 2026-11-25:** these are preserved early working
notes. Their broad missing-compiler statements have been superseded by
the full-rate cyclic formula construction and the characteristic-two
count-bit formula, reviewed in `FORMULA-CYCLOTOMIC-GENERATOR.md` and
`CHAR2-COUNT-BIT-FORMULA.md`. They give O(D) stages on arbitrary occupied
rows with the stated finite widths, including a `2^(m^C)` width in the
fixed-field case. Polynomial width is still a separate open target. The
formal determinant constraint and the ABP/full-rate distinction below
remain valid in their stated scopes and do not obstruct those later
positive constructions.

Status: **working notes; one scoped algebraic lemma, no new compiler**.
Saved before the independent bounded-source-generator audit on 2026-11-25.
The finite-characteristic count aliasing obstruction does not apply to the
source's integral multilinear predictor. Its high count digits survive in
the divided powers. The unresolved question is whether that predictor can
be evaluated in O(D) pencil stages at polynomial batch width while every
coordinate carries an independent input.

## 1. Three interfaces which must be distinguished

An algebraic branching program may compute P as one entry of a product of
affine matrices. That only evaluates P times one selected input when the
other initial coordinates are zero. The source instead constructs a formal
identity L^b=P I_R. Every coordinate then carries an independent input.
A third possibility is a matrix product which becomes z I_R only on the
Boolean sign patterns where P=z; it need not equal P I_R as a formal
polynomial. Results about one of these interfaces do not automatically
apply to the others.

The elementary-symmetric expansion of the binary divided-power predictor
has a polynomial-width branching program: choose variables in increasing
order along a path, and sum the products of D selected variables. Equivalent
truncated-series algorithms multiply (1+x_j T) in K[T]/(T^(D+1)). The latter
uses m query stages. Evaluation T=-2 is not a homomorphism out of that
truncated ring. Neither observation yields the required full-rate,
O(D)-stage interface.

## 2. A formal determinant constraint

Let K be any field. For 1<=D<m, the elementary symmetric polynomial
e_D(x_1,...,x_m) is irreducible over K. Indeed, a factorization of a
multiaffine polynomial partitions the variables between its nonconstant
factors, since the degrees in each variable add in a domain. Because e_D is
homogeneous, the factors can be chosen homogeneous. Every monomial in their
product would then use a fixed number of variables from each part. But the
D-subsets of [m] have different intersection sizes with every nontrivial
partition when 1<=D<m. This is a contradiction.

Consequently any polynomial P whose highest homogeneous part is a nonzero
multiple of e_D is irreducible. This applies to the canonical multilinear
binary predictor when its top degree is D<m and the characteristic is odd:
the coefficient of e_D in the indicator variables is (-2)^D, and the affine
change from indicators to query signs is invertible.

Suppose there is a **formal polynomial identity**

    L_D(x) ... L_1(x) = P(x) I_R,

where each L_i is an R-by-R affine pencil and deg P=D<m. Taking
determinants in the polynomial UFD gives

    det L_i = c_i P^(a_i),    sum_i a_i=R,
    D a_i <= R.

There are exactly D factors. Summing the last inequalities saturates the
total degree, so each D a_i=R. In particular D divides R, R>=D, and
every factor is a linear determinantal representation of P^(R/D).
With more than D factors one still obtains R>=D from any nonconstant
determinant, but not this divisibility statement.

This is only a polynomial dimension obstruction. It does not prove an
exponential lower bound. Most importantly, the UFD argument is invalid
for an identity asserted only modulo x_j^2-1. Over characteristic zero the
univariate count factorization does work in that quotient with width one,
illustrating why the distinction is substantial.

## 3. Workspace restoration does not itself give full rate

A branching program can be embedded in an invertible upper-unipotent matrix
product B, with P in its (sink,start) entry. Adjoin two coordinates a,b on
which B is the identity. Conjugating the elementary shear from a to start
by B gives X'=I+u e_a^T, where u=B e_start. Let Y=I+e_b e_sink^T.
Because the cross products in the reverse order vanish, their commutator
is

    Y X' Y^(-1) X'^(-1) = I+P e_b e_a^T.

Thus a polynomial shear can be implemented while returning arbitrary
workspace values to their original state. The construction spends a
constant multiple of the branching program's pencil depth. It acts on only
two designated data coordinates; the other coordinates are restored rather
than transformed. Counting them as independently processed inputs would
give an invalid volume saving.

There is a potentially useful quotient identity. With

    U(P)=[[1,P],[0,1]],   V(P)=[[1,0],[-P,1]],

the product U(P)V(P)U(P) becomes P*[[0,1],[-1,0]] whenever P^2=1.
Multiplication by the inverse constant matrix then gives P I_2 on that
set, although its formal determinant remains one. This shows why a formal
determinant lower bound cannot rule out every matrix predictor on the good
Boolean frequencies. An actual construction which uses essentially every
coordinate at O(D) depth is still missing.

## 4. Deferred directions and scope

For quadratic formal square roots, coefficient comparison gives Clifford
anticommutation relations and can force exponential dimension in the rank
of the quadratic form. Extending that phenomenon to the present degree-D
divided-power family, or to identities only on sign points, needs an actual
proof and is not claimed here. Trace identities in characteristic p provide
some divisibility restrictions for p-power matrix roots, but the source
uses a power of two and therefore does not fit that special case.

The source generic matrix root remains a valid but enormous construction.
Its size is precisely what the bounded-source-generator extraction now
attempts to pay. These notes identify a possible improvement target; they
do not change any global integer multiplication bound.

Sources: pinned OpenAI Fourier `repair.tex`, especially integral count
interpolation and the matrix-root lemma; the characteristic exclusions and
count-aliasing proofs in the other Route C notes. This checkpoint contains
no claim of novelty for branching programs, determinant representations,
or elementary matrix commutators.
