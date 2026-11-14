# What a legal short-caller tensor source must improve

## Status

This package supplies exact necessary budgets and scoped source obstructions for the legal two-tag P104 tensor in binary dimension18 with208 ports. The short-caller identity is proved in the separate `short-rectangular-caller` package; actual six- and eight-stage words there have independent review. Here the rank14 row cost is the algebraic pairing price of a specified eight-row decomposition, not an emitted native source. The native acquisition, correction, helper, erasure, precision and compiler interfaces remain open. **No new kappa.**

Proved results below:

1. Six stages maximize the optimistic room per native invocation, while eight maximize the total caller gap.
2. Two complete cohorts of tag9 main-field stops cannot fit any caller in this even-stage family while paying the stipulated separate rank14 row account and nonnegative additional net cost.
3. Sixteen separate Hub-style rank16 row routes, eight per plane, fail every even stage count.
4. Under a precise direct-original, single-cochart row interface, moving a row's formation/deposit to a proper chart cannot improve on that rank16 Hub account once all mandatory original-X stops are charged. This last statement includes arbitrary width and entangled gathering charts under its stated support contract.

A caller-level conversion and source-bound negative check for the actual h9 native are separately proved in `H9-CONVERSION.md`. The same physical costs are not asserted for a native endpoint wrapper.

## 1. Exact source row geometry, with the asymmetric supports retained

The eight rows come from DreamingOfClouds' open CrocSwap/integer-mult-bounds#7583 at `0c8b204a5fc9fce057bdbdc13eda0990c4f8b207`, `research/p104-decoder-wall/rows.py` and its pinned `data/lines120.json`. These exact source bytes are preserved. The data SHA256 is `4a91033b56fe23feb897b90e6259b33dfbe428ff07ad7ce511a73835074f2708`.

Write G for the integer120-line Gram array, q_i for its odd F2^9 labels, and take the first104 ports. For the eight pinned pairs `(d_k,e_k)` among the sixteen virtual lines, set

    w_k(i)=G[i,d_k],    u_k(j)=G[j,e_k]/(2G[d_k,e_k]).

Direct exact entry verification gives `sum_k w_k u_k^T=G_104/2=M`. Thus M has diagonal1 and zero off-diagonal entries whenever q_i dot q_j=1. Both104-by8 factors have rational rank8. The row data are part of the proof certificate: `rows_geometry.py` imports none of the source scientific code, checks every104-squared decoder entry and all120-squared Gram/label parity entries, and identifies the104 labels with the actual native labels through an explicit permutation. Equal ordering is not assumed.

Each D_k=supp w_k and S_k=supp u_k has52 ports. Their binary spans are distinct hyperplanes

    span(D_k)=q_(d_k)^perp,    span(S_k)=q_(e_k)^perp,

of dimension8, with q_(d_k) dot q_(e_k)=0. Their pairing rank is7. Tensor with the legal two-label factor on e_0,e_1 with decoder J_2. Each tensor row has104 source ports and104 destination ports, source/deposit spans of dimension16 in F2^18, and pairing rank14. Its common destination-facet intersection has dimension2. Distinct source spans sum to the full18-space, as do distinct destination spans. These facts are checked exactly for all eight rows and all28 pairs in `ROWS.json`.

This distinction is essential: an orthogonal omitted Gram row with identical source and destination hyperplanes has pairing price8 in the base geometry. The asymmetric virtual-line rows above have price7. The checker includes that price8 comparison as a negative control. The orthogonal omitted-Gram source and the asymmetric row-price decomposition must not be silently identified.

The tensor matrix `M tensor J_2` has rank8 and each off-diagonal tag block equals M. In particular, every receiver has a nonzero off-block row (indeed the matching base port contributes1). This is an algebraic correction requirement, not an automatic physical traffic lower bound without an interface hypothesis.

## 2. Exact short-caller moment and the two different optima

Put `t=199/200`, `b=17`, `n=208`, and let `s=2a` be the number of native calls. The proved caller gives per-port wrapper moment

    W_a=2(1+34a)^t+4 sum(j=1..a)(1+17j)^t
        −4−4 sum(j=1..a−1)(17j)^t.

Grant four direct rank17 main routes per port per native, two independent sets of eight rank14 row chains, and zero other net expense. This favorable account leaves

    g_a=W_a−8a*17^t−(4a*8/208)*14^t.

No positive result about a supplier follows merely from g_a>0. Any extra helper must either have zero productive credit or obey the retained nested-boundary contract under which its paid route moment is at least that credit. A different helper architecture with a legitimately different net contribution requires a new complete account and is outside the exclusions here.

The sequence g_a is strictly concave. To see this, expand `(1+17j)^t=(17j)^t+delta(17j)`, where delta(x)=(1+x)^t−x^t is strictly decreasing. The differences of the two remaining power terms decrease by concavity, as do the added delta terms; linear terms have constant differences. Exact adjacent signs `g_4>g_3` and `g_5<g_4` therefore prove that total gap is maximized at eight stages:

    g_4=0.4457069135248235814461627206... per port.

For actual native design the relevant allowance is `r_a=g_a/(2a)`. Define `d_a=a*g_(a+1)−(a+1)*g_a`. Then

    d_(a+1)−d_a=(a+1)*(g_(a+2)−2g_(a+1)+g_a)<0.

Exact signs `r_3>r_2` and `r_4<r_3` establish the global maximum at six stages:

    r_3=0.06798816087596853162371790006... per port per native,
    n*r_3=14.14153746220145457773332321... per native.

Both source words exist formally; this is not a search over hypothetical invoice profiles. The source-dependent native costs remain unconstructed.

## 3. Exact tariff for tag-subspace station reads

A public X starts on its one-dimensional label line and ends at dimension18. A public Y starts at zero and ends at its rank17 facet. If either must visit a rank9 station, splitting its actual route at that visit gives moment at least `8^t+9^t`: each segment's total rank variation dominates its endpoint dimension difference, and concavity gives the cheapest single jump. Turns cannot reduce this bound. Relative to its direct route, one compulsory visit costs at least

    delta_9=8^t+9^t−17^t
           =0.05804469100584703554012063954....

If k distinct main fields must stop, necessarily `k*delta_9<n*r_a`. Even at a=3 this requires `k<243.63188462450304...`, hence at most243 fields. One complete208-field cohort fits the six-stage relaxation by0.05966081922072897... per port over all calls, but fails at eight stages by0.01865061452195270.... The eight-stage one-cohort failure must not be promoted to an all-caller obstruction.

Two complete cohorts require416 fields and fail every even stage count:

    max_a r_a−2delta_9=−0.04810122113572553945652... <0.

**Station-only correction application.** Suppose the fixed tensor decoder introduces its off-block M term in each plane, and all corrections to a main receiver's off-block dependence come from direct reads at its designated rank9 tag station. No other bank, receiver feedback, inherited history or correction outside that station changes this dependence. Every receiver in each plane must visit, since its off-block row contains the matching-port coefficient1 while the native identity requires zero cross-tag dependence. The forward Y fields and reverse X-type fields form two distinct208-field receiver cohorts. This station-only completion fails the budget. The rank8 off-block matrix alone does not imply416 visits under an arbitrary encoded network.

If a shared-row architecture kept these two cohorts but improved both private decoders symmetrically, it would have to remove more than5.0025269981154565 moment units per plane per native just to reach equality in the favorable budget. Positive ordinary and other source costs need further strict improvement. Changing the compulsory visits is another possible escape.

## 4. Hub-style separate rows fail at every stage count

Consider one separate forward row record born at chart C. Its destination-side reads occur at charts contained in the recipients' own facets. Let K be the orthogonal complement of its current chart. Initially K has dimension18−dim C. The visited K spaces together must span all destination normals, a16-dimensional space. A downward owned MOVE of rank d can add at most d new dimensions to the span of visited K; upward moves add none. Thus total downward rank is at least

    dim(span(destination normals)+C^perp)−dim(C^perp)
        >= dim C−2.

The sum of downward moments is at least `(dim C−2)^t`. This permits arbitrary owned turns and no prescribed final chart. Reverse the geometric path for the reverse row, whose own-facet gathers precede a common X-side deposit chart C. Copies or several rows sharing one route are outside this single-row-record premise.

A Hub-born forward row, or a reverse row delivered to full Hub, therefore costs at least16^t. Sixteen such rows, eight per plane, plus the four cheapest public routes give

    g_a^(16)=W_a−8a*17^t−(4a*8/208)*16^t.

This separate-row template retains nonnegative additional net expense. Its exact gaps at2,4,6,8 stages are

    −0.7810742491691874..., −0.4634211536577081...,
    −0.4981835666116230..., −0.7624431289650886....

The first difference is positive and the next negative. Strict concavity proves that four stages give the global maximum, already negative. Every positive even stage count fails. This rejection needs no extra acquisition, correction, erasure, ordinary or precision charge. It is not an exclusion of every decoder on the label set.

## 5. Direct-original cocharted row formation cannot repair the Hub deficit

### Precise interface

Fix any positive integer width V and the specified eight tensor rows in each plane. Geometry lives in the binary space of dimension18V; scalar coefficients remain in characteristic zero. Assume the following source interface.

- Each forward row forms its complete indicated linear combination of the104 original X fields by direct reads at one chart C_k. At those reads C_k contains each corresponding original label subspace `q_s tensor F2^V`. Thus C_k contains the16V-dimensional source span. Encoded or line-erasing replacements of the original donors are not supplied for free.
- The reverse row has the time-reversed interface: one common X-side chart C_k, containing its16V-dimensional deposit-label span, receives the row on all104 indicated X-type fields.
- Each X-type field follows an arbitrary nested-MOVE path from its original V-dimensional label subspace to Hub. Turns are allowed. Different modes may be formed at different times. Each row uses its own owned record; its opposite-side accesses lie within the relevant native facets, as in section4.
- All operations are charged; any additional helper has nonnegative net moment under the declared helper contract. No other productive credit is invented.

No restriction that C_k be a scalar chart tensored with V is imposed. Its dimension may be any integer between16V and18V. This theorem concerns the stated direct-original contact geometry. A more powerful encoded acquisition or a changed opposite-side read interface remains open.

### A route inequality that prices every proper cochart

Normalize dimensions by V. Let one X field visit, in chronological order, distinct required row cocharts C_1,...,C_k, and put `a_i=18−dim(C_i)/V`, so0<=a_i<=2. Every pair of these cocharts sums to the full ambient space, because the underlying distinct row support spans already do. A proper chart therefore cannot host two different indicated rows. Repeated Hub contacts have a_i=0 and contribute zero surcharge.

For the segment C_i→C_(i+1), total upward rank is at least a_i V and downward rank at least a_(i+1) V. To see the first claim, project current charts into the quotient by C_i: the terminal image has dimension a_i V, and only upward moves can increase this dimension. For the second, track intersection with C_i, whose dimension must decrease by a_(i+1)V and cannot decrease at an upward move. Subadditivity separately on upward and downward moves gives normalized segment moment at least `a_i^t+a_(i+1)^t`.

Use the potential `Phi(C)=18^t−(18−dim(C)/V)^t`. The preceding segment bound exceeds its potential change by at least `2a_(i+1)^t`. The initial segment from the label line to C_1 has normalized cost at least `(17−a_1)^t`, whose excess over its potential change is

    delta(a_1)=(17−a_1)^t+a_1^t−17^t.

The final segment C_k→Hub costs at least a_k^t, exactly its potential change. Since `0<=delta(a)<=a^t`, summing the segments proves

    public route moment / V^t >=17^t+sum(i=1..k)delta(a_i).

This charges every required cochart without double counting a field's baseline route. It permits arbitrary turns and entangled intermediate charts; it uses no finite-path search or extrapolation.

### Complete per-row tariff and the exclusion

For a row whose common X-side cochart has normalized dimension c in[16,18], section4 charges its owned route at least `(c−2)^t`. Its104 original-X contacts collectively receive the public stop surcharge `104*delta(18−c)` from the preceding inequality. Their sum, beyond the already counted direct public routes, is at least

    F(c)=(c−2)^t+104*((c−1)^t+(18−c)^t−17^t).

This is concave on[16,18]. At the endpoints,

    F(18)=16^t,
    F(16)−16^t=1.2057417949261035174538283305... >0.

Therefore F(c)>=16^t for every real c in[16,18], and it is strictly larger for c<18. This proves the all-width statement, including c values between the integer base dimensions. The integer c=17 control has excess0.9788039147886568216030475866...; it is not needed to interpolate the proof.

Summing over eight rows in each plane and all original main fields yields a complete lower account at least as large as section4's sixteen rank16 Hub rows. Consequently **no source in this direct-original, cocharted row interface meets the target moment for any positive even stage count**. Shared original routes have already been accounted for, so changing the order of its proper gathers cannot repair the loss.

The mechanism of failure is quantitative. A rank16 proper cochart saves about two units on one owned row relative to Hub, but forces104 genuine original-X contacts; even their small individual route refinements cost more than that saving. Distinct row cocharts cannot combine into one proper stop because their support spans sum to the ambient space.

This conclusion leaves several structurally different interfaces open: encoded mixtures prepared before coalescence, acquiring several row histories through one shared moving record, explicit loss and reconstruction of original label subspaces at the read sites, own-facet departures with fully paid restoration, or a new decoder and row-support geometry. Each must retain its new operations and helper accounting. The result does not turn an optimistic row-price bound into a universal lower bound for those alternatives.

## 6. Verification and interpretation

`rows_geometry.py` checks the exact fixed row data and its native-label permutation, all10816 decoder entries, every support and pairing rank, and all56 same-side support-span pairs. It rejects an incorrect dual scalar and distinguishes same-support price8 rows. `budget.py` uses integer200th-root enclosures with denominator10^45, checks both global-optimum sign tests, the station inequalities, the rank16 all-stage maximum, the proper-cochart endpoint, and the source-bound h9 invoices. The all-width and all-stage theorems follow from the stated algebra and concavity arguments; finite tests alone are not claimed as those proofs.

Reproduction:

    python3 -B rows_geometry.py PATH_TO_PINNED_NATIVE.json.gz
    python3 -B budget.py
    python3 -B verify_conversion.py

Expected results are `PASS_PINNED_TENSOR_ROW_GEOMETRY`, `PASS_SHORT_TENSOR_SOURCE_SCREEN`, and `PASS_CALLER_LEVEL_B_CONVERSION`. Normal and optimized receipts agree. Pin manifests separate upstream source bytes, author mathematics and the root/worker-independent reviews. The original PR's rigidity enumeration is not needed or rerun here: this result concerns its specified eight rows, whose geometry is checked directly.

Credit DreamingOfClouds and the PR7583 predecessor decoder authors for the row decomposition and row-model distinction; @CubeJerry for the persistent programme and inherited QUERY-only caller mechanism; the retained native/caller/compiler lineage; and the S012 independent reviewers. These new source-specific tariff proofs and exact checkers were developed with OpenAI assistance. The complex and ordinary BIT suppliers, compatibility bridge and five foundational assumptions remain open.
