# Independent review of the occupied-parameter SWAP/Weyl bridge

Reviewer: E002 conditional review C. Gate: **PASS for the exact identities and stated scoped falsifiers**.

Reviewed complete `SWAP-WEYL-CONTRACTION-GATE.md`, SHA-256
`5be659cade5396420a38ab06dbb852a59a56a3aa00858308f0be4f277033012b`, together with corrected source map `STAR-SWAP-FALSIFIER.md` at `5db06e11c67fba3e0ed5db2a060bf3616a40f42c5d2281853f58f50f50fd3ceb`. The source register here is the complete two-half composite of width 2f; applying the abstract expansion to it requires four original f-bit parameter fields, as the note now states.

For the exact Weyl expansion, the inverse phase is necessary. After multiplying the two actions, character summation over xi vanishes unless s=z+x. It then contributes exactly Q, canceled by the prefactor 1/Q, and the remaining data address is (x,z). Thus WC1 and the weighted linear extension WC2 hold for arbitrary inputs.

The occupied-parameter distinction is correct. Q^2 independently occupied rows are not Q^2 equal copies of one row. A literal contraction from those rows to one loses rank and cannot later become the independently applied invertible SWAP by linear postprocessing. Retaining a new parameter register instead costs its actual Q^2 volume. These are properties of the specified expansion/contraction, not a lower bound on every way to compute the operator.

Conjugating the diagonal family by the normalized parameter Walsh transform gives the block indexed by row difference (alpha,beta). Summation over xi forces s=z+x+beta and yields exactly WC4, including its remaining 1/Q factor and sign. Every block is a nonzero scalar times an invertible signed permutation. Scaling to fix the diagonal block therefore retains every off-diagonal transfer. Complete occupancy prevents those unwanted blocks from being ignored.

The phase-pinching claims also have the stated scope. Fourier inversion uniquely requires all r Walsh characters to produce the identity row-pair mask. More general weighted diagonal conjugations each contribute a rank-one row-pair coefficient matrix, so universally preserving diagonal blocks while canceling arbitrary off-diagonal blocks requires at least r terms. This says nothing about shared physical evaluation of those terms or specialized exploitation of WC4.

For fixed p, each lifted A_(p,j) is an involution: both Weyl factors square to the same sign and their product has square one. They are real orthogonal involutions, hence self-adjoint. Different j commute because their query factors are on distinct registers and their common auxiliary factor commutes with itself. The odd sum therefore has only odd nonzero eigenvalues, of absolute value at least one. Parameter Walsh conjugation preserves its invertibility and smallest singular value.

By contrast, direct application of the three star transpositions to `|01>-|02>+|23>-|13>` cancels all four classes of output basis vectors. The vector is nonzero, and its binary-symbol orbit is invariant in every larger register alphabet. Thus the equal-weight target sum is singular, including after tensoring with the parameter identity. Invertible input and output changes cannot rectify the rank difference. This is a valid stronger falsifier of this particular literal lift even when only one fixed sum is being matched.

For one query the lifted operator is unitary and its diagonal-block part has norm 1/Q. The off-diagonal defect is therefore invertible for Q>1 by the elementary norm perturbation criterion. For an odd m sum the analogous diagonal-block norm is at most m/Q while the lifted smallest singular value is at least one; Q>m again gives an invertible defect. The full-rank conclusion is correct. It does not exclude a different lift, noninvertible correction, special cancellation, or a physical implementation that avoids these blocks.

## Independent finite replay

I read the complete checker, copied it and the two corrected notes into `e002-review-c/replay-swap-bridge/`, and ran it independently. It passed at `2026-11-25T23:59:41.491494+00:00`, with checker hash
`d6c90c3dd4d1439d7ba1e805dba665dbb4fa5aba3ed583bb9e413f6e3626c75e`.

The checks include every parameter/datum column for the stated small f values, the full unwanted cross-row blocks, character orthogonality, inverse-phase negative controls, the actual rank-six source Gram coordinates, relative swap witnesses, the fixed-sum kernel, lifted involution/commutator identities, and all 768 full two-half composite-register identities. The latter binds the corrected physical source map rather than the withdrawn spectator-half shortcut.

The universal algebra and rank conclusions rely on the written proofs; the checker is finite support, not a tape runtime simulator. The constructive Weyl-star theorem remains valid in its own interface, while its extension to the retained occupied star swaps, NI5 and RV-W remains open. No new unconditional multiplication bound or physical lower bound follows.

Credits: @CubeJerry; standard Weyl and finite-character identities; the pinned source geometry; the batching author's bridge analysis; substantial ChatGPT multi-agent assistance.
