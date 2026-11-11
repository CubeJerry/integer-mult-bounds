# Fuse an unobserved two-return block and reduce 26 observer terms to 22

**Exact conditional reference construction at the unchanged seven-MOVE paid
profile. No new kappa.** This strengthens the S003 seven-rewrite candidate by
removing an unnecessary intermediate owned-state reconstruction. It introduces
no extra paid transport and makes four fewer explicit observation demands.

## 1. The source block and its observable effect

The pinned native has this exact source interval, with zero-based event indices:

| Event | Source operation |
|---:|---|
|40094|MOVE owned1512 from597 to1031|
|40095|ADD owned1512 -= helper1362 in1031|
|40096|MOVE owned1512 from1031 to591|
|40097|SCALE owned1512 by-1/2 in591|
|40098|ADD helper901 += owned1512 in591|
|40099|CLEAR owned1512 in591|

The only public write in this interval is to helper901. The intermediate owned
state in chart1031 has no reader outside this block. Therefore the source does
not require that state to be materialized if the block's entire public effect
and owned cleanup are preserved.

On the 400 independent main-difference inputs, with equal arbitrary entering
helper values in the two copies, the predecessor's exact current identity at
event40096 is

    delta1512 = delta133/2 + 2 delta901.

Both observer values already exist in chart591 before event40094: their last
value events are40084 and37114. The six-event block changes neither observer
until the final update to901. Consequently the complete block maps

    delta901_after = delta901_before - delta1512_before40097/2
                   = -delta133_before/4,

and retires owned1512. This is an endpoint identity on the stated difference
domain, not an identity on arbitrary independent entering helper differences.

## 2. Conditional physical lowering

For every permitted complete-array dimension, assume the two actual difference
observers delta133 and delta901 are physically available, live and cochart in591.
Replace the six source difference-rail instructions by

```text
CLEAR owned1512 in597
INIT  owned1512 as zero in591
ADD   owned1512 += (-1/4) delta133
ADD   owned1512 += (-1)   delta901
ADD   delta901  += owned1512
CLEAR owned1512 in591
```

The first ADD pair reconstructs precisely the source owned value after its
SCALE at40097. The next ADD has the original public effect, and the final CLEAR
has the original cleanup. Other fields are untouched. Hence the original and
rewritten states agree at the exit of this block, and all later operations
agree by induction. Both terminal observers are used before either is modified.

The source chart1031 state need not be reconstructed. Its four old observation
premises, for helpers695,1336,1362 and owned1502, disappear. The remaining two
terminal helper observations remain real acquisition obligations: the endpoint
identity does not manufacture their physical difference fields. The original
common rail also still needs its correct execution and cost.

This is a justified change to an internal observation contract. It is not a
claim that an externally required read may be skipped. The exact six-event
source slice is checked by the builder, and an altered slice is rejected.

## 3. Composition and actual reference word

Retain the five other S7 current-return replacements at28169,33558,34479,39217,
41758, and retain all four historical returns and the three current returns
33272,33281,37606. Together these six modules still remove exactly seven source
owned-difference MOVEs, including both40094 and40096. They use22 observer terms:
4main,16helper,2owned. The reference transcript is generated and exactly replayed
on all400 independent q inputs, with all1480 public endpoints checked.

| Quantity | Original source | S7 separate macros | Fused S7 reference |
|---|---:|---:|---:|
|Instructions|71261|71294|71286|
|ADD|61180|61206|61201|
|MOVE|6310|6303|6303|
|INIT / CLEAR|54 /54|61 /61|60 /60|
|SCALE / COPY|3662 /1|3662 /1|3661 /1|
|Owned labels|51|51|51|
|Owned lifetimes|54|61|60|
|Peak owned fields|43|43|43|
|Final owned fields|0|0|0|

Relative to the original source, the exact operation delta is+21ADD,+6INIT,
+6CLEAR,-7MOVE,-1SCALE. Relative to S7, it removes5ADD,1INIT,1CLEAR and1SCALE.
One removed ADD is the original40095 intermediate update; four are the old
40094 reconstruction. Absorbing40097 into the new coefficients removes its
SCALE. This bill counts real emitted instructions in the difference reference;
it does not stand in for a shared native's full ordinary or ownership tariffs.

The emitted word retains all other original helper-difference MOVEs. Thus it
is an equivalence certificate under the 400-input difference domain, not an
1880-input shared-code implementation with those transports already removed.

## 4. Unchanged full provisional paid profile

With the exact pinned H4 target and paid profiles,

    T_fused = T4,
    P_fused = P4 + 18(O-S7),
    O  = {1:20,2:9,3:2,4:13,5:2,6:1},
    S7 = {1:4,3:1,4:1,6:1}.

This is byte-for-byte the S7 profile:27344 target positions,153144 paid positions,
rank surplus3346. At exponent199/200, exact integer-power brackets prove

    70010917576579126/10^15 <= sum_r(T_r-P_r) r^(199/200)
                           <=70010917576650854/10^15.

The remaining paid moment/native is strictly below3.889495420926, leaving at
most three added positive-rank complete-field arrivals with other terms fixed.
The improvement is a verified reduction of interface obligations and actual
reference operations at the same provisional price. No higher exponent or
complete physical-cost dominance theorem is inferred.

## 5. Verification and remaining obligations

The standalone builder pins the native, current identities, H4 invoice and S7
receipt. It freshly replays the original and fused words, checks five current
reconstruction states plus the scaled fused owned state, all public endpoints,
typed chart/ownership invariants, actual lifecycle counts, and the complete paid
profile. Exact power brackets certify the margin without floating point.

Four controls reject a wrong fused coefficient, wrong destination chart, wrong
endpoint-cancellation sign, and an independent entering helper400 difference.
The last control independently replays the original on that enlarged domain
before comparing the modified source rows. Normal and optimized receipts and
deterministic compressed transcripts agree.

All22 physical observer terms, full shared execution, ordinary/compiler/precision
costs, compatible uniform complex and covered BIT suppliers, and the five global
foundations remain obligations. Prepared for @CubeJerry with OpenAI assistance;
credit S002's current-row identities, S003's seven-rewrite selection, the pinned
native and H4 invoice authors. Independent review is recorded separately.
