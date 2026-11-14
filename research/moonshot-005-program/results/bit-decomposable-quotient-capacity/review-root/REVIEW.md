# Independent proof review: decomposable quotient capacity

**Accepted with the stated near-width or MDS hypotheses. No new kappa.**

Reviewed proof SHA256f02b571f5556ea73dd99d0cc62fc08a1d0243ed93e9bb7b1cd1fb4d917a21645. Root directly reviewed the universal argument. This is mathematical review, not a claim that rerunning an author checker is independent implementation.

A row has matrices M_a=m_a v_a of rank at most one. Annihilator duality correctly places identity in their span whenever a canonical block is deleted. Dual matrix functionals extract local scalar representatives even if the scalar h_a are dependent. The unique identity expansion in independent active M_a has at least V nonzero coefficients; the resulting scalar rows are support-contained in the block row. Repeated scalar codes may be counted with multiplicity as an upper bound, not extra resources.

For a minimal dependence of c active matrices, absorb coefficients into left columns X to get XY=0. Sylvester gives rankX+rankY<=c. Completing both spans to V with the remaining a-c generators gives 2V<=2a-c, hence c<=2(a-V). With r<=V+1 and distinct value lines, only c<=2 is possible, contradicting nonzero rank-one matrices with different value lines. The repeated-line case is correctly separate: a singleton basis line gives one global scalar contraction.

In the MDS case c<=V forces X=0. If c>V, the right rank is V and the full left span is at most a-V<=r-V<V, contradicting identity. The strict r<2V boundary is essential. The F4 dependence at r=2V correctly marks failure of that independence proof without claiming a target source.

Thus V*S<=17r follows from the inherited scalar cardinality capacity. V3/r5 is only an arithmetic allowance in this theorem; later proper-cover capacity can exclude it without invalidating the result. No packet count follows from r, and field extension provides no machine resource. Source chronology, precision, erasure, compiler and complete costs remain open.

Author binary/F4 controls and native examples are supporting finite checks. Universal quantifiers follow from linear algebra and the admitted scalar theorem. Credit Worker C, root independent review, predecessors and @CubeJerry, with OpenAI assistance.
