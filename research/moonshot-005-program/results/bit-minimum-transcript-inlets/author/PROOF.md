# Paid exterior entries exclude every minimum linear transcript on the three current source cuts

**Theorem.** Take the scalar pair, two-copy F4 or three-copy F8 source at its authenticated cut, with b respectively 1, 2 or 3. Let V be any positive record width over any characteristic-two field. Any linear continuation that completes all native receivers and uses exactly 9b downward MOVEs into the remaining 95-receiver downset D_U requires additional movement of at least

    b · (9(2 + 24589/25000 + 95/54) + 8 − 8·9651/10000)
      = b · 42.96457333333333… .

The tariff is [g] = g^(199/200) on each strict nested rank change. Arbitrary joint-bank linear recoding, arbitrary earlier use of payloads, arbitrary numbers and directions of paid owned moves, and all admissible monotone public routes are allowed. The necessary limiting room is 30.9537726582179… for the scalar word and 42.9433924269585… per copy for both field-source words. Thus a target-feasible linear continuation of these fixed cuts needs at least 10, 19 or 28 receiver-downset descents, respectively.

## 1. The source and the exterior

Write T = {14,17,19,20,96,99,101,102}, U = {8,…,110} minus T, and let F_i be the orthogonal hyperplane of native real root R_i. D_U is the union of all subspaces of F_i over i in U. It is closed under passing to subspaces. A chart outside D_U is exterior. Write S(B) = {i ∈ U : R_i ∈ B}.

Fix all original Ys and Xs outside U. This conditioning supplies no physical operation. By [all-field locality](../../bit-low-exterior-formation-gate/author/PROOF.md), each initial field at B is supported on S(B). The [prefix replay](check.py) checks an additional fact on all 410, 812 or 1,218 live fields: every U-informative initial field at rank ≤5 lies in D_U. Each such field's actual chart lies in an authenticated F_i with i ∈ U. Hub inputs, rank-three half caches and all public Ys remain in the literal replay.

By [induced 95-role equality](../../bit-induced95-equality-rigidity/author/PROOF.md), at 9b downset descents their payloads C_e comprise 9bV independent canonical rows after invertible per-role gauges. Their destinations have rank zero or one. Subtracting any strictly earlier cut-block contributions preserves jointly independent canonical innovations. Any nonzero canonical row has native real support rank at least seven. Therefore every downset event whose origin has rank ≤5 has exterior origin. If such an origin B lay inside D_U, after cutting every downset descent all uncut initial data reaching B would follow local and upward paths alone. An exterior chart cannot reach B without a cut. Subtracting the earlier downset contributions would produce a nonzero canonical row supported in S(B), a contradiction.

All original Xs are at Hub. The public Y_i for i ∈ U remain inside D_U on their monotone paths to F_i. The T-records already have rank six. Only the eight coordinate Ys per copy can ascend from D_U to an exterior chart of rank ≤5. Each starts at ground, finishes at its own coordinate facet of rank seven, and can exit D_U at most once. Their retained closure charges exactly one [7] jump apiece. The closure contains no owned MOVE. These facts are checked separately on each word.

## 2. Coordinate-projection density for arbitrary block widths

Let ξ_i ∈ F2^9 be the pinned canonical vector at i. The dimension of the binary subcode supported in S is 9 minus the rank of the ξ_i for i outside S. These binary coefficients tensor with block coordinates in any characteristic-two extension. Invertible vertex gauges preserve supports and coordinate projection ranks.

Let z_1,…,z_511 be the sorted weights of the binary directions. Each role in the joint support of an h-dimensional subcode appears in 2^(h−1) of its nonzero words. Its support size is therefore at least ceil[(z_1+…+z_(2^h−1))/2^(h−1)]. The nine finite lower bounds are

    35, 55, 68, 75, 80, 83, 85, 88, 95.

Every bound is at least (95/9)h. Given A ⊆ U of vector rank k, its complement supports a binary subcode of dimension 9−k, so 95−|A| ≥ (95/9)(9−k). Hence k ≥ (9/95)|A| for every A.

Let E be any subspace of the gauge-transformed canonical row code, and t_i the rank of its projection at role i. Sort the roles by t_i and greedily choose a binary vector basis. For each z≥0 the number of chosen basis elements of weight ≥z is nine minus the rank of the roles of weight <z. It is at most (9/95) times the number of all roles of weight ≥z. Integrating the finite step functions yields a basis of total weight ≤(9/95) sum_i t_i. Projection onto any such nine-role basis is injective on the full gauged code because its binary coefficient matrix and each individual gauge are invertible. Consequently

    sum_(i∈U) rank(projection_i E) ≥ γ dim E,       γ = 95/9.       (1)

This includes arbitrary noncommuting block gauges and all positive widths. Equality is attained on the full canonical space.

## 3. Each layer is supplied by downward crossings or actual inlets

Fix r=1,…,5. Let m count downset events whose origin has rank ≤r. All of those origins are exterior. Let c count exterior descents from rank >r to rank ≤r. Let C_r be the number of all downward crossings from above r to rank ≤r. Since each of the 9b downset destinations has rank ≤1,

    C_r = 9b − m + c.

Let J_r consist of all upward MOVEs whose origin A is in D_U and whose destination is exterior of rank ≤r. Include owned and public records. Then

    9b ≤ C_r + (1/γ) sum_(j∈J_r) |S(A_j)| .                       (2)

To prove this, cut all downward events into D_U, all c high-to-low exterior descents, and all J_r inlets. The low exterior charts initially have zero U-dependence by Section 1. Their only possible new U-dependence in the opened network passes through one of these cuts. Local operations and moves internal to the low exterior convey no other input. A path entering from D_U by a down-move into an exterior chart is impossible by inclusion. A path entering from any higher exterior chart is cut at its downward crossing. Thus each low downset payload is a linear combination of earlier downset cut values, the c arbitrary exterior crossing payloads, and the inlet payloads.

For any inlet at A ∈ D_U, open its expression with all downset descents cut. Any uncut initial dependence reaching A flows local/upward entirely inside D_U. Its residual after subtracting earlier downset contributions is a width-V row block L_j supported in S(A_j). Substitute these expressions into the preceding low payloads and gather all strictly earlier downset terms. We obtain m jointly independent canonical innovation blocks that are linear combinations of the c exterior crossing payloads and these L_j. When m>c, annihilating the coefficients of the cV crossing rows leaves a space E of at least (m−c)V independent canonical rows in the span of the L_j. For each role i its projection rank is at most V times the number of inlet charts having i in S(A_j). Applying (1) and summing over i gives γ(m−c) ≤ sum_j |S(A_j)|. With m≤c, (2) follows directly. This elimination uses entire actual crossing payloads and preserves all prior recoding. No independence of those exterior crossing payloads is presumed.

## 4. A numerical dual on five rank layers

Multiply (2) by the following positive rational weights and sum:

    (w1,w2,w3,w4,w5) = (1, 24589/25000, 1, 95/108, 95/108).
    W_s = sum(w_r : r≥s),          β = 9651/10000.

Each actual downward MOVE from s to d contributes Σ_{d≤r<s} w_r, at most [s−d]. This is checked for every one of the 36 pairs 0≤d<s≤8 by raising the rational left side to power 200 and comparing with (s−d)^199.

An upward inlet from rank a to exterior rank s≤5 contributes at most u_a W_s/γ, where u_a = (0,1,3,6,12) for a=0,…,4. These are upper bounds on the number of native roles in a real chart of rank a. Reduction modulo 3 preserves every vanishing integer minor, so the native roles of a real rank-a chart have ternary rank ≤a. The 95 native lines reduce to distinct ternary projective points and their total ternary rank is at least four. The [exact small enumerator](flat_four.cpp) visits all independent native subsets of ranks 1…4, including 3,125,924 rank-four bases. Their maximum native-line counts are 1, 3, 6, 12. The upper bound on the number of native roles simultaneously in a coordinate hyperplane and a rank-four chart is 11 for each of the eight coordinate hyperplanes. The case of fewer than eleven lines is automatic; the checker explicitly examines every larger candidate.

For an **owned** inlet, u_a W_s/γ ≤ [s−a] for all 15 pairs a<s≤5; this charge is part of its actual upward MOVE. For a **public axis** inlet, its pre-exit chart also lies in its own terminal coordinate facet. Use u'_a = (0,1,3,6,11). Monotonicity gives an actual public route of cost at least [a]+[s−a]+[7−s] by subadditivity of x^(199/200). Its source invoice already includes [7]. The additional available premium is therefore

    p(a,s) = [a] + [s−a] + [7−s] − [7].

For the same 15 rank pairs, the directed interval checks give

    u'_a W_s/γ ≤ β + p(a,s).

This is tight enough to matter: at a=3,s=4 the inlet bound is exactly 1 and p(3,4)=0.0349085895959…, so β alone does not cover it. All other public moves have nonnegative additional cost over their paid direct endpoint by subadditivity. At most 8b public axis records can use the allowance β. Each such record is used once even when its one exit supplies several layers.

After this pricing, the actual additional downward, owned inlet, and applicable public splitting costs are at least 9b·sum_r w_r − 8bβ. The separate [private-region theorem](../../bit-separated-private-transcript/author/PROOF.md) requires 8b positive owned arrivals ending at rank six or seven. None can be a downward crossing of these five layers or an inlet at rank ≤5. Hence adding their 8b lower cost introduces no duplicate charge. Here downward MOVEs with zero dual load need not be charged; private descents landing at ranks six or seven have zero such load.

The resulting per-copy floor is exactly 42.96457333333333… . Its strict deficits relative to the three optimistic necessary source rooms are 12.0108006751154… for the scalar cut and 0.0211809063747… for each F4/F8 cut. Both sides of each comparison are enclosed by the [outward rational certificate](CERTIFICATE.json). The theorem changes no caller price or source closure. Rank-nine rigidity is used at the current cuts; additional transcript events, nonlinear encoders, and changes before the cut are outside this exclusion.

Run `python -B PATH/TO/check.py --repo . --out /tmp/inlet-certificate.json` from the repository root and compare with the saved certificate. The verifier requires Python and a C++17 compiler. The compiler only enumerates finite ternary geometry. The quantified linear and physical-cost implications are proved above. Credit the source and private-region authors, predecessor equality and paid-formation results, S022's rank-layer and generalized shortening work, S022 worker B's exterior-inlet proof and dual, Jerry Chen / @CubeJerry, and substantial OpenAI assistance. No new complete κ.
