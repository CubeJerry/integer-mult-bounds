# Nonlinear surplus transcripts must pay for raised destinations on the scalar source

**Theorem.** Fix any of the three audited source cuts, a finite record alphabet of size at least two, a deterministic zero-error fixed schedule and exactly N=9b+s future downward movements into the remaining 95-receiver downset D_U. The nonnegative integer s counts redundant physical record slots in the entropy bound; it does not assert that particular payload values are redundant. No linearity is required. For each of those movements let o,d be its origin and destination ranks. At t=199/200 write [g]=g^t and define

    Δ = Σ_downset ( [o−min(d,1)] − [o−d] ).

This is an accounting correction calculated on the actual route. At a ground or rank-one destination the summand is zero; all others are positive. The additional physical movement bill is at least the larger of the two expressions

    9b Σ w_r + (9b+s) + 8b − 8bβ − sη − Δ

with the following exact rational decimals.

| Dual | w2 | w3 | w4 | w5 | β | η |
|---|---:|---:|---:|---:|---:|---:|
| 1 | .99308 | .72026 | .33149 | .92753 | .73402 | 4.46267 |
| 2 | .99308 | .58187 | .26856 | .74999 | .58717 | 2.51092 |

For the scalar pair source the limiting room is 30.9537726582179… . The exact lower bills before subtracting Δ are 34.41641, 32.62230 and 31.11138 at N=10, 11 and 12. These still exceed the room whenever the total integer excess destination rank Σ max(d−1,0) is at most 3, 1 or 0, respectively. The exact Δ comparison sometimes admits a wider exclusion. This does not prohibit every ten-, eleven- or twelve-record schedule.

## Entropy lost by an inside-origin event

Use the authenticated 838 witnesses; each has four isolates and a Petersen graph. Fix every original variable outside W, including Ys. Independent uniform whole-record inputs on W imply that the complete ordered downset transcript T has entropy at least 9b record units on every slice. This follows by decoding the four isolates, then applying the exact conditional Petersen bound to the remaining ten.

Call a downset event inside-origin if its origin B belongs to D_U. With all downset descents cut, any input initially reaching B before that event is supported on S(B), the U-roles with native root in B. Exterior-to-inside transitions must be cut descents. Hence whenever W misses S(B), this event is deterministic given the outside variables and all earlier actual downset messages, even under arbitrary feedback and nonlinear local maps. For each W, every such event consumes a full unit of the conditional entropy deficit

    Σ_e (1−H(T_e | T_<e, outside W)) = N−H(T | outside W) ≤ s.

In particular there are at most s missed inside-origin events for each W. Under the positive 102-witness measure put p(B)=Pr(W meets S(B)). Averaging yields Σ_inside (1−p(B)) ≤ s. It is essential that the deficit is computed after conditioning on all preceding messages. An unconditionally informative copy of an earlier message can have zero conditional entropy.

## Formation accounting without a minimum-code premise

For r in {2,3,4,5} let H_r count all downset events with origin rank >r, independently of destination. Let E_r count exterior downward movements from rank >r to rank ≤r. Let J_r be all actual upward exits of D_U whose exterior destination has rank ≤r. For a fixed witness W supply the H_r whole payloads, E_r exterior crossing payloads, all inlets in J_r whose origin contains a W role, and those low-origin downset events whose origin is inside D_U and contains a W role.

These data reconstruct T chronologically on the slice. The low exterior begins without U-sensitive data. A high exterior arrival at low rank is supplied. An inlet missed by W is reconstructed from its fixed local inputs and earlier downset messages. Local exterior computations and internal exterior movements can then be simulated. A low inside-origin downset event missed by W is reconstructed by the same local-input argument. A low exterior-origin downset message is computed from the simulated exterior. Every other required downset value was explicitly supplied. Therefore, averaging over the fixed W measure,

    9b ≤ H_r + E_r + Σ_(j∈J_r) p(origin j)
          + Σ_(inside-origin downset e, o_e ≤ r) p(origin e).

The bound identifies all high-origin events as oracles, even when their real destinations lie above r. No destination or origin rank cutoff is a premise. The Δ term below prices that relaxation explicitly.

## Pricing the two inequalities

Multiply the four formation inequalities by their w_r and add the identity N=9b+s, charging one unit per actual downset event. An exterior descent's total charge is Σ_{d≤r<o} w_r≤[o−d]. An upward inlet from a to u is charged at most α_a Σ_{r≥u} w_r, with the rank caps α from the [102-witness coverage](../../bit-nonlinear-weighted-inlets/review/CERTIFICATE.json). We use 1 as a conservative cap above rank four. For each of the 15 inlet types, an owned upward move pays its charge. A public axis inlet is covered by β plus its actual minimum extra premium [a]+[u−a]+[7−u]−[7] over the direct endpoint. There are at most 8b such public inlets. Other original publics cannot make a low exterior inlet, and public routes cannot reduce their retained endpoint invoice.

A downset event receives total charge

    1 + Σ_(r<o) w_r + 1_inside p(B) Σ_(r≥o) w_r.

For all possible ranks o>d and both inside/exterior origins the [exact pricing checker](check.py) establishes that this is at most

    [o−min(d,1)] + η·1_inside·(1−p(B)).

It suffices to check p(B)=α_o because the left minus right is nondecreasing in p(B). There is no such residual for an exterior origin. Sum the displayed hypothetical gap prices, replace them by actual prices plus the exact Δ, and charge the missed-witness terms by ηs. The independent eight private arrivals per copy end at rank six or seven and cannot belong to any downset event, charged exterior crossing, or low inlet here. They supply the final +8b. Subadditivity gives [o−1]−[o−d] ≤ [d−1] ≤ d−1 for d>1, justifying the simple integer endpoint conditions.

The [certificate](CERTIFICATE.json) checks every source and destination pair with exact rational 200th powers or outward root intervals. Removing the missed-event credit deliberately breaks selected per-event prices. Run `python -B PATH/TO/check.py --repo . --coverage PATH/TO/INDEPENDENT-COVERAGE-CERTIFICATE.json --out /tmp/surplus.json`. The referenced coverage receipt is content-pinned; the inequality proof does not rely on an optimizer. Credit the 838 induced witnesses, original source words, S022's weighted nonlinear inlet architecture and measure, S022 worker B's surplus deficit and endpoint pricing, @CubeJerry, and substantial OpenAI assistance. No complete new κ.
