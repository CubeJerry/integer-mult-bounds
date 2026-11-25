# A limitation of the current formula-to-factor compiler

Status: **accepted restricted consequence of a published formula lower
bound after independent Route C and lead review**. The independent review
is `../C/REVIEW-B-MULTILINEAR-COMPILER-BARRIER.md`. This does not bound arbitrary
full-rate matrix representations, nonmultilinear formulas, circuits with
reuse, or identities only in the Boolean quotient.

## 1. The precise class

Consider a formula for the literal original binary predictor P_beta over
a characteristic-zero field, of syntactic degree at most its actual degree
D. Every gate polynomial must be multilinear. Affine linear forms may be
leaves. Compile by the canonical cyclic rules: products tensor and
concatenate; an addition of positive degree d multiplies row width by d.
Degree-zero arithmetic is folded and identities provide padding. No
subsequent compression to a proper submodule is assumed.

For D=Theta(sqrt(m log m)) and sufficiently large m, this class necessarily
produces

    log2(row width) >= D^{Omega(log D)}
                     = 2^{Omega((log m)^2)}.             (MB1)

Thus the current `2^{2^{O((log m)^2)}}` row envelope has the correct two
exponential levels and logarithm-squared scale within this class. Changing
only the balanced variable split cannot supply the singly exponential
representation in polynomial m requested by IP.

## 2. The published input

Hrubes and Yehudayoff prove that a homogeneous multilinear formula for
the elementary symmetric polynomial e_D on m>=2D variables has at least
`m D^{Omega(log D)}` leaves: Theorem 1(i), proved through Proposition 7
and Corollary 8, of *Homogeneous formulas and symmetric polynomials*,
Computational Complexity 20 (2011), 559--578.

Primary author copy read for this audit:
<https://users.math.cas.cz/~hrubes/PDFs/SymPoly.pdf>.

Only that restricted published theorem is used. It is not a
superpolynomial lower bound for unrestricted homogeneous formulas.

## 3. Extract the top component without duplicating the formula

The source predictor has top homogeneous component

    [P_beta]_D = (-1)^(u-sum beta_j)
                 e_D((-1)^beta_1 q_1,...,(-1)^beta_m q_m).

Its highest generating-series term is `(-2)^D e_D(I)`, with
`I_j=(1-(-1)^beta_j q_j)/2`; the indicators' degree-D coefficient cancels
`(-2)^D`. The source prefactor gives the displayed sign.

At a product gate take the top component of each child relative to its
syntactic degree and multiply. At a sum gate retain only children of
maximum degree, taking their top components. An affine leaf contributes
its linear part. This prunes the formula without copying subexpressions.
It applies because the root's syntactic and actual degree are both D.
Remove zero subtrees and fold constants. The result is a homogeneous
multilinear formula for e_D up to invertible scalar and variable signs,
without any new addition gates.

## 4. Count higher-degree additions, not all formula nodes

Fold each maximal degree-one subtree into an affine leaf. Let A count
the remaining binary addition gates, all of degree at least two, and let
L count affine leaves. Scalar multipliers are absorbed into adjacent
leaves or edges. Then

    L <= D(A+1).                                        (MB2)

Induct on a homogeneous formula of degree d. At a product, degrees add
and the child bounds sum to at most `d(A+1)`. At an addition both children
have degree d, while `A=A_1+A_2+1`, giving that bound. A leaf has
d=1, A=0, L=1. These are all cases after scalar folding.

Expanding each affine leaf into at most `2m+1` ordinary leaves and using
the published theorem yields

    (2m+1) D(A+1) >= m D^{Omega(log D)},
    A >= D^{Omega(log D)}

for sufficiently large D, after changing absolute constants. Each such
addition descends from a degree-at-least-two addition in the original
formula. The canonical graded sum compiler multiplies width by at least
two at each, and product gates multiply widths. Hence its row width is
at least `2^A`, proving (MB1).

## 5. What could evade the result

The argument leaves meaningful alternatives: nonmultilinear intermediate
polynomials with cancellation, a circuit-to-factor construction sharing
work across uses, compression of modules, or an identity only on the
involution quotient. It also leaves other predictors with the required
error pattern open. An interpolation formula of syntactic degree m evades
the degree premise but gives m stages under this compiler, losing the
square-root stage saving. A small coefficient circuit alone still lacks
a whole-row matrix identity.

Credits: Hrubes and Yehudayoff's lower bound; the source predictor;
Jerry Chen (@CubeJerry); AI-assisted derivation of this restricted
compiler-width consequence during session S002.
