# Exact endpoint-peeling obstruction

## 1. Frozen map and allowed changes

Work over Q, or any characteristic-zero extension such as Q(i). Let V be the 1375-dimensional public-coordinate space of the retained native. All owned coordinates start at zero and are initialized/cleared according to the retained word. Its public endpoint T is invertible and equals the two-plane map

`X=x, Y=y+x, X2=x2−y2, Y2=y2`, with each helper fixed.

Let Gin be the initial zero-frame scalar block, Gout the final full-frame scalar block, and K the map of the intervening scalar core, including the ideal owned resets. Then

`T = Gout K Gin`, so `K^(-1) = Gin T^(-1) Gout`.

The exact checker verifies T and all 1375 rows of `K K^(-1)=I`; invertibility is not inferred from a random evaluation.

For one retained port q, choose distinct original helpers h and g, both with initial zero frame and final full frame. The first MOVE of h must be zero→span(q); the last MOVE of g must be q-perp→full. Delete those two MOVEs, declare the initial frame of h to be span(q), and the final frame of g to be q-perp. No other initial/final labels or interior scalar gates change. Because there are no zero-frame or full-frame scalar operations inside the core, these deletions do not make a retained interior scalar gate unavailable.

Allow completely new endpoint matrices A and B. A may be any invertible matrix block-diagonal by the **new initial frame groups**, and B any invertible matrix block-diagonal by the **new final frame groups**. The candidate public endpoint is `B K A`.

This includes all finite sequences of legal constant ADD/SCALE/SWAP operations on the fields available at the endpoint, all permutations and basis changes inside one frame group, and mixing the proposed mains with existing mains in that group. It is more permissive than the repository's dyadic elementary alphabet. It excludes mixing different frame groups, altering an interior scalar gate, introducing a new field that persists through the core, or changing any other recursive endpoint.

The proposed target U is T plus one independent unit shear, either

- reverse: `h←h−g`, or
- forward: `g←g+h`.

All other public endpoints remain exactly those of T.

**Theorem.** No eligible pair (q,h,g) for the retained source admits such matrices A,B for either orientation.

## 2. Forward and inverse block-rank lemma

Let `{I_a}` be the new input-frame partition and `{O_b}` the new output-frame partition, indexed by the underlying F2 frame subspaces. Allowing every basis change within such a group is at least as permissive as the literal common-chart gate rule. For invertible block-diagonal A and B,

`(B K A)[O_b,I_a] = B_b K[O_b,I_a] A_a`.

Thus each individual forward frame-block rank is invariant. Inverting gives

`(B K A)^(-1)[I_a,O_b] = A_a^(-1) K^(-1)[I_a,O_b] B_b^(-1)`.

The corresponding inverse frame-block ranks are also invariant. Both statements hold over Q and Q(i), and require no coefficient-size or dyadic-denominator assumption on A,B. A nonzero entry in a block required to be zero is already an obstruction.

The inverse lemma is not an assertion that matching forward block ranks is sufficient for equivalence. In this example, the two final reverse candidates meet the forward rank condition in the decisive block but fail the inverse condition.

## 3. Complete finite family reduction

Every source port is anisotropic: `q·q=1` over F2. Enumerating the actual first and last MOVEs gives 363 eligible h choices and295 eligible g choices. Pairing only equal ports yields 984 candidate pairs.

A new q-input group cannot map into a final-frame group absent from the target. For each h, the checker therefore tests its core column against all output groups except:

- the final-frame groups of fields already starting at span(q), and
- the group at q-perp, which receives the existing forward shear and could receive the proposed forward shear.

Whenever an unallowed coefficient is nonzero, the exact rational coefficient and its row are retained in `RESULT.json`. Since g originally ends at full, promoting g cannot remove one of these forbidden non-full output rows. The witness rejects every pair containing that h.

Dually, a new q-perp output group may only receive the initial-frame groups already associated with q-perp output fields, together with span(q). An exact nonzero coefficient outside this set in core row g rejects every pair containing that g. Since h originally starts at zero, promoting h cannot remove a forbidden nonzero-frame input column.

The explicit witnesses eliminate every pair except:

`(q,h,g) = (268,793,1352)` and `(268,1202,1352)`.

This is exhaustive over the stated finite family. The inventory and every witness are regenerated from the retained word; the result is not inferred from sampled pairs or an unsuccessful optimization.

## 4. The two exact residual obstructions

For either residual h, the new q-input group and q-perp output group are

`I_q = [47,819,h]`, `O_perp = [159,931,1352]`.

Exact rational replay gives

\[
K[O_\perp,I_q]=
\begin{pmatrix}1&0&0\\0&0&0\\0&0&0\end{pmatrix},
\qquad
K^{-1}[I_q,O_\perp]=
\begin{pmatrix}0&0&0\\0&1&1/2\\0&0&0\end{pmatrix}.
\]

Both ranks are1. The inverse matrix is evaluated over exact Fractions, not identified only by its residue modulo a prime.

The source's original forward plane contributes one to the forward block rank. Its original reverse plane contributes one to the inverse block rank. An additional independent forward unit shear raises the required pair of ranks to(2,1). An additional independent reverse unit shear raises it to(1,2). All other identities preserve these counts: an identity field cannot simultaneously have an initial frame containing anisotropic q and a final frame contained in q-perp under the source's public ascent rule.

The residual pair has ranks (1,1), so it is equivalent to neither target under the endpoint transformations of Section2. This completes the theorem. The same rank argument also excludes any nonzero scalar coefficient in place of the displayed unit coefficient of an added independent shear: the required rank increase is unchanged.

## 5. Why the candidate would have mattered

Let t=1−κ and let R_(g,h)(t) denote the complete one-port root-minus-thin-minus-idle profile of a chain with L=g+h full stages:

\[
R_{g,h}(t)=(8L+1)^t+A_g(t)+A_h(t)-2,
\qquad
A_m(t)=\sum_{j=1}^{m}(8j+1)^t-\sum_{j=1}^{m-1}(8j)^t.
\]

The promoted pair loses two rank-nine helper credits and removes two paid rank-one MOVEs per call. The complete signed profile change, if this endpoint existed and if its new caller were implemented, would therefore be

\[
\Delta M(t)=R_{g,h}(t)-2L(9^t-1).
\]

At t=1, `A_m(1)=8m+m=9m` for m≥1, so `R_(g,h)(1)=17L−1` and `ΔM(1)=L−1`. This favorable rank surplus motivated the investigation; it is not an implemented supplier, a proof of a positive moment at the relevant price, or a κ improvement. The exact all-input endpoint obstruction stops this class before those further obligations.

## 6. Limits

The theorem is source-bound and changes one pair at one retained port. It does not exclude new interior contacts, new owned/public frame trajectories, another helper circulation, simultaneous promotion of several pairs, cross-plane coupled targets that change the existing two-plane endpoint, or a different word. It does not admit the source's owned-ascent convention or any outer multiplication assumptions. It establishes the finite formal obstruction under the stated ideal-reset semantics and no broader impossibility claim.
