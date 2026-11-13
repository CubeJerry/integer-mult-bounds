# Unverified next-wave candidate: error versus outward norm slack

Canonical base: e54523517d0f03e58352e647c403a5af3e525a57.
This is a work checkpoint, not a published theorem or verified contribution.

Let U be rational orthogonal with a column a/q in lowest denominator form,
q>1. Let F be an injective integer-output map on the complete integer ball
S_n, with ||F(x)-Ux||<=M for every x. Choose positive n, q not dividing n,
such that 2n/q>M^2. Then

    max_(x in S_n) (||F(x)||-||x||) >= sqrt(n^2+1)-n.

If the maximum were strictly smaller than this gap, every input norm sqrt(k),
k<=n^2, could only decrease: the next possible larger squared norm is at least
k+1, and sqrt(k+1)-sqrt(k)>=sqrt(n^2+1)-n. Thus F is norm-nonincreasing
on S_n. It injects S_n into itself and hence permutes it. The credited finite
sum argument from #2589 forces every individual norm to be preserved. At
n e_j the radial arithmetic theorem from #6619 then forces squared error
at least 2n/q>M^2, contradiction. This requires no period, linearity,
surjectivity on the entire lattice, or global definition beyond the stated ball.

Take n=floor(q M^2/2)+1 and add one if q divides it. Then n>q M^2/2,
q does not divide n, and n<=q M^2/2+2. A global such map has outward slack
at least the displayed radical gap, which is strictly greater than
1/(q M^2+5). On grid h, a fixed Ch approximation error therefore forces
at least h*(sqrt(n(C,q)^2+1)-n(C,q)) pointwise outward slack whenever the
entrance contains h S_n. It does not imply escape from a fixed unit ball:
the witness can occur in a small interior neighborhood of zero.

For #6619's exact four-coordinate Sylvester Hadamard matrix H4/2 and M=1,
the first such n is three. A finite exact matching on all 425 inputs of S_3
currently attains the lower bound sqrt(10)-3 with error<=1 and distinct
integer outputs. This would make the finite-ball optimum sharp. The root
constructor uses a complete exact candidate graph and iterative augmentation;
an independent certificate checker is still required.

Bounded extensions: R=4 has 1,281 inputs and also admits that threshold.
R=5 has 3,121 inputs; the candidate graph has 21,889 edges and a failed
augmentation reports an explicit Hall subset of 1,692 inputs with 1,691
neighbors at that same threshold. This is unverified finite evidence pending
an independent full neighbor census. No global construction, asymptotic
feasibility, or exact R=5/global optimum is claimed.

Sources inspected: #6619 eaa967e7e8aa12cc53ec246a5fc00c5f8873a50b proof,
README and exact Hadamard fixture in verify.py; #2589
399aa4293d40061fad8ee7e55b39cd1491c7d917 full proof. Both treat zero outward
slack and leave the positive-slack relaxation open. Bounded GitHub searches
for outward/slack/period/radial found no matching quantitative result; this
is not exhaustive novelty certification. Root's general theorem is a short
quantitative corollary of credited predecessors, not a new radial lemma.

Prepared for @CubeJerry with substantial OpenAI assistance. No new kappa,
selected interface rejection, physical tariff or unconditional multiplication
theorem is asserted. Fixed error M, full entrance ball, same output grid and
injectivity are essential premises.

## Later bounded evidence: exact radius-five candidate

The complete search on S_5 has 3,121 input points. Its exact optimum candidate
for injectivity, integer output and uniform Euclidean error at most one is
`beta=sqrt(21)-sqrt(19)`. R5-OPTIMUM.json contains a complete attaining
injection (58 edges have squared norms 19 -> 21), and a subset of 1,692 inputs
whose entire allowed neighbor set under strict outward growth <beta has
1,691 points. Hall's counting inequality would rule out every smaller bound.
The separate check_candidates.py imports no search routine; it regenerates
the complete ball using two-coordinate square sums, verifies the injection
with the exact dot-product error formula, and re-enumerates every possible
strict-threshold neighbor. Exact 128-bit rational square-root enclosures
separate all unequal candidate gaps; the equality pair (21,19) is handled
explicitly. Its DIRECT-CHECK.json passes. Independent worker review remains
required before publication.

This is a finite-domain optimum and a necessary lower bound for any global
injective/bijective rounder with this error cap. It is not a global sufficient
bound. The completed search domain is radii 3,4,5, the exact H4/2 fixture,
and error cap one; radius six, other operators/error caps and global matching
extensions are untouched. The optimizer ran eight finite threshold probes
among 130 distinct positive candidate gaps. No heuristic or stochastic seed
is used in these constructors.

There is an exact transfer to #6509's actual ideal Gaussian pair. In real
coordinates (Re x,Im x,Re y,Im y), let R(a,b,c,d)=(a,-b,c,d) and
L(a,b,c,d)=(a,c,-d,b). Direct integer matrices give H4=L(2C_+)R. Both L and R
are signed permutations, so F for C_+ corresponds to G=L F R for H4/2,
preserving the complete input ball, output lattice, injectivity, error and
outward increment. Conjugation gives the negative sign as well. Thus the
same finite optimum and global necessary beta bound transfer to the native
pair without imposing any sum, center, affine-period or covariance premise.
The retained center family supplies a global bijective error-one upper bound
with outward supremum one. At that fixed error cap the unrestricted global
infimum is therefore confined to [beta,1], conditional on source functional
theorems, while its exact value and any construction below one remain open.
