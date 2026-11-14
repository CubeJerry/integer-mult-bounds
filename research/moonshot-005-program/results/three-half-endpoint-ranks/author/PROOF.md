# Fresh inverse-cross chains lose one Gaussian rank per stage

**Proved source-specific path and support theorem.** For the actual112-port R0 geometry, a product of r inverse G kernels in distinct fresh rank-eight stages, followed by the complete m-stage body Gaussian, has Gaussian rank8m−r in each individual port path. In particular the first and second coded outputs of the actual all-positive three-half elimination have per-path ranks23 and21, respectively. Their row-support upper bounds are4·2^(23V) and64·2^(21V), for every width V. They are not established rank25 productive Gaussian jobs, including on differently chosen25-dimensional subspaces. No new κ.

## 1. Exact objects and scope

Use the original source R0 and actual route records pinned in source/. R0 is a whole-array112-port scalar matrix, with four coefficients ±1/2 per row. Every nonzero entry R_(h,j) has distinct orthogonal odd binary normals q_h,q_j in F2^9. Each actual stage-s route has the same orthogonal permutation P_(s,h): it fixes q_h, exchanges an orthonormal basis of q_h-perp with the eight fresh stage-s axes, and fixes all other fresh stages. The actual M_s and O_s also have signed translation factors. Those factors affect phases but do not affect the Gaussian ranks or support bounds proved here.

Write

Q=diag_h C_(q_h)^(tensor V),
R'_s=O_s R0 O_s^-1,
G_s=R'_s Q,
D_tot=D_1 ... D_m,

where each D_s is the whole Gaussian on its own eight fresh axes. The single-column analysis lifts to V columns; every scalar R0 coefficient is outside that tensor power. The theorem concerns any nonzero port path in

G_(s_r)^-1 ... G_(s_1)^-1 D_tot

when s_1,...,s_r are distinct, hence r<=m. It does not treat repeated stages as fresh. It does not assert that a sum of different paths is itself one Gaussian job.

For the three-half caller, the exact chronological elimination is established separately by Worker B. Its two outputs, up to signs and swapping the two original inputs, are

G_2^-1 D_tot,   G_3^-1 G_2^-1 G_1^-1 D_tot,

with m=3. The present theorem also stands independently as a statement about these explicit operators; it does not rely on an optimistic caller substitution.

## 2. Gaussian kernel and rank-removal lemma

Factor a single-column operator as a Gaussian convolution times an invertible linear permutation. The convolution has a binary symmetric kernel K, its X part on Z Paulis. The full operator has the same Gaussian rank, since the remaining invertible permutation only multiplies this Pauli block by an invertible matrix. For D_tot this is the orthogonal projection onto the8m fresh axes. A permutation P conjugates K to P K P^T. Left multiplication by C_q or its inverse adds q q^T over F2. The inverse has the same binary kernel; its sign affects only the exact phases.

These statements follow directly from the defining C_q=((1+i)I+(1−i)X_q)/2, or from its exact Pauli action. Gaussian rank is rank(K). An actual translation changes only Pauli signs and preserves K. An orthogonal linear permutation has P^-1=P^T.

Let K be a symmetric idempotent matrix and let q satisfy Kq=q and q·q=1. Then

K_new=K+q q^T

is symmetric idempotent and has rank(K)−1. Indeed K_new q=0; K_new agrees with K on q-perp, and image(K) is the orthogonal direct sum of <q> and image(K)∩q-perp. This is an exact rank drop, not just an upper bound.

Consider one new stage-s edge j→h in G_s^-1. Ignoring its nonzero scalar coefficient and translation phases, its operator is

C_(q_h)^-1 P_(s,h) P_(s,j).

Let K_old be the kernel accumulated before this edge. Because no earlier stage uses s, K_old is identity on the entire fresh-s block and has no coupling of that block with the other coordinates. Let P=P_(s,h)P_(s,j). Then

P^T q_h=P_(s,j)P_(s,h)q_h=P_(s,j)q_h.

The edge condition q_h·q_j=0 places this vector entirely in the fresh-s block. Hence K_old P^Tq_h=P^Tq_h, and K'=P K_old P^T satisfies K'q_h=q_h. Since q_h is odd, the rank-removal lemma applies. The new kernel is again a projection and its rank drops exactly one. Operations from this stage still fix every unused fresh block, so the hypothesis is preserved for the next distinct stage.

Induction proves rank8m−r for every authentic path, uniformly over stage choices and port choices. This proof uses only the actual orthogonal edge condition and actual fresh route geometry; no finite search is needed for the general implication.

## 3. Exact per-path support and the summed endpoints

For completeness, a unitary Gaussian convolution with symmetric binary kernel K of rank r has exactly2^r nonzero entries in every row, all of magnitude2^(-r/2). One direct proof writes its Fourier multiplier as i^φ(z), where φ has quadratic polarization2 z^T K w. Squaring the absolute value of its Fourier sum leaves a character sum over ker(K). This vanishes except on one affine coset of image(K); that coset has2^r elements, and each surviving squared magnitude is2^(-r). Translation and permutation factors preserve this row cardinality. The argument applies to the actual signed kernels; inverse signs alter the affine coset or phases but not r.

A width-V path is a tensor lift of that single-column signed Gaussian map, multiplied by its actual scalar R coefficients. It therefore has exactly2^(rV) nonzero entries per row. The scalar product is nonzero, so it does not remove support. An r-edge inverse chain has4^r port paths per output port. Summing them can cause cancellations, but cannot increase their support union. Hence

row_support(G_(s_r)^-1 ... G_(s_1)^-1 D_tot)
 <=4^r · 2^((8m−r)V).

For the actual three-half endpoints with m=3:

- Every first-output path has rank23; there are four paths per row, so support<=4·2^(23V).
- Every second-output path has rank21; there are64 paths per row, so support<=64·2^(21V).

These are bounds for every row and every width, without assuming that different paths have disjoint support or that their signs do not cancel. For V>=2, the maximum over both output banks is at most4·2^(23V). Thus arbitrary mixing of the two banks must use this common maximum; it is invalid to retain the smaller second-bank bound after allowing access to the first bank.

## 4. What this excludes and what remains open

A whole rank25 Gaussian job has2^(25V) nonzero entries in each row, irrespective of which admissible25-dimensional subspace or monomial coordinates describe it. Therefore these coded outputs cannot simply be relabelled as rank25 jobs on different subspaces.

More quantitatively, suppose all additional input/output adapters are a sequence of monomial whole-array maps and L elementary scalar ADD factors (including invertible role/port reencodings built from such factors). Multiplication on either side by a monomial preserves row support; one scalar ADD factor increases a row-support upper bound by at most2. Applied to the complete two-bank coded endpoint, the final maximum is at most

2^(L+2+23V).

Producing even one full rank25 output bank consequently requires L>=2V−2. In particular a fixed finite ordinary recipe, or a family with o(V) such branching factors, cannot supply the missing rank. This is a support statement, not a lower bound for arbitrary ordinary computation, Gaussian-query circuits, helper-assisted algorithms or total bit complexity. A width-growing adapter with enough branching is outside this conclusion and must be costed separately. The root programme's separate support-depth analysis may compose this bound with explicit paid query layers; no such aggregate cost inference is assumed here.

The source remains a constructive exact coded map with its actual tariff. The conclusion is that the indicated three-half closure does not already expose the claimed independent rank25 Gaussian jobs. Nonunitary width-dependent decoders, changed output histories, extra paid body operations and different elimination chronologies remain open. No unconditional impossibility of the target multiplication bound is claimed.

## 5. Verification, negative controls and provenance

Run python check.py and python -O check.py --out RESULT-OPTIMIZED.json. The checker reconstructs the actual R0 entries from all448 independent original source rows, authenticates the route receipt, and checks all448 nonzero first-output paths and all7168 three-stage paths. Their Gaussian ranks are23 and21 respectively; every final triple kernel is again an exact binary projection. The fresh-stage eigenvector condition is checked at each step.

A repeated-stage control restores rank instead of decrementing twice; a diagonal/nonorthogonal edge does not give the required removable unit eigenvector. These controls delimit the fresh and orthogonal hypotheses. The proof establishes the general rank formula; finite checks establish its exact source instantiation. Source pins, normal and optimized outputs are preserved in the manifest. No scientific claim relies on Python assert statements.

Credit Worker B for the actual complete R0 source, inverse/half sources and three-half chronology; the retained physical compiler authors for the exact route construction; Worker A for the fresh-stage projection theorem, all-path rank/support proof and checker. Worker B independently noticed the first-output rank-seven head factor before this package was frozen. This work is for @CubeJerry with OpenAI assistance. No new κ.
