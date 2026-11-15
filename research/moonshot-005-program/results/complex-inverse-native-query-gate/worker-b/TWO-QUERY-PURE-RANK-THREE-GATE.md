# Two rank-one queries cannot give two pure rank-three endpoints in the stated scopes

**Proved scoped obstruction, pending independent review. No new kappa.** Both same-side and split-query placements are excluded in every faithful phase sector. A physical-rank argument strengthens an earlier augmentation-only draft and permits ordinary zero divisors. Endpoints (3,2) remain open.

## 1. Algebraic hypotheses and source

Let G be a fixed finite Clifford group on a fixed number of head coordinates, with its finite scalar centre retained. Let H be its full monomial ordinary subgroup. Gaussian rank gives direct H-bimodules E_r in a sufficiently large faithful tensor representation of the relevant central-character quotient. Write F_j for the direct sum of E_0 through E_j. We use E_0=C[H] and F_j F_k subset F_{j+k}, where multiplication is operator composition. Ordinary role matrices and their inverses have entries in E_0.

There are exactly two independent retained roles. A native has the rank-two-cross form

    N = [[A, -A^2], [0,A]],     r(A)=1, r(A^2)=2.

All ordinary invertible role encodings are allowed. Each of two one-bank paid queries is an in-place rank-one transform or a distinct-bank shear whose coefficient has rank one. Such a query fixes one standard input column and one standard output row (not necessarily with the same role label), and its entries belong to F_1. Its inverse has the same properties. The source orientations with an ordinary cross term are simpler and included in the same-side conclusion. Transposition and interchange of the two role labels treat reversed source orientations.

An independent endpoint of ranks (3,3), even with arbitrary invertible ordinary boundary encodings, is a matrix supported entirely in E_3 and invertible. The conclusions below need only that property; they exclude every invertible pure-E_3 output matrix, not just a prescribed diagonal pair.

## 2. Both queries on one side: every phase sector

**Theorem 1.** Two rank-one queries both after one native cannot give an invertible pure-E_3 output. The same holds with both queries before the native.

Absorb the outer ordinary boundaries. Write the word Q_2 C_2 Q_1 C_1 N. A row unaffected by Q_2 is a row of C_2 Q_1 C_1 N. Its two active entries have the form

    [L A, -L A^2 + M A],             L,M in F_1.

If the complete word is pure E_3, this row has no E_2 component. Its first entry gives pi_2(LA)=0, so LA belongs to F_1. Therefore LA^2=(LA)A belongs to F_2, as does MA. The entire row has no E_3 component. It must be zero, contradicting invertibility. For an ordinary-cross native the row belongs to F_2 immediately. Transposition reverses the word, preserves Gaussian rank and ordinary monomiality, and restores the native after swapping role labels. This proves the before-native case.

This is a universal component argument. No scalar augmentation, numerical search or assumption about invertibility of individual ordinary entries is used.

## 3. One query on each side: every phase sector

**Theorem 2.** One rank-one query before and one rank-one query after the native cannot give an invertible pure-E_3 output. This statement uses physical matrix rank and holds in every faithful central-character sector.

Suppose M=Q_+ C N D Q_- were such an output, where C,D are invertible ordinary matrices. Let e_s be a standard column fixed by Q_- and let e_t^T be a standard row fixed by Q_+. Set K=D e_s=(k_1,k_2)^T and L=e_t^T C=(l_1,l_2). Then

    e_t^T M e_s = L N K.

The left side belongs to E_3 and the right side to E_1+E_2, so both vanish. Its separate rank components give

    l_1 A^2 k_2 = 0,
    l_1 A k_1 + l_2 A k_2 = 0.                 (1)

Let the physical dimension of one field be d. Write row i of Q_+ C as (u_i,v_i), with u_i,v_i in F_1. The corresponding block of M e_s is

    u_i A k_1 + v_i A k_2 - u_i A^2 k_2.

The first two terms lie in F_2. Ordinary bimodularity therefore gives

    pi_3((M e_s)_i) = -pi_3(u_i A^2) k_2.

Because M is pure E_3, its whole d-column block has the factorization

    M e_s = - W k_2,

where W is the 2d-by-d matrix stacking pi_3(u_i A^2). Invertibility of M implies rank(M e_s)=d. Hence k_2, a square d-by-d matrix, has rank d and is invertible. The first equation in (1) now gives l_1=0 because A^2 and k_2 are invertible. The second gives l_2=0 because A and k_2 are invertible. This contradicts L=e_t^T C having full row rank d. QED.

No individual ordinary coefficient was assumed invertible: k_2 was proved invertible by the independent-output rank requirement. All ordinary zero divisors, including projector routing, are permitted. A singular k_2 may solve the two kernel equations, but it cannot be completed to an invertible pure-rank-three endpoint with only the remaining rank-one query.

### 3.1 Required zero-divisor negative control

A nonzero ordinary unimodular pair L,K with LNK=0 can exist. Root's independently developed Pauli-projector construction has k_2=E_b^-=(I-Z_b^{tensor V})/2, a singular half-rank projector; on odd collective widths its flips are collective X operators, and a proposed marked-first-column variant works at all widths. Therefore the zero corner alone is not an obstruction. The decisive added condition above is the full-rank independent pure-E_3 endpoint, which forces k_2 invertible and excludes this singular projector completion. The exact root control and its all-width marked-algebra admission are tracked separately.

### 3.2 Superseded augmentation argument

An earlier draft obtained a narrower trivial-central-character result by applying the group-algebra augmentation to (1). That argument was valid in its stated sector, but the physical-rank argument above removes the sector restriction. The draft's proposed nontrivial-residue escape is therefore no longer open under the stated rank-bimodule hypotheses. The scalar finite control is retained only as a historical algebra control; it is not the proof of the stronger theorem.

## 4. Uniformity, arithmetic and the surviving interface

For every fixed finite Clifford family, the rank bimodules are independent at every sufficiently large tensor width in each phase residue, by the programme tensor-separation argument. The proof above does not change the central character, specialize group elements to one, or use a one-column polynomial identity. It therefore applies to all those widths.

A possible extension separates a fixed number of individually addressed columns as a finite matrix factor and grades the remaining bulk tensor columns. The abstract proof applies if the enlarged ordinary algebra is proved to preserve these rank bimodules and all source/query/target bulk ranks retain the stated values. The marked-column phase and tensor-factor verification is a separate admission obligation; this document does not claim it discharged. Unrestricted width-growing ordinary algebras are outside the established scope.

The optimistic common-body invoice for (3,3) is target 2[10] against price 3[1]+[7]+[8], with [r]=r^t. That arithmetic remains correct but does not produce the missing caller. This candidate is closed by Theorems 1 and 2 throughout the stated rank-bimodule model, in every phase residue.

The proposed (3,2) target has [10]+[9] against the same price. Its output has both E_2 and E_3 components, so the premise LNK=0 used above is unavailable. Neither theorem excludes it. A precise next problem is to characterize the ordinary source/destination compression LNK when it equals the rank-two part of an independently diagonalizable (3,2) endpoint, and then solve or disprove the required split-query completion. This is a mathematical construction obligation, not an accepted supplier.

Dependencies: `THREE-HEAD-SOURCE-AND-ONE-QUERY-GATE.md` for the exact spectator source; `ONE-NATIVE-QUERY-GATE.md` and the programme tensor-separation proof for rank bimodularity/faithfulness. No new paid operation is introduced by these proof-only compressions. All actual ordinary routing, source, erasure and compiler costs remain payable in any prospective caller. All five foundational assumptions remain retained. Credit @CubeJerry, predecessor source/compiler authors, S014 Worker B and OpenAI assistance.
