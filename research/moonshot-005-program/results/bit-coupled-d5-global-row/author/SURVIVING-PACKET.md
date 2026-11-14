# The unchanged surviving packet has only five fitting choices

**All-width, characteristic-two source-interface theorem. No new kappa.**

This addendum concerns the actual two-D5 transfer from bit-coupled-d5-global-row/author/PROOF.md, blobdbb3bcdff4e9f9e5ba9b9d829ae8d26ce6fb274e. After P becomes the proper fitting row for72, the other packet has Q=G+bI_V, where
\[
 b=1_{D'\setminus\{72\}},\qquad D'=F1\cap F18\cap F31,
\]
and G is any V-row block of the canonical code C tensor k^V.

For every characteristic-two field k and positive width V, Q can itself be a complete fitting block for a receiver only for
\[
 i\in\{1,18,31,35,49\}.
\]
In each case the canonical part is forced to be G=K_i tensor I_V. The resulting foreign support has quadratic evaluation rank28 on its real rank7 facet, so it cannot be covered by two proper facet charts. Each has charge2. Thus changing only the canonical initial choice of G cannot turn this unchanged surviving packet into a cheap proper-correction second decoder.

## Proof

The source is the derived native-root blob8eba43d142c819c206dce5df87ea4571aaead287. The checker reconstructs C directly from the native K rows. For every i it proves
\[
 \operatorname{rank}(C|_{N_i\setminus D'})=8,
\]
where N_i is the set of distinct real noncontacts of i. The restriction kernel is therefore exactly span(K_i).

Since b is zero outside D', the fitting zeros force G=K_i tensor T for some V-by-V T. If i is outside supp(b), the own block forces T=I_V. Then b must be supported on foreign contacts of i. Its real support spans D', so D' must be contained in F_i. The native normal-root set of D' is exactly{1,18,31,35,49}; all five are outside D' and work.

If i lies in supp(b), its own block instead forces T=0. But b has a noncontact coefficient at every such i and hence cannot be a fitting. The remaining inside-chart receiver72 has T=I but also has a noncontact in supp(b), so it fails.

These arguments apply entrywise to arbitrary, including noncommuting, canonical block coefficients. No finite-field enumeration is used as a universal premise. The exact binary rank8 certificate persists under every characteristic-two scalar extension.

For the five surviving rows, the checker independently obtains real foreign rank7 and quadratic evaluation rank28 modulo103 in the eight ambient coordinates. The latter equals the full dimension of homogeneous quadratics on F_i. Two proper subspaces would be contained in hyperplanes whose product is a nonzero vanishing quadratic, a contradiction. This proves charge2.

As a finite cross-check, the checker separately enumerates all512 canonical scalar words, including zero and the transfer's c, against all111 receivers. It finds exactly the five predicted choices. This enumeration is a consistency check on the structural proof, not its all-width justification.

## Boundary

The result fixes the final packet as Q=G+bI_V. A further genuine local update, additional actual history, a different helper, a different birth or route, or a receiver receiving several packet values changes the interface. Such mechanisms remain open. Completing one of these five rows with its larger correction support is also not excluded; only a cheap one- or two-proper-chart correction from this unchanged row is ruled out.

Run node check_survivor.mjs RECOVERED-NATIVE-ROOTS.json. Expected status: PASS_D5_SURVIVING_PACKET_GATE. The CLI pins the source Git blob. The exported JavaScript checker was actually executed in the cloud tool; local Node replay is not claimed during the executor outage.

Prepared for @CubeJerry, crediting Worker A's actual transfer and the programme's canonical-local-kernel and quadratic-cover results, with OpenAI assistance. No complete supplier and no new kappa.
