# Independent review of the three-query placement reduction

**Worker C: accepted under the stated rank-band hypotheses. No new kappa.** Reviewed `worker-b/THREE-QUERY-PLACEMENT-GATE.md`, including its intermediate-interface section.

Removing the outer query from the pure E3 endpoint confines the two-query intermediate W to E2+E3. Its E3 part A occupies one block, since degree three uses both inner queries. The last query leaves one row unchanged, so its ordinary input encoding sends B=pi2(W) into one row; rank B is at most d. The opposite corner is an untouched F1 compression and must vanish.

The decisive rank argument is valid with ordinary zero divisors. Restricting invertible W=A+B to the opposite input role eliminates A and forces that restriction of B to be injective. Projecting onto the opposite output role also eliminates A and forces the corresponding projection of B to be surjective. Thus B has rank exactly d. Its image maps isomorphically onto the opposite output role, and the opposite input role maps isomorphically onto its image. Their composition, the purportedly zero opposite corner, must be invertible. Transposition supplies the reversed placement.

For the surviving same-side word, the intermediate E2 and E3 parts each have rank at most d. Invertibility of their sum forces rank exactly d and complementary images and row spaces. The E3 image is an entire standard output role; the E2 image is an inverse ordinary encoding applied to an entire standard role. Their complementary ordinary column frames form an invertible ordinary output change. Thus the claimed separation into pure E2 and E3 rows is justified.

The obstruction to factoring that E2 row as H V2, with H invertible in E2 and V2 an ordinary input row, also holds. In original coordinates the row unaffected by the second query is a full-rank ordinary invertible multiple of H V2. The inverse-native proof's cR argument makes the first query's E2 row factor through V2. Every E3 term then factors through V2 as well. W would have row rank at most d, contradicting invertibility. H need not be a single Gaussian basis element.

The open caller is narrowed to three queries on one side and an intermediate E2 row that cannot be separated into an invertible pure-rank operator and an ordinary input role. This does not rule out that representation or furnish its implementation. Fixed marked columns require the separately proved bulk-algebra extension. Source, body, cost, uniformity and foundational assumptions remain explicit.

Credit: Worker B's argument, programme source/rank-space authors, Worker C's independent review, @CubeJerry and OpenAI assistance.
