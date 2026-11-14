# Closed-handoff rank obstruction with clean nested productive helpers

**Status: proved in the stated linear, whole-chart, nested-helper continuation interface.** The two applications are independently replayed finite source identities. This does not rule out redesigning their acquisition histories, introducing an admitted different helper interface, or changing the native geometry. **No new κ.**

## 1. Exact interface and independent source coordinates

Fix an ambient chart H of rank h>=2, exponent 0<t<=1, and whole-field value width V over a characteristic-zero field K. A rank-r MOVE has normalized moment r^t; its actual moment has the common factor V^t. We retain the ordinary width lift of the native chart system: a rank-r chart has spatial dimension rV, and all proper charts have rank at most h−1. In particular every actual Hub/proper crossing has rank at least one. This is a geometric rank-quantum premise. Arbitrary V-by-V linear value operators and feedback are allowed; arbitrary intermediate spatial charts of codimension o(V) are not included in this tariff.

A closed handoff has independent public coordinates, some at H and the others at proper charts, and no live owned records or uncharged retained side information. The required continuation is a fixed linear map. Let r_HP V be the rank of its block from Hub-side handoff inputs to proper-side final outputs, and r_PH V the reverse rank. Initially existing public records finish at their same charts and receive no new productive credit.

A continuation may introduce any number of independent arbitrary helper fields. Each such helper is one independent input slot with one specified invertible whole-field output G_j z_j, containing no native or other-helper input. Its endpoint charts must be nested, in either direction. Its productive credit is exactly r_j^t, where r_j is their rank difference. There is one credit for this one input/output job; successive credits on the same input are not additional independent helper slots. Helpers' prescribed input values may be granted at their specified initial charts for free, a favorable relaxation. Actual source-access expense can only increase the bill. New owned records are born zero, have no productive credit, and may be retired under the separately retained owned-erasure assumption.

All operations are linear and spatially local. ADD/SCALE/read interactions require cocharting. MOVE chains are finite chains of nested chart inclusions or reverse inclusions. We allow arbitrary public and helper turns, arbitrary cocharted value mixing, and arbitrary numbers of intermediate owned records. The theorem bounds movement moment minus the stated productive helper credit; all other expenses are ignored favorably.

Define

\[
c_h=1+h^t-(h-1)^t,\qquad \eta_h=c_h/2.
\]

Then 0<eta_h<=1. The theorem is

\[
\boxed{\quad Q_t-H_{\rm added,t}\ \geq\ \eta_h(r_{HP}+r_{PH}).\quad} \tag{1}
\]

The common V^t factor has been divided out. Thus this is uniform for every width V in the declared spatial lift, and is not restricted to scalar value operations.

## 2. Directional information rank, including new helpers

Collapse all proper charts into one party and H into the other. Grant unlimited free linear processing, memory, and communication within each party. Every real Hub/proper MOVE transmits one V-dimensional field; all other real operations are local in this relaxation. A zero-owned birth or deletion creates no new dependence on the opposite party's initial inputs.

Let k_HP and k_PH be the numbers of transmitted fields in each direction. If b_HP independent helpers start at H and finish proper, the required Hub-to-proper block contains the native block of rank r_HP V and b_HP disjoint invertible helper blocks, each of rank V. These act on independent inputs and have disjoint output coordinates, so their ranks add. The proper party's opposite-input coefficient space can grow by at most V for every Hub-to-proper transmission; its own outgoing messages and subsequent feedback do not increase this bound. Consequently

\[
k_{HP}\geq r_{HP}+b_{HP},\qquad
k_{PH}\geq r_{PH}+b_{PH}. \tag{2}
\]

This is the usual elementary coefficient-rank argument, not a one-way-protocol assumption. It applies to arbitrary alternating linear protocols. With k=k_HP+k_PH and b=b_HP+b_PH, it yields k−b>=r_HP+r_PH. Granting each helper input earlier than physically available only relaxes the continuation.

## 3. Physical route tariff after productive credit

Track each physical field identity. For any route let k_j count its Hub/proper crossings; for an added helper let b_j be one if exactly one of its endpoints is H, and zero otherwise. We prove

\[
\operatorname{movement}_t(j)-\operatorname{credit}_t(j)
\geq\eta_h(k_j-b_j). \tag{3}
\]

A nested-move route between charts with rank difference d has total absolute rank at least d, so its moment is at least d^t: for nonnegative lengths, sum ell_i^t >= (sum ell_i)^t >= d^t. Every crossing independently costs at least one.

For an original public field, or an owned field, there is no new productive credit. Its movement moment is at least k_j, which is at least eta_h k_j. Owned initialization and retirement need no special endpoint assumption for this estimate.

For a helper with both endpoints H, its credit is zero and the same estimate applies. For a helper with one endpoint H and the other a proper rank-a chart, take its last departure from H (or time-reverse the route). That final tail costs at least (h−a)^t, exactly the credit. The other k_j−1 crossings cost at least one each. Hence its net moment is at least k_j−1, as required.

For a helper with two proper endpoints of ranks a,b, nestedness makes its credited rank r=|a−b|. If its route never visits H, the endpoint-rank argument gives nonnegative net expense. Otherwise k_j>=2. Its prefix through the first arrival at H costs at least (h−a)^t, its suffix from the last departure costs at least (h−b)^t, and the remaining k_j−2 crossings cost at least one each. These disjoint route pieces give

\[
\operatorname{movement}_t(j)-r^t
\geq (h-a)^t+(h-b)^t-r^t+k_j-2.
\]

Put u=h−max(a,b)>=1. Since the endpoints are proper, 0<=r<=h−1. Monotonicity in u and concavity of x^t give

\[
(u+r)^t+u^t-r^t
\geq (1+r)^t+1-r^t
\geq h^t+1-(h-1)^t=c_h.
\]

Thus its net expense is at least c_h+k_j−2, which is at least c_h k_j/2 because k_j>=2 and c_h<=2. This proves (3). Summing (3), then using (2), proves (1). No information-rank gain is equated with an individual geometric route rank.

## 4. Application to the exact all-hosted Gram and parity handoffs

The pinned fresh words developed by Worker B have 416 independent arbitrary inputs, four cohorts of 104. Their full rational maps, independently reproduced here from the literal instructions, are

\[
X=x,\quad U=u-L^Td,\quad Y=y+Lx,\quad D=d.
\]

At the closed handoff, X,U are at H of rank nine; Y,D are at their prescribed rank-eight facets. All owned records have been retired. Dirty retirement is explicitly counted and remains subject to the existing owned-erasure assumption. This proof does not claim that finite replay establishes that physical assumption.

The complete HOST2 target is the same map with L=I. Because the handoff map is invertible, its 416 current public values themselves form independent coordinates. Relative to these coordinates the required continuation is

\[
X'=X,\quad U'=U-(I-L)^TD,\quad
Y'=Y+(I-L)X,\quad D'=D.
\]

It therefore has equal directional cut ranks r=rank(I−L). Literal sparse rational replay checks all 10,816 paired entries and obtains r=104 for the omitted-Gram handoff and r=56 for the parity-C4 handoff. The matrices are characteristic-zero matrices; extending scalars and tensoring the input values by K^V multiplies these ranks by V.

Consequently the normalized completion expense, after all newly added helper credits admitted by Section 1, is at least

\[
104\,[1+9^t-8^t]\quad\text{or}\quad
56\,[1+9^t-8^t], \tag{4}
\]

respectively. This is a continuation obstruction to the actual closed words, including newly introduced clean nested productive helpers. It is stronger than a no-helper cut. It does not apply if useful information remains in an uncharged owned record, if the actual main handoff is changed before closure, or if a different helper boundary contract is proved and paid.

## 5. Complete optimistic caller comparison

Use t=199/200 and the parity-uniform body-eight short caller with 104 type-A ports and s=2a stages. Its per-port wrapper surplus is

\[
W_a=2(1+16a)^t+4\sum_{j=1}^a(1+8j)^t
-4-4\sum_{j=1}^{a-1}(8j)^t,
\qquad L_a=\frac{104W_a}{2a}.
\]

The same source/caller convention is used throughout: an actual native's paid profile N and its independent productive-helper profile H enter as N_t−H_t. No old coupled port is treated as a free hosted input. The pinned complete all-hosted native has 416 main fields and 1080 helpers, and its actual conversion adds 24 rank-one and 16 rank-eight moves over the prior native. Its net moment is approximately 3498.94998032775652.

The maximum of L_a over **all** positive integers is at a=6, i.e. twelve stages. For completeness, the first difference of W_a is

\[
2[(1+16(a+1))^t-(1+16a)^t]
+4[(9+8a)^t-(8a)^t],
\]

which strictly decreases by strict concavity. The difference-sign numerator H_a=aW_(a+1)−(a+1)W_a therefore strictly decreases because H_(a+1)−H_a=(a+1)(Delta W_(a+1)−Delta W_a). Exact 200th-root intervals give H_5>0 and H_6<0. Thus

\[
\max_{a\ge1}L_a=L_6\approx3444.42138662032549.
\]

This all-arm optimizer was independently developed by Worker C in the pinned review, and is reused with credit. It is not a finite-scan extrapolation.

The independently replayed source moments are

\[
Q_{\rm Gram}=112[1]+112[2]+96[3]+208[5]+224[8],
\]

\[
Q_{\rm parity}=320[1]+112[2]+304[3]+208[4]+208[5]+16[8].
\]

Their largest limiting continuation allowances, even before other ordinary/precision expenses, are respectively

| Actual closed source | Largest remaining moment | Helper-aware minimum completion moment |
|---|---:|---:|
| Gram, rank104 residual each way | 17.64479758968223 | 206.37892976769965 |
| Parity C4, rank56 residual each way | 9.59879101367346 | 111.12711602876135 |

These are rigorous interval comparisons; displayed decimals are summaries. For the retained fixed-m substitution the available per-native moment is further reduced to

\[
L_a-Q_t-\frac{(N_{0,t}-H_{0,t})-L_a}{m-1},
\]

with the actual all-hosted complete source N0,H0. The numerator is positive even at the global optimum; at twelve stages it is approximately 54.52859370743103. Hence every allowed finite even m is worse than the limiting comparison above. The receipt includes exact six/eight/twelve/eighteen-stage and finite-m controls.

The cutoff (4) already exceeds the most favorable complete movement allowance. Adding ordinary operations, restoration, source-access, precision, decoder or compiler expenses cannot rescue these exact closed handoffs in the stated helper grammar. They remain valid partial constructions and may serve a redesigned earlier acquisition, but they are not completable by appending such a suffix at κ=1/200.

## 6. Explicit boundaries of the theorem

**Nonnested productive jobs.** Consider two distinct rank-(h−1) facets A,B with A+B=H. The real nested route A->H->B consists of two rank-one moves. If a new interface were to credit this as a rank-two productive whole job, its net moment would be 2−2^t, about 0.00692 at t=199/200. This is strictly smaller than c_h, even though the route crosses the cut twice and has no cross-side helper endpoint. Thus (3) would fail under that replacement of the helper-credit rule. This is a precise counterexample to extending the tariff, **not** evidence that such a productive job is accepted by the current native/caller/compiler contract. Its endpoint transform, independent source, physical backward move, output restoration, ordinary corrections and productive occurrence would all need an actual compatible construction. Prior quiet-rechart and fragmentation restrictions must still be checked.

**New spatial rank scale.** If width-V records may cross to proper charts of codimension smaller than V, a crossing need not cost at least V^t. Equation (2) remains an information statement, but the quantitative tariff (3) must be reproved with that geometry. No all-width exclusion is claimed for such an altered interface.

**Open handoffs and changed acquisition.** A live retained record can hold information across the cut before the alleged start. Such information must be included among the initial coordinates and charged in the prefix. The present theorem is about the exact closed sources, which have no such owners. It does not charge a prefix twice or forbid a better joint history.

**Other assumptions.** Dirty owned erasure, the complete native's uniform/compiler/precision contract and the remaining foundational assumptions stay explicit. Finite all-column replay proves the displayed abstract maps and source invoice; it does not discharge these foundations or establish a multiplication theorem.

## 7. Reproduction and provenance

Run from this directory:

```sh
python replay.py
python budget.py
python -O replay.py --out REPLAY-OPTIMIZED.json
python -O budget.py --out BUDGET-OPTIMIZED.json
```

The replay uses only the Python standard library, exact rational coefficients and its own binary chart-rank implementation. It imports no Worker B scientific module. It checks every original input, all endpoint charts, zero-owned births, every literal nested move, retirement of all owners, all paired coefficients and both residual ranks. Perturbing the last actual ADD and leaving the last owned record live are negative controls for each source. Nonzero owned retirement is reported honestly.

Source development and all-hosted conversion: Worker B under @CubeJerry's direction, with predecessor credits in its frozen `native-repartition` package. Actual short callers: Worker A; independent all-arm optimum: Worker C. Helper-aware cut, route proof, source replay and source-bound composition: Worker A, with OpenAI assistance. Exact dependency bytes and verification receipts are listed in `FREEZE.json`; these are one cumulative programme contribution, not a new independent research branch.
