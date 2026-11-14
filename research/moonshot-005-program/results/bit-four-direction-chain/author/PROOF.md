# A native completely coupled chain, its binary capacity gate, and geometric limits

**Author construction and scoped obstruction; independent review pending.
No physical decoder, target construction, supplier or new kappa.**

The four-direction chain lies beyond the proved width-two envelope-three
obstruction. It is compatible with a native fitting and nonzero arrival
savings. Its binary specialization nevertheless has a further197 gate.
Over larger fields, a target requires at least four exceptional receiver
kernel types. The actual native control's geometry is audited separately
from its cardinality charge.

## 1. Chain space and first native fitting

Let h0,h1,h2,h3 be independent scalar directions modulo the canonical code
C. Define the three quotient rows

    q0=(h0,h1), q1=(h1,h2), q2=(h2,h3).

They are independent, with scalar envelope dimension four. A nonzero
combination with coefficients(a,b,c) has scalar-coordinate columns
(a,b,c,0) and(0,a,b,c). Their first and last nonzero coordinates prevent
proportionality over any field extension. Thus the quotient has no nonzero
decomposable tensor, even after extension.

For an exact native instance, receivers7,24,25 have36 common foreign
contacts T. In increasing order split T into its first32 contacts P and
four final tips(a,b,c,d)=(103,105,107,109). Put

    h0=1_P+e_a, h1=e_b, h2=e_c, h3=1_P+e_d.

Exact binary ranks give dim(C+span(h0,h1,h2,h3))=13. At the three receivers
respectively choose quotient-selector row pairs

    (e0,e2), (e0+e1,e2), (e0,e1+e2),

and use canonical rows elsewhere. All four scalar representatives are
own-zero and local at these receivers. The fitting is therefore
K_i tensor I plus its selected chain rows. Each changed receiver erases
exactly P, reducing foreign support60 to28. The identity diagonal and
forbidden zeros are preserved. Its actual canonical quotient dimension
is three, scalar envelope is four, and cardinality charge is216.

The full fixed permitted code has exactly the same minimum cardinality
charge216 over F2: the checker computes each exact forbidden restriction
kernel, enumerates every normalized output-row pair, and sums independent
row minima. There are378 such pairs across all111 receivers. This is a
finite fixed-code optimum, not a theorem about all chains or larger fields.

## 2. Receiver coefficient map and exceptional conic

Consider any fitting in a chain envelope over a characteristic-two field.
At a row erasing a canonical contact, the quotient selector U is a full
rank2-by3 matrix by canonical quotient injection. The scalar coefficient
map is

    Phi(g)=U H(g),
    H(g)=[(g0,g1,g2)^T,(g1,g2,g3)^T].

Canonical rigidity and the matrix-annihilator argument give I in im Phi.
A scalar coefficient vector c supplies a support-dominated row in the
global code C+span(sum c_j h_j) whenever c annihilates ker Phi and
c dot a is nonzero for an identity preimage Phi(a)=I. This is the same
functional criterion as in the reviewed three-direction theorem.

For completeness, this functional criterion does not assume the individual
scalar representatives are already local. Write each row as its canonical
part plus the displayed coefficient matrices times the global h_j. If a
matrix functional f annihilates im Phi, applying f leaves a local scalar
row in C. Canonical rigidity makes it f(I)K_i; a deleted contact forces
f(I)=0. This proves I belongs to im Phi. Conversely, c annihilating ker Phi
is f composed with Phi for some matrix functional f. Then f(A_i) lies in
C+span(sum c_j h_j), has own coefficient f(I)=c dot a, and vanishes wherever
the block row vanishes. Division by that nonzero own coefficient gives the
required scalar fitting row. Only this sufficient direction is needed.

The map Phi is invertible unless ker U is one of the conic lines

    k(t)=(1,t,t^2), t in k;  k(infinity)=(0,0,1).

In that exceptional case its kernel is the corresponding cubic line

    gamma(t)=(1,t,t^2,t^3);  gamma(infinity)=(0,0,0,1).

To prove this, Phi(g)=0 means both columns of H(g) lie in the one-dimensional
ker U. Their overlap forces either g proportional to gamma(t), or the
infinity case with first column zero. Conversely each displayed gamma has
rank-one evaluation H(gamma) with column line k(t), proving the claim.
Every identity preimage has rank H(a)=2 and hence is not on any gamma line.

## 3. At most three exceptional types imply charge at least197

**Theorem.** If the charge-saving receivers use at most three distinct
exceptional conic-kernel parameters, then ell>=197, over any
characteristic-two field.

Choose three distinct parameters containing those that occur; extra ones
may be added after extension if needed. Write their cubic points gamma1,
gamma2,gamma3. They are independent, by a Vandermonde minor, including the
infinity case. For each pair ij choose a generic scalar vector c_ij in
the annihilator of P_ij=span(gamma_i,gamma_j). Concretely choose a basis
b,d of that two-dimensional annihilator and put c_ij=b+z d for a fresh
transcendental z. Whenever a is outside P_ij, c_ij dot a is nonzero.

At an exceptional row of type i, both incident pair codes are local.
An identity preimage a cannot lie in P_ij: Phi kills gamma_i, while
Phi(gamma_j) has rank at most one, so their span cannot map to identity.
Thus both incident codes dominate that row.

At a nonexceptional row Phi is invertible, so every scalar coefficient
vector is local. Its identity preimage a can lie in at most one of the
three pair spaces: their pairwise intersections are the individual gamma
lines, on which H has rank one. At least two pair codes therefore dominate
this row also.

Every positive saving is charged to at least two of the same three global
one-direction scalar codes. Their independently established native capacity
is17 each. Thus2S<=51, S<=25 and ell>=197. Row choices and scalar
normalizations may vary; the three scalar directions are fixed globally.
The argument counts double savings with weight two.

**Binary corollary.** Over F2 there are exactly three conic parameters,
0,1,infinity. Every binary chain fitting satisfies ell>=197. Hence no
binary chain search at the194 target is needed. A chain target over a larger
field must use at least four exceptional types; that condition is not
sufficient. F4 is the first possible coefficient field for that escape.

When the four scalar directions are dependent, the existing envelope-three
theorem already gives197. Thus the binary exclusion also covers degenerate
chain representations, without pretending their quotient has dimension3.

For explicit finite controls, write F4={0,1,alpha,alpha+1} with
alpha^2=alpha+1. The three pair-code coefficient vectors for binary
exceptional types are

    c_0,infinity=(0,1,alpha,0),
    c_0,1=(0,1,alpha,alpha+1),
    c_infinity,1=(alpha+1,1,alpha,0).

All42 full-rank binary selectors are checked. Exactly36 admit identity in
im Phi;21 are dominated by two displayed codes and15 by all three.
The checker also verifies the conic/cubic kernel formulas for all3780
full-rank F4 selectors. The F4 selector

    U=((0,1,alpha),(1,0,alpha+1))

has kernel k(alpha+1), identity preimage(0,1,0,0), and is dominated by only
one of these three fixed codes. This is a scope control for the fixed
binary cover. It is not a native target fitting or a counterexample to
any all-chain197 theorem over F4.

## 4. Cardinality216, quadratic-rank proxy219, exact cover proxy220

All geometry in this section is over the reals, using the pinned rational
native roots. The coefficient field of the fitting must not replace the
real chart geometry. For a receiver's foreign whole-block support S in
its seven-dimensional facet, let d1 be its real linear-span dimension and
d2 its degree-two Veronese-span dimension. The companion geometric gate
defines gamma=1[d1=7]+1[d2=28]. Define the stronger capped covering proxy

    chi=1[S is not contained in one proper linear subspace]
         +1[S is not contained in a union of two proper linear subspaces].

Both are necessary support charges for the existing arrival argument, with
gamma<=chi. They are not complete physical costs or sufficient routability
conditions. The constant2 cap avoids any assertion about the exact number
of charts needed above two.

Every unchanged canonical support has quadratic span28, certified by a
28-by-28 rational minor nonzero modulo257. The changed supports have:

| Receiver | Foreign blocks | d1 | d2 | Cardinal ell | gamma | chi |
|---:|---:|---:|---:|---:|---:|---:|
|7|28|7|27|0|1|2|
|24|28|7|27|0|1|1|
|25|28|7|26|0|1|1|

For receiver7 use facet coordinates y0,...,y6 inherited from ambient
coordinates0,...,6. Its unique vanishing homogeneous quadratic, up to
nonzero scale, is

    Q=-2 y1 y6+y2^2-4 y2 y5-y3^2-y4^2+y5^2.

The symmetric coefficient matrix has rank6. A product of two real linear
forms has symmetric matrix rank at most2. If S were covered by two proper
subspaces, enlarge those subspaces to hyperplanes; their product would be
a nonzero vanishing quadratic. Uniqueness forces a multiple of Q, which
contradicts the rank bound. Thus chi_7=2. This explicitly demonstrates why
quadratic rank deficiency alone is not sufficient for a two-chart cover.

For receivers24 and25 use ambient coordinates1,...,7 as facet coordinates.
Their supports respectively lie in the zero sets of

    (y0-y1-y3-y6)(y0-y1-y3+y6),
    (y0+y1-y3-y6)(y0+y1-y3+y6).

Each factor is a nonzero real linear form. The two hyperplanes give an
explicit cover; linear rank7 excludes a single proper subspace. Hence
chi_24=chi_25=1. The complete totals are therefore

    cardinality ell=216,  rank proxy gamma=219,  covering proxy chi=220.

The exact fixed-code optimization in section1 concerns cardinality only.
It does not optimize gamma or chi over that permitted code. No statement
about a legal decoder history follows merely from these support covers.

## 5. Verification and remaining construction frontier

check.py authenticates the native source, reconstructs the111-port fitting,
computes its actual quotient and scalar envelope, and enumerates378 exact
normalized receiver row pairs for the fixed binary code. capacity.py
checks the conic map and finite cover controls with direct F4 arithmetic.
geometry.py independently rebuilds the construction from the source,
checks all111 canonical quadratic minor certificates, computes exact
rational ranks of the changed supports, and verifies the nonfactorable
quadratic and explicit real hyperplane covers. All checks use explicit
exceptions rather than Python assert, and normal/-O results agree.

The all-field three-type theorem is the proof in section3, not a finite
enumeration extrapolation. Its native17 capacity, canonical rigidity and
functional scalarization are inherited from the pinned reviewed programme
results named in SOURCES.json. The real support-charge interpretation uses
the companion geometric gate, whose exact source hash is pinned there.

This package removes binary chains from target194 synthesis. A larger
coefficient field with at least four exceptional receiver kernels is an
unexcluded chain mechanism. Any future fitting must meet both the algebraic
quotient conditions and exact real support geometry, then separately obtain
the required paid acquisition, retained-state, decoding, restoration and
complete recursive accounting. No new kappa is established.

Prepared for @CubeJerry with OpenAI assistance. Credit the native retained
word, canonical rigidity and scalar17-capacity predecessors, the root's
functional/Jordan envelope theorem, and Worker A's real geometric gate.
