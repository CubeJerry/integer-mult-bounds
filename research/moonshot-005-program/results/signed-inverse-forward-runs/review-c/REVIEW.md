# Independent review: signed fresh chains and alternating targets

**Accepted as a structural theorem and positive endpoint interface. No caller or new κ is inferred.** The author is `worker-a/signed-inverse-forward-runs`, freeze `d84e6ea5d662c1fdf54e47955bbbb29fd4660053d784d038d2071df31dfc4203`, proof `8878de72284ec4a02d928480f38e68a66e7768306885d2b86b557e11d6490937`.

## Universal signed-rank proof

The incoming state Kq_j=e q_j is preserved by the induction. For a fresh edge, conjugation makes the new normal q_h a unit eigenvector independently of e. An inverse edge removes that direction and leaves state0. A forward edge updates by vv^T with v=Pq_j, an odd vector perpendicular to q_h. Since K'v=e v, it adds a dimension when e=0 and removes one when e=1, while retaining state1 at q_h. In both cases the symmetric projection property remains valid.

Exactly the starts of positive runs contribute+1; every other step contributes−1. This proves8m−r+2p on every authentic path for all distinct-stage choices. For odd r, the maximal run count is(r+1)/2 and occurs only at strict positive-start, positive-end alternation. The stronger alternating kernels follow because each route maps E_s⊕<q_j> to E_s⊕<q_h>; its orthogonal projection is F+q_hq_h^T. The inverse next edge removes that head direction exactly.

**Support qualification:** the exact rank formula allows arbitrary m and r. The whole-row support corollary must retain the4^r path count. With L_V extra binary branching factors the nonalternating bound is2^(2r+L_V+(8m−1)V). A rank8m+1 target is excluded when2r+L_V<2V, in particular for fixed r and L_V=o(V), or r=o(V) and L_V=o(V). Unrestricted r(V) proportional to V cannot be absorbed into a constant. The intended fixed three- and five-half applications satisfy this regime. Worker A confirmed this interpretation without changing the frozen scientific bytes.

## Exact positive target maps

Substituting G_s=R'_s Q in the odd alternating product cancels adjacent Q and Q inverse literally, giving R'_r...R'_1 Q. The left decoder R'_1...R'_r cancels the involutions in the correct reverse order and yields QD_tot with exact phases retained. This is stronger than observing the correct path ranks.

The even normal form is Q^-1R'_r...R'_1Q. The retained actual identity D_tot R_s D_tot^-1=Q^-1R'_sQ follows from the reviewed own-stage exchange and other-stage commutation. Applying it to the ordered product gives W D_tot=D_tot R_r...R_1. Thus input preencoding R_1...R_r gives D_tot. No Q is moved through an R. If several endpoints share original registers, their simultaneous preencodings and actual chronology still require a joint proof.

The odd three-stage endpoint is a concrete productive target for a new caller. The earlier inverse-chain caller has a different endpoint and is not repaired just by this identity.

## Ordinary realization and independent checks

The emitted R0 recipe is an invertible in-place map on112 arbitrary registers:280 ADDs,58 nonzero SCALEs,56 SWAPs, with dyadic coefficients of magnitude at most2. Independent source-column reconstruction followed by column-wise recipe replay gives exactly the same112-by112 matrix. There are no auxiliary fields. Surrounding actual M/O monomial legs implement R_s or R'_s and must be counted; this does not establish free incompatible-chart arrivals. The stated length-r ordinary invoice is correct and finite for fixed r, while compiler and precision obligations remain inherited.

`check.py` imports no author builder or checker. It credits and pins the preceding Worker C direct-matrix engine, then independently checks65408 signed path updates by33-column K conjugation. All9408 strict alternating prefixes match the entire claimed kernel. It verifies eleven exact prefix normal forms, correct odd/even order, the literal ordinary recipe on112 independent columns, and wrong-order/wrong-codec-sign controls. The finite word controls illustrate the universal identities; they do not extrapolate to arbitrary length.

```bash
python check.py --author /path/to/signed-inverse-forward-runs --output RESULT.json
python -O check.py --author /path/to/signed-inverse-forward-runs --output RESULT-OPTIMIZED.json
cmp RESULT.json RESULT-OPTIMIZED.json
```

Both receipts are byte-identical. The explicit author argument supports relocation. Credit Root for the signed-run insight, Workers A/B for the exact target interfaces and source work, and Worker C for this independent review. Prepared for @CubeJerry with OpenAI assistance.
