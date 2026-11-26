# Independent review of the occupied-parameter SWAP/Weyl bridge

Reviewer: E002 independent reviewer A. Status: **PASS for the exact expansion,
occupied-parameter calculation and scoped algebraic obstructions**. The
physical bridge to NI5/RV-W remains open; Theorem V is unchanged.

Reviewed complete final `SWAP-WEYL-CONTRACTION-GATE.md`, SHA-256
`5be659cade5396420a38ab06dbb852a59a56a3aa00858308f0be4f277033012b`.
Read and independently replayed final checker SHA-256
`d6c90c3dd4d1439d7ba1e805dba665dbb4fa5aba3ed583bb9e413f6e3626c75e`.
I also read the complete Weyl-star supplier and source-star falsifier,
including the amended two-half composite-register interpretation, and the
pinned Fourier source's full endpoint-transform subsection. This is a
focused bridge review, not a fresh audit of every physical claim in the
separately reviewed positive Weyl-star executor.

## 1. Exact Weyl expansion and operator order

For the stated pullback convention, applying W twice contributes the
constant sign (-1)^(xi dot s). Its inverse is therefore that sign times W.
On the auxiliary/query tensor product, A_(s,xi) has sign
`(-1)^(xi dot(s+z+x))` and translates both coordinates by s. Summing xi
vanishes unless s=z+x; in that case it contributes Q and the translated
arguments are (x,z). This proves WC1 with exactly the scale 1/Q.
Omitting the inverse phase is incorrect and is specifically caught by the
checker. Row matrices B_j commute with the address actions, so linearity
gives WC2 in the stated order. No commutation of different star swaps is
assumed, and no sum is replaced by a product.

The literal expansion has Q^2 parameter terms. Fresh equal copies of each
input and existing independent parameter rows are different linear inputs.
Collapsing Q^2 independently occupied rows to one has deficient dimension;
without preserving their other data it cannot become an independent SWAP
on every original row. The note limits this to that literal contraction,
not every possible execution or cancellation strategy.

## 2. Complete parameter conjugation

The unnormalized parameter Walsh matrix satisfies H_P^2=Q^2 I, so WC3
is a similarity transform of the invertible diagonal block family. Its
row-difference block contains phase
`alpha dot s + beta dot xi + xi dot(s+z+x)`. Summing xi forces
`s=z+x+beta`, leaving exactly WC4 and its 1/Q scale. Consequently every
nonzero row difference has an invertible signed-permutation block. Scaling
cannot remove these blocks. The calculation holds on arbitrary occupied
rows; it does not presume a zero parameter register.

For scalar diagonal-phase conjugations, the coefficient on a row pair is
one rank-one outer product per phase vector. Preserving diagonal blocks
and cancelling arbitrary off-diagonal blocks requires the identity matrix
of size Q^2. Rank subadditivity therefore requires at least Q^2 terms,
even with signed or complex weights. Walsh-character weights are uniquely
1/Q^2 by finite Fourier inversion. These are term-count statements inside
that phase-averaging class. They do not lower-bound a shared physical
implementation, nor exclude a cancellation circuit using other operations.

## 3. Source relevance and the two physical halves

The q=4,L=2 source Gram construction has the displayed orthonormal e_a
and hyperbolic p,q pair. Its six independent vectors span the actual
radical quotient. The I={(0,0),(1,0)}, J={(2,0),(3,0)} rectangle is a
nonzero-weight free rectangle, with weight -1/2. The proposed source and
destination coordinate lists use legal dual auxiliary bases independent
of query j; H and H-perp lie in their required auxiliary spaces.

The amended interpretation correctly treats the two physical halves.
The middle map exchanges X_j with Z_b and Z_j with X_b. On complete
composite registers x_j=(X_j,Z_j) and z=(Z_b,X_b), this is exactly SWAP.
Other auxiliary paired exchanges are fixed and disjoint, and unrelated
query halves remain spectators. Applying WC1 to this composite means
replacing f by twice the original axis width; its two parameter registers
then comprise four original axes. No missing spectator exchange or factor
of two in the parameter width is hidden.

For relative star swaps, the witness (1,0,0,0) is sent to the query-2
basis location by R_2 R_3 and to query-3 by R_3 R_2, with R_j=P_j P_1^-1.
Nonzero phases cannot change these distinct permutations. Common left/right
bases making all terms scalar diagonal would make the relative operators
commute, which is impossible for this specified source contribution.
This does not rule out other endpoint coordinates, block representations,
a basis for one fixed sum, or cancellation after combining all rectangles.

## 4. Equal-weight rank falsifier and full-rank defect

For fixed p, each A_(p,j) is a real orthogonal involution, hence
self-adjoint. They commute because their only shared factor is the same
auxiliary Weyl operator, while query factors act on separate registers.
They are simultaneously diagonalizable with sign eigenvalues. For odd m,
their sum therefore has smallest singular value at least one. The common
normalized Walsh similarity is orthogonal, preserving that bound.

For m=3 I checked the four basis coefficients of the proposed nonzero
kernel vector. Applying the three star swaps to
`|01>-|02>+|23>-|13>` cancels every resulting coefficient exactly. The
alphabet-two subspace is invariant under swaps, so the same witness works
at every register width. The independently applied unsigned equal-weight
star-swap sum is singular, whereas the literal lifted sum is invertible.
Arbitrary invertible common preprocessing/postprocessing cannot change
this rank mismatch. The conclusion is specifically for this unsigned
equal-weight test; it does not assert the same kernel for every signed
source contribution or every affine pencil coefficient choice.

The additional defect claim also follows rigorously. For one SWAP, K is
unitary and its diagonal part D has norm 1/Q. Hence
`sigma_min(K-D)>=1-1/Q>0`. For odd m, the lifted sum L has minimum
singular value at least one, and the diagonal part has norm at most m/Q.
Thus `sigma_min(L-D)>=1-m/Q>0` when Q>m. The exact off-diagonal defect
is then full rank. Treating that specific defect as a small-rank row repair
is invalid; a different lift or cancellation mechanism is not excluded.

## 5. Independent finite replay and limitations

An isolated copy ran at 2026-11-25T23:57:54.417557+00:00, exit code zero.
Files, complete output and the exact theorem/checker receipt are retained
in `replay-swap-weyl/`. The replay passed:

- 84 exact Weyl/SWAP columns and 84 wrong-inverse-phase rejections;
- 84 conjugated blocks, 4,368 block columns and 4,284 nonzero cross-row
  columns, together with 4,368 character-orthogonality entries;
- 36 actual source Gram basis pairings and all sixteen label Gram rows;
- three relative-swap noncommutation witnesses and three star-sum kernels;
- 384 lifted involution/commutator checks and 768 complete two-half
  composite-register swap checks.

The all-width expansion, pinching rank bound and norm-perturbation argument
are written proofs; the finite script does not simulate their tape cost or
formally establish the asymptotic multiplier. The review accepts the bridge
as a precise successful identity plus a falsifier for particular tempting
implementations. It does not establish the missing contraction executor,
RV-W, an improved global envelope, a general physical lower bound, formal
refinement, practical thresholds or literature priority.

Credits: @CubeJerry; the pinned endpoint proof; standard Weyl and matrix-rank
algebra; the protected batching agent's construction and bridge audit;
substantial ChatGPT multi-agent mathematical assistance.
