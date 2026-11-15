# Independent review, marked columns, and a zero-divisor control

**Proved algebraic scope extension and independent mathematical review. No new kappa.** Root developed the marked-column argument and projector control independently of Worker B's two-query proofs. Worker C's separate audit is recorded separately. Finite computations illustrate the written identities, not a uniform supplier or exhaustive search.

## 1. Review of the pure rank-three proof

Root checked both same-side and split placements in `TWO-QUERY-PURE-RANK-THREE-GATE.md`. The essential hypotheses are two retained roles, one stated native, two one-bank rank-one queries, ordinary boundaries and the faithful direct Gaussian-rank decomposition.

For same-side placement, the row unaffected by the last query has entries `LA` and `-LA^2+MA`, with L,M in F1. Vanishing of its rank-two component forces LA into F1, so both entries have degree at most two. A pure rank-three invertible endpoint cannot have that zero row. Transposition gives the other placement, with role exchange if necessary.

For split placement, compression between the query-fixed row and column gives `l1 A^2 k2=0` and `l1 A k1+l2 A k2=0`. These equations alone do **not** imply that an ordinary boundary is singular; Section 3 explicitly disproves that tempting argument. The decisive step is `M e_s=-W k2` for the entire pure-rank-three output column. Invertibility of M forces this block column to have rank d, hence the square k2 is invertible. The equations then force l1=l2=0, contradicting full row rank of the ordinary boundary. This permits ordinary zero divisors, uses no scalar augmentation, and retains the actual phase sector.

## 2. Review of the inverse degree-one gate

Root separately checked `INVERSE-NATIVE-TWO-QUERY-GATE.md`. For split placement, all rank-three terms use both queries and occupy one block. The independent rank-three endpoint component has physical rank d, so that sole block is invertible. Its ordinary output column and input row are supported in the corresponding role alone. Ordinary boundary invertibility then forces the complementary rank-two corner to be invertible by block triangularity. That corner is untouched by both queries, so lies in F1, contradicting pure E2 support.

For same-side placement, all rank-two terms after the first query lie in its affected row. The other final output row is pure rank two with physical row rank d. Its square ordinary multiplier c is therefore invertible. Cayley-Hamilton makes c inverse ordinary in the finite unital matrix algebra. All rank-three terms then factor through the same ordinary input row as the rank-two endpoint, contradicting their independent input row spaces. The dual column argument gives the reverse placement. No integral-domain assumption is hidden here.

The quadratic-cross native has inverse `[[A^-1,I],[0,A^-1]]`, entirely in F1. An ordinary-cross native itself lies in F1. Inverting a Clifford endpoint preserves Gaussian rank, and admitted query inverses retain one-bank rank-one form. Thus the gate applies in the direction appropriate to each exact orientation. More queries, higher-rank queries, more retained roles or a base outside the filtration remain outside this theorem.

## 3. Nonzero ordinary zero compression at every width

For the three-head source A=C_b S, where S sends a to c, b to a, c to b, direct Pauli conjugation gives

    A Z_a = Z_c A,   A Z_b = Z_a A,   A^2 Z_b = Z_c A^2.

At width V>=1 put A_V=A tensor ... tensor A and `E_j^+=(I+Z_j^tensor V)/2`, `E_j^-=I-E_j^+`. Let X_j^(first) flip only the first tensor column and define

    H' = X_a^(first) (SWAP_ab)^tensor V,
    H  = X_c^(first) (SWAP_ac)^tensor V.

The marked flip contributes exactly one minus sign at every width. Hence A_V H' maps plus b parity to minus c parity, H A_V maps minus b parity to plus c parity, and A_V^2 preserves the b-to-c parity sign. Set

    O_L = [[E_c^+, E_c^- H], [E_c^-, E_c^+ H]],
    O_R = [[H' E_b^+, H' E_b^-], [E_b^-, E_b^+]].

Orthogonality and completeness of the projectors make both matrices unitary. For `N=[[A_V,-A_V^2],[0,A_V]]`, both diagonal blocks of O_L N O_R vanish by the parity identities. Its first row L and first column K are therefore nonzero unimodular ordinary boundaries with L N K=0. Here k2=E_b^- has rank d/2, so it cannot satisfy the full-rank pure endpoint requirement in Section 1. The off-diagonal blocks remain compound F2 operators; this is not a completed high-rank caller.

The independent SymPy checker verifies widths1 and2, unitary boundaries, both zero corners, singular k2 and rejection when a required flip is omitted. It constructs matrices directly without importing Worker B's Gaussian-dyadic code. A collective flip would work only at odd widths and is not silently used at even widths. These are algebraic ordinary boundary matrices; their physical realization and temporary costs are not certified by this control.

## 4. Fixed marked columns preserve the gates

**Lemma.** Fix k independent of total width V. Suppose bulk width v=V-k is sufficiently large for the established finite Clifford rank spaces E_r^(v) to be direct in its actual phase sector. For a finite exceptional-column space of dimension D0 define

    E'_r = Mat_(D0)(C) tensor E_r^(v).

Then the E'_r are direct, E'_0 is a unital ordinary algebra, each E'_r is an E'_0 bimodule, and `F'_a F'_b subset F'_(a+b)`. Invertible members of E'_0 have inverses in E'_0. Consequently both reviewed gates apply whenever exceptional factors are arbitrary but the source, query and endpoint **bulk ranks** retain their stated values.

Proof: expand in the D0-squared matrix units. A relation among E'_r yields one relation among the direct bulk E_r^(v) in every matrix entry; each vanishes. Bimodularity and the filtration follow term by term from bulk properties and matrix-unit multiplication. E'_0 is finite dimensional and unital, so inverse closure follows from Cayley-Hamilton. A source `A^tensor k tensor A^tensor v` retains bulk rank one, and its square bulk rank two. Query and endpoint bulk ranks are explicit hypotheses. QED.

The actual marked ordinary algebra is contained in this deliberately larger algebra: arbitrary finite-factor actions tensor collective ordinary bulk actions, finite sums, compositions and invertible ordinary role matrices lie in E'_0. An obstruction in the enlargement applies to the actual subalgebra. Central phases remain `zeta^V=zeta^k zeta^v`; the finite factor carries the first term and the faithful bulk representation the second. Bulk faithfulness is required in each actual residue. No one-column identity is substituted into an invalid tensor identity.

This covers the marked column in Section 3, removing it as an escape from these gates. It does not cover a number of exceptional columns growing with V, arbitrary per-column ordinary bulk actions, or primitives outside the filtration. No physical operation is free: ordinary transformations, temporary owners, precision and compiler passes still require their full invoice in any candidate construction.

Dependencies: the pinned three-head source, the programme finite tensor-separation/rank-bimodule results, and the two Worker B proofs. All five foundational premises remain. Credit @CubeJerry, predecessor authors, Worker B's main gates, Root's independent review and marked-column lemma; OpenAI-assisted research. **No new kappa.**
