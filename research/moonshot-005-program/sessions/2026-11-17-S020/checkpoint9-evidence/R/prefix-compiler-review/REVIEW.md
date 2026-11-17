# Independent review of the exact finite-prefix compiler classification

**PASS under the exact stated primitive class.** For R=Z[i,1/2], pi=1+i,
b>=2 equal banks with d fixed prefix coordinates, a matrix M in GL_(bd)(R)
has a literal whole-bank ADD / unit SCALE / root-four prefix MONO program
if and only if d divides v_pi(det M). The program uses the existing banks
only and tensors with any tail identity. The theorem includes the special
target diag(A,I) with an arbitrary borrowed bank restored.

The reviewed author proof SHA256 is
`75636359ce7472f902f51f209f50c0e5e348646405c7fd3558f4325d80dae1b0`;
checker SHA256 is
`5a75913c9f2f9f55fe33174802e3fa40b8e1358ccb3966ce6638eaab9b4ffedb`.
The review reads the complete constructive argument and uses a separate
SymPy primitive interpreter. It imports none of the author's compiler or
Gaussian arithmetic. Finite examples support the explicit identities;
the following argument supplies the unbounded quantifiers.

## Necessity and coefficient ring

Gaussian-integer Euclid follows by rounding both coordinates of a quotient;
the remainder norm is at most half the divisor norm. Inverting2 inverts only
the Gaussian prime pi, since2=-i*pi^2. The units of R are exactly i^e*pi^k.
Thus their valuations are integers, and valuation-zero units are root-four.
The commutative adjugate criterion correctly identifies GL over this ring.
It is not a criterion about a noncommutative ordinary operator algebra.

For a tail dimension N, every full-bank SCALE contributes dN*v_pi(c) to
the full determinant valuation. ADD contributes zero, as does every allowed
root-four monomial. The target contributes N*v_pi(det M). Cancelling N
proves divisibility by d. This argument survives arbitrary intermediate
coupling and any number of restored equal-width borrowed banks. It does
not survive uncharged erasure or arbitrary larger-ring scalar roots, which
are excluded by the theorem's explicit model.

## Literal coordinate operations

For a cross-bank coefficient cU with c a scalar unit and U an allowed
prefix monomial, transform the source by cU, ADD the whole bank, and undo
the transformation. The source is restored for every initial value. A
Gaussian-dyadic coefficient r may be a nonunit; split its real and imaginary
numerators into signed binary powers instead of ever using SCALE(r).

The author improves the proposed Walsh expansion to the two-term identity
E_ab=(P_ab-D_a P_ab)/2. Here P_ab is the coordinate swap and D_a changes
the sign of output coordinate a. Left multiplication by I-D_a selects
precisely row a of P_ab, whose input coordinate is b. Both coefficients
for each scalar unit summand are units. This proves every cross-bank
coordinate shear for every positive integer d, including odd d.

For within-bank I+rE_ab, a!=b, set P=rE_ab and Q=E_bb. Then QP=0 and
PQ=P. The four chronological cross-bank operations B+=QA, A+=PB,
B-=QA, A-=PB give (A,B)=((I+P)x,y) for arbitrary (x,y). No zero helper
assumption occurs. An existing second bank can be restored after every
elementary factor even when it stores other target coordinates.

## Elementary generation and determinant normalization

The proof clears a common power-of-two denominator algebraically to select
Gaussian-integer Euclidean quotients. It never treats denominator clearing
as a free physical row operation. Quotient subtractions and signed swaps
are determinant-one elementary row operations. They reduce a unimodular
column to (g,0,...,0); preservation of its generated ideal proves that g
is a unit of R, even if intermediate pivots were nonunits.

The paired diagonal diag(g^-1,g) is a product of six elementary shears,
using w(u)=E12(u)E21(-u^-1)E12(u) and
w(u)w(-1)=diag(u,u^-1). It normalizes the pivot without requiring a
coordinate-selective scalar primitive. Recursive elimination uses only
the remaining rows, leaving previous columns fixed. The last pivot is1
because the remaining determinant is1. Back substitution finishes an
elementary factorization of every SL matrix. No stability theorem or
additional bank is assumed.

Finally det M=i^e*pi^(dk) is normalized by one whole-bank SCALE(pi^-k)
and one coordinate root-four phase i^-e, producing determinant1. Compile
the SL part and undo those two admitted normalizers. The word depends on
M and d but not the tail dimension. This establishes sufficiency.

## Independent executable checks and limitations

The separate checker expands a Walsh selector service for dimensions2/4,
using coefficients3 and(3+5i)/8, and replays every primitive on all arbitrary
bank columns. It verifies internal commutators and a six-shear paired
diag(1+i,(1-i)/2). Four omitted ADDs each fail. An independently implemented
two-term selector also checks both cross-bank and within-bank shears at
d=3, using a column-image monomial convention distinct from the author's
row-image convention. It checks exact scalar valuations and the obstruction
diag(2,1,1,1) at d=4. The author additionally compiles a concrete Gaussian
Euclid reduction with a nonunit first pivot; this is reviewed separately
and is not imported into the independent executable.

Full prefix root-four monomial availability is essential. With a restricted
catalogue, its needed sign selectors and permutations require their own
compilation. The theorem supplies no uniform resource bound as d or
coefficient height grows, no general noncommutative endpoint compiler,
and no ownership, erasure, precision, recursion or analytic recovery
implementation. The five programme foundations remain open. Native and
endpoint prefixes remain paid. No complete supplier or new kappa follows.

Credit root's determinant-classification proposal, C's complete all-size
proof and two-term selector improvement, the retained paid-normalizer
commutator, @CubeJerry and OpenAI assistance.
