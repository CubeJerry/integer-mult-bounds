# Minimum-rank strengthening and the four-query pure-four screen

**Author proof supplement pending independent review. No new kappa.** The main proof needs only that the final two-role operator M is invertible and has no components of ranks0,1,2. It does not need M to be pure E3.

For the same-side placement, remove the last rank-one query. The remaining two-query word W2 has no component below two and has no component above three. Its E3 part lies in Q2's affected row; its other row is full pure E2. Since M has no E2 component, the same unaffected-row argument at Q3 confines the ordinary image of pi2(W2) to one role. The canonical R,S and T arguments in PROOF.md apply unchanged and contradict both first-query types.

For a mixed placement, choose the outer query so that removing it leaves a two-query word with one query on each side of the F1 base. Again W2 belongs to E2+E3. Its E3 part occupies a single corner; its E2 part has physical rank at most d because the removed query leaves an unaffected row/column with no rank-two final component. The opposite corner is untouched by both remaining queries and belongs to F1; it therefore vanishes. The admitted three-query placement proof's complementary-corner lemma now contradicts invertibility of W2. That lemma uses only these component and rank facts, not pure E3 status of M. Transpose covers the reversed placement.

Therefore, for every placement of three rank-one queries around the exact native L, an invertible result must have a nonzero component of rank at most two. This is a statement about Gaussian group-basis components, not a physical matrix-rank assertion.

**Corollary.** Four rank-one queries cannot produce an invertible operator with all components of rank at least four. Remove a query at an outer end of the nonordinary factors (there is one, since only one factor is L), together with its adjacent ordinary boundary. Its inverse has coefficients in F1, so the remaining invertible three-query word has no components below three. This contradicts the preceding theorem. In particular, the proposed one-native/four-query independent (4,4) endpoint is excluded at every fixed head count.

Inductively, q>=3 rank-one queries cannot produce an invertible result with all components of rank at least q. This induction only removes outer queries until three remain; it is weaker than the conjectural total-head bound h1+h2<=q+2 and does not prove that conjecture.

The four-query endpoint (4,3) has minimum rank three and remains outside this corollary. A changed native count or retained-role count also remains outside it. All actual phase, group-span, fixed bulk, ordinary-invertibility and independent-input premises of PROOF.md remain. No all-query movement impossibility is inferred beyond the separately proved invoices.

Dependencies: PROOF.md plus the exact S014 THREE-QUERY-PLACEMENT-GATE.md pinned in DEPENDENCIES.json. No finite search or numerical inference is used. Credit @CubeJerry, S014 placement proof, Worker B's minimum-rank observation, and separate reviewers upon admission. OpenAI-assisted research.
