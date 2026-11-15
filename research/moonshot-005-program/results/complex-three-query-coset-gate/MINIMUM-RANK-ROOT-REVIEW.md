# Independent review of the minimum-rank strengthening

**Accepted.** Root checks the stronger premise against the full coset and mixed-placement arguments. They need invertibility and absence of final components below three, not purity of the final operator.

Removing the last rank-one query gives a preword in E2+E3 by the lower triangle and source/query upper bound. In the same-side case E3 occupies one row and the other is full pure E2. The last query's untouched row has no E2 component, so E2 still has an ordinary one-role image. All forced-pivot/coset normal forms and both contradictions remain valid.

For mixed placement, remove an outer query leaving one on each side. E3 occupies one corner, E2 has rank at most one role, and the opposite corner belongs to both F1 and E2+E3, so is zero. The complementary-corner lemma forces it invertible: the opposite input restriction and output projection have full rank through the rank-d E2 image. This contradiction needs no final purity. Transposition covers reversed placement.

Every invertible three-query result therefore has a nonzero component of rank at most two. With q>=4, an outer query exists since there is one native factor. Removing it and adjacent ordinary encoding lowers minimum rank by at most one. Induction excludes invertible results supported entirely in ranks at least q, including pure(4,4) with four queries. It does not exclude(4,3) or prove the conjectured total-head bound for general q.

All finite-group, phase-faithfulness, ordinary-invertibility and homogeneous-query premises remain. Companion and S014 placement proofs retain exact dependency pins. This is a written strengthening, not a finite synthesis search or new supplier. All foundations remain; no new kappa. Credit @CubeJerry, predecessors, Worker B and Root's independent review; substantial OpenAI assistance.
