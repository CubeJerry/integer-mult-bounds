# Nine nonlinear records per copy on the remaining 95 receivers

Fix the S021 pair, F4 or F8 cut (1985, 4010, 6119), with b=1,2,3 paid copies. U consists of roles 8–110 except T={14,17,19,20,96,99,101,102}. Write R_i for the real native root line, F_i for its perpendicular facet and D_U for the union of the downsets of the 95 facets. Every fixed-schedule deterministic zero-error continuation on a finite whole-record alphabet A of size at least two has at least **9b** further owned downward MOVEs ending in D_U. Four private regions require another **8b** owned arrivals. A can represent any positive record width. The continuation may recode nonlinearly and turn paid owned records in either nested direction.

| Source | b | Original columns | Live fields | Downset | Private + downset |
|---|---:|---:|---:|---:|---:|
| Pair repair | 1 | 222 | 410 | 9 | 17 |
| Two-copy F4 | 2 | 444 | 812 | 18 | 34 |
| Three-copy F8 | 3 | 666 | 1,218 | 27 | 51 |

The preceding nonlinear bound was 8b+ceil(17b/2). The canonical code attains 9b in the abstract broadcast problem over finite characteristic-two fields. Physical delivery remains open. Other sources require their own locality and private-region proofs.

## Entropy on the three sources

For a witness W below, fix all original Ys and all Xs outside W. The dependence of each initial field at chart B is now confined to roles j with R_j contained in B by the [three-source audit](../bit-low-exterior-formation-gate/ADMISSION.md). All Xs have reached Hub, and public records move upward. Give receiver i its native neighbours in W. From these data and every downward record whose destination lies in F_i, it can simulate that facet's downset by time induction. An upward move can enter the region only from within. Local gates, zero births and erasures supply no external input.

Each W has four isolated roles and ten inducing the Petersen graph. Its receivers define an index code using the ordered tuple Z_W of downward records ending below any of their fourteen facets. Count each event once. Choose the inputs independently uniformly. The four isolates recover 4b records from Z_W given the outside values. Condition further on those isolates. The Petersen rate-five inequality applies in each slice with message alphabet A^b. Therefore

    H(Z_W | X_outside_W, Y) ≥ (4+5)b log|A|.

The Petersen inequality is due to Blasiak, Kleinberg and Lubetzky, *Index coding via linear programming*, v2, Fact 5.6. The [S019 rational dual](../../sessions/2026-11-17-S019/checkpoint1-evidence/R/PETERSEN-SHORT-DUAL.json) proves the entropy version. The [independent review](review/REVIEW.md) reconstructs its 2,520 elementary terms and the three physical source premises. The [four private pairs](../bit-separated-private-transcript/ADMISSION.md) still each need 2b arrivals outside D_U.

## Exact witness family and its geometry

Enumerate the 43,492 pairwise nonorthogonal four-sets on U. The other roots nonorthogonal to all four number at most ten. Exactly 838 four-sets have ten. Label each of these ten vertices by the two independent four-sets on the ten containing it. All ten two-subsets of five labels occur, and native orthogonality agrees exactly with disjointness of labels. This verifies KG(5,2). The 838 role sets are distinct. An example has isolates 8,15,30,47 and core 9,24,38,53,59,60,74,78,88,92.

If N=9b+s events land in D_U, every W must see at least 9b, so at most s can land outside all its facets. At s=0 the entire tuple has maximum conditional entropy on each outside-input slice. Each event is then uniform even given the outside inputs and its predecessors. Its value can still depend on outside inputs.

Call a real subspace hitting if it contains a native root from every W. The smallest hitting dimension is six. Exactly 194 six-dimensional root spans hit all W. Visibility of chart B to W means B is contained in some F_i with i in W. Equivalently, its perpendicular contains R_i. Thus **every equality destination has rank at most two**. The perpendicular of any rank-two destination must be one of the 194 six-spans. Replacing an arbitrary real subspace by the span of its contained U-roots preserves hitting.

Start at the zero span. For any missed W, every hitting extension contains one of its fourteen roots. Branch on these roots, identify equal spans by their U-root closures, and stop at a hit or at rank six. Each extension raises rank by one. Induction covers every minimum-dimensional hitting span. None of rank at most five hits. The [exact enumeration](FLATS.txt) gives all 194 bases. Row reduction modulo 257 computes real rank on the native roots. Each integral row has Euclidean norm two. Every s-by-s minor has absolute value at most 2^s ≤ 256 by Hadamard, so every nonzero minor survives reduction. No arbitrary chart is rounded.

## Formation and cost at equality

Suppose every uncut contribution from the initial state to an event origin S uses only upward moves and local steps after cutting all D_U descents. At equality S is hitting. Otherwise, fix all inputs outside a missed W. All the uncut initial data reaching S are constant. The payload is then a deterministic function of earlier cut values, contradicting its full conditional entropy.

In particular, if no future exterior downward move lands at rank at most five, an origin of rank ≤5 satisfies that hypothesis: the last uncut descent on any path to it would itself have to land at rank ≤5. Thus every equality origin has rank ≥6 and every destination rank ≤2. Each of 9b moves has gap at least four. Including 8b independent private arrivals gives a necessary bill **9b·4^t + 8b** for 0<t≤1. At t=199/200 this is 43.75132983573329… per copy. It exceeds the scalar room by 12.7975571775… and the two- and three-copy rooms by 0.8079374087… per copy. The [S021 price certificate](../bit-low-exterior-formation-gate/author/output/RESULT.json) bounds both sides with outward rational intervals. Public ascents already charged by the direct suffix cannot offset these owned movements.

Extra downset messages retain the per-witness visibility inequalities. Fully general exterior schedules remain open. No new κ. Credit the S019 Petersen work, the S021 source authors and reviewers, Blasiak–Kleinberg–Lubetzky, Jerry Chen / @CubeJerry and substantial OpenAI assistance.
