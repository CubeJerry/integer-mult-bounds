# Fresh audit of the retained characteristic-two finite construction

Status: **lead reconstructed the listed finite algebra and found no defect
in that scope**. This strengthens the audit of the existing AQ construction;
it does not establish a new bound or a complete kernel-checked theorem.
Route B is conducting a separate supplier audit.

The source remains OpenAI math
3344da59991ed94f9ba711217b29c1d760badfa6. The lead read these entire notes:

- `routes/B/characteristic-two-order-three-interchange.md`;
- `routes/A/characteristic-two-count-formula.md`;
- `routes/B/formula-full-rate-linearization.md`;
- `routes/A/power-two-degree-predictor.md`;
- `routes/B/structured-shift-check-refinement.md`;
- S003 `route-b/succinct-factor.md` and `route-b/compact-interchange.md`;
- S003 `route-c/COMPACT-SPECTRAL-REPAIR-EXECUTOR.md`;
- S003 `route-c/P-POWER-ONLY-COUNT-COMPILER.md` (optional distinct
  extension, not required by the retained characteristic-two route).

## Count semantics and the actual field

At an allowed order-three spectral tuple, a ternary digit has two
Boolean indicators in F4. Its natural value is I_1+2 I_2; this 2 belongs
to the integer interpretation, not to an F4 linear combination. Binary
carry formulas compute ordinary sum bits because their Boolean identities
hold in characteristic two. Their leaves are then substituted by the
affine F4 indicator expressions in q and q^2.

Syntactic degree counts q and q^2 as the two permitted affine query
variables, rather than treating q^2 as degree one in an ordinary
univariate polynomial. Bit k has budget 2^k. Copied carry syntax contains
the preceding carry once; balanced count formulas are polynomial in m,
including the constant offset and the final copies of their bits.

For every integer a, including negative a,
(1+T)^(2^t)=1 modulo T^(2^t) in F2 shows that the needed binomial
coefficients depend only on a modulo 2^t. Thus the offset residue is
valid also when c-u is negative. On the central window it is exactly
c-u, so the Lucas predictor gives the required omega power. Factorial
division and Boolean multilinear reduction are not used to shorten degree.

The four S005 formal files prove precise Boolean/count and resource
subclaims. They do not formalize the full F4 substitution, spectral
diagonalization or cyclic construction.

## Power-of-two predictor, shifts and cutoff

The current grammar assigns power-of-two lengths to positive sum nodes.
For b0=5 ceil(sqrt(m)), let T be the least power of two at least 2b0+1
and D=T-1. The shifted window contains [m-b0,m+b0]. The bounds
D<=20 sqrt(m)+21<24 sqrt(m) for m>=4096 match the compact interchanger's
constant. Bounded smaller m use the retained direct base routine.

The pairwise independent ternary shifts have B=3^r with
2m+1<=B<6m+3. At every spectral input their count has mean m and
variance 2m/3. Chebyshev gives outside fraction at most 2/75. For the
actual sufficiently large B, (2/75)B<=floor(B/32), so integer check-row
rounding has real slack. This is sparsity in *shifts*, not in the much
larger independent formula-module coordinate.

## Whole-row cyclic identity and phase orientation

Every cyclic rotation equals the scalar predictor times the whole
identity. A distinguished output coordinate would be insufficient.
Multiplication concatenates tensor-factor words. Separate tensor actions
commute, so any split word rejoins a valid child cyclic product. Identity
padding and scalar factors preserve this, including zero polynomials.

For a power-of-two sum gate, commuting graded transitions satisfy
(A+B)^d=A^d+B^d by characteristic-two Frobenius. Restricting to total
grade gives square successive factors. The B child is read at the grade
complementary to the A grade; coefficients use the INPUT grade before
the transition. These orientations were reconstructed explicitly.

The historical general lemma needs odd cyclotomic roots for lengths
with an odd part. The current power-of-two grammar does not. It would
be wrong to reintroduce the historical root requirement into the current
smaller field. Succinct traversal stores polynomially many grade counters
and formula tokens, while every exponentially numerous module row still
contains an independent input payload.

## Check nodes, scalar repair and full-rate packing

The check matrix is H0 tensor I_v, v=32w, with w the whole formula
module. A bad shift selects all module coordinates under that shift.
Only B distinct field nodes are required. F_(4^e), 4^e>=B, supplies
them; the full-payload field codec may round e to a power of two.
These Vandermonde nodes need not be primitive roots of any specified
order. In particular, no large 3-power root requirement survives here.

For the actual defect set J, the first |J| Vandermonde rows V_J are
invertible. If g=p-z is the F4-valued predictor gap, the correction uses

    V_J^(-T) diag(g^2) V_J^(-1).

On a nonzero-gap coordinate the checked residual lifts to
g^2(gX)=X since nonzero F4 elements have cube one. Outside the gap
support, arbitrary lifted values are annihilated by the gap. Some rows
outside the certified central window can also have zero gap; this does
not invalidate the identity PX+PZ+FZ=FX.

The actual check rows are padded to the documented coarse shift-role
count, even when the padding is not an integral number of v-row modules.
Regrouping sixteen parent blocks into child shift/duplicate roles leaves
the w-coordinate untouched. No exponentially long module transpose is
silently introduced.

## Order-three words and recursion mass

On unequal address pairs, C=[[0,1],[1,1]], D=diag(omega,omega^2) and
Q=[[0,1],[1,0]] obey C^3=D^3=I, T C S=D for the supplier's
specified C,D words S,T, and its stated word for Q in C,D. Equal
pairs are fixed points and require
their separate identity case. Distinct tensor-coordinate queries commute.
An inverse-target pencil exchanges the coefficient roles of C and C^2;
C^2 is one allowed query power, not two separately executed queries.
The factor two in the local predictor bill comes from the two complete
predictor evaluations PX and PZ. This clarification follows Route B's
independent review of this audit note.

C and C^2 each equal the shared swap plus one original-layout comparison
projection. The succinct affine factor thus has one shared swap pencil
and original-coordinate comparisons. Moving a comparison through a
spatial endpoint without conjugating it would be wrong; the retained
executor does not do so.

The two check families together occupy R/16. Forward and inverse words
give four check phases at that fraction, total recursive volume R/4.
The documented depth and positive base bill then give the claimed
square-root normalized recurrence with its retained overhead. This is
an audit of that construction, not a universal complexity lower bound.

## Boundary of the audit

AI/UP physical delivery, bijective changing-field packing, the numerical
Walsh recurrence and actual integer caller are still necessary. Their
S005 critical-chain/source-interface reviews are separate. Algebraic rank
does not certify physical time; live memory does not certify cells ever
visited; the source uniform o(x) excess alone does not certify AQ's rate.

No full astronomical template, end-to-end tape multiplier, matching
upstream Lean closure, comparator or human referee check was executed.
The absence of a found defect is limited to the reconstructed arguments.
Historical test receipts retain their provenance; no rerun of every
historical test is claimed here.

Credits: pinned source and matrix-factorization literature; Jerry Chen
(@CubeJerry); S002/S003 and concurrent suppliers; substantial ChatGPT
assistance in this independent audit.
