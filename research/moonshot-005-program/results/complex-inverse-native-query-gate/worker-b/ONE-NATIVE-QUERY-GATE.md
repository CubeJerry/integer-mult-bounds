# A two-sided ordinary-kernel gate for one native and arbitrary monomial phases

**Proved theorem, pending independent admission.** In the enlarged finite Clifford ordinary family, one native half and q one-bank queries can deliver at most q independent Gaussian rank-two head jobs. Three rank-two jobs need at least three queries, excluding the former one-native/one-rank-one/one-rank-two inventory even with noncommuting ordinary quadratic phases. This is a scoped source/interface obstruction. **No new kappa.**

## 1. Exact model and dependencies

Fix a finite projective Clifford group G on the two binary head coordinates, retaining scalar phases, and an ordinary subgroup H of computational-coordinate monomial Clifford maps. H may be the full subgroup including the quadratic phases in `PROOF.md`; it is not restricted to H24. On each scalar-phase width residue use the exact twisted collective tensor algebra. The programme's tensor-separation theorem makes it faithful for every sufficiently large width. An all-width caller must satisfy the argument at such a width.

Let A be that algebra and B=C[H] its ordinary *-closed subalgebra. Gaussian-rank projections pi_r, r=0,1,2, are B-bimodule maps by the existing general Clifford rank-component lemma: ordinary left/right multiplication preserves the rank of the binary symplectic B block. The projective basis is a direct sum in a faithful tensor representation. Scalar phases and width residues are retained.

There are R arbitrary independent retained banks of dimension D. Ordinary interstage and outer encodings are invertible matrices over B, permitting arbitrary finite linear combinations of ordinary Clifford maps. Algebra membership does not assert free implementability.

Exactly one gate is a native half N on two banks with identity on the others, in any pentagonal forward/inverse orientation and with ordinary boundary encodings. The other q nonordinary gates are one-bank queries: an invertible in-place operation on one bank, or a shear adding an operator applied to one source bank into a distinct destination bank. Query coefficients may be any permitted group-algebra operator; their Gaussian ranks do not enter the proof. Each query acts identically on a zero source/affected bank and, on the left, on a zero destination/affected bank.

The complete endpoint, up invertible ordinary encodings, is a diagonal list of independent Gaussian jobs of ranks 0,1,2. Let h_2 count rank-two jobs. No bank is zero, discarded or omitted. No extra native or multi-bank primitive is included.

## 2. Abstract compression theorem

**Theorem.** If N_low=(pi_0+pi_1)(N) is invertible, every caller satisfies h_2<=q.

**Proof.** Split the chronological word at its sole native: M=A_after N A_before. Write q_before+q_after=q. Let O_before and O_after be the respective products of ordinary gates in their original orders.

For each pre-native query impose a coordinate-bank constraint after its ordinary-only prefix: zero source bank for a shear, or zero affected bank for an in-place call. Each constraint has rank at most D and entries in B. Their common right kernel K_r has dimension at least (R-q_before)D. Chronological induction makes all pre-native queries act identically on trajectories from K_r: after the previous queries act identically, the next actual state equals its ordinary-only state. Thus A_before P_r=O_before P_r, where P_r projects orthogonally onto K_r.

The constraint matrix has entries in B. Its zero-eigenspace Gram projector is a polynomial in the Gram matrix, so P_r belongs to Mat_R(B), a finite-dimensional *-closed algebra. This is a proof device, not a free physical projection.

For post-native queries proceed in reverse time, imposing zero destination bank for a shear or zero affected bank for an in-place query after its ordinary-only suffix row state. Their common left kernel K_l has dimension at least (R-q_after)D; its projector P_l lies in Mat_R(B). Reverse induction gives P_l A_after=P_l O_after. The left shear condition is on the destination, not the source. Hence

    P_l M P_r = P_l O_after N O_before P_r.        (1)

Apply pi_low=pi_0+pi_1 and bimodularity:

    P_l pi_low(M) P_r
       = P_l O_after N_low O_before P_r.         (2)

The independent Gaussian endpoint and invertible ordinary boundary encodings give rank(pi_low(M))=(R-h_2)D. The left side has at most this rank. The middle factor O_after N_low O_before on the right is invertible, so Sylvester's inequality gives compressed rank at least

    rank(P_l)+rank(P_r)-RD >= (R-q)D.

Therefore (R-q)D <= (R-h_2)D, proving h_2<=q. The q>=R case is already trivial. QED.

## 3. Every pentagonal native orientation

The active native block is

    [[B^sigma, c B^(sigma+epsilon)], [0, B^sigma]],

for sigma,epsilon,c in {+1,-1}. Its diagonal coefficients have Gaussian rank one. Its cross coefficient has rank zero when sigma+epsilon=0 and rank two otherwise. N_low is either the same triangular block or its invertible diagonal part. Identity idle banks remain included. Ordinary boundary encodings preserve its invertibility by bimodularity.

The theorem therefore covers every source orientation and query order, both query modes, inverses and fixed scalars, including noncommuting ordinary quadratic phases. In particular, one native and two one-bank queries of any Gaussian ranks cannot give three rank-two jobs. A rank-two query exposes one bank; it is not two independently callable rank-one queries for this invariant. This proof does not use the old parity involution, which fails in the new order-five algebra.

## 4. Scope and next construction

This theorem does not cover multiple native halves, multi-bank paid primitives, changed input/output retention, approximate limits, width-growing algebras, or arbitrary non-Clifford ordinary maps lacking the faithful rank decomposition. It proves no general movement or multiplication lower bound.

A surviving small inventory is one native and three separately callable rank-one queries on three roles. Its query moment 3[1] slightly exceeds [1]+[2] for 0<t<1. Favorable raw arithmetic still requires an actual caller, all ordinary/precision/layout charges and strict supplier admission. The three-native/four-role construction remains open.

## 5. Verification and provenance

Dependencies are `results/complex-tensor-rank-components/author/PROOF.md` for tensor separation and the rank bimodule, and the explicit native in `PROOF.md`. The finite ordinary algebra's *-closure establishes projector membership only; no projector is physically executed or credited. The universal proof is separate from finite controls.

Independent review must check chronological right/source and reverse left/destination constraints, both query modes, the endpoint component rank after ordinary encodings, and all native orientations. Root's independent scalar-C5 determinant calculation can serve as a special-case certificate, without replacing this broader proof.

Credit @CubeJerry, the native/compiler and tensor-component authors, S013's kernel-projection technique, and S014 Worker B with substantial OpenAI assistance. All five foundations remain retained. No new kappa.
