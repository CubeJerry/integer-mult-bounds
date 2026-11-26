# The exact SWAP-to-Weyl bridge and its occupied-parameter contraction

Status: **proved identity and scoped interface obstruction; physical bridge
still open**. This tests whether the constructive Weyl-star executor can
replace the star swaps found in a retained free rectangle. It identifies
what the tempting use of two existing auxiliary fields actually computes.
No lower bound on other executors or multiplication is asserted.

## 1. The exact expansion

Write Q=2^f for the dimension of one query register, distinct from the
small label alphabet in the source geometry. For the two-half composite
register in STAR-SWAP-FALSIFIER.md, substitute twice the original axis
width for f. Its complete expansion then has four original f-bit
parameter fields; this only strengthens the occupancy issue below. For s,xi in F_2^f define

    (W_(s,xi) F)(x)=(-1)^(xi dot x) F(x+s).

Its inverse/transpose is W_(s,xi)^(-1)=(-1)^(xi dot s) W_(s,xi).
For an auxiliary field z and query field x,

    SWAP_(z,x) = (1/Q) sum_(s,xi)
                    W_(s,xi)^(-1)|_z tensor W_(s,xi)|_x.   (WC1)

Indeed the right side, evaluated at (z,x), equals

    (1/Q) sum_(s,xi) (-1)^(xi dot (s+z+x)) F(z+s,x+s).

The sum over xi is Q when s=z+x and zero otherwise, leaving F(x,z).
All coefficients are exact rational signs and the scale 1/Q.

Consequently a weighted star-swap pencil has the exact expression

    sum_j B_j tensor SWAP_(z,x_j)
      = (1/Q) sum_(s,xi) W_(s,xi)^(-1)|_z
                     [sum_j B_j tensor W_(s,xi)|_(x_j)].  (WC2)

The inner bracket is the Weyl-star family of the companion construction.
The outer contraction has Q^2=2^(2f) parameter terms. WC2 is a sum,
not a product or a promise that these terms can be delivered at low cost.
The inverse Weyl action on z must also be implemented and charged.

## 2. Literal expansion and why occupied parameters differ

For one arbitrary data array, literal broadcast into all (s,xi) slots
creates Q^2 copies before the parameter-dependent operations are summed.
Its expanded input bit volume is Q^2 V. Sequentially evaluating all
parameters avoids retaining all copies but still has Q^2 terms to price.
This is exponential in f, not the polynomial-m ordinary allowance of
NI5 or RV-W.

Two complete existing auxiliary fields do supply Q^2 parameter values,
but their slots already contain Q^2 independent arrays. They do not
supply Q^2 equal copies of each such array. Applying the parameter-
dependent Weyl pencil diagonally preserves these independent parameter
labels. Summing those labels afterward contracts the row space rather
than applying the desired operator independently to each original row.
Even for one SWAP, which is invertible, a map from Q^2 independent rows
to one row cannot restore every row through later linear operations.
This is a dimension statement about that literal contraction, not a
runtime lower bound.

Initializing one parameter row and leaving the others zero makes the
broadcast-and-contract identity applicable, but violates the required
full independent occupancy. Adding a new parameter register restores the
identity at the explicit Q^2 volume expansion. Neither choice closes the
physical bridge under the existing interfaces.

## 3. What conjugation by a parameter Walsh transform really gives

One can instead preserve all occupied parameter rows by placing a Walsh
transform before and after the diagonal Weyl family. This is invertible,
but it does not perform the needed contraction independently at every row.
The cross-row blocks can be written exactly.

Let p=(s,xi) index the Q^2 parameter rows, let H_P be their unnormalized
binary Walsh matrix, and put

    A_p = W_p^(-1)|_z tensor W_p|_x,
    K = (H_P/Q^2) diag_p(A_p) H_P.                    (WC3)

For row difference d=(alpha,beta), the corresponding block is

    K_d = (1/Q^2) sum_(s,xi)
           (-1)^(alpha dot s + beta dot xi) A_(s,xi).

Summing xi explicitly gives

    (K_d F)(z,x)
      = (1/Q) (-1)^(alpha dot (z+x+beta))
                       F(x+beta,z+beta).              (WC4)

Thus the diagonal block is SWAP/Q, but EVERY off-diagonal block is also
1/Q times an invertible signed permutation. Scaling K by Q makes its
diagonal blocks the desired SWAP while retaining every unwanted row
transfer. Complete occupancy makes those transfers observable; no scalar
normalization removes them.

This calculation tests the actual use of full parameter fields. It does
not treat their entries as zero, or discard their data when a parameter
sum is performed. A new cancellation mechanism could still repair these
blocks, but its cost and independent-row identity must be supplied.

## 4. A precise limit on one proposed cancellation mechanism

For r=Q^2 parameter rows, diagonal pinching can be obtained by averaging
r conjugations by all Walsh character phases. Within that literal
character-averaging family the coefficients are uniquely determined by
Fourier inversion: annihilating every nonzero row difference and retaining
the zero difference uses every character with weight 1/r.

More generally, if weighted diagonal phase conjugations cancel arbitrary
off-diagonal row blocks while preserving every diagonal block, their
row-pair coefficient matrix is the r-by-r identity. A family of t phase
vectors contributes a sum of t rank-one outer products, even with arbitrary
signed or complex weights. Its rank is at most t, hence t>=r. This rules
out a shorter universal diagonal-phase pinching formula. It does not rule
out sharing physical work between the terms, exploiting the specific
blocks WC4, or using a different linear cancellation circuit.

There is also no one common termwise scalar-diagonal correction for the
entire star-swap family when m>=3. The Weyl products A_(p,j) commute for
fixed p, and their relative operators commute. The relative star swaps
do not: SWAP_j SWAP_1^(-1) include noncommuting 3-cycles. A common pair of
input/output bases would preserve the commutation of these relative
operators. STAR-SWAP-FALSIFIER.md gives the explicit source-relevant
witness. A correction depending on j is not excluded, but cannot be
called a once-only common correction without its own invoice.

## 5. A fixed-sum rank falsifier for the same literal lift

For m=3 the literal full-parameter lift also fails a stronger test that
only concerns the equal-weight sum, rather than each query separately.
For every fixed p the three A_(p,j) commute and square to the identity.
Their eigenvalues are signs, so their three-term sum has only odd,
nonzero eigenvalues. Therefore sum_j K_j is invertible on the complete
parameter/data space.

The corresponding three-star-swap sum is singular even for one-bit
query and auxiliary fields. Write |ab> for the address basis vector
whose ones occur exactly in positions a,b, with position 0 auxiliary
and positions 1,2,3 the queries. Then the nonzero vector

    v = |01> - |02> + |23> - |13>

satisfies

    (SWAP_01 + SWAP_02 + SWAP_03) v = 0.

For any f>=1 use only the symbols 0 and 1 in those four registers; their
orbit remains the same. Tensoring with the untouched parameter identity
preserves this kernel. Thus no invertible common preprocessor and
postprocessor can convert this particular literal lifted sum to the
independently applied star-swap sum: their ranks differ.

This does not exclude a noninvertible correction, a different lift, a
source-specific cancellation, or treating an affine pencil with different
weights. It falsifies only the proposed full-parameter Walsh conjugation
followed by invertible once-only corrections, including arbitrary linear
ones. Its scope is broader than the termwise scalar-diagonal test but
still gives no time lower bound.

The off-diagonal defect of this literal lift is not a small-rank defect,
either. For one SWAP, K in WC3 is unitary and its diagonal-block part is
I tensor SWAP/Q, of operator norm 1/Q. Their difference is invertible
when Q>1, hence has full rank. For an odd m-star sum, the lifted sum has
smallest singular value at least one (it is a conjugate of a sum of
commuting self-adjoint involutions). The diagonal-block part has norm at
most m/Q. Thus when Q>m, the entire off-diagonal defect is again invertible
by the same norm perturbation argument. This prevents treating that exact
defect as a low-rank row repair; it does not exclude other cancellations.

## 6. The remaining constructive gate

A successful bridge must implement WC2's parameter contraction with
arbitrary independent parameter data restored, or implement the entire
star-swap pencil by another method. It must count the inverse auxiliary
Weyl action, all cancellations, retained arrays, field movements and
precision. Merely observing that two occupied auxiliary fields have the
right number of values does not supply the broadcast state or the row
identity.

This identifies a concrete local problem. WC4 gives exact unwanted blocks
that another geometric routing construction might cancel in a shared
way. Conversely, the factor Q^2 in a literal parameter loop cannot be
silently absorbed into an arity-polynomial descriptor or per-volume cost.

The constructive Weyl-star theorem remains valid within its interface.
Its extension to the retained Fourier star swaps, NI5 and RV-W is open.
The unconditional global bound remains E002 Theorem V.

Credits: @CubeJerry, standard finite Weyl matrix expansion, the pinned
Fourier endpoint construction, the E002 lead's proposed bridge test,
and substantial ChatGPT multi-agent assistance. These exact identities
and finite-parameter rank statements are not physical runtime bounds.
