# Lead review of two scoped representation barriers

Status: **both proofs accepted within their stated algebraic models**. This is an AI-assisted independent mathematical review. Neither theorem is a general lower bound for integer multiplication, nor an impossibility result for every compact predictor.

## A: exact formal product decompositions

I checked `routes/A/chow-compression-barrier.md` against the source integral predictor. Its top homogeneous part is a signed elementary symmetric polynomial e_D. The sign includes both the predictor phase and the selected shifted variables. The squarefree order-k derivative coefficient matrix is a disjointness matrix, equivalent by complementation to a subset-inclusion matrix. The note's induction proves its characteristic-zero full rank under k<=D/2 and D<=m. The adjacent-subset connectivity and nonvanishing binomial coefficient are both needed.

A product of b affine forms has at most binom(b,k) derivative directions because each differentiated factor is used at most once. Therefore an exact sum of h such products must have h>=binom(m,k)/binom(b,k). Taking k=floor(D/2), b<2D and D=Theta(sqrt(m log m)) gives the claimed exponential lower bound for h. The specified one-tensor-factor-per-product construction consequently retains a double exponential module scale.

This concerns an exact formal identity in characteristic zero. The Boolean quotient, finite-characteristic-only identities, other matrix representations and different predictors are explicitly excluded. The proof does not infer a lower bound for those alternatives. Its use of Gottlieb rank and derivative spaces is credited as standard prior art.

The lead's isolated checker replay passed 102 modular full-rank certificates, 243 formal predictor cases and 2214 top coefficients. Three rank-drop controls demonstrate the field limitation, and 1089 missing-phase cases reject the incorrect sign. Modular full rank certifies rational full rank in these finite cases; the general theorem is the written induction.

## C: full-rate two-stage evaluation in characteristic two

I checked `routes/C/CHAR2-FULL-RATE-WIDTH.md`. Normalizing the constant matrices is legitimate because the target constant term is I. Comparing degree-one and degree-two coefficients gives the exact commutator relations. Differences A_i+A_m have pairwise commutator I. Their alternating form has rank 2 floor((m-1)/2), yielding that many hyperbolic pairs.

After scalar extension, the commuting central squares have a nonzero common eigenspace preserved by every generator. Subtracting their scalar square roots gives square-zero pairs without changing commutators. The complementary idempotents UV and VU split that space into equal-dimensional pieces; the other pairs preserve the split. Induction gives dimension at least 2^floor((m-1)/2). Scalar extension does not change the original matrix width.

The explicit tensor construction attains this bound over F_2, including the extra identity in the even-m generator and the linear terms in A_0. Both are necessary. Thus the stated exact two-stage minimum is established. For t stages, the (1,1) quadratic coefficient matrix factors with rank at most (t-1)R; symmetrization yields only (t-1)R>=floor(m/2). The exponential two-stage theorem is correctly not extended to t=Theta(sqrt(m)).

The lead's isolated replay passed all m=1,...,16 constructions through width 128, 680 quadratic and 680 reverse-product pairs, 560 commutators, exhaustive width-one/two compatibility graphs and 22 negative controls. This is finite support for the proof, not enumeration of the general lower bound or a tape timing test.

## Consequence for the programme

These proofs identify costs that cannot be removed by the specified shortcuts. A compact full-rate Boolean-quotient representation or a sufficiently long polynomial-width evaluator remains open. The characteristic-two spatial rank approximation and the new order-three physical construction retain their own correction and representation obligations. They are not contradicted by either scoped theorem.

Credits: source predictor, standard inclusion-rank and Clifford methods, Jerry Chen (@CubeJerry), and AI-assisted proofs and independent replay. Replay logs: `lead-replay-A-chow.json`, `lead-replay-C-char2-width.json`.
